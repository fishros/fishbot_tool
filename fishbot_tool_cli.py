import os
import sys

def check_installation(package_name,install_pkg):
    try:
        __import__(package_name)
        return True
    except ImportError:
        print(f'{package_name} 未安装,尝试安装')
        os.system(f'pip install {install_pkg}')
        return False

check_installation('serial',"pyserial")
check_installation('esptool','esptool')
check_installation('requests','requests')

import serial #导入模块
import serial.tools.list_ports
import requests
import time


def list_serial_ports():
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) == 0:
        print('无可用串口，请插入串口设备')
        return False
    else:
        print('当前可用串口有：')
        for i in range(0,len(port_list)):
            print(port_list[i].name)
        return True
    
def download_firmware(firmware_path):
    print('将测到固件在HTTP路径上，开始下载')
    response = requests.get(firmware_path, stream=True)
    response.raise_for_status()

    filename = os.path.basename(firmware_path)
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

    print(f'下载完成：{filename}')
    return filename

def flash_firmware():
    firmware_path = 'firmware.bin'
    while not os.path.exists(firmware_path):
        print(f"提示：{firmware_path}固件文件不存在,请重新输入")
        firmware_path = input("请输入固件文件路径(可以是网址): ")
        if firmware_path.startswith('http'):
            firmware_path = download_firmware(firmware_path)


    while list_serial_ports()==False:
        time.sleep(1)
    port = input("请输入要烧录的串口设备名称: ")

    flash_command = f'esptool.py --port {port} write_flash 0x00000 {firmware_path}'
    os.system(flash_command)



def config_board(key: str, value: str, port='/dev/ttyUSB0', baudrate=115200):
    try:
        ser = serial.Serial(port, baudrate)
    except:
        return {"error": "串口打开异常,请检查设备是否被占用"}

    config_str = f"${key}={value}\n".encode()
    print(f"发送 {str(config_str)} 到 {ser.port}")
    ser.write(config_str)
    start_time_timeout = time.time()
    recv_avaliable_data = False
    while (time.time()-start_time_timeout < 5) and (not recv_avaliable_data):
        print("开始接收...")
        try:
            recv = ser.read_all().decode()
            print(f"尝试接收..{recv}")
            time.sleep(0.5)
            if len(recv) > 0:
                print(f"接收到有效数据 :{recv}")
                recv_avaliable_data = True
        except Exception as e:
            print(e)

    if len(recv) == 0:
        return {"error": "串口数据异常,请确认设备在配置模式"}

    result = {}
    lines = recv.splitlines()
    for line in lines:
        if len(line) > 0 and line[0] == '$':
            split_result = line[1:].split("=")
            if len(split_result) == 2:
                result[split_result[0]] = split_result[1]
    ser.close()
    if len(result) == 0:
        return {"error": "串口数据异常,请确认设备在配置模式"}
    return result


def restart_device_bt_rst(port):
    try:
        ser = serial.Serial(port, baudrate=74880)
        ser.setRTS(False)
        ser.setDTR(False)
        time.sleep(0.2)
        ser.setRTS(True)
        ser.setDTR(True)
        time.sleep(0.2)
        time.sleep(0.1)
        return "[提示]发送RTS成功！"
    except Exception as e:
        ser.close()
        print(e)
        return {"error": "串口打开异常,请检查设备是否被占用"}


def print_help():
    print("使用方法:")
    print("  python fishbot_tool_cli.py list_port - 列出可用的串口")
    print("  python fishbot_tool_cli.py flash - 下载固件")
    print("  python fishbot_tool_cli.py read_config COMX - 读取配置,COMX替换为设备编号")
    print("  python fishbot_tool_cli.py config name value - 设置配置项")
    print("  python fishbot_tool_cli.py - 打印帮助信息")


def main():
    if len(sys.argv) == 1:
        print_help()
    elif sys.argv[1] == 'list_port':
        list_serial_ports()
    elif sys.argv[1] == 'flash':
        flash_firmware()
    elif sys.argv[1] == 'read_config':
        if len(sys.argv)!=3:
            print('请在read_config后添加你要读取的设备串口号')
            return
        all_configs = config_board("command", "read_config", port=sys.argv[2], baudrate=115200)
        print(all_configs)
    elif sys.argv[1] == 'config':
        if len(sys.argv)!=5:
            print('请在config后添加你的：设备号 配置项 配置值')
            return
        result = config_board(sys.argv[3], sys.argv[4], port=sys.argv[2], baudrate=115200)
        print(result)
    else:
        print("未知的命令")
        print_help()

if __name__ == "__main__":
    main()
