import subprocess
import time


class CmdTask():
    def __init__(self) -> None:
        pass

    def run(self, command, cwd=None):
        self.sub = subprocess.Popen(command,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    cwd=cwd,
                                    shell=True,
                                    bufsize=1,  # Line buffered
                                    universal_newlines=True)

    def getlog(self,callback=None):
        stdout_line = ""
        for line in iter(self.sub.stdout.readline,'b'):
            line = line.rstrip()#.decode('utf8', errors="ignore")
            if callback:
                print(line)
                callback(line)
            # 你的操作
            if(subprocess.Popen.poll(self.sub) is not None):
                if(line==""):
                    break

        for line in iter(self.sub.stderr.readline,'b'):
            line = line.rstrip()#.decode('utf8', errors="ignore")
            if callback:
                print(line)
                callback(line)
            # 你的操作
            if(subprocess.Popen.poll(self.sub) is not None):
                if(line==""):
                    break

    def getlogs(self):
        out = []
        lines = self.sub.stdout.readlines()
        for line in lines:
            line = line.decode("utf-8", errors="ignore").strip("\n")
            out.append(line)
            time.sleep(0.01)
        lines = self.sub.stderr.readlines()
        for line in lines:
            line = line.decode("utf-8", errors="ignore").strip("\n")
            out.append(line)
            time.sleep(0.01)

        logstr = ""
        for log in out:
            logstr += log
        return logstr


    def is_finish(self):
        if self.sub.poll() == None:
            return -1
        return self.sub.poll()


if __name__=='__main__':
    task = CmdTask()
    task.run(r'powershell ../esptool/esptool_win64.exe -p COM12 -b 460800 --before default_reset --after hard_reset --chip esp32 write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x00 C:\Users\wjm\AppData\Local\Temp\_MEI106162\1710596193698-fishbot_motion_control_v1.0.0.240316.bin')
    def getlog(msg): print(msg)
    task.getlog(getlog)
