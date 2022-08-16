import sys
sys.path.append('/fishbot')
sys.path.append('fishbot_tool/libs/')
import libfishbot as fishbot


def get_fishbot_by_uart(port: str, baudrate: int):
    bot = fishbot.FishBot()
    bot.set_protocol_serial(port, baudrate)
    bot.set_motion_model_diff2(0.170, 3293, 0.065 / 2)
    bot.init()
    return bot
    # fishbot.update_wifi_config_sta("JKC", "jkc20210106")
    # fishbot.restart()

    # fishbot.destory()
