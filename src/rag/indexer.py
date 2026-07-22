"""
Document Indexer

Indexes enterprise documents into the RAG vector store.
"""

from pathlib import Path

from src.rag.loader import DocumentLoader
from src.rag.splitter import DocumentSplitter
from src.rag.vectorstore import DocumentVectorStore


class DocumentIndexer:

    def __init__(self):

        self.loader = DocumentLoader()

        self.splitter = DocumentSplitter()

        self.store = DocumentVectorStore()

    def index_document(
        self,
        file_path: str,
    ):

        text = self.loader.load(file_path)

        chunks = self.splitter.split(text)

        self.store.add_document(
            chunks=chunks,
            source=Path(file_path).name,
        )

        print(f"Indexed {len(chunks)} chunks.")