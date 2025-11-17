import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class InMemoryVectorStore:
    def __init__(self):
        self.vectors = None  # np.array shape (n, d)
        self.metadatas = []  # list of dicts, e.g. {'chunk_id': i, 'text': text}
    
    def add(self, vectors, metadatas):
        vecs = np.array(vectors, dtype=float)
        if self.vectors is None:
            self.vectors = vecs
        else:
            self.vectors = np.vstack([self.vectors, vecs])
        self.metadatas.extend(metadatas)
    
    def search(self, query_vector, top_k=3):
        if self.vectors is None or len(self.metadatas) == 0:
            return []
        q = np.array(query_vector, dtype=float).reshape(1, -1)
        sims = cosine_similarity(q, self.vectors)[0]  # shape (n,)
        idx = sims.argsort()[::-1][:top_k]
        results = []
        for i in idx:
            results.append({"score": float(sims[i]), "metadata": self.metadatas[i]})
        return results
