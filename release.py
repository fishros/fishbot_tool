import os
from fishbot_tool.__init__ import __version__

def release_docker():
    tag = f"fishros2/fishbot-tool:{__version__}"
    os.system("docker login")
    os.system(f"docker build -t {tag} .")
    os.system(f"docker push {tag}")


release_docker()