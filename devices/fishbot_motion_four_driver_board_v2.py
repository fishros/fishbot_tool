from devices.board import Board
from devices.device_helper import Device


class BoardFishBotMotion4DV2(Board):
    def __init__(self,logger):
        super().__init__('FishBot 四驱主控板V2','fishbot_motion_4driver_v2',logger=logger)
        
    def write_flash(self,device: Device,bin_file=None):
        """
        None: Erase Flash
        self.esp_tool.write_flash(port,460800,chip,firmware_path,cwd=CURRENT_DIR):
        """
        self.logger(f'[提示]{self.name} 准备烧录固件:{bin_file}')
        self.esp_helper.write_flash(device.device_name,460800,'esp32s3',bin_file,flash_freq='keep')

    def reset(self, device: Device):
        if not device:
            self.logger("[错误]设备为空，请选择设备")
            return
        ret = device.reset_by_rst()
        if ret['code']==1:
            self.logger(ret['msg'])
        else:
            self.logger("[提示]通过RST重启完成")

    def config(self, key, value,device:Device):
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
        all_config = self.esp_helper.config_board('command','read_config',device.device_name,baudrate=115200)
        return all_config