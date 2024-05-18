import os
import shutil


def ui():
    os.chdir("./web/frontend")
    os.system("yarn")
    os.system("yarn run build")
    shutil.copytree("./dist", "../ui", dirs_exist_ok=True)