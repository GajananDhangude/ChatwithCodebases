
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7,
    max_tokens=1000,
    max_retries=2
)






# if __name__ == "__main__":
#     message = llm.invoke("The First person to go to moon was")
#     print(message)