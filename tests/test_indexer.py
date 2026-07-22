from src.rag.indexer import DocumentIndexer

indexer = DocumentIndexer()

indexer.index_document(
    "data/uploads/TravelPolicy.txt"
)