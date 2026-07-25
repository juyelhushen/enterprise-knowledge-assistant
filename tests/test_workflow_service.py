from app.services.workflow_service import WorkflowService


def test_workflow_service(workflow):
    service = WorkflowService(workflow)

    response = service.ask("How many annual leave days?")

    print(response)

    assert response.answer is not None
    assert "20" in response.answer

    assert len(response.citations) == 1
    assert response.citations[0].source == "sample.pdf"
