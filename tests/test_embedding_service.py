from app.services.embedding_service import EmbeddingService


def test_embed_single_text():
    service = EmbeddingService()

    embedding = service.embed_text(
        "Employees receive 20 days of annual leave."
    )

    assert embedding is not None
    assert isinstance(embedding, list)
    assert len(embedding) > 0
    assert all(isinstance(value, float) for value in embedding)


def test_embed_multiple_texts():
    service = EmbeddingService()

    texts = [
        "Annual Leave Policy",
        "Health Insurance",
        "Work From Home",
    ]

    embeddings = service.embed_texts(texts)

    assert len(embeddings) == len(texts)

    for embedding in embeddings:
        assert isinstance(embedding, list)
        assert len(embedding) > 0