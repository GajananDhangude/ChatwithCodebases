import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectoreStore():
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.documents = []

    def add(self , docs):
        texts = [d['content'] for d in docs]
        embeddings = self.model.encode(texts)

        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings))
        self.documents = docs

    def search(self , query , k=5):
        query_enb = self.model.encode([query])
        _ , idxs = self.index.search(np.array(query_enb) , k)
        return [self.documents[i] for i in idxs[0]]
    
    