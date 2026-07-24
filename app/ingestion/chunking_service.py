import uuid

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings
from app.models.chunk import ChunkData
from app.models.document import DocumentData


class ChunkingService:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
        )

    def chunk_documents(self, documents: list[DocumentData]) -> list[ChunkData]:
        chunks = []
        for document in documents:
            texts = self.splitter.split_text(document.content)

            for index, text in enumerate(texts):
                metadata = dict(document.metadata)
                metadata["chunk_index"] = index
                chunks.append(
                    ChunkData(
                        id=str(uuid.uuid4()),
                        content=text,
                        metadata=metadata,
                    )
                )
        return chunks
