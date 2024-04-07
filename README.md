# FishBot配置工具

支持设备：
- FishBot二驱板
- FishBot四驱动板
- FishBot雷达转接板
- FishBot_Camera无线摄像头


## 使用方法(可视化版)

### 1.直接下载（推荐）

到[release](https://github.com/fishros/fishbot_tool/releases)页面下载构好的二进制文件（Linux需要下载后右击勾选可执行）双击运行即可。

### 2.Docker使用

首先确保你的电脑安装了Docker，然后直接运行以下命令（注意，最新版本需要到[release](https://github.com/fishros/fishbot_tool/releases)页面查看）：

```
xhost + && sudo docker run -it --rm --privileged -v /dev:/dev -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY fishros2/fishbot_tool:v1.0.0.beta
```

### 3.源码使用
首先克隆代码到本地，接着安装 PyQt6,pyserial,esptool,requests
```
sudo apt install python3-pip
sudo pip3 install PyQt6 requests pyserial esptool -i https://pypi.tuna.tsinghua.edu.cn/simple
```

接着执行（注意Linux下要给串口设备权限）

```
python3 main.py
```


## 使用方法（无界面版本）

安装好Python3.8+，到release页面下载fishbot_tool_cli.py，接着执行：

```
python fishbot_tool_cli.py 
```

最后根据提示使用即可。



- Autor: [fishros](https://github.com/fishros)
