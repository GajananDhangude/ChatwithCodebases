from langchain_core.prompts import PromptTemplate

CODE_QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an expert software engineer.
Answer the question using ONLY the code context below.
Be precise and factual.
Mention file names and function/class names in your answer.

Code Context:
{context}

Question:
{question}

Answer:
"""
)