def test_embedding_dimension(embedding_service):
    embedding = embedding_service.embed_text("Employees receive annual leave.")

    assert isinstance(embedding, list)

    assert len(embedding) > 0

    assert all(isinstance(x, float) for x in embedding)
