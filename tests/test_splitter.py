from src.rag.loader import DocumentLoader
from src.rag.splitter import DocumentSplitter

loader = DocumentLoader()

splitter = DocumentSplitter()

text = loader.load(
    "data/uploads/TravelPolicy.txt"
)

chunks = splitter.split(text)

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i+1}")
    print("=" * 60)
    print(chunk)