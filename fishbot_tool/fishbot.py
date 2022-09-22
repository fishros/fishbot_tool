from time import sleep, time
import serial
import sys
sys.path.append('/fishbot')
sys.path.append('fishbot_tool/libs/')
import libfishbot as fishbot


def get_fishbot_by_uart(port: str, baudrate: int):
    bot = fishbot.FishBot()
    bot.set_protocol_serial(port, baudrate)
    bot.set_motion_model_diff2(0.170, 3293, 0.065 / 2)
    bot.init()
    return bot
    # fishbot.update_wifi_config_sta("JKC", "jkc20210106")
    # fishbot.restart()

    # fishbot.destory()


def config_laser_wifi(ssid: str, pswd: str, port: str,  baudrate=115200):
    ser = serial.Serial(port, baudrate)
    config_str = f"config,wifi,{ssid},{pswd}\n"
    print(f"send {config_str} to {ser.port}")
    ser.write(config_str.encode())
    sleep(2)
    recv = ser.read_all()
    print(recv.decode())
    ser.close()


def config_laser_proto_udp_client(ip: str, server_port, port: str, baudrate=115200):
    ser = serial.Serial(port, baudrate)
    config_str = f"config,proto,udp_client,{ip},{server_port}\n"
    print(f"send {config_str} to {ser.port}")
    ser.write(config_str.encode())
    sleep(2)
    recv = ser.read_all()
    print(recv.decode())
    ser.close()

