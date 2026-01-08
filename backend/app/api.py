from fastapi import FastAPI
from pydantic import BaseModel
from vectorestore import VectoreStore
from langchain_core.output_parsers import StrOutputParser
from llm import llm
from prompt import CODE_QA_PROMPT
from ingestion import ingest_repo
from load_repo import load_repository
from main import build_context
import uvicorn
from dotenv import load_dotenv

load_dotenv()




app = FastAPI(title="Chat with Codebase API")


store = VectoreStore()

rag_chain = CODE_QA_PROMPT | llm | StrOutputParser()

class ChatRequest(BaseModel):
    repo_url: str
    question: str


class ChatResponse(BaseModel):
    answer: str


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    repo_path = ingest_repo(request.repo_url)
    docs = load_repository(str(repo_path))
    store.add(docs)



    results = store.search(request.question, k=2)
    context = build_context(results)

    answer = rag_chain.invoke({
        "context":context,
        "question":request.question
    })


    return ChatResponse(answer=answer)


if __name__ =="__main__":

    uvicorn.run(app , host='localhost' ,  port=8080)