from app.services.llm_service import LLMService


def test_llm_connection():
    service = LLMService()

    response = service.invoke("Reply with exactly one word: Hello")
    print(response)
    assert response is not None
    assert len(response) > 0
