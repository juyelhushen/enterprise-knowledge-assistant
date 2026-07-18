from pathlib import Path

from docx import Document as DocxDocument
from pypdf import PdfReader

from app.ingestion.exceptions import UnsupportedDocumentTypeError
from app.models.document import DocumentData


class DocumentLoader:

    def load(self, file_path: Path) -> list[DocumentData]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        suffix = path.suffix.lower()

        if suffix == ".pdf":
            return self._load_pdf(path)

        if suffix == ".docx":
            return self._load_docx(path)

        if suffix == ".txt":
            return self._load_txt(path)

        raise UnsupportedDocumentTypeError(f"Unsupported document type: {suffix}")

    def _load_pdf(self, file_path: Path) -> list[DocumentData]:
        reader = PdfReader(file_path)
        documents = []

        for page_number, page in enumerate(reader.pages, start=1):
            documents.append(
                DocumentData(
                    content=page.extract_text() or "",
                    metadata={
                        "source": file_path.name,
                        "page": page_number,
                    },
                )
            )
        return documents

    def _load_docx(self, file_path: Path) -> list[DocumentData]:
        doc = DocxDocument(file_path)

        text = "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
            if paragraph.text.strip()
        )

        return [
            DocumentData(
                content=text,
                metadata={
                    "source": file_path.name,
                }
            )
        ]


    def _load_txt(self, file_path: Path) -> list[DocumentData]:
        return [
            DocumentData(
                content=file_path.read_text(encoding="utf-8"),
                metadata={
                    "source": file_path.name,
                }
            )
        ]
