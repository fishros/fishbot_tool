FROM python:3.8.12

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install rich esptool pyserial

RUN pip install prompt_toolkit requests

# docker build -t fishros2/fishbot-tool .
# docker run -it --rm -v `pwd`:`pwd` -w `pwd` -p 2001:2001 fishros2/fishbot-tool python 
