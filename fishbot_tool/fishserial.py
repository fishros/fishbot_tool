import serial
import threading

class SerialCommunication:
    def __init__(self):
        self.serial_port = None
        self.read_thread = None
        self.receive_callback = None
        self.is_running = False
        
    def open_port(self, port, baudrate, timeout):
        self.serial_port = serial.Serial(port, baudrate, timeout=timeout)
        self.is_running = True
        
        self.read_thread = threading.Thread(target=self.read_data)
        self.read_thread.start()
        
    def close_port(self):
        self.is_running = False
        
        # if self.read_thread:
        #     self.read_thread.join()
            
        if self.serial_port:
            self.serial_port.close()
            
    def set_receive_callback(self, callback):
        self.receive_callback = callback
        
    def send_data(self, data):
        if self.serial_port:
            self.serial_port.write(data.encode())
        
    def read_data(self):
        while self.is_running:
            if self.serial_port.in_waiting > 0:
                data = self.serial_port.readline().decode().strip()
                if self.receive_callback:
                    self.receive_callback(data)

import time

if __name__=="__main__":
    def receive_callback(data):
        print("Received data:", data)

    serial_communication = SerialCommunication()
    serial_communication.set_receive_callback(receive_callback)
    serial_communication.open_port("/dev/ttyUSB0", 115200, 1)

    time.sleep(5)
    print("ready quit")
    serial_communication.close_port()
    print("quit")
    time.sleep(1)
    # serial_communication.send_data("Hello, world!")
