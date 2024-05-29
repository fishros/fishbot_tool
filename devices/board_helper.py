from devices.fishbot_camera_baord import BoardFishBotCamera
from devices.fishbot_laser_board import BoardFishBotLaser
from devices.fishbot_motion_board import BoardFishBotMotion
from devices.fishbot_motion_four_driver_board import BoardFishBotMotion4D
from devices.fishbot_ulsound_board import BoardFishBotUlsound


class BoardHelper:
    def __init__(self,logger) -> None:
        self.logger = logger
        self.boards = {}
        board_class = [
            BoardFishBotCamera,
            BoardFishBotLaser,
            BoardFishBotMotion,
            BoardFishBotMotion4D,
            BoardFishBotUlsound,
        ]

        for boardc in board_class:
            board = boardc(self.logger)
            self.boards[board.name] = board
    def get_boards_name(self):
        return self.boards.keys()
    def get_board(self,name):
        return self.boards[name]