from app.common.logger import get_logger
from app.graph.workflow import create_workflow

logger = get_logger(__name__)

def test_workflow():

    workflow = create_workflow()

    result = workflow.invoke({"question": "How many annual leave days?"})

    print("\n========== RESULT ==========\n")
    logger.info(result)

    assert result["answer"] is not None
    assert "20" in result["answer"]

    assert result["citations"][0]["source"] == "sample.pdf"
    assert result["citations"][0]["page"] == 1
