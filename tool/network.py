import requests
import json
import time

class FishBotFirmwareDownloader:
    def __init__(self,logger):
        self.logger = logger
        self.version_info_url = 'https://fishros.org.cn/forum/api/v3/posts/2301'

    def get_version_data(self):
        """
        获取版本数据信息
        """
        configs = []
        try:
            response = requests.get(self.version_info_url)
            raw_data = response.text
            start = raw_data.find("```json")+7
            end = raw_data.find('```', start)
            while start != -1 and end != -1:
                json_str = raw_data[start:end].replace("\\n", "").replace('\\"', '"')
                configs.append(json.loads(json_str))
                raw_data = raw_data[end+3:]
                start = raw_data.find("```json")+7
                end = raw_data.find('```', start)
        except:
            self.logger('[警告]:获取最近版本固件地址失败，请手动指定')
            pass

        if len(configs) > 0:
            return configs[0]
        else:
            return {}

    def download_firmware(self, firmware_path, path):
        """
        下载固件
        """
        self.logger(f'[提示]检测到固件{firmware_path}在HTTP路径上，开始下载')
        response = requests.get(firmware_path, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        bytes_written = 0
        last_print_time = time.time()
        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    bytes_written += len(chunk)
                    if time.time()-last_print_time>0.3:
                        last_print_time = time.time()
                        progress = (bytes_written / total_size) * 100 if total_size > 0 else 0
                        self.logger(f'[进度]下载中：{path} - {progress:.2f}%完成')
        self.logger(f'\n[提示]下载完成：{path}')
        return path

if __name__ == "__main__":
    downloader = FishBotFirmwareDownloader()
    version_data = downloader.get_version_data()
    print(version_data)
