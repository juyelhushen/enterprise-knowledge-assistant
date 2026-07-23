from app.models.chunk import ChunkData


class PromptBuilder:
    SYSTEM_PROMPT = """
    You are an Enterprise Knowledge Assistant.
    
    Answer ONLY using the provided context.
    
    If the answer cannot be found in the context,
    respond exactly with:
    
    "I don't have enough information to answer that."
    
    Do not make up facts.
    """.strip()

    def build(
        self,
        question: str,
        chunks: list[ChunkData],
    ) -> str:
        context = self._build_context(chunks)

        return f"""
{self.SYSTEM_PROMPT}

Context:
---------
{context}

Question:
{question}

Answer:    
""".strip()

    def _build_context(self, chunks: list[ChunkData]) -> str:
        sections = []

        for index, chunk in enumerate(chunks, start=1):
            source = chunk.metadata.get("source", "Unknown")

            page = chunk.metadata.get("page", "?")

            sections.append(
                f"""
Document {index}
Source: {source}
Page: {page}

{chunk.content}
""".strip()
            )
        return "\n\n---------------\n\n".join(sections)
