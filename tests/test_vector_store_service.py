from app.mapper.document_mapper import DocumentMapper


def test_similarity_search(
    loader,
    chunker,
    vector_store,
    sample_pdf,
):
    documents = loader.load(str(sample_pdf))

    chunks = chunker.chunk_documents(documents)

    docs = DocumentMapper.to_documents(chunks)

    vector_store.add_documents(docs)

    results = vector_store.similarity_search("How many annual leave days?")

    assert len(results) > 0

    assert "20 days" in results[0].page_content
