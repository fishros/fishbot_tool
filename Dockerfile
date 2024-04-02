FROM ubuntu:jammy

RUN apt-get update && apt-get install -y \
    wget \
    fonts-wqy-zenhei \
    libgl1 \
    libegl1 \
    && apt-get clean && apt-get autoclean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY "dist-for-docker/fishbot_tool_linux_amd64" /fishbot_tool
RUN chmod +x /fishbot_tool
ENTRYPOINT ["/fishbot_tool"]

# docker run -it --rm --privileged -v /dev:/dev  -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY fishbot-tool