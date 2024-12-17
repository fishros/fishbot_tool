from devices.fishbot_camera_baord import BoardFishBotCamera
from devices.fishbot_camera_baord_v2 import BoardFishBotCameraV2
from devices.fishbot_laser_board import BoardFishBotLaser
from devices.fishbot_motion_board import BoardFishBotMotion
from devices.fishbot_motion_four_driver_board import BoardFishBotMotion4D
from devices.fishbot_ulsound_board import BoardFishBotUlsound
from devices.ros2_multi_protocol_board import BoardROS2MultiProtocol
from devices.fishbot_motion_four_driver_board_v2 import BoardFishBotMotion4DV2

class BoardHelper:
    def __init__(self,logger) -> None:
        self.logger = logger
        self.boards = {}
        board_class = [
            BoardFishBotMotion,
            BoardFishBotMotion4D,
            BoardFishBotMotion4DV2,
            BoardFishBotLaser,
            BoardFishBotCameraV2,
            BoardFishBotCamera,
            BoardFishBotUlsound,
            BoardROS2MultiProtocol,
        ]

        for boardc in board_class:
            board = boardc(self.logger)
            self.boards[board.name] = board
    def get_boards_name(self):
        return self.boards.keys()
    def get_board(self,name):
        return self.boards[name]