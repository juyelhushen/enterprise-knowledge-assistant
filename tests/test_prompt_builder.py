from app.models.chunk import ChunkData
from app.prompts.prompt_builder import PromptBuilder


def test_prompt_contains_context():

    chunk = ChunkData(
        id="1",
        content="Employees receive 20 days of annual leave.",
        metadata={"source": "sample.pdf", "page": 1},
    )

    builder = PromptBuilder()

    prompt = builder.build("How many leaves days?", [chunk])

    assert "20 days" in prompt
    assert "sample.pdf" in prompt
    assert "How many leaves days?" in prompt
