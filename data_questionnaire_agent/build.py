from enum import StrEnum
import json
import os
import shutil

from pathlib import Path


def ui():
    os.chdir("./data-wellness-companion-ui")
    os.system("yarn")
    if os.path.exists("./dist"):
        shutil.rmtree("./dist")
    os.system("yarn run build")
    if os.path.exists("../ui"):
        shutil.rmtree("../ui")
    shutil.copytree("./dist", "../ui", dirs_exist_ok=True)


def check():
    os.system("black .")
    os.system("ruff check --fix .")


class ProjectName(StrEnum):
    """Supported project names"""
    D_WELL = "d-well"
    RES_AI = "res-ai"


class Environment(StrEnum):
    """Supported environments"""
    PRODUCTION = "production"
    DEVELOPMENT = "development"


def create_index_html(project_name: ProjectName, environment: Environment):
    base_folder = Path(__file__).resolve().parent.parent
    ui_folder = base_folder / "data-wellness-companion-ui"
    assert ui_folder.exists(), f"{ui_folder} does not exist"
    index_config_folder = ui_folder / "config"
    assert index_config_folder.exists(), f"{index_config_folder} does not exist"
    with open(index_config_folder / "ui-configs.json", "r", encoding="utf-8") as f:
        ui_configs = json.load(f)
    ui_config = ui_configs[project_name]
    environment_config = ui_config[environment]
    index_template_path = index_config_folder / "index-template.html"
    assert index_template_path.exists(), f"{index_template_path} does not exist"
    print(f"Creating index.html for {project_name}")
    index_html = index_template_path.read_text(encoding="utf-8")
    for key, value in ui_config.items():
        if isinstance(value, str):
            index_html = index_html.replace(f"{{{{ {key} }}}}", value)
    for key, value in environment_config.items():
        index_html = index_html.replace(f"{{{{ {key} }}}}", str(value))
    
    target_path = base_folder / "ui" / "index.html"
    target_path.write_text(index_html, encoding="utf-8")
    print(f"Created index.html for {project_name} in {target_path}")

    (ui_folder / "index.html").write_text(index_html, encoding="utf-8")


if __name__ == "__main__":
    import sys

    project_name = ProjectName.RES_AI
    environment = Environment.DEVELOPMENT
    if len(sys.argv) == 3:
        project_name = ProjectName(sys.argv[1])
        environment = Environment(sys.argv[2])
    print(f"Creating index.html for {project_name} in {environment}")
    create_index_html(project_name, environment)
