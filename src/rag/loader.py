"""
Document Loader
Loads enterprise documents from disk.
"""

from pathlib import Path
from pypdf import PdfReader
from docx import Document


class DocumentLoader:
    """
    Loads PDF, DOCX and TXT files.
    """

    def load(self, file_path: str)-> str:
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == ".pdf":
            return self._load_pdf(path)
        
        if suffix == ".docx":
            return self._load_docx(path)

        if suffix == ".txt":
            return self._load_txt(path)

        raise ValueError(
            f"Unsupported file type: {suffix}"
        )
    
    def _load_pdf(self,path: Path,)-> str:
        reader = PdfReader(path)

        text = ""

        for page in reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"
        
        return text

    def _load_docx(self,path: Path,)-> str:
        document = Document(path)
        paragraphs = []

        for paragraph in document.paragraphs:
            paragraphs.append(paragraph.text)
        
        return "\n".join(paragraphs)
    
    def _load_txt(self,path: Path,)-> str:
        return path.read_text(encoding= "utf-8")

        

    