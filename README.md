# 配置工具



## 快速使用

安装好Docker,在你的终端输入下面代码，既可使用

```
docker run -it --rm --privileged -v /dev:/dev fishros2/fishbot-tool 
```
## 设计思考

```
功能列表
固件相关
1.烧录fishbot固件(手动选择软件版本)
2.烧录雷达转接板固件(只做一个固件即可)
配置相关
1.配置雷达转接板波特率等(wifi&ip&port&baut)
2.配置运动控制板相关内容(wifi&ip&port&reduce&pid)
```