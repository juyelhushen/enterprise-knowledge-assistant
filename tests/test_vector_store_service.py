def test_similarity_search(
    loader,
    chunker,
    vector_store,
    sample_pdf,
):
    documents = loader.load(str(sample_pdf))

    chunks = chunker.chunk_documents(documents)

    vector_store.add_chunks(chunks)

    results = vector_store.similarity_search(
        "How many annual leave days?"
    )

    assert len(results) > 0

    assert "20 days" in results[0].page_content