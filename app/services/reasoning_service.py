from app.models.chunk import ChunkData
from app.prompts.prompt_builder import PromptBuilder
from app.services.llm_service import LLMService


class ReasoningService:
    """
    Responsible for generating an answer from the
    retrieved chunks.

    Workflow:
        Question
            ↓
        Prompt Builder
            ↓
        LLM
            ↓
        Answer
    """

    def __init__(self):
        self.prompt_builder = PromptBuilder()
        self.llm_service = LLMService()

    def generate_answer(
            self,
            question: str,
            chunks: list[ChunkData]
    ) -> tuple[str,str]:
        """
        Generates an answer using the retrieved chunks.

        Returns:
            tuple(prompt, answer)
        """

        prompt = self.prompt_builder.build(
            question=question,
            chunks= chunks
        )

        answer = self.llm_service.invoke(prompt)

        return prompt, answer
