def test_get_documents(
    client,
    sample_pdf,
):
    with open(sample_pdf, "rb") as f:
        client.post(
            "/documents",
            files={
                "file": (
                    "sample.pdf",
                    f,
                    "application/pdf",
                )
            },
        )

    response = client.get("/documents")

    assert response.status_code == 200

    documents = response.json()

    assert len(documents) == 1

    assert documents[0]["original_filename"] == "sample.pdf"


def test_get_document(
    client,
    sample_pdf,
):
    with open(sample_pdf, "rb") as f:
        client.post(
            "/documents",
            files={
                "file": (
                    "sample.pdf",
                    f,
                    "application/pdf",
                )
            },
        )

    documents = client.get("/documents").json()

    document_id = documents[0]["document_id"]

    response = client.get(
        f"/documents/{document_id}"
    )

    assert response.status_code == 200

    assert (
        response.json()["document_id"]
        == document_id
    )



def test_delete_document(
    client,
    sample_pdf,
):
    with open(sample_pdf, "rb") as f:
        client.post(
            "/documents",
            files={
                "file": (
                    "sample.pdf",
                    f,
                    "application/pdf",
                )
            },
        )

    documents = client.get("/documents").json()

    document_id = documents[0]["document_id"]

    response = client.delete(
        f"/documents/{document_id}"
    )

    assert response.status_code == 204

    response = client.get(
        f"/documents/{document_id}"
    )

    assert response.status_code == 404

def test_delete_document_removes_embeddings(
    client,
    sample_pdf,
    vector_store_repository,
):
    with open(sample_pdf, "rb") as f:
        client.post(
            "/documents",
            files={
                "file": (
                    "sample.pdf",
                    f,
                    "application/pdf",
                )
            },
        )

    documents = client.get("/documents").json()

    document_id = documents[0]["document_id"]

    client.delete(
        f"/documents/{document_id}"
    )

    results = vector_store_repository.similarity_search(
        "annual leave",
        k=3,
    )

    assert len(results) == 0