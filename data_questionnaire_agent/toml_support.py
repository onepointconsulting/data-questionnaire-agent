from os import replace
from pathlib import Path
import tomli
from data_questionnaire_agent.config import cfg
import shutil


def read_toml(file: Path) -> dict:
    with open(file, "rb") as f:
        return tomli.load(f)


def read_prompts_toml() -> dict:
    prompts_file = 'prompts.toml'
    prompts_file_pt = 'prompts_pt.toml'
    # todo: change this to the correct path
    shutil.copyfile(prompts_file_pt, f"{cfg.project_root}/{prompts_file}")
     
    return read_toml(cfg.project_root / prompts_file)


prompts = read_prompts_toml()

if __name__ == "__main__":
    from data_questionnaire_agent.log_init import logger
    
    prompts_config = read_prompts_toml()
    
    assert prompts_config is not None
    assert prompts_config["questionnaire"] is not None
    logger.info("prompts: %s", prompts_config)
