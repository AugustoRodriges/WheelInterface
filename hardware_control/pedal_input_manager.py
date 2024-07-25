from pyfirmata import Arduino
from common.utils import CacheValidation

class PedalInputManager:

    def __init__(self, board: Arduino):
        self.PEDALS = {
            "acelerator": board.get_pin('a:0:i'), 
            "brake": board.get_pin('a:1:i'), 
            "clutch": board.get_pin('a:2:i')
        }

        self.cache_validation = CacheValidation('C:\\Users\\augus\\Documentos\\GitHub\WheelInterface\\hardware_control\\calib_data.json')
    
    def get_raw_data(self):
        data = {
            "acelerator": self.PEDALS["acelerator"].read(),
            "brake": self.PEDALS["brake"].read(),
            "clutch": self.PEDALS["clutch"].read()
        }

        return data

    def _read_and_map_pedal(self, pin, pedal_range):
            value = pin.read()
            if value is None:
                return None
            result = (value - pedal_range[1]) / pedal_range[2] * 100

            # if pin is self.PEDALS['brake']:
                # return int(max(0, min(result * -1, 100)))
                
            return int(max(0, min(result, 100)))

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

        data["acelerator"] = self._read_and_map_pedal(self.PEDALS["acelerator"], pedals_range["acelerator"])
        data["brake"] = self._read_and_map_pedal(self.PEDALS["brake"], pedals_range["brake"])
        data["clutch"] = self._read_and_map_pedal(self.PEDALS["clutch"], pedals_range["clutch"])

        return data
