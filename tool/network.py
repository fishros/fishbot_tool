import requests
import json
import threading
import yaml
import time
def parse_yaml_from_json(json_data):
    yaml_content = json_data['response']['content']
    yaml_content = yaml_content.replace("```yaml\n","").replace("```","").strip()
    data = yaml.safe_load(yaml_content)
    return data

class FishBotFirmwareDownloader:
    def __init__(self, logger):
        self.logger = logger
        self.version_info_url = 'https://fishros.org.cn/forum/api/v3/posts/10390'

    def get_version_data(self, callback=None,is_async=False):
        """
        Asynchronously retrieves version data using threading.
        """
        def thread_func():
            try:
                response = requests.get(self.version_info_url)
                response.raise_for_status()  # Raises stored HTTPError, if one occurred.
                raw_data = response.text
                version_info = parse_yaml_from_json(json.loads(raw_data))
                if callback:
                    callback(version_info)
            except Exception as e:
                error_message = f'[警告]: 获取最近版本固件地址失败，请手动指定，错误: {str(e)}'
                self.logger(error_message)
                if callback:
                    callback(None)
        if is_async:
            thread = threading.Thread(target=thread_func)
            thread.start()
        else:
            thread_func()

    def download_firmware(self, firmware_path, path):
        """
        Downloads firmware with progress logs.
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
                    if time.time() - last_print_time > 0.3:
                        last_print_time = time.time()
                        progress = (bytes_written / total_size) * 100 if total_size > 0 else 0
                        self.logger(f'[进度]下载中：{path} - {progress:.2f}%完成')
        self.logger(f'\n[提示]下载完成：{path}')
        return path

if __name__ == "__main__":
    def log(msg):
        print(msg)

    def callback(data):
        if data:
            print("Version Data Retrieved Successfully:", data)
        else:
            print("Failed to retrieve version data.")

    downloader = FishBotFirmwareDownloader(log)
    downloader.get_version_data(callback)
