from fastapi import FastAPI

from app.api.routes import router

from exceptions.custom_exceptions import (
    LLMException,
    RetrievalException,
    DocumentException,
)
from exceptions.handlers import (
    llm_exception_handler,
    retrieval_exception_handler,
    document_exception_handler,
    generic_exception_handler,
)

app = FastAPI(
    title="Enterprise knowledge Assistant",
    version="1.0.0",
)

app.include_router(router)

app.add_exception_handler(
    LLMException,
    llm_exception_handler
)

app.add_exception_handler(
    RetrievalException,
    retrieval_exception_handler
)

app.add_exception_handler(
    DocumentException,
    document_exception_handler
)

app.add_exception_handler(
    Exception,
    generic_exception_handler
)
