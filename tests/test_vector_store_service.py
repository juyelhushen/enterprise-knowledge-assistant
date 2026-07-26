def test_similarity_search(
    document_loader,
        chunker_service,
        vector_store,
        sample_pdf,
        vector_store_repository
):
    documents = document_loader.load(sample_pdf)

    chunks = chunker_service.chunk_documents(documents)

    vector_store_repository.add_documents(chunks)

    results = vector_store.similarity_search("How many annual leave days?")

    assert len(results) > 0

    assert "20 days" in results[0].page_content
