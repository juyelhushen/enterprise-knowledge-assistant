from app.models.document import DocumentData


def test_load_pdf(loader, sample_pdf):
    documents = loader.load(str(sample_pdf))

    assert len(documents) > 0

    assert isinstance(documents[0], DocumentData)

    assert "Employee Handbook" in documents[0].content

    assert documents[0].metadata["source"] == "sample.pdf"

    assert documents[0].metadata["page"] == 1
