from langchain_core.documents import Document

from app.models.chunk import ChunkData


class DocumentMapper:

    @staticmethod
    def to_documents(
        chunks: list[ChunkData],
    ) -> list[Document]:

        documents = []

        for chunk in chunks:
            documents.append(
                Document(
                    id=chunk.id,
                    page_content=chunk.content,
                    metadata=chunk.metadata,
                )
            )

        return documents