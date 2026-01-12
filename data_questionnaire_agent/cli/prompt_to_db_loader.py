from pathlib import Path

from data_questionnaire_agent.toml_support import read_toml
from data_questionnaire_agent.config import cfg


def load_prompts_to_db(file_path: Path):
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} not found")
    toml_data = read_toml(file_path)

    def process_section(key: str, value: dict, parent_id: int | None = None):
        for subkey, subvalue in value.items():
            if isinstance(subvalue, dict):
                process_section(subkey, subvalue)
            else:
                print(f"{key}.{subkey}: {subvalue}")

    for key, value in toml_data.items():
        process_section(key, value)


if __name__ == "__main__":
    language_code = "en"
    file_path = cfg.project_root / f"{cfg.prompts_prefix}_{language_code}.toml"
    load_prompts_to_db(file_path)