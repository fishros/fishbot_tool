from devices.board import Board
from devices.device_helper import Device


class BoardFishBotUlsound(Board):
    def __init__(self,logger):
        super().__init__('FishBot 多路超声波控制板','fishros_ulsound',logger=logger)
        
    def write_flash(self,device: Device,bin_file=None):
        """
        None: Erase Flash
        """
        self.logger(f'[提示]{self.name} 准备烧录固件:{bin_file}')
        self.stm_helper.write_flash(device.device_name,115200,'stm32f1',bin_file)

    def reset(self, device: Device):
        if not device:
            self.logger("[错误]设备为空，请选择设备")
            return
        self.logger("[提示]该设备暂不支持软件重启")
        # device.reset_by_rst()

    def config(self, key, value,device:Device):
        self.logger("[提示]该设备暂不支持配置")
        return 
        result = self.esp_helper.config_board(
            key, value, port=device.device_name, baudrate=115200)
        
        self.logger(f"[提示]收到结果{result}")
        if 'error' in result.keys():
            self.logger(f"[错误]配置失败{str(result)}")
            return False

        if len(result) > 0 and result['result'] == 'ok':
            self.logger(f"[提示]配置{key}={value}成功！")
        else:
            self.logger(f"[警告]配置{key}={value}失败！")
        return True

    def get_all_config(self, device:Device):
        self.logger("[提示]该设备暂不支持配置")
        return 
        all_config = self.esp_helper.config_board('command','read_config',device.device_name,baudrate=115200)
        return all_config
