from langchain_core.prompts import PromptTemplate

CODE_QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an expert software engineer who reads codebases and explains them.
Answer the question using ONLY the code context below and also explain the code.
Be precise and factual.
Mention file names and function/class names in your answer.

Code Context:
{context}

Question:
{question}

Answer:
"""
)