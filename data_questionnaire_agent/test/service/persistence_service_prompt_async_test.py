import pytest
from data_questionnaire_agent.model.prompt import DBPrompt, PromptCategory
from data_questionnaire_agent.service.persistence_service_prompt_async import (
    delete_prompt,
    delete_prompt_category,
    persist_prompt,
    persist_prompt_category,
    read_prompt,
    read_prompt_by_prompt_key,
)


async def create_prompt_category():
    prompt_category = PromptCategory(
        name="Test Prompt Category",
        prompt_category_parent_id=None,
        language_code="en",
    )
    prompt_category = await persist_prompt_category(prompt_category)
    return prompt_category


@pytest.mark.asyncio
async def test_persist_prompt_category():
    prompt_category_id = None
    try:
        prompt_category = await create_prompt_category()
        prompt_category_id = prompt_category.id
        assert prompt_category is not None
        assert prompt_category_id is not None
        assert prompt_category.name == "Test Prompt Category"
        assert prompt_category.prompt_category_parent_id is None
        assert prompt_category.created_at is not None
        assert prompt_category.updated_at is None
    finally:
        if prompt_category_id:
            deleted = await delete_prompt_category(prompt_category_id)
            assert deleted == 1, "Deleted count is expected to be 1"


@pytest.mark.asyncio
async def test_persist_prompt():
    prompt_id = None
    try:
        prompt_category = await create_prompt_category()
        prompt = DBPrompt(
            prompt_category=prompt_category,
            prompt_key="test_prompt_key",
            prompt="test_prompt",
        )
        prompt = await persist_prompt(prompt)
        prompt_id = prompt.id
        assert prompt is not None
        assert prompt.id is not None
        prompt_from_db = await read_prompt(prompt_id)
        assert prompt_from_db is not None
        assert prompt_from_db.id is not None
        assert prompt_from_db.prompt_category.id is not None
        assert prompt_from_db.prompt_category.name == prompt_category.name
        assert prompt_from_db.prompt_category.prompt_category_parent_id is None
        assert prompt_from_db.prompt_key == "test_prompt_key"
        assert prompt_from_db.prompt == "test_prompt"
        assert prompt_from_db.created_at is not None
        prompt_from_db = await read_prompt_by_prompt_key(["Test Prompt Category"], "test_prompt_key")
        assert prompt_from_db is not None
        assert prompt_from_db.id is not None
        assert prompt_from_db.prompt_category.id is not None
        assert prompt_from_db.prompt_category.name == prompt_category.name
        assert prompt_from_db.prompt_category.prompt_category_parent_id is None
        assert prompt_from_db.prompt_key == "test_prompt_key"
        assert prompt_from_db.prompt == "test_prompt"
        assert prompt_from_db.created_at is not None
    finally:
        if prompt_id:
            deleted = await delete_prompt(prompt_id)
            assert deleted == 1, "Deleted count is expected to be 1"
        if prompt_category.id:
            deleted = await delete_prompt_category(prompt_category.id)
            assert deleted == 1, "Deleted count is expected to be 1"
