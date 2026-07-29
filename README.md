# Enterprise Knowledge Assistant

An Enterprise Knowledge Assistant built using **FastAPI**, **LangGraph**, **ChromaDB**, and **Ollama**. The application allows users to upload enterprise documents, ask questions in natural language, retrieve accurate answers with citations, and maintain audit logs of all interactions.

---

# Features

- Upload PDF documents
- Automatic document chunking and embedding
- Store embeddings in ChromaDB
- Retrieval-Augmented Generation (RAG)
- Answer questions using an LLM
- Source citations for every response
- Audit logging for every query
- REST APIs with Swagger UI
- Unit and Integration Tests

---

# Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.13 | Programming Language |
| FastAPI | REST API |
| LangGraph | RAG Workflow |
| LangChain | LLM Integration |
| ChromaDB | Vector Database |
| Ollama | Local LLM |
| SQLite | Audit Logs |
| PyPDF | PDF Parsing |
| Pytest | Testing |

---

# Project Structure

```
app
├── api
├── config
├── domain
├── repository
├── services
├── workflow
├── schemas
├── utils
└── main.py

tests
├── unit
└── integration

storage
├── chroma
└── audit_logs.db
```

---

# Prerequisites

Before running the application, install:

- Python 3.13+
- Ollama
- Git

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

Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux / Mac

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

```
http://localhost:8000
```

Swagger UI:

```
http://localhost:8000/docs
```

---

# API Endpoints

## Upload Document

```
POST /documents
```

Upload a PDF document.

---

## List Documents

```
GET /documents
```

Returns all uploaded documents.

---

## Get Document

```
GET /documents/{document_id}
```

Returns document metadata.

---

## Delete Document

```
DELETE /documents/{document_id}
```

Deletes a document and its embeddings.

---

## Ask Question

```
POST /ask
```

Example Request

```json
{
    "question": "What is annual leave?"
}
```

Example Response

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

List Logs

```
GET /logs
```

Delete Logs

```
DELETE /logs
```

---

# Running Tests

Run all tests

```bash
pytest
```

Run Unit Tests

```bash
pytest tests/unit
```

Run Integration Tests

```bash
pytest tests/integration
```

---

# Manual Testing

## Step 1

Open Swagger UI.

```
http://localhost:8000/docs
```

---

## Step 2

Upload a PDF document using

```
POST /documents
```

---

## Step 3

Verify upload

```
GET /documents
```

---

## Step 4

Ask a question

Example:

```
What is annual leave?
```

---

## Step 5

Verify citations are returned.

---

## Step 6

Verify audit logs

```
GET /logs
```

---

## Step 7

Delete document

```
DELETE /documents/{document_id}
```

---

# Example Workflow

```
Upload PDF
      │
      ▼
Document Parsing
      │
      ▼
Chunking
      │
      ▼
Embeddings
      │
      ▼
Store in ChromaDB
      │
      ▼
User Question
      │
      ▼
Similarity Search
      │
      ▼
LLM
      │
      ▼
Answer + Citations
      │
      ▼
Audit Log
```

---

# Future Improvements

- Conversation memory
- Multi-document collections
- User authentication
- Role-based access control
- Hybrid search
- Streaming responses
- Docker deployment

---

# Author

**Juyel Hushen**

Enterprise Knowledge Assistant Capstone Project

```

---

## Demo

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
10. Run the test suite (`pytest`) and show all tests passing

---

This README keeps the project easy to understand for a mentor while covering setup, testing, and the overall architecture without overwhelming detail.