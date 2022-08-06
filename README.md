# 配置工具

功能列表
固件相关
1.烧录fishbot固件(手动选择软件版本)
2.烧录雷达转接板固件(只做一个固件即可)

配置相关
1.配置雷达转接板波特率等(wifi&ip&port&baut)
2.配置运动控制板相关内容(wifi&ip&port&reduce&pid)


以下docker不支持建议放到外面(比如一键安装中)
软件环境相关
1.安装基础环境(fish_protocol&&fishbot-motion-driver&laser-driver)

```
docker run -it --rm --privileged -v /dev:/dev -v `pwd`:`pwd` -w `pwd` -p 2001:2001 fishros2/fishbot-tool python main.py
```
