#!/usr/bin/python3
# coding=utf-8

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog
from PySide6.QtCore import Qt, QTimer, Slot


import time
import threading
from queue import Queue

from flash import CmdTask
from data import get_all_device, get_version_data
from fishbot import config_board, restart_device_bt_rst


class FishBotTool():
    def __init__(self) -> None:
        Form, Window = uic.loadUiType("main.ui")
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

        self.devices_map = {"motion_board": "esp32", "laser_board": "esp8266","motion_board_4driver":"esp32"}
        self.board_map = {0: "motion_board", 1: "laser_board",2:"motion_board_4driver"}
        self.devices2board_map = {"motion_board": 0, "laser_board": 1}
        self.board = "motion_board"  # motion_board | laser_board
        self.current_configs = {}

        # log
        self.log_queue = Queue()
        self.log_text = ""
        self._timer = QTimer()
        self._timer.timeout.connect(self.handleTimeoutLog)
        self._timer.setInterval(100)
        self._timer.start()
        self.second_update = False

        self.click_fresh_device_port()
        self.click_scan_config_button()
        self.form.deviceTypeComboBox.currentIndexChanged.connect(
            self.choose_device_callback)
        self.choose_device_callback()

    def restart_device(self):
        """
        重新启动设备
        """
        port = self.form.devicesComboBox.currentText()
        if len(port) == 0:
            self.put_log(f"[错误]检测当前端口号为空,请重新选择端口号！")
            return
        self.put_log(restart_device_bt_rst(port))

    def put_log(self, log):
        self.log_queue.put(log)

    def download(self):
        threading.Thread(target=self.download_thread).start()

    def download_thread(self):
        port = self.form.devicesComboBox.currentText()
        if len(port) == 0:
            self.put_log(f"[错误]检测当前端口号为空,请重新选择端口号！")
            return

        url = self.form.binAddress.text()
        if len(url) == 0:
            self.put_log(f"[错误]检测当前固件地址为空,请输入固件网址！")
            return

        board = self.board_map[self.form.deviceTypeComboBox.currentIndex()]
        chip = self.devices_map[board]
        self.put_log(
            f"准备从{url}下载固件到{port}对应芯片为{chip}")

        def update_log(log): self.put_log(log)

        self.put_log("准备从网址下载固件...")
        self.cmd_task = CmdTask()
        self.cmd_task.run(f"wget {url} -O {chip}.bin", cwd="/tmp/")
        self.cmd_task.getlog(update_log)
        if self.cmd_task.is_finish() == 0:
            self.put_log("固件下载完成！")
        else:
            self.put_log("[错误]固件下载失败，请检查地址或网络。。")
            return

        self.put_log("开始烧录固件...")
        self.cmd_task = CmdTask()
        self.cmd_task.run(
            f"esptool.py -p {port} -b 460800 --before default_reset --after hard_reset --chip {chip}  write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x00 {chip}.bin", cwd="/tmp/")
        self.cmd_task.getlog(update_log)

        if self.cmd_task.is_finish() == 0:
            self.put_log("固件写入完成！")
        else:
            self.put_log("[错误]固件写入失败，请检查日志或重试。。。")

    def click_about(self):
        # webbrowser.open("https://fishros.com/")
        pass
        Form, Window = uic.loadUiType("about.ui")
        window = Window()
        form = Form()
        form.setupUi(window)
        window.show()
        window.exec()

    def click_shop(self):
        Form, Window = uic.loadUiType("taobao.ui")
        window = Window()
        form = Form()
        form.setupUi(window)
        window.show()
        window.exec()

    def click_fresh_device_port(self):
        devices = get_all_device()
        self.update_log(f"[提示]获取到当前系统设备 {str(devices)}")
        print(devices)

        self.form.devicesComboBox.clear()
        self.form.devicesComboBox.addItems(devices)
        self.form.devicesComboBox.setCurrentIndex(0)

    def scan_device_config(self):
        port = self.form.devicesComboBox.currentText()
        if len(port) == 0:
            self.put_log(f"[错误]清先选择端口号，并进入配置模式！")
            return
        all_configs = config_board(
            "command", "read_config", port=port, baudrate=115200)

        self.form.configKeyComboBox.clear()
        if 'error' in all_configs.keys():
            self.put_log(f"[错误]读取到配置项失败{str(all_configs)}")
            return

        if 'board' in all_configs.keys():
            self.board = all_configs['board']
            self.put_log(f"[提示]获取到当前设备为{self.board}")
            board = self.board_map[self.form.deviceTypeComboBox.currentIndex()]
            if self.board != board:
                self.form.deviceTypeComboBox.setCurrentIndex(
                    self.devices2board_map[self.board])

            del all_configs['board']

        self.current_configs.clear()
        self.current_configs = all_configs

        for key in all_configs.keys():
            value = all_configs[key]
            self.put_log(f"[提示]读取到配置项{key}->{value}")
            self.form.configKeyComboBox.addItem(key)

    def choose_device_callback(self):
        self.put_log(f"[操作]切换设备类型{self.form.deviceTypeComboBox.currentText()}")
        # if len(self.form.binAddress.text()) == 0:
        board_bin = get_version_data()
        board = self.board_map[self.form.deviceTypeComboBox.currentIndex()]
        self.form.binAddress.setText(board_bin[board])
        # self.scan_device_config()

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

        result = config_board(
            key, value, port=port, baudrate=115200)


        self.put_log(f"收到结果{result}")
        if 'error' in result.keys():
            self.put_log(f"[错误]读取到配置项失败{str(result)}")
            return


        if len(result) > 0 and result['result'] == 'ok':
            self.put_log(f"[提示]配置{key}={value}成功！")
            self.current_configs[key] = value
        else:
            self.put_log(f"[警告]配置{key}={value}失败！")

    def show(self):
        self.window.show()
        self.app.exec()

    def update_log(self, text):
        self.log_text = str(time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime()))+" > "+str(text)
        print(self.log_text)
        self.form.system_log.append(self.log_text)

    @Slot()
    def handleTimeoutLog(self):
        while self.log_queue.qsize() > 0:
            text = self.log_queue.get()
            self.update_log(text)


if __name__ == "__main__":
    fishbottool = FishBotTool()
    fishbottool.update_log("FishBot配置工具已启动.")
    fishbottool.show()
