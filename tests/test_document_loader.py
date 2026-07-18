from pathlib import Path

from app.ingestion.document_loader import DocumentLoader

PROJECT_ROOT = Path(__file__).resolve().parent.parent
pdf_path = PROJECT_ROOT / "documents" / "sample.pdf"


def main():
    print(pdf_path)
    loader = DocumentLoader()

    documents = loader.load(str(pdf_path))

    print(f"Loaded {len(documents)} documents.\n")

    for document in documents:
        print(document.metadata)
        print(document.content)
        print("_" * 50)

if __name__ == "__main__":
    main()