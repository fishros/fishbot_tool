import time
import serial
import sys
sys.path.append('/fishbot')
sys.path.append('fishbot_tool/libs/')


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
        print("start recv")
        recv = ser.read_all().decode()
        print(f"recv temp:{recv}")
        time.sleep(0.5)
        if len(recv) > 0:
            print(f"recv avaliable data :{recv}")
            recv_avaliable_data = True

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


if __name__ == "__main__":
    # all_configs = config_board(
    #     "command", "read_config", port='/dev/ttyUSB0', baudrate=115200)
    # print(all_configs)
    print(restart_device_bt_rst('/dev/ttyUSB0'))
