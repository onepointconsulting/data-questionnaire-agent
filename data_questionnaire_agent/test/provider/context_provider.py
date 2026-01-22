import json
from pathlib import Path

from data_questionnaire_agent.model.context import Context


def create_sample_context() -> Context:
    context_file = (
        Path(__file__).parent.parent.parent.parent / "data" / "full_context.json"
    )
    assert context_file.exists(), f"Context file {context_file} does not exist"
    with open(context_file, "r", encoding="utf-8") as f:
        context_json = json.load(f)
    return Context(**context_json)
