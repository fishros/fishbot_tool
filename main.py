from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt
from rich import print

from tools.flash import Tool as ToolEspFlash

tool_map = {
    "flash": ToolEspFlash(),
}

help_hint = f"""
- flash : 烧录FishBot相关固件 (主板&雷达)
- config: 配置FishBot
- help  : 查看帮助信息
- exit  : 退出命令行交互模式
"""


def command_parse(cmd: str):

    if(text == "help"):
        print(help_hint)
    elif text in tool_map.keys():
        tool = tool_map[cmd]
        tool.run()
    else:
        print(f"不支持的命令:{cmd}")


if __name__ == '__main__':
    command_completer = WordCompleter(list(tool_map.keys())+["help", "exit"])
    print("欢迎使用FishBot配置工具")
    print(help_hint)
    text = prompt('请输入命令(help查看帮助): ', completer=command_completer)
    while text != "exit":
        command_parse(text)
        text = prompt('请输入命令(help查看帮助): ', completer=command_completer)
