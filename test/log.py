import sys

class OutputRedirector:
    def __init__(self, output):
        self.output = output

    def write(self, message):
        self.output.write(message)

    def flush(self):
        pass

# 创建一个文件用于保存输出
with open('output.txt', 'w') as f:
    # 将 sys.stdout 重定向到文件对象上
    sys.stdout = OutputRedirector(f)
    
    # 下面的所有 print() 函数调用都会输出到 output.txt 文件中
    print('Hello, world!')
    print('This is a redirected output.')

# 恢复 sys.stdout 到原始状态
sys.stdout = sys.__stdout__
