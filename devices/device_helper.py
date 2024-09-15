import serial.tools.list_ports
import os
import time
from tool.cmd_task import CmdTask

class Device:
    def __init__(self, index, device_name, device_type):
        self.index = index
        self.device_name = device_name
        self.device_type = device_type

    def __repr__(self):
        return f"{self.index}: {self.device_type} | {self.device_name}"


class SerialDevice(Device):
    def __init__(self, index, device_name):
        super().__init__(index, device_name, 'Serial')
    
    def reset_by_rst(self):
        try:
            ser = serial.Serial(self.device_name, baudrate=74880)
            ser.setDTR(False)
            time.sleep(0.1)
            ser.setDTR(True)
            time.sleep(0.05)
            ser.close()
            return {'code':0,'msg':'[提示]发送RTS成功！'}
        except Exception as e:
            e_str = str(e)
            if e_str.find('Permission')>0 or e_str.find('权限')>0:
                return {'code':1,'msg':f'[警告]串口打开异常,请检查设备权限,手动单次添加可使用命令:\n    sudo chmod 666 {self.device_name}\n彻底解决:\n    sudo usermod -a -G dialout $USER'}
            return {'code':1,'msg':f'[警告]串口打开异常,请检查设备'}



class DeviceHelper:
    def __init__(self, logger):
        self.logger = logger
        self.device_index = 0

    def get_all_devices(self):
        self.device_index = 0
        self.devices = {}
        self.devices = self.get_all_serial_devices()
        if os.name == 'posix':
            if self.check_port_claim():
                self.logger("""
    ================重要提示===================
    检测到端口占用，请打开终端输入命令: 
        sudo apt remove brltty 
    输入命令解除占用后重新插拔设备生效
    ===========================================""")
        .
        if len(self.devices) == 0:
            self.logger('[提示]无可用串口，请插入串口设备')
        return self.devices
    
    def get_device(self,device_name):
        return self.devices[device_name]

    def check_port_claim(self):
        task = CmdTask()
        task.run('dpkg -l | grep brltty')
        ret_brltty = task.getlogs().find('brltty')>0
        task = CmdTask()
        task.run('lsusb')
        ret_qinheng = task.getlogs().find('QinHeng')>0
        device_count = len(self.get_all_serial_devices())
        if ret_brltty and ret_qinheng and device_count==0:
            return True
        return False
        

    def get_all_serial_devices(self):
        self.devices = {}
        self.device_index = 0
        port_list = list(serial.tools.list_ports.comports())
        if os.name == 'posix':  # Linux or macOS
            for port in port_list:
                device = SerialDevice(self.device_index, port.device)
                if str(port.device).find('/dev/ttyS')==0:
                    continue
                self.devices[str(device)] = device
                self.device_index += 1
        elif os.name == 'nt':  # Windows
            for port in port_list:
                device = SerialDevice(self.device_index, port.device)
                self.devices[str(device)] = device
                self.device_index += 1
        return self.devices


if __name__ == "__main__":
    def logger(msg):
        print(msg)

    device_helper = DeviceHelper(logger)
    all_devices = device_helper.get_all_devices()
    print(all_devices)
