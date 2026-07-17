from langchain_ollama import ChatOllama

from app.core.config import settings


class LLMService:
    def __init__(self):
        self.llm = ChatOllama(
            model=settings.LLM_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0
        )

    def invoke(self, prompt: str):
        return self.llm.invoke(prompt)
