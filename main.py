#!/usr/bin/python3
# coding=utf-8

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
import time
import threading
import signal
import sys
from queue import Queue
from tool.network import FishBotFirmwareDownloader
from devices.device_helper import DeviceHelper,Device
from devices.board_helper import BoardHelper

import os
CURRENT_DIR = os.path.dirname(__file__) 
os.environ['FISHBOT_CURRENT_DIR'] = CURRENT_DIR

class FishBotTool():
    def __init__(self) -> None:
        Form, Window = uic.loadUiType(f"{CURRENT_DIR}/ui/main.ui")
        self.app = QApplication([])
        self.window = Window()
        self.form = Form()


        self.form.setupUi(self.window)
        self.form.downloadButton.clicked.connect(self.download)
        self.form.freshDevicePortButton.clicked.connect(
            self.click_fresh_device_port)
        self.form.action_fishros.triggered.connect(self.click_about)
        self.form.action_shop.triggered.connect(self.click_shop)
        self.form.configKeyComboBox.currentIndexChanged.connect(
            self.choose_config_callback)
        self.form.scanConfigButton.clicked.connect(
            self.click_scan_config_button)
        self.form.configButton.clicked.connect(self.click_config_button)
        self.form.restartDeviceButton.clicked.connect(self.restart_device)
        self.window.setFixedSize(self.window.size())

        self.current_configs = {}

        self.log_queue = Queue()
        self.log_text = ""
        self._timer = QTimer()
        self._timer.timeout.connect(self.handleTimeoutLog)
        self._timer.setInterval(100)
        self._timer.start()
        self.second_update = False

        self.download = FishBotFirmwareDownloader(self.put_log)
        self.device_helper = DeviceHelper(self.put_log)
        self.board_helper = BoardHelper(self.put_log)

        self.click_fresh_device_port()
        self.form.deviceTypeComboBox.clear()
        self.form.deviceTypeComboBox.addItems(self.board_helper.get_boards_name())
        self.form.deviceTypeComboBox.currentIndexChanged.connect(
            self.choose_device_callback)
        
        self.refresh_ui = False
        self.download.get_version_data(self.recv_version_data_callback,is_async=True)
        # Set up signal handler for graceful exit
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        print("Exiting...")
        self.app.quit()
        sys.exit(0)
    def recv_version_data_callback(self,version_data):
        for device_name in self.board_helper.get_boards_name():
            board = self.board_helper.get_board(device_name)
            if board.board_id in version_data.keys():
                for version in version_data[board.board_id]:
                    if version['version']=='latest':
                        board.set_default_url(version['url'])
        self.refresh_ui = True
    def get_current_device_and_board(self):
        device_str = self.form.devicesComboBox.currentText()
        board_str = self.form.deviceTypeComboBox.currentText()
        device,board = None,None
        if len(device_str) == 0:
            self.put_log(f"[错误]检测当前端口号为空,请重新选择端口号！")
        else:
            device = self.device_helper.get_device(device_str)
        board = self.board_helper.get_board(board_str)
        return device,board
    def restart_device(self):
        device,board = self.get_current_device_and_board()
        board.reset(device)

    def put_log(self, log):
        self.log_queue.put(log)

    def download(self):
        threading.Thread(target=self.download_thread).start()
    def download_thread(self):
        device,board = self.get_current_device_and_board()
        if not device or not board:
            return

        url = self.form.binAddress.text()
        if len(url) == 0:
            self.put_log(f"[错误]检测当前固件地址为空,请输入固件地址！")
            return
        
        firmware_name = os.path.basename(url)
        self.put_log(f"[提示]准备从{url}下载固件到{device}")
        path = os.path.join(CURRENT_DIR,firmware_name)
        if url.startswith('http'):
            firmware_path = self.download.download_firmware(url,path)
        else:
            firmware_path = url
        # self.put_log(f"[提示]开始烧录固件{firmware_path}")
        board.write_flash(device,firmware_path)


    def click_about(self):
        Form, Window = uic.loadUiType(f"{CURRENT_DIR}/ui/about.ui")
        window = Window()
        form = Form()
        form.setupUi(window)
        window.show()
        window.exec()

    def click_shop(self):
        Form, Window = uic.loadUiType(f"{CURRENT_DIR}/ui/taobao.ui")
        window = Window()
        form = Form()
        form.setupUi(window)
        window.show()
        window.exec()

    def click_fresh_device_port(self):
        devices = self.device_helper.get_all_devices()
        self.update_log(f"[提示]获取到当前系统设备 {str(devices)}")
        self.form.devicesComboBox.clear()
        self.form.devicesComboBox.addItems(devices.keys())
        self.form.devicesComboBox.setCurrentIndex(0)

    def scan_device_config(self):
        device,board = self.get_current_device_and_board()
        if not device or not board:
            return
        all_configs = board.get_all_config(device)
        self.form.configKeyComboBox.clear()
        if not all_configs:
            return
        self.current_configs.clear()
        self.current_configs = all_configs
        for key in all_configs.keys():
            value = all_configs[key]
            self.put_log(f"[提示]读取到配置项{key}->{value}")
            self.form.configKeyComboBox.addItem(key)
    def choose_device_callback(self):
        self.put_log(f"[操作]切换设备类型{self.form.deviceTypeComboBox.currentText()}")
        device,board = self.get_current_device_and_board()
        # if board.default_bin_url: # fix: https://fishros.org.cn/forum/topic/2502
        self.form.binAddress.setText(board.default_bin_url)
    def choose_config_callback(self):
        key = self.form.configKeyComboBox.currentText()
        if key in self.current_configs.keys():
            self.form.configValueLineEdit.setText(self.current_configs[key])

    def click_scan_config_button(self):
        self.scan_device_config()

    def click_config_button(self):
        key = self.form.configKeyComboBox.currentText()
        if len(key) == 0:
            self.put_log(f"[错误]请先扫描并填写配置！")
            return

        value = self.form.configValueLineEdit.text()
        if len(value) == 0:
            self.put_log(f"[错误]请先扫描并填写配置！")
            return

        port = self.form.devicesComboBox.currentText()
        if len(port) == 0:
            self.put_log(f"[错误]记得选择端口号哈！")
            return

        if key not in self.current_configs.keys():
            self.put_log(f"[错误]当前的KEY不在可配置项中！")
            return

        if value == self.current_configs[key]:
            self.put_log(f"[警告]配置值和当前设备值相同")

        device,board = self.get_current_device_and_board()
        if not device or not board:
            return
        
        if board.config(key, value,device):
            self.current_configs[key] = value

    def show(self):
        self.window.show()
        self.app.exec()

    def update_log(self, text):
        self.log_text = str(time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime()))+" > "+str(text)
        print(self.log_text)
        self.form.system_log.append(self.log_text)
        scrollbar = self.form.system_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def handleTimeoutLog(self):
        while self.log_queue.qsize() > 0:
            text = self.log_queue.get()
            if len(text.strip())>0:
                self.update_log(text)
        if self.refresh_ui:
            self.refresh_ui = False
            self.choose_device_callback()



if __name__ == "__main__":
    fishbottool = FishBotTool()
    fishbottool.update_log("FishBot配置工具已启动.")
    fishbottool.show()
