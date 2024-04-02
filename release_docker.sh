docker build -f Dockerfile -t fishros2/fishbot_tool:$GITHUB_REF_NAME .
docker push fishros2/fishbot_tool:$GITHUB_REF_NAME