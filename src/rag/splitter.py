"""
Document Splitter

Splits large documents into smaller chunks
for embedding and retrieval.
"""


from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentSplitter:
    """
    Splits documents into overlapping chunks.
    """

    def __init__(self,chunk_size: int = 500, chunk_overlap: int = 100,):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
        )
    

    def split(self, text: str,)->list[str]:
        """
        Split document into chunks
        """

        return self.splitter.split_text(text)

