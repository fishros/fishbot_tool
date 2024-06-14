import serial.tools.list_ports
import os
import time

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
            return {'code':0,'msg':'[提示]发送RTS成功！'}
        except Exception as e:
            ser.close()
            print(e)
            return {'code':1,'msg':'[警告]串口打开异常,请检查设备是否被占用'}



class DeviceHelper:
    def __init__(self, logger):
        self.logger = logger
        self.device_index = 0

    def get_all_devices(self):
        self.device_index = 0
        self.devices = {}
        self.devices = self.get_all_serial_devices()

        if len(self.devices) == 0:
            self.logger('[提示]无可用串口，请插入串口设备')
        return self.devices
    
    def get_device(self,device_name):
        return self.devices[device_name]

    def get_all_serial_devices(self):
        port_list = list(serial.tools.list_ports.comports())

        if os.name == 'posix':  # Linux or macOS
            for port in port_list:
                device = SerialDevice(self.device_index, port.device)
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
