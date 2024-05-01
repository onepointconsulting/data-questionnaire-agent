import os
import shutil


def ui():
    os.chdir("./data-wellness-companion-ui")
    os.system("yarn")
    os.system("yarn run build")
    shutil.copytree("./dist", "../ui", dirs_exist_ok=True)
