import requests
import json
import os
import re


def get_version_data() -> list:
    """
    获取版本数据信息
    编辑地址：https://fishros.org.cn/forum/topic/541/fishtool%E9%85%8D%E7%BD%AE%E5%90%8E%E5%8F%B0%E6%95%B0%E6%8D%AE%E9%9B%86
    """
    version_info_url = 'https://fishros.org.cn/forum/api/v3/posts/2301'
    response = requests.get(version_info_url)
    raw_data = response.text
    configs = []
    start = raw_data.find("```json")+7
    end = raw_data.find('```', start)
    while start != -1 and end != -1:
        json_str = raw_data[start:end].replace("\\n", "").replace('\\"', '"')
        # print(json_str)
        configs.append(
            json.loads(json_str)
        )
        raw_data = raw_data[end+3:]
        start = raw_data.find("```json")+7
        end = raw_data.find('```', start)
    if len(configs) > 0:
        return configs[0]
    else:
        return {"laser_board": "https://fishros.org.cn/forum/assets/uploads/files/1666192469873-fishbot_laser_control_v1.0.0.221019.bin", "motion_board": "https://fishros.org.cn/forum/assets/uploads/files/1672542988816-fishbot_motion_control_v1.0.0.230101.bin"}


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
    # print(get_all_device())
    print(get_version_data())
