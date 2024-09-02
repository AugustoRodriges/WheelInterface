from hardware_control.serial_communication import ArduinoWheel
from common.utils import CacheValidation

class InputManager():
    def get_map_data(self):
        raise NotImplementedError()
    
class WheelInputManager(InputManager):
     
    def __init__(self, board: ArduinoWheel):
        self.board = board
    
    def get_map_data(self):
        try:
            return int(self.board.wheel_data)
        except TypeError:
            return 0
        

class PedalInputManager(InputManager):

    def __init__(self, board: ArduinoWheel):
        self.board = board

        self.cache_validation = CacheValidation('F:\\GitHub\WheelInterface\\hardware_control\\calib_data.json')

    def _read_and_map_pedal(self, value, pedal_range):
            try:
                result = (value - pedal_range[1]) / pedal_range[2] * 100
            
            except ZeroDivisionError:
                self.cache_validation.set_backup()
                return 0
                
            return max(0, min(result, 100))

    def get_map_data(self):
        cache_data = self.cache_validation.get_data()

        pedals_min_value = cache_data['pedals_min_value']
        pedals_max_value = cache_data['pedals_max_value']
        
        pedals_range = {
            "acelerator": [
                pedals_max_value[0], pedals_min_value[0], pedals_max_value[0] - pedals_min_value[0]
                ], 
                
            "brake": [
                pedals_max_value[1], pedals_min_value[1], pedals_max_value[1] - pedals_min_value[1]
                ], 

            "clutch": [
                pedals_max_value[2], pedals_min_value[2], pedals_max_value[2] - pedals_min_value[2]
                ]
        }

        data = {"acelerator": None, "brake": None, "clutch": None}

        data["acelerator"] = self._read_and_map_pedal(self.board.pedals_data[0], pedals_range["acelerator"])
        data["brake"] = self._read_and_map_pedal(self.board.pedals_data[1], pedals_range["brake"])
        data["clutch"] = 0 # self._read_and_map_pedal(self.PEDALS["clutch"], pedals_range["clutch"])

        return data