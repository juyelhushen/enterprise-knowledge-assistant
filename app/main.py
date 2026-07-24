from app.exceptions.custom_exceptions import LLMException
from app.exceptions.custom_exceptions import RetrievalException
from app.exceptions.custom_exceptions import DocumentException

from app.exceptions.handlers import (
    document_exception_handler,
    generic_exception_handler,
    llm_exception_handler,
    retrieval_exception_handler,
)
from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="Enterprise knowledge Assistant",
    version="1.0.0",
)

app.include_router(router)

app.add_exception_handler(LLMException, llm_exception_handler)

app.add_exception_handler(RetrievalException, retrieval_exception_handler)

app.add_exception_handler(DocumentException, document_exception_handler)

app.add_exception_handler(Exception, generic_exception_handler)
