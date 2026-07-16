"""
ChromaDB Cache

Stores and retrieves semantically similar questions.
"""
import uuid
import chromadb
from src.cache.embeddings import EmbeddingGenerator

class ChromaCache:
    def __init__(self):
        #Persistent database
        self.client = chromadb.PersistentClient(path = "cache_db")

        #Collection
        self.collection = self.client.get_or_create_collection(name= "query_cache")

        self.embedder = EmbeddingGenerator()

    def add(self,question : str, answer : str)-> None:
        """Stores a question-answer"""
        embedding  = self.embedder.generate(question)
        self.collection.add(ids = [str(uuid.uuid4())],embeddings = [embedding],documents=[question],
        metadatas=[{
            "answer" : answer}]
        )
    
    def search(self,question : str, n_results: int = 1):
        embedding = self.embedder.generate(question)
        results = self.collection.query(query_embeddings=[embedding],n_results = n_results)
        return results
    
    def clear(self):
        self.client.delete_collection("query_cache")
        self.collection = self.client.get_or_create_collection("query_cache")