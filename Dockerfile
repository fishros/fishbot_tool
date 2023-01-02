FROM fishros2/ros:humble-desktop

# COPY docs/docker/sources.list /etc/apt/sources.list
# RUN apt update 
# RUN apt install python3 -y
# RUN apt install cmake libboost-dev libboost-dev  libgtest-dev   libboost-thread-dev  libboost-python-dev  libpython3-dev -y


RUN apt update \
    && apt install python3-pip -y \
    && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install  esptool pyserial pyqt6 requests



WORKDIR /fishbot

# RUN git clone https://github.91chi.fun/https://github.com/fishros/fish_protocol.git \
#     && cd fish_protocol && mkdir build  && cd build \
#     && cmake .. && make install && ldconfig

# #install libfishbot
# RUN git clone https://github.91chi.fun/https://github.com/fishros/fishbot-motion-driver.git -b v1.0.0.20220717 \
#     && cd fishbot-motion-driver && mkdir build  && cd build \
#     && cmake .. && make -j7 install \
#     && cp libfishbot.so /fishbot
RUN pip install PySide6
RUN apt install language-pack-zh-hans fonts-noto-cjk -y \
    && locale-gen zh_CN.UTF-8
ENV LANG zh_CN.UTF-8
COPY fishbot_tool /fishbot_tool/fishbot_tool
ENV PYTHONPATH /fishbot_tool
WORKDIR /fishbot_tool/fishbot_tool
ENTRYPOINT []

CMD ["/bin/bash"]
# ENTRYPOINT ["python3", "main.py"]

# docker build -t fishros2/fishbot-tool .
# docker run -it --rm --privileged -v /dev:/dev  -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY fishros2/fishbot-tool python main.py


