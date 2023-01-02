import subprocess
import time


class CmdTask():
    def __init__(self) -> None:
        pass

    def run(self, command, cwd):
        self.sub = subprocess.Popen(command,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    cwd=cwd,
                                    shell=True)

    def getlog(self,callback=None):
        # stdout_line = self.sub.stdout.readline().decode("utf-8")
        # stderr_line = self.sub.stderr.readline().decode("utf-8")
        stdout_line = ""
        for line in iter(self.sub.stdout.readline,'b'):
            line = line.rstrip().decode('utf8')
            if callback:
                print(line)
                callback(line)
            # 你的操作
            if(subprocess.Popen.poll(self.sub) is not None):
                if(line==""):
                    break

        for line in iter(self.sub.stderr.readline,'b'):
            line = line.rstrip().decode('utf8')
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
            line = line.decode("utf-8").strip("\n")
            out.append(line)
            time.sleep(0.01)
        lines = self.sub.stderr.readlines()
        for line in lines:
            line = line.decode("utf-8").strip("\n")
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


if __name__ == "__main__":
    cmd = CmdTask()
    cmd.run("wget https://fishros.org.cn/forum/assets/uploads/files/1672542988816-fishbot_motion_control_v1.0.0.230101.bin -O esp32.bin",
            "/home/fishros/code/fishbot_tool/fishbot_tool")
    while cmd.is_finish() == None:
        print(cmd.getlog())

    print(cmd.getlogs())
