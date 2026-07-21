"""
Document Retriever

Retrieves the most relevant document chunks
from the enterprise knowledge base.
"""

import chromadb

from src.cache.embeddings import EmbeddingGenerator
from src.schemas import (
    RetrievedChunk,
    RetrievalResult,
)


class DocumentRetriever:
    """
    Retrieves semantically similar document chunks
    from ChromaDB.
    """

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="data/chroma"
        )

        self.collection = self.client.get_or_create_collection(
            name="company_documents"
        )

        self.embedder = EmbeddingGenerator()

    def retrieve(
        self,
        question: str,
        top_k: int = 3,
    ) -> RetrievalResult:
        """
        Retrieve the top-k most relevant chunks.
        """

        embedding = self.embedder.generate(question)

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

        chunks = []

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):

            chunks.append(
                RetrievedChunk(
                    text=document,
                    source=metadata.get("source", "Unknown"),
                    distance=round(distance, 4),
                )
            )

        return RetrievalResult(
            chunks=chunks
        )