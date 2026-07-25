from app.models.chunk import ChunkData


def test_chunk_pdf(document_loader, chunker_service, sample_pdf):
    documents = document_loader.load(str(sample_pdf))

    chunks = chunker_service.chunk_documents(documents)

    assert len(chunks) > 0

    assert isinstance(chunks[0], ChunkData)

    assert "chunk_index" in chunks[0].metadata
