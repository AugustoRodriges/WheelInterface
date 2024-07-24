from pyfirmata import Arduino, util
from hardware_control.pedal_input_manager import PedalInputManager
from common.config import ARDUINO_PORT

class ArduinoController():
    def __init__(self):

        self.board = Arduino(ARDUINO_PORT)

        self.pedal_mannager = PedalInputManager(self.board)

        self.it = util.Iterator(self.board)
        self.it.start()
