
import os
from time import sleep
import esptool
from prompt_toolkit.shortcuts import yes_no_dialog
from rich import print
from fishbot_tool.data import get_all_device
from fishbot_tool.fishbot import get_fishbot_by_uart
from fishbot_tool.fishbot import config_laser_proto_udp_client,config_laser_wifi
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
        proto_config = {
            "uart": {
                "115200": None,
            },
            "udp_server": {
                "3474": None,
            },
            "udp_client": {
                "192.168.4.1": {
                    "3474": None,
                },
            },
        }

        devices = get_all_device()
        config_map = {}
        for d in devices:
            config_map[d] = {
                "wifi": wifi_config,
                "proto": proto_config,
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
        if commands[1]=="fishbot":
            self.config_fishbot(commands)
        elif commands[1]=="laser":
            self.config_laser(commands)


    def config_laser(self, commands):
        if commands[3] == "wifi":
            config_laser_wifi(commands[4], commands[5],commands[2])
        if commands[3] == "proto":
            config_laser_proto_udp_client(ip=commands[5],server_port=commands[6],port=commands[2],baudrate=76800)


    def config_fishbot(self, commands):
        if commands[3] == "wifi":
            self.config_wifi(commands)
        if commands[3] == "proto":
            self.config_proto(commands)

    def config_proto(self, commands):
        bot = get_fishbot_by_uart(commands[2], 115200)
        sleep(0.1)
        # bot.update_wifi_config_sta(commands[4], commands[5])
        if commands[4]=="uart":
            bot.update_protocol_config_uart(int(commands[5]))
        if commands[4]=="udp_server":
            bot.update_protocol_config_udp_server(int(commands[5]))
        if commands[4]=="udp_client":
            bot.update_protocol_config_udp_client(commands[5],int(commands[6]))
        sleep(0.1)
        bot.restart()
        bot.destory()

    def config_wifi(self, commands):
        bot = get_fishbot_by_uart(commands[2], 115200)
        sleep(0.1)
        bot.update_wifi_config_sta(commands[4], commands[5])
        sleep(0.1)
        bot.restart()
        bot.destory()
