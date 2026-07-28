from app.services.workflow_service import WorkflowService


def test_workflow_service(workflow, audit_log_service):
    service = WorkflowService(workflow, audit_log_service)

    response = service.ask("How many annual leave days?")

    print(response)

    assert response.answer is not None
    assert "20" in response.answer

    assert len(response.citations) == 1
    assert response.citations[0].source == "sample.pdf"
