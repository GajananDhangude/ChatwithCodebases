from load_repo import load_repository
from parser import parse_code
from vectorestore import VectoreStore
from langchain_classic.chains import LLMChain
from llm import llm
from prompt import CODE_QA_PROMPT
from ingestion import ingest_repo
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough



def build_context(result):
    context_block = []

    for r in result:
        block = f"""
        File:{r['path']}
        Symbol: {r.get('symbol')}
        Lines: {r.get('start_line')}-{r.get('end_line')}
        Code: {r['content']}
        """

        context_block.append(block)

    return "\n\n ---- \n\n".join(context_block)



rag_chain = CODE_QA_PROMPT | llm | StrOutputParser()



if __name__ == "__main__":

    repo_url = input("Enter GitHub Repo URL: ").strip()

    repo_path = ingest_repo(repo_url)

    docs = load_repository(str(repo_path))

    store = VectoreStore()
    store.add(docs)

    while True:
        user_question = input("\nAsk Question (or type 'exit'): ")
        if user_question.lower() == "exit":
            break

        results = store.search(user_question, k=2)
        context = build_context(results)

        answer = rag_chain.invoke({
            "context":context,
            "question":user_question
        })

        print("\nANSWER:\n", answer)

