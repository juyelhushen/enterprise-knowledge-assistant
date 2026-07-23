from app.models.chunk import ChunkData
from app.models.document import DocumentData


class RAGDebugger:
    @staticmethod
    def print_documents(documents: list[DocumentData]):

        print("\n" + "=" * 80)
        print("Documents:")
        print("=" * 80)

        for index, document in enumerate(documents, start=1):
            print(f"\nDocument {index}")

            print(f"Metadata : {document.metadata}")

            preview = document.content[:300]

            print(preview)

            if len(document.content) > 300:
                print("...")

    @staticmethod
    def print_chunks(chunks: list[ChunkData]):
        print("\n" + "=" * 80)
        print("Chunks:")
        print("=" * 80)

        print(f"\nTotal chunks: {len(chunks)}")

        for chunk in chunks:
            print("-" * 80)
            print("ID")
            print(chunk.id)
            print()

            print("Metadata")
            print(chunk.metadata)

            print()

            print("Content")
            print(chunk.content[:300])

            print()

    @staticmethod
    def print_embedding(embedding: list[float]):

        print("\n" + "=" * 80)
        print("Embedding:")
        print("=" * 80)

        print("Dimension:", len(embedding))

        print()

        print("First 10 values")
        print(embedding[:10])

    @staticmethod
    def print_retrieval(chunks: list[ChunkData]):

        print("\n" + "=" * 80)
        print("RETRIEVED CHUNKS")
        print("=" * 80)

        for index, chunk in enumerate(chunks, start=1):
            print(f"\nResult {index}")

            print("Metadata")
            print(chunk.metadata)

            print()

            print(chunk.content[:300])

    @staticmethod
    def print_prompt(prompt: str):
        print("\n" + "=" * 80)
        print("Prompt:")
        print("=" * 80)

        print(prompt)

    @staticmethod
    def print_response(response: str):

        print("\n" + "=" * 80)
        print("LLM RESPONSE:")
        print("=" * 80)

        print(response)
