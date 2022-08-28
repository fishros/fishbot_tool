from time import sleep
import serial #导入模块

import serial.tools.list_ports
port_list = list(serial.tools.list_ports.comports())
print(port_list)
if len(port_list) == 0:
   print('无可用串口')
else:
    for i in range(0,len(port_list)):
        print(port_list[i])


#---------------------------------------------------------------------------------------------
import serial

def config_laser_wifi(ssid: str, pswd: str, port: str,  baudrate=76800):
    ser = serial.Serial(port, baudrate)
    config_str = f"config,wifi,{ssid},{pswd}\n"
    print(f"send {config_str} to {ser.port}")
    ser.write(config_str.encode())
    sleep(2)
    recv = ser.read_all()
    print(recv.decode())

config_laser_wifi("m","88888888","/dev/ttyUSB0",76800)

