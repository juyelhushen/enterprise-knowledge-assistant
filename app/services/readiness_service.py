from app.models.readiness_response import ReadinessResponse


class ReadinessService:

    def ready(self) -> ReadinessResponse:

        chroma = True
        ollama = True
        embedding = True

        status = (
            "READY"
            if chroma and ollama and embedding
            else "NOT_READY"
        )

        return ReadinessResponse(
            status=status,
            chroma=chroma,
            ollama=ollama,
            embedding_model=embedding,
        )