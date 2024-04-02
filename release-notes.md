版本更新：
- [feat]发布Linux可执行文件
- [feat]发布Windows可执行文件
- [feat]增加固件下载进度提示
- [feat]支持填写本地固件路径下载
- [feat]添加无界面版本fishbot_tool_cli.py

版本说明：
- alpha:内部测试版本（不建议使用）
- beta:新功能测试版本（可以尝试）
- release:最终测试版本（推荐）

注意事项:
- Windows版本未签名，注意不要被操作系统误杀
- Linux下载后需要先给可执行权限，然后双击运行
- 无界面版本需要先安装Python3.8+,然后直接python+可执行文件名字运行
- Docker版本直接运行命令(Linux): xhost + && sudo docker run -it --rm --privileged -v /dev:/dev -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY fishros2/fishbot_tool:DOCKER-TAG