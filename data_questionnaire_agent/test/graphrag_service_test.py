import asyncio

from data_questionnaire_agent.service.graphrag_service import graphrag_context


def test_graphrag_context():
    result = asyncio.run(graphrag_context("What are the main topics?"))
    assert len(result) > 100, "Length should be at least 100 characters"
