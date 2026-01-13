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


if __name__ == "__main__":
    # Usage:
    #   python -m data_questionnaire_agent.cli.prompt_to_db_loader <language_code> <path_to_toml_file>
    #
    # Example:
    #   python -m data_questionnaire_agent.cli.prompt_to_db_loader en /tmp/hypergility_prompts_en.toml
    #   python -m data_questionnaire_agent.cli.prompt_to_db_loader de /tmp/hypergility_prompts_de.toml
    #   python -m data_questionnaire_agent.cli.prompt_to_db_loader en data_wellness_prompts_en.toml
    #   python -m data_questionnaire_agent.cli.prompt_to_db_loader de data_wellness_prompts_de.toml
    #
    # This script loads prompt categories and prompts from a TOML file into the database for the specified language.
    import asyncio
    import sys
    from data_questionnaire_agent.log_init import logger

    if len(sys.argv) != 3:
        logger.error("Please enter the language code and the file path as an argument.")
        sys.exit(1)

    language_code = sys.argv[1]
    file_path = Path(sys.argv[2])
    assert file_path.exists(), f"File {file_path} does not exist."

    asyncio.run(load_prompts_to_db(file_path, language_code))
    
