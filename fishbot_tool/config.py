
import os
from time import sleep
import esptool
from prompt_toolkit.shortcuts import yes_no_dialog
from rich import print
from fishbot_tool.data import get_all_device
from fishbot_tool.fishbot import get_fishbot_by_uart
# result = yes_no_dialog(
#     title='Yes/No dialog example',
#     text='Do you want to confirm?').run()


class Tool():
    def __init__(self) -> None:
        pass

    def get_complete(self):
        """
        """
        wifi_config = {
            "name": {
                "password": None,
            },
        }

        devices = get_all_device()
        config_map = {}
        for d in devices:
            config_map[d] = {
                "wifi": wifi_config,
            }
        result = {
            'fishbot': config_map,
            'laser': config_map,
        }
        return result

    def run(self, commands: list):
        """
        flash esp8266 auto_detect https://fishros.org.cn/forum/assets/uploads/files/1657479890115-fishbot_laser_driver.v1.0.0.220628.bin
        """
        print(commands)
        bot = get_fishbot_by_uart(commands[2], 115200)
        bot.update_wifi_config_sta(commands[4], commands[5])
        sleep(0.5)
        bot.restart()
        sleep(1)
        bot.destory()

    def config_wifi(self):
        pass
