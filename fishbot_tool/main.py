from curses import flash
from rich import print
from fishbot_tool.flash import Tool as ToolEspFlash
from fishbot_tool.config import Tool as ToolConfig
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit import prompt
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML


def bottom_toolbar():
    return HTML('小鱼提示: exit:退出 help:查看帮助')


tool_map = {
    "flash": ToolEspFlash(),
    "config": ToolConfig(),
}

help_hint = f"""
- flash  : 烧录FishBot固件 (主板&雷达)
- config : 配置WIFI&电机等
"""
# - config: 配置FishBot


def command_parse(cmd: str):
    commands = cmd.split()
    if len(commands) == 0:
        print(help_hint)
        return
    text = commands[0]
    if(text == "help"):
        print(help_hint)
    elif text in tool_map.keys():
        tool = tool_map[text]
        tool.run(commands)
    else:
        print(f"不支持的命令:{cmd}")


def main():
    dics = {'help': None,
            'exit': None, }
    for command in tool_map.keys():
        dics[command] = tool_map[command].get_complete()
    command_completer = NestedCompleter.from_nested_dict(dics)

    print("欢迎使用FishBot配置工具")
    print(help_hint)
    while True:
        text = prompt('fishbot>>', completer=command_completer,
                      bottom_toolbar=bottom_toolbar)
        if(text == "exit"):
            print("再见!记得关注鱼香ROS哦~")
            break
        command_parse(text)


if __name__ == '__main__':
    main()
