import requests
import json
import os
import re


def get_version_data() -> list:
    """
    获取版本数据信息
    """
    version_info_url = 'https://fishros.org.cn/forum/api/v3/posts/2301'
    response = requests.get(version_info_url)
    raw_data = response.text
    configs = []
    start = raw_data.find("```json")+7
    end = raw_data.find('```', start)
    while start != -1 and end != -1:
        json_str = raw_data[start:end].replace("\\n", "").replace('\\"', '"')
        print(json_str)
        configs.append(
            json.loads(json_str)
        )
        raw_data = raw_data[end+3:]
        start = raw_data.find("```json")+7
        end = raw_data.find('```', start)
    return configs


def get_fishbot_control_version():
    pass
    get_version_data()


def get_all_device(path="/dev/"):
    devices = []

    def is_need_dev(name):
        return name.find("ttyUSB") > -1 or name.find("ttyACM") > -1

    for root, dirs, files in os.walk(path):
        for f in files:
            file_path = os.path.join(root, f)
            if is_need_dev(f):
                devices.append(file_path)
        # 遍历所有的文件夹
        for d in dirs:
            os.path.join(root, d)
    return devices

if __name__ == "__main__":
    # get_fishbot_control_version()
    print(get_all_device())

