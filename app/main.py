from fastapi import FastAPI

from app.api.audit_log_controller import audit_router
from app.api.document_controller import doc_router
from app.api.routes import router
from app.exceptions.custom_exceptions import (
    DocumentException,
    FileValidationException,
    LLMException,
    RetrievalException,
)
from app.exceptions.handlers import (
    document_exception_handler,
    generic_exception_handler,
    handle_file_validation,
    llm_exception_handler,
    retrieval_exception_handler,
)

app = FastAPI(
    title="Enterprise knowledge Assistant",
    version="1.0.0",
)

app.include_router(router)
app.include_router(doc_router)

app.include_router(audit_router)

app.add_exception_handler(LLMException, llm_exception_handler)

app.add_exception_handler(RetrievalException, retrieval_exception_handler)

app.add_exception_handler(DocumentException, document_exception_handler)

app.add_exception_handler(FileValidationException, handle_file_validation)

app.add_exception_handler(Exception, generic_exception_handler)
