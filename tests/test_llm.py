from app.services.llm_service import LLMService


def main():
    service = LLMService()

    response = service.invoke(
        "Reply with exactly one word: Hello"
    )

    print(response.content)


if __name__ == "__main__":
    main()