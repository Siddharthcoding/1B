import fitz, logging
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

class DocumentLoader:
    def __init__(self, chunk_size=7500, chunk_overlap=100):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def load_multiple_pdfs(self, pdf_paths: List[Path]) -> List[Document]:
        docs = []
        for p in pdf_paths:
            doc = fitz.open(str(p)); pages = 0
            for i, page in enumerate(doc):
                text = page.get_text()
                if text.strip():
                    docs.append(Document(
                        page_content=text,
                        metadata={"page": i+1, "source": p.name, "file_path": str(p)}
                    ))
                    pages += 1
            doc.close()
            logger.info(f"Loaded {pages} pages from {p.name}")
        return docs

    def split_documents(self, documents: List[Document]) -> List[Document]:
        return self.splitter.split_documents(documents)
