from pathlib import Path

from data_questionnaire_agent.model.prompt import DBPrompt, PromptCategory
from data_questionnaire_agent.service.persistence_service_prompt_async import persist_prompt, persist_prompt_category
from data_questionnaire_agent.toml_support import read_toml
from data_questionnaire_agent.config import cfg


async def load_prompts_to_db(file_path: Path, language_code: str):
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} not found")
    toml_data = read_toml(file_path)

    async def process_section(key: str, value: dict, parent_id: int | None = None):
        prompt_category = PromptCategory(
            name=key,
            prompt_category_parent_id=parent_id,
            language_code=language_code,
        )
        prompt_category = await persist_prompt_category(prompt_category)
        for subkey, subvalue in value.items():
            if isinstance(subvalue, dict):
                await process_section(subkey, subvalue, prompt_category.id)
            else:
                prompt = DBPrompt(
                    prompt_category=prompt_category,
                    prompt_key=subkey,
                    prompt=str(subvalue),
                )
                prompt = await persist_prompt(prompt)

    for key, value in toml_data.items():
        await process_section(key, value)


