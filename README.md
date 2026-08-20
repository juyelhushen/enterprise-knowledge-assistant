# Enterprise Knowledge Assistant

An Enterprise Knowledge Assistant built using **FastAPI**, **LangGraph**, **ChromaDB**, and **Ollama**. The application allows users to upload enterprise documents, ask questions in natural language, retrieve accurate answers with citations, and maintain audit logs of all interactions.

---

# Features

* Upload PDF documents
* Automatic document chunking and embedding
* Store embeddings in ChromaDB
* Retrieval-Augmented Generation (RAG)
* Multi-agent workflow using LangGraph
* Answer questions using an LLM
* Source citations for responses
* Document management APIs
* Audit logging for queries and responses
* REST APIs with Swagger UI
* Unit and Integration Tests
* Global exception handling
* Dependency Injection for services and repositories

---

# Tech Stack

| Technology  | Purpose                          |
| ----------- | -------------------------------- |
| Python 3.13 | Programming Language             |
| FastAPI     | REST API                         |
| LangGraph   | Multi-agent RAG Workflow         |
| LangChain   | LLM and RAG Integration          |
| ChromaDB    | Vector Database                  |
| Ollama      | Local LLM and Embeddings         |
| SQLite      | Audit Logs and Document Metadata |
| SQLAlchemy  | Persistence Layer                |
| PyPDF       | PDF Parsing                      |
| Pytest      | Testing                          |

---

# Architecture

The application follows a **layered architecture** with clear separation between the API, application services, domain models, infrastructure, and RAG workflow.

The overall architecture can be represented as:

```text
                         ┌───────────────────────────┐
                         │        Client/User        │
                         │                           │
                         │ Swagger / REST API / UI   │
                         └─────────────┬─────────────┘
                                       │
                                       ▼
                         ┌───────────────────────────┐
                         │       API Layer            │
                         │                           │
                         │ FastAPI Controllers       │
                         │ Request / Response DTOs   │
                         │ Exception Handling        │
                         └─────────────┬─────────────┘
                                       │
                                       ▼
                         ┌───────────────────────────┐
                         │     Application Layer     │
                         │                           │
                         │ DocumentService           │
                         │ DocumentUploadService     │
                         │ IngestionService          │
                         │ RetrieverService          │
                         │ EmbeddingService          │
                         │ WorkflowService           │
                         │ AuditLogService           │
                         └───────┬─────────┬─────────┘
                                 │         │
                    ┌────────────┘         └─────────────┐
                    ▼                                    ▼
          ┌─────────────────────┐              ┌─────────────────────┐
          │   RAG Workflow      │              │   Repository Layer  │
          │                     │              │                     │
          │ LangGraph           │              │ VectorStoreRepository│
          │                     │              │ DocumentRepository  │
          │ Retrieval Agent     │              │ AuditLogRepository  │
          │ Reasoning Agent     │              └──────────┬──────────┘
          │ Citation Agent     │                         │
          └──────────┬──────────┘                         │
                     │                                    │
                     ▼                                    ▼
          ┌─────────────────────┐              ┌─────────────────────┐
          │ Infrastructure      │              │ Persistence         │
          │                     │              │                     │
          │ ChromaFactory       │              │ ChromaDB            │
          │ FileStorageService  │              │ SQLite              │
          │ DocumentLoader      │              │ SQLAlchemy          │
          │ Ollama Integration  │              └─────────────────────┘
          └─────────────────────┘

                     RAG Question Flow

User Question
      │
      ▼
FastAPI
      │
      ▼
WorkflowService
      │
      ▼
LangGraph
      │
      ├──► RetrievalAgent
      │        │
      │        ▼
      │   ChromaDB
      │        │
      │        ▼
      │   Relevant Chunks
      │
      ├──► ReasoningAgent
      │        │
      │        ▼
      │      Ollama
      │        │
      │        ▼
      │      Answer
      │
      └──► CitationAgent
               │
               ▼
           Citations
               │
               ▼
        WorkflowResponse
               │
               ├──────────► AuditLogService
               │
               ▼
             Client
```

---

# Architecture Layers

## 1. API Layer

The **API layer** is responsible for exposing the application through REST endpoints using FastAPI.

It handles:

* HTTP requests
* Request validation
* Response serialization
* HTTP status codes
* Dependency injection
* Routing
* API-level exception handling

Example controllers include:

```text
app/api/
├── routes.py
├── document_controller.py
└── audit_log_controller.py
```

The API layer should not contain business logic.

For example:

```text
POST /documents
       │
       ▼
DocumentController
       │
       ▼
DocumentUploadService
```

This keeps the controller thin and makes the application easier to test.

---

## 2. Schema / DTO Layer

The schema layer defines the objects exchanged through the API.

Examples include:

```text
UploadResponse
WorkflowResponse
Citation
DocumentResponse
AuditLogResponse
AskRequest
```

These models are implemented using **Pydantic**.

The responsibility of this layer is to provide:

* Request validation
* Response validation
* Type safety
* API contracts

For example:

```text
HTTP Request
     │
     ▼
AskRequest
     │
     ▼
Application Service
     │
     ▼
WorkflowResponse
     │
     ▼
HTTP Response
```

This prevents API-specific data structures from leaking into the core application logic.

---

## 3. Application / Service Layer

The **service layer** contains the application's business logic.

Examples include:

```text
DocumentUploadService
DocumentService
IngestionService
EmbeddingService
RetrieverService
WorkflowService
AuditLogService
```

The service layer coordinates different components instead of directly exposing infrastructure details to controllers.

For example, document upload follows:

```text
DocumentUploadService
        │
        ├── FileValidator
        │
        ├── FileStorageService
        │
        └── IngestionService
                  │
                  ├── DocumentLoader
                  ├── ChunkingService
                  └── VectorStoreRepository
```

This separation makes individual components independently testable.

---

## 4. Workflow / Agent Layer

The workflow layer contains the **LangGraph-based multi-agent RAG pipeline**.

The current workflow consists of:

```text
START
  │
  ▼
RetrievalAgent
  │
  ▼
ReasoningAgent
  │
  ▼
CitationAgent
  │
  ▼
END
```

### RetrievalAgent

Responsible for retrieving relevant document chunks from the vector store.

```text
Question
   │
   ▼
RetrieverService
   │
   ▼
VectorStoreRepository
   │
   ▼
ChromaDB
   │
   ▼
Relevant Chunks
```

### ReasoningAgent

Responsible for constructing the prompt and generating an answer using the retrieved context.

```text
Question + Retrieved Chunks
              │
              ▼
       ReasoningService
              │
              ▼
            Ollama
              │
              ▼
            Answer
```

### CitationAgent

Responsible for generating source references from the retrieved document chunks.

```text
Answer + Retrieved Chunks
            │
            ▼
      CitationAgent
            │
            ▼
         Citations
```

The workflow is orchestrated using **LangGraph**, allowing individual agents to remain independently testable and replaceable.

---

## 5. Domain Layer

The domain layer contains application-level data models and business concepts that should remain independent of infrastructure implementations.

Examples include:

```text
DocumentData
ChunkData
AuditLog
WorkflowResult
```

For example:

```text
Document
   │
   ├── content
   ├── metadata
   └── identifier

Chunk
   │
   ├── content
   ├── metadata
   └── identifier
```

The domain layer does not need to know whether data is stored in ChromaDB, SQLite, PostgreSQL, or another database.

---

## 6. Repository Layer

The repository layer provides an abstraction over data storage.

Examples:

```text
VectorStoreRepository
DocumentMetadataRepository
AuditLogRepository
```

Services depend on repository abstractions rather than directly depending on database implementations.

For example:

```text
IngestionService
       │
       ▼
VectorStoreRepository
       │
       ▼
ChromaDB
```

and:

```text
AuditLogService
       │
       ▼
AuditLogRepository
       │
       ▼
SQLite
```

This makes it possible to replace the persistence implementation without changing the application services.

For example, ChromaDB could later be replaced by another vector database.

---

## 7. Infrastructure Layer

The infrastructure layer contains implementations of external technology integrations.

Examples include:

```text
ChromaFactory
SQLite repositories
SQLAlchemy configuration
Ollama integration
File storage
Document loaders
```

The infrastructure layer is where technology-specific code lives.

For example:

```text
ChromaFactory
      │
      ▼
ChromaDB

Ollama Integration
      │
      ▼
Ollama LLM

SQLite Repository
      │
      ▼
SQLite Database
```

This prevents technology-specific code from spreading throughout the application.

---

# Document Ingestion Architecture

When a user uploads a document, the following pipeline is executed:

```text
PDF
 │
 ▼
DocumentUploadService
 │
 ├── Validate File
 │
 ├── Store File
 │
 ▼
IngestionService
 │
 ▼
DocumentLoader
 │
 ▼
DocumentData
 │
 ▼
ChunkingService
 │
 ▼
ChunkData
 │
 ▼
VectorStoreRepository
 │
 ▼
ChromaDB
 │
 ▼
Embeddings
```

The configured chunking parameters are:

```env
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

The chunking strategy uses `RecursiveCharacterTextSplitter`.

---

# Question Answering Architecture

When a user asks a question:

```text
User Question
      │
      ▼
POST /ask
      │
      ▼
WorkflowService
      │
      ▼
LangGraph
      │
      ▼
RetrievalAgent
      │
      ▼
ChromaDB Similarity Search
      │
      ▼
Top-K Relevant Chunks
      │
      ▼
ReasoningAgent
      │
      ▼
Prompt + Context
      │
      ▼
Ollama LLM
      │
      ▼
Generated Answer
      │
      ▼
CitationAgent
      │
      ▼
Answer + Citations
      │
      ├──────────────► AuditLogService
      │
      ▼
FastAPI Response
```

This represents the complete RAG lifecycle implemented in the application.

---

# Audit Logging Architecture

Every question-answer interaction is recorded by the audit logging system.

The logged information includes:

* User question
* Generated answer
* Source documents
* Number of retrieved chunks
* Request latency
* Timestamp

The flow is:

```text
WorkflowService
      │
      ▼
AuditLogService
      │
      ▼
AuditLogRepository
      │
      ▼
SQLite
```

Audit logs can be accessed using:

```text
GET /logs
```

and removed using:

```text
DELETE /logs
```

---

# Dependency Injection

The application uses **Dependency Injection** to keep components loosely coupled.

For example:

```text
Controller
    │
    ▼
Service
    │
    ▼
Repository
    │
    ▼
Infrastructure
```

Dependencies are constructed in the application's dependency/container layer rather than being manually created inside controllers.

This makes it easier to:

* Replace implementations
* Mock dependencies during testing
* Separate application logic from infrastructure
* Maintain the application as it grows

---

# Project Structure

```text
app
├── api
│   ├── routes.py
│   ├── document_controller.py
│   └── audit_log_controller.py
│
├── config
│   └── settings.py
│
├── domain
│   ├── document.py
│   ├── chunk.py
│   └── audit_log.py
│
├── repository
│   ├── vector_store_repository.py
│   ├── document_repository.py
│   └── audit_log_repository.py
│
├── services
│   ├── document_service.py
│   ├── document_upload_service.py
│   ├── ingestion_service.py
│   ├── embedding_service.py
│   ├── retriever_service.py
│   ├── workflow_service.py
│   └── audit_log_service.py
│
├── workflow
│   ├── graph.py
│   ├── state.py
│   └── agents
│
├── infrastructure
│   ├── vectorstore
│   ├── persistence
│   ├── storage
│   └── llm
│
├── schemas
│   ├── requests
│   └── responses
│
├── utils
│
└── main.py

tests
├── unit
├── integration
└── resources

storage
├── chroma
└── audit_logs.db
```

---

# Prerequisites

Before running the application, install:

* Python 3.13+
* Ollama
* Git

---

# Install Ollama

Download from:

https://ollama.com/download

Pull the model:

```bash
ollama pull llama3.2
```

Start Ollama:

```bash
ollama serve
```

---

# Clone Repository

```bash
git clone https://github.com/juyelhushen/enterprise-knowledge-assistant.git
cd enterprise-knowledge-assistant
```

---

# Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configure Environment

Create a `.env` file in the project root.

Example:

```env
OLLAMA_MODEL=llama3.2

CHUNK_SIZE=1000
CHUNK_OVERLAP=200

TOP_K=3

CHROMA_DB_PATH=storage/chroma

AUDIT_DB_PATH=storage/audit_logs.db
```

---

# Run the Application

```bash
uvicorn app.main:app --reload
```

Application:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

# API Endpoints

## Upload Document

```text
POST /documents
```

Upload a PDF document.

---

## List Documents

```text
GET /documents
```

Returns all uploaded documents.

---

## Get Document

```text
GET /documents/{document_id}
```

Returns document metadata.

---

## Delete Document

```text
DELETE /documents/{document_id}
```

Deletes a document and its embeddings.

---

## Ask Question

```text
POST /ask
```

Example request:

```json
{
    "question": "What is annual leave?"
}
```

Example response:

```json
{
    "answer": "...",
    "citations": [
        {
            "source": "employee_handbook.pdf",
            "page": 3
        }
    ]
}
```

---

## Audit Logs

List logs:

```text
GET /logs
```

Delete logs:

```text
DELETE /logs
```

---

# Running Tests

Run all tests:

```bash
pytest
```

Run unit tests:

```bash
pytest tests/unit
```

Run integration tests:

```bash
pytest tests/integration
```

The project includes unit and integration coverage for:

* Document loading
* Chunking
* Embeddings
* Retrieval
* RAG workflow
* Document upload
* Document management
* Audit logging
* API endpoints
* Validators
* Repository implementations

---

# Manual Testing

## Step 1

Open Swagger UI:

```text
http://localhost:8000/docs
```

## Step 2

Upload a PDF using:

```text
POST /documents
```

## Step 3

Verify the document:

```text
GET /documents
```

## Step 4

Ask a question:

```text
What is annual leave?
```

## Step 5

Verify that the response contains:

* Answer
* Source citations

## Step 6

Verify audit logs:

```text
GET /logs
```

## Step 7

Delete the document:

```text
DELETE /documents/{document_id}
```

---

# Example Workflow

```text
                    DOCUMENT INGESTION

Upload PDF
    │
    ▼
File Validation
    │
    ▼
File Storage
    │
    ▼
Document Parsing
    │
    ▼
Chunking
    │
    ▼
Embedding Generation
    │
    ▼
ChromaDB
```

```text
                    QUESTION ANSWERING

User Question
    │
    ▼
FastAPI
    │
    ▼
WorkflowService
    │
    ▼
LangGraph
    │
    ├── RetrievalAgent
    │        │
    │        ▼
    │     ChromaDB
    │        │
    │        ▼
    │   Relevant Chunks
    │
    ├── ReasoningAgent
    │        │
    │        ▼
    │      Ollama
    │        │
    │        ▼
    │      Answer
    │
    └── CitationAgent
             │
             ▼
          Citations
             │
             ▼
       WorkflowResponse
             │
             ├──► AuditLogService
             │
             ▼
           Client
```

---

# Design Principles

The project follows several principles commonly used in production-oriented backend applications:

### Separation of Concerns

Each layer has a clearly defined responsibility.

### Dependency Injection

Services depend on abstractions rather than directly constructing infrastructure components.

### Repository Pattern

Persistence details are isolated behind repository interfaces/implementations.

### DTO-Based API Contracts

Pydantic schemas define clear request and response contracts.

### Modular RAG Architecture

Retrieval, reasoning, and citation responsibilities are separated into independent agents.

### Testability

Services and repositories can be tested independently using mocks and test fixtures.

### Configuration Driven

Important RAG parameters such as chunk size, overlap, top-K retrieval, models, and database paths are configurable through environment settings.

### Explainability

Responses include source citations so users can identify the documents used to generate an answer.

---

# Future Improvements

Possible future enhancements include:

* Conversation memory
* Multi-document collections
* User authentication
* Role-based access control
* Hybrid search
* Re-ranking
* Streaming responses
* Evaluation metrics such as Recall@K and MRR
* Docker deployment
* Production vector database
* Cloud deployment
* Observability and distributed tracing

---

# Author

**Juyel Hushen**

Enterprise Knowledge Assistant Capstone Project

---

# Demo

A short demo video can follow these steps:

1. Start Ollama
2. Start the FastAPI application
3. Open Swagger UI
4. Upload a PDF
5. List uploaded documents
6. Ask multiple questions
7. Show responses with citations
8. View audit logs
9. Delete the document
10. Run the test suite with `pytest` and show all tests passing
