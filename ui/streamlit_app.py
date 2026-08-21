import json
import os
from typing import Any

import requests
import streamlit as st

DEFAULT_API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
REQUEST_TIMEOUT_SECONDS = 60


def apply_animated_theme() -> None:
    st.markdown(
        """
        <style>
        @keyframes gradientFlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .hero {
            background: linear-gradient(120deg, #2563eb, #7c3aed, #0ea5e9);
            background-size: 200% 200%;
            animation: gradientFlow 8s ease infinite;
            color: #ffffff;
            padding: 1.2rem 1.4rem;
            border-radius: 14px;
            margin-bottom: 0.9rem;
            box-shadow: 0 8px 24px rgba(2, 6, 23, 0.25);
        }

        .hero h1 {
            margin: 0 0 0.3rem 0;
            font-size: 1.8rem;
            line-height: 1.2;
        }

        .hero p {
            margin: 0;
            opacity: 0.95;
            font-size: 0.95rem;
        }

        [data-testid="stVerticalBlock"] > div {
            animation: fadeInUp 0.4s ease;
        }

        .stButton > button {
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 18px rgba(2, 6, 23, 0.2);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def build_url(base_url: str, path: str) -> str:
    return f"{base_url.rstrip('/')}{path}"


def parse_error(response: requests.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        return response.text or f"HTTP {response.status_code}"

    if isinstance(payload, dict):
        message = payload.get("message")
        error = payload.get("error")
        detail = payload.get("detail")
        if isinstance(message, str) and message:
            return message
        if isinstance(error, str) and error:
            return error
        if isinstance(detail, str) and detail:
            return detail
    return json.dumps(payload)


def request_json(
    method: str,
    base_url: str,
    path: str,
    **kwargs: Any,
) -> Any:
    response = requests.request(
        method=method,
        url=build_url(base_url, path),
        timeout=REQUEST_TIMEOUT_SECONDS,
        **kwargs,
    )
    if response.status_code >= 400:
        raise RuntimeError(parse_error(response))

    if response.status_code == 204 or not response.content:
        return None
    return response.json()


st.set_page_config(page_title="Enterprise Knowledge Assistant", layout="wide")
apply_animated_theme()
st.markdown(
    """
    <div class="hero">
        <h1>Enterprise Knowledge Assistant</h1>
        <p>Document upload, Q&A with citations, and audit log review</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Backend")
    api_base_url = st.text_input("FastAPI Base URL", value=DEFAULT_API_BASE_URL).strip()
    health_col, ready_col = st.columns(2)
    if health_col.button("Health"):
        try:
            health = request_json("GET", api_base_url, "/health")
            st.success(f"Status: {health.get('status', 'unknown')}")
        except requests.RequestException as exc:
            st.error(f"Request failed: {exc}")
        except RuntimeError as exc:
            st.error(str(exc))

    if ready_col.button("Ready"):
        try:
            ready = request_json("GET", api_base_url, "/ready")
            st.success(f"Ready: {ready.get('ready', False)}")
        except requests.RequestException as exc:
            st.error(f"Request failed: {exc}")
        except RuntimeError as exc:
            st.error(str(exc))

ask_tab, documents_tab, logs_tab = st.tabs(["Ask", "Documents", "Audit Logs"])

with ask_tab:
    st.subheader("Ask a question")
    question = st.text_area(
        "Question",
        placeholder="Example: What is the annual leave policy?",
        height=120,
    )
    if st.button("Get Answer", type="primary"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            try:
                with st.spinner("Generating answer..."):
                    response = request_json(
                        "POST",
                        api_base_url,
                        "/ask",
                        json={"question": question.strip()},
                    )
                st.markdown("**Answer**")
                st.write(response.get("answer", "No answer returned."))

                citations = response.get("citations", [])
                st.markdown("**Citations**")
                if citations:
                    st.table(citations)
                else:
                    st.info("No citations returned.")
                st.toast("Answer ready")
            except requests.RequestException as exc:
                st.error(f"Request failed: {exc}")
            except RuntimeError as exc:
                st.error(str(exc))

with documents_tab:
    st.subheader("Upload documents")
    uploaded_files = st.file_uploader(
        "Select files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
    )
    if st.button("Upload Selected Files"):
        if not uploaded_files:
            st.warning("Select at least one file.")
        else:
            uploaded_successfully = 0
            for uploaded_file in uploaded_files:
                try:
                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type or "application/octet-stream",
                        )
                    }
                    with st.spinner(f"Uploading {uploaded_file.name}..."):
                        result = request_json(
                            "POST", api_base_url, "/documents", files=files
                        )
                    st.success(
                        f"{uploaded_file.name}: {result.get('message', 'Uploaded successfully.')}"
                    )
                    uploaded_successfully += 1
                except requests.RequestException as exc:
                    st.error(f"{uploaded_file.name}: Request failed: {exc}")
                except RuntimeError as exc:
                    st.error(f"{uploaded_file.name}: {exc}")
            if uploaded_successfully:
                st.balloons()

    st.divider()
    st.subheader("Manage documents")
    try:
        documents = request_json("GET", api_base_url, "/documents")
        if documents:
            st.dataframe(documents, use_container_width=True)
            selected_doc_id = st.selectbox(
                "Select document to delete",
                options=[doc["document_id"] for doc in documents],
            )
            if st.button("Delete Selected Document"):
                try:
                    with st.spinner("Deleting document..."):
                        request_json(
                            "DELETE", api_base_url, f"/documents/{selected_doc_id}"
                        )
                    st.success(f"Deleted document: {selected_doc_id}")
                    st.toast("Document deleted")
                except requests.RequestException as exc:
                    st.error(f"Request failed: {exc}")
                except RuntimeError as exc:
                    st.error(str(exc))
        else:
            st.info("No documents uploaded yet.")
    except requests.RequestException as exc:
        st.error(f"Request failed: {exc}")
    except RuntimeError as exc:
        st.error(str(exc))

with logs_tab:
    st.subheader("Audit logs")
    st.button("Refresh Logs")
    clear_logs = st.button("Clear Logs")

    if clear_logs:
        try:
            with st.spinner("Clearing logs..."):
                request_json("DELETE", api_base_url, "/logs")
            st.success("Audit logs cleared.")
            st.toast("Logs cleared")
        except requests.RequestException as exc:
            st.error(f"Request failed: {exc}")
        except RuntimeError as exc:
            st.error(str(exc))

    try:
        logs = request_json("GET", api_base_url, "/logs")
        if logs:
            st.dataframe(logs, use_container_width=True)
        else:
            st.info("No audit logs available.")
    except requests.RequestException as exc:
        st.error(f"Request failed: {exc}")
    except RuntimeError as exc:
        st.error(str(exc))
