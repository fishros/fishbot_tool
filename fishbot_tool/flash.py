
import os
import esptool
from prompt_toolkit.shortcuts import yes_no_dialog
from rich import print
from fishbot_tool.data import get_all_device

# result = yes_no_dialog(
#     title='Yes/No dialog example',
#     text='Do you want to confirm?').run()


class Tool():
    def __init__(self) -> None:
        pass

    def get_complete(self):
        """
          'esp32': {
                "auto_detect": {
                    "v1.0.0": None,
                },
            },
            'esp8266': {
                "auto_detect": {
                    "v1.0.0": None,
                },
            },
        """
        devices = get_all_device()
        devices_map = {}
        for d in devices:
            devices_map[d] = None
        result = {
            'esp32': devices_map,
            'esp8266': devices_map,
        }
        return result

    def run(self, commands: list):
        """
        flash esp8266 auto_detect https://fishros.org.cn/forum/assets/uploads/files/1657479890115-fishbot_laser_driver.v1.0.0.220628.bin
        """
        if len(commands) != 4:
            print(
                "指令错误\n示例:\n\tflash 芯片名称(esp8266|esp32) 端口号(/dev/ttyXXX) 固件地址(https://xxx)")
            return 
        chip = commands[1]
        port = commands[2]
        url = commands[3]
        os.system(f"wget {url} -O {chip}.bin")
        os.system(
            f"esptool.py -p {port} -b 460800 --before default_reset --after hard_reset --chip {chip}  write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x00 {chip}.bin")
        print("固件写入完成..")

    def flash_8266(self):
        """
        docker run -it --rm --privileged -v=/dev:/dev  -v `pwd`:`pwd` -w `pwd` fishros2/fishbot-tool esptool.py -p /dev/ttyUSB0 -b 460800 --before default_reset --after hard_reset --chip esp8266  write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x1000 fishbot_laser_control_v1.0.0.2022-08-05.bin
        """
        pass