import os
import shutil


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
