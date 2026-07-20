"""
RAG Vector Store

Stores enterprise document chunks
inside ChromaDB.
"""

import uuid 
import chromadb
from src.cache.embeddings import EmbeddingGenerator

class DocumentVectorStore:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path = "data/chroma"
        )

        self.collection = self.client.get_or_create_collection(name = "company_documents")

        self.embedder = EmbeddingGenerator()

    def add_document(self,chunks : list[str], source : str,)-> None:
        """
        This function stores document chunks
        """

        for chunk in chunks:
            embedding  = self.embedder.generate(chunk)

            self.collection.add(
                ids = [str(uuid.uuid4())],
                embeddings= [embedding],
                documents = [chunk],
                metadatas = [{"source" :source}]
            )
    
    def clear(self):
        self.client.delete_collection("company_documents")

        self.collection  = self.client.get_or_create_collection("company_documents")