from pathlib import Path

from app.ingestion.document_loader import DocumentLoader

PROJECT_ROOT = Path(__file__).resolve().parent.parent
pdf_path = PROJECT_ROOT / "documents" / "sample.pdf"


def test_pdf_loader():
    print(pdf_path)
    loader = DocumentLoader()

    docs = loader.load(str(pdf_path))

    assert len(docs) > 0

    assert docs[0].metadata["source"] == "sample.pdf"


