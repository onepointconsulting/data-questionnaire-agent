import asyncio
from data_questionnaire_agent.service.consultant_service import convert_to_markdown, convert_all_consultants

from data_questionnaire_agent.test.provider.consultant_provider import (
    create_simple_consultant,
)

def test_convert_to_markdown():
    consultant = create_simple_consultant()
    markdown = convert_to_markdown([consultant])
    assert markdown is not None, "There is no markdown"
    assert "John" in markdown, "John is not in markdown"
    assert "Doe" in markdown, "Doe is not in markdown"


def test_convert_all_consultants():
    markdown = asyncio.run(convert_all_consultants())
    assert markdown is not None, "there is not markdown"
    from pathlib import Path
    Path("/tmp/consultants.md").write_text(markdown)