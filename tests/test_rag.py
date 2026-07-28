from src.rag.indexer import DocumentIndexer
from src.rag.retriever import DocumentRetriever

# Index document
indexer = DocumentIndexer()

indexer.index_document(
    "data/uploads/TravelPolicy.txt"
)

print()

# Retrieve
retriever = DocumentRetriever()

result = retriever.retrieve(
    "Can employees travel in business class?"
)

print("=" * 70)

for chunk in result.chunks:

    print(f"Source: {chunk.source}")
    print(f"Distance: {chunk.distance}")
    print()
    print(chunk.text)
    print("-" * 70)
    