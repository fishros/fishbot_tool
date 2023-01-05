import os
from fishbot_tool.__init__ import __version__


def run_commad(command):
    r = os.popen(command)
    text = r.read()
    r.close()
    return text.replace("\r", "").replace('\n', "")


def replace(file, value, new_value):
    data = ""
    with open(file, "r") as f:
        data = f.read()
    data = data.replace(value, new_value)
    with open(file, "w") as f:
        f.write(data)


def release_docker():
    tag = f"fishros2/fishbot-tool:{__version__}"
    version_code = run_commad("git rev-parse --short HEAD")
    print(f"当前构建版本代码{version_code}")
    replace("fishbot_tool/main.ui", "VCODE", version_code)
    os.system("docker login")
    os.system(f"docker build -t {tag} .")
    os.system(f"docker push {tag}")
    replace("fishbot_tool/main.ui", version_code, "VCODE")


release_docker()
