from app.prompts.prompt_builder import PromptBuilder
from app.services.llm_service import LLMService
from app.services.retriever_service import RetrieverService


class RAGService:

    def __init__(self):
        self.retriever = RetrieverService()
        self.prompt_builder = PromptBuilder()
        self.llm = LLMService()

    def answer(
            self,
            question: str,
    ) -> str:

        chunks = self.retriever.retrieve(question)

        if not chunks:
            return "I'm sorry, I couldn't find any relevant information to answer your question."

        prompt = self.prompt_builder.build(
            question,
            chunks,
        )

        response = self.llm.invoke(prompt)

        return response.content