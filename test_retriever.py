from src.rag.retriever import DocumentRetriever

retriever = DocumentRetriever()

result = retriever.retrieve(
    "Can employees travel in business class?"
)

print("=" * 60)

for i, chunk in enumerate(result.chunks, start=1):

    print(f"Chunk {i}")
    print(f"Source   : {chunk.source}")
    print(f"Distance : {chunk.distance}")
    print()
    print(chunk.text)
    print("-" * 60)