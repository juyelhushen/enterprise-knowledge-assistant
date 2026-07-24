from app.models.health_response import HealthResponse


class HealthService:

    def health(self) -> HealthResponse:
        return HealthResponse(
            status='UP',
        )
