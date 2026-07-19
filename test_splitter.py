from src.rag.loader import DocumentLoader
from src.rag.splitter import DocumentSplitter

loader = DocumentLoader()

splitter = DocumentSplitter()

text = loader.load(
    "data/uploads/TravelPolicy.pdf"
)

chunks = splitter.split(text)

print(f"Total Chunks: {len(chunks)}")

print()

print(chunks[0])

print()

print("=" * 60)

print()

print(chunks[1])