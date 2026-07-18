from app.models.chunk import ChunkData


def test_chunk_pdf(loader, chunker, sample_pdf):
    documents = loader.load(str(sample_pdf))

    chunks = chunker.chunk_documents(documents)

    assert len(chunks) > 0

    assert isinstance(chunks[0], ChunkData)

    assert "chunk_index" in chunks[0].metadata