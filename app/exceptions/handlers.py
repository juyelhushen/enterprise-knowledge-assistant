from datetime import UTC, datetime

from fastapi import Request
from fastapi.responses import JSONResponse
from models.error_response import ErrorResponse

from app.exceptions.custom_exceptions import (
    DocumentException,
    LLMException,
    RetrievalException,
)


async def llm_exception_handler(request: Request, exc: LLMException):
    response = ErrorResponse(
        timestamp=datetime.now(UTC),
        status=503,
        error="Service Unavailable",
        message=str(exc),
        path=request.url.path,
    )

    return JSONResponse(status_code=503, content=response.model_dump(mode="json"))


async def retrieval_exception_handler(request: Request, exc: RetrievalException):
    response = ErrorResponse(
        timestamp=datetime.now(UTC),
        status=500,
        error="Retrieval Error",
        message=str(exc),
        path=request.url.path,
    )

    return JSONResponse(status_code=500, content=response.model_dump(mode="json"))


async def document_exception_handler(request: Request, exc: DocumentException):
    response = ErrorResponse(
        timestamp=datetime.now(UTC),
        status=404,
        error="Document Not Found",
        message=str(exc),
        path=request.url.path,
    )

    return JSONResponse(status_code=404, content=response.model_dump(mode="json"))


async def generic_exception_handler(request: Request, exc: Exception):
    response = ErrorResponse(
        timestamp=datetime.now(UTC),
        status=500,
        error="Internal Server Error",
        message="An unexpected error occurred.",
        path=request.url.path,
    )

    return JSONResponse(status_code=500, content=response.model_dump(mode="json"))
