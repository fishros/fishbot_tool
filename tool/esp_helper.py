import time
import serial
import serial.tools.list_ports
import os
from tool.cmd_task import CmdTask
import platform
def select_esptool():
    system = platform.system()
    if system == "Linux":
        if platform.machine() == "x86_64":
            return "./esptool/esptool_linux_amd64"
        elif platform.machine() == "aarch64":
            return "./esptool/esptool_arm64"
    elif system == "Darwin":
        return "./esptool/esptool_macos"
    elif system == "Windows":
        return "powershell ./esptool/esptool_win64.exe"
    else:
        raise Exception("Unsupported platform")


class ESPToolHelper:
    def __init__(self,logger):
        self.logger = logger

    def config_board(self, key: str, value: str, port='/dev/ttyUSB0', baudrate=115200):
        try:
            ser = serial.Serial()
            ser.port = port
            ser.baudrate = baudrate
            ser.rts = False # fix restart board
            ser.open()
        except Exception as e:
            e_str = str(e)
            if e_str.find('Permission')>0 or e_str.find('权限')>0:
                return {"info":f'sudo chmod 666 {port}','msg':f'[警告]串口打开异常,请检查设备权限,手动单次添加可使用命令:\n    sudo chmod 666 {port}\n彻底解决:\n    sudo usermod -a -G dialout $USER'}
            return {"error": "串口打开异常,请检查设备是否被占用","info":str(e)}

        config_str = f"${key}={value}\n".encode()
        self.logger(f"[提示]发送 {str(config_str)} 到 {ser.port}")
        ser.write(config_str)
        start_time_timeout = time.time()
        recv_avaliable_data = False
        while (time.time()-start_time_timeout < 1) and (not recv_avaliable_data):
            try:
                recv = ser.read_all().decode()
                time.sleep(0.5)
                if len(recv) > 0:
                    self.logger(f"[日志]读取到数据:{recv}")
                    print()
                    recv_avaliable_data = True
            except Exception as e:
                self.logger(f"[警告]{e}")

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

    def write_flash(self, serial_port, baud_rate, chip, firmware_image,cwd=None,flash_freq='40m'):
        try:
            ser = serial.Serial()
            ser.port = serial_port
            ser.baudrate = 115200
            ser.rts = False # fix restart board
            ser.open()
        except Exception as e:
            e_str = str(e)
            if e_str.find('Permission')>0 or e_str.find('权限')>0:
                self.logger(f'[警告]串口打开异常,请检查设备权限,手动单次添加可使用命令:\n    sudo chmod 666 {serial_port}\n彻底解决:\n    sudo usermod -a -G dialout $USER')
            return False
        try:
            if not cwd:
                cwd = os.environ['FISHBOT_CURRENT_DIR']
            def update_log(log): self.logger(log)
            self.logger("[提示]开始烧录固件...")
            self.cmd_task = CmdTask()   
            esptool = select_esptool()
            cmd = f"{esptool} -p {serial_port} -b {baud_rate} --before default_reset --after hard_reset --chip {chip} write_flash --flash_mode dio --flash_size detect --flash_freq {flash_freq} 0x00 {firmware_image}"
            print('----------------------------------------------')
            print(cmd)
            self.cmd_task.run(cmd, cwd=cwd)
            self.cmd_task.getlog(update_log)

            if self.cmd_task.is_finish() == 0:
                self.logger("[提示]固件写入完成！")
                return True
            else:
                self.logger("[错误]固件写入失败，请检查日志或重试。。。")
                return False
        except Exception as e:
            print(e)
            return False

    def restart_device_bt_rst(self, port):
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
    esp_tool = ESPToolHelper()
    # 示例使用
    # all_configs = esp_tool.config_board(
    #     "command", "read_config", port='/dev/ttyUSB0', baudrate=115200)
    # print(all_configs)
    print(esp_tool.restart_device_bt_rst('/dev/ttyUSB0'))
