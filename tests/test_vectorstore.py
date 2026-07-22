from src.rag.loader import DocumentLoader
from src.rag.splitter import DocumentSplitter
from src.rag.vectorstore import DocumentVectorStore

loader = DocumentLoader()

splitter = DocumentSplitter()

store = DocumentVectorStore()

store.clear()

text = loader.load(
    "data/uploads/TravelPolicy.txt"
)

chunks = splitter.split(text)

store.add_document(
    chunks=chunks,
    source="TravelPolicy.txt",
)

print(f"Stored {len(chunks)} chunks.")