"""
Embedding Generator

Generates vector embeddings using a local SentenceTransformer model.
"""
from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    """
    Generates semantic embeddings for text. 
    """

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
    
    def generate(self, text : str, )-> list[float]:
        embedding = self.model.encode(text, normalize_embeddings = True,)
        return embedding.tolist()

