"""
ChromaDB Cache

Stores and retrieves semantically similar questions.
"""

import uuid

import chromadb

from src.cache.embeddings import EmbeddingGenerator
from src.schemas import CacheResult


# Maximum distance allowed for a cache hit.
# Lower distance = more similar.
MAX_CACHE_DISTANCE = 0.40


class ChromaCache:
    """
    Semantic cache using ChromaDB.
    """

    def __init__(self):

        # Persistent local database
        self.client = chromadb.PersistentClient(
            path="cache_db"
        )

        # Create (or load) collection
        self.collection = self.client.get_or_create_collection(
            name="query_cache"
        )

        self.embedder = EmbeddingGenerator()

    def add(
        self,
        question: str,
        answer: str,
    ) -> None:
        """
        Store a question-answer pair in the cache.
        """

        embedding = self.embedder.generate(question)

        self.collection.add(
            ids=[str(uuid.uuid4())],
            embeddings=[embedding],
            documents=[question],
            metadatas=[
                {
                    "answer": answer,
                }
            ],
        )

    def search(
        self,
        question: str,
        n_results: int = 1,
    ) -> CacheResult:
        """
        Search for a semantically similar question.
        """

        embedding = self.embedder.generate(question)

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results,
        )

        # No results found
        if len(results["documents"][0]) == 0:
            return CacheResult(
                hit=False,
            )

        distance = results["distances"][0][0]

        # Cache Hit
        if distance <= MAX_CACHE_DISTANCE:

            answer = results["metadatas"][0][0]["answer"]

            return CacheResult(
                hit=True,
                answer=answer,
                distance=distance,
            )

        # Cache Miss
        return CacheResult(
            hit=False,
            distance=distance,
        )

    def clear(self) -> None:
        """
        Delete all cached entries.
        """

        self.client.delete_collection(
            "query_cache"
        )

        self.collection = self.client.get_or_create_collection(
            "query_cache"
        )