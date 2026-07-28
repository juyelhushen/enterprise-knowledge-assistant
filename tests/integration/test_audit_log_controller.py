def ask_question(client, question: str):
    return client.post(
        "/ask",
        json={
            "question": question
        },
    )

def test_get_logs_returns_workflow_logs(
    client,
    sample_pdf,
):
    with open(sample_pdf, "rb") as file:
        upload_response = client.post(
            "/documents",
            files={
                "file": (
                    "sample.pdf",
                    file,
                    "application/pdf",
                )
            },
        )

    assert upload_response.status_code == 201

    ask_response = ask_question(
        client,
        "What is annual leave?",
    )

    assert ask_response.status_code == 200

    response = client.get("/logs")

    assert response.status_code == 200

    logs = response.json()

    assert len(logs) == 1

    log = logs[0]

    assert log["question"] == "What is annual leave?"

    assert len(log["answer"]) > 0

    assert isinstance(log["sources"], list)

    assert log["retrieved_chunks"] > 0

    assert log["latency_ms"] >= 0

    assert log["created_at"] is not None


def test_clear_logs(
    client,
    sample_pdf,
):
    with open(sample_pdf, "rb") as file:
        client.post(
            "/documents",
            files={
                "file": (
                    "sample.pdf",
                    file,
                    "application/pdf",
                )
            },
        )

    ask_question(
        client,
        "What is annual leave?",
    )

    response = client.delete("/logs")

    assert response.status_code == 204

    response = client.get("/logs")

    assert response.status_code == 200

    assert response.json() == []


def test_logs_are_returned_in_descending_order(
    client,
    sample_pdf,
):
    with open(sample_pdf, "rb") as file:
        client.post(
            "/documents",
            files={
                "file": (
                    "sample.pdf",
                    file,
                    "application/pdf",
                )
            },
        )

    ask_question(client, "Question A")

    ask_question(client, "Question B")

    ask_question(client, "Question C")

    response = client.get("/logs")

    assert response.status_code == 200

    logs = response.json()

    assert len(logs) == 3

    assert logs[0]["question"] == "Question C"

    assert logs[1]["question"] == "Question B"

    assert logs[2]["question"] == "Question A"

def test_get_logs_returns_empty_list_when_no_logs_exist(
    client,
):
    client.delete("/logs")

    response = client.get("/logs")

    assert response.status_code == 200

    assert response.json() == []


def test_every_question_creates_new_log(
    client,
    sample_pdf,
):
    with open(sample_pdf, "rb") as file:
        client.post(
            "/documents",
            files={
                "file": (
                    "sample.pdf",
                    file,
                    "application/pdf",
                )
            },
        )

    questions = [
        "What is annual leave?",
        "Who can approve leave?",
        "How many casual leaves?",
        "What is probation period?",
        "What is maternity leave?",
    ]

    for question in questions:
        ask_question(
            client,
            question,
        )

    response = client.get("/logs")

    logs = response.json()

    assert len(logs) == len(questions)


def test_log_contains_sources(
    client,
    sample_pdf,
):
    with open(sample_pdf, "rb") as file:
        client.post(
            "/documents",
            files={
                "file": (
                    "sample.pdf",
                    file,
                    "application/pdf",
                )
            },
        )

    ask_question(
        client,
        "What is annual leave?",
    )

    logs = client.get("/logs").json()

    assert len(logs[0]["sources"]) > 0


def test_latency_is_recorded(
    client,
    sample_pdf,
):
    with open(sample_pdf, "rb") as file:
        client.post(
            "/documents",
            files={
                "file": (
                    "sample.pdf",
                    file,
                    "application/pdf",
                )
            },
        )

    ask_question(
        client,
        "What is annual leave?",
    )

    log = client.get("/logs").json()[0]

    assert log["latency_ms"] >= 0