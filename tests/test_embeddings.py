from src.cache.embeddings import EmbeddingGenerator

embedder = EmbeddingGenerator()

embedding = embedder.generate(
    "What is the baggage allowance?"
)

print(f"Embedding length: {len(embedding)}")

print(embedding[:10])