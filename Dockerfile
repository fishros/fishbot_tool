FROM python:3.8.12

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install rich esptool pyserial

RUN pip install prompt_toolkit requests

COPY fishbot_tool /fishbot_tool/fishbot_tool
ENV PYTHONPATH /fishbot_tool
WORKDIR /fishbot_tool/fishbot_tool

ENTRYPOINT ["python","main.py"]
# docker build -t fishros2/fishbot-tool .
# docker run -it --rm --privileged -v /dev:/dev fishros2/fishbot-tool python main.py


