
from hardware_control.serial_communication import ArduinoWheel
from hardware_control.devices_input_manager import PedalInputManager, WheelInputManager
from common.config import ARDUINO_PORT, BPS

class ArduinoController():
    def __init__(self):

        self.board = ArduinoWheel(ARDUINO_PORT, BPS)

        self.pedal_manager = PedalInputManager(self.board)

        self.wheel_manager = WheelInputManager(self.board)

