from pathlib import Path
import tomli
from data_questionnaire_agent.config import cfg


def read_toml(file: Path) -> dict:
    with open(file, "rb") as f:
        return tomli.load(f)


# Need to add a language parameter.
# Pick the right file based on the language parameter.
# Default to English if the language is not supported.

DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ["en", "fa"]


def read_prompts_toml(language=DEFAULT_LANGUAGE) -> dict:

    if language not in SUPPORTED_LANGUAGES:
        print(f"Warning: Language  not supported. Using default language.")
        language = DEFAULT_LANGUAGE

    print(f"Reading prompts from prompts_{language}.toml")

    return read_toml(cfg.project_root / f"prompts_{language}.toml")


selected_language = "fa"  # Just to test with farsi language

prompts = read_prompts_toml(selected_language)


if __name__ == "__main__":
    from data_questionnaire_agent.log_init import logger

    prompts_config = read_prompts_toml()
    assert prompts_config is not None
    assert prompts_config["questionnaire"] is not None
    logger.info("prompts: %s", prompts_config)
