FROM python:3.8.12

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install rich esptool pyserial

RUN pip install prompt_toolkit requests


COPY docs/docker/sources.list /etc/apt/sources.list
RUN apt update 
RUN apt install cmake libboost-dev libboost-dev  libgtest-dev -y
RUN apt install libboost-thread-dev -y
RUN apt install libboost-python-dev -y
RUN apt install libpython3-dev -y


WORKDIR /fishbot


RUN git clone https://github.91chi.fun/https://github.com/fishros/fish_protocol.git \
    && cd fish_protocol && mkdir build  && cd build \
    && cmake .. && make install && ldconfig

#install libfishbot
RUN git clone https://github.91chi.fun/https://github.com/fishros/fishbot-motion-driver.git -b v1.0.0.20220717 \
    && cd fishbot-motion-driver && mkdir build  && cd build \
    && cmake .. && make -j7 install \
    && cp libfishbot.so /fishbot

COPY fishbot_tool /fishbot_tool/fishbot_tool
ENV PYTHONPATH /fishbot_tool
WORKDIR /fishbot_tool/fishbot_tool
# ENTRYPOINT ["python","main.py"]

# docker build -t fishros2/fishbot-tool .
# docker run -it --rm --privileged -v /dev:/dev fishros2/fishbot-tool python main.py


