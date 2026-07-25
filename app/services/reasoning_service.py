from app.common.logger import get_logger
from app.models.chunk import ChunkData
from app.prompts.prompt_builder import PromptBuilder
from app.services.llm_service import LLMService

logger = get_logger(__name__)


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

    def __init__(
            self,
            prompt_builder: PromptBuilder,
            llm_service: LLMService,
    ):
        self.prompt_builder = prompt_builder
        self.llm_service = llm_service

    def generate_answer(
        self, question: str, chunks: list[ChunkData]
    ) -> tuple[str, str]:
        """
        Generates an answer using the retrieved chunks.

        Returns:
            tuple(prompt, answer)
        """

        logger.info("Building prompt")

        prompt = self.prompt_builder.build(question=question, chunks=chunks)
        logger.info("Prompt built")

        logger.info("Calling LLM...")

        answer = self.llm_service.invoke(prompt)

        logger.info("LLM returned")

        return prompt, answer
