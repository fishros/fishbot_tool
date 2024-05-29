from devices.device_helper import Device
from tool.esp_helper import ESPToolHelper
from tool.stm_helper import STMHelper

class Board:
    def __init__(self, name, board_id,logger):
        self.name = name
        self.board_id = board_id
        self.logger = logger
        self.default_bin_url = ""

        self.esp_helper = ESPToolHelper(logger)
        self.stm_helper = STMHelper(logger)
    def set_default_url(self,url):
        self.default_bin_url = url
        
    def write_flash(self, *args, **kwargs):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def reset(self, device: Device):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def config(self, *args, **kwargs):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def get_all_config(self, *args, **kwargs):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def __repr__(self):
        return f"Board(ID={self.name}, Device={self.board_id})"
