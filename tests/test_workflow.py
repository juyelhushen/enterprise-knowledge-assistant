from app.graph.workflow import create_workflow


def test_workflow():

    workflow = create_workflow()

    result = workflow.invoke(
        {
            "question": "How many annual leave days?"
        }
    )

    print("\n========== RESULT ==========\n")
    print(result)

    assert result["answer"] is not None
    assert "20" in result["answer"]

    assert len(result["citations"]) == 1
    assert result["citations"][0]["source"] == "sample.pdf"