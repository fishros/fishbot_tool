import serial
import libfishbot as fishbot
import sys
from time import time
sys.path.append('/fishbot')
sys.path.append('fishbot_tool/libs/')


def get_fishbot_by_uart(port: str, baudrate: int):
    bot = fishbot.FishBot()
    bot.set_protocol_serial(port, baudrate)
    bot.set_motion_model_diff2(0.170, 3293, 0.065 / 2)
    bot.init()
    return bot
    # fishbot.update_wifi_config_sta("JKC", "jkc20210106")
    # fishbot.restart()

    # fishbot.destory()


def config_laser_wifi(ssid: str, pswd: str, port: str,  baudrate=76800, timeout=1):
    ser = serial.Serial(port, baudrate, timeout)
    ser.open()
    config_str = f"config,wifi,{ssid},{pswd}\n"
    print(f"send {config_str} to {ser.port}")
    ser.write(config_str.encode())
    recv = ser.readline()
    print(recv.decode())


def config_laser_proto_udp_client(ip: str, server_port, port: str, baudrate=76800, timeout=1):
    ser = serial.Serial(port, baudrate, timeout)
    ser.open()
    config_str = f"config,proto,udp_client,{ip},{server_port}\n"
    print(f"send {config_str} to {ser.port}")
    ser.write(config_str.encode())
    recv = ser.readline()
    print(recv.decode())
