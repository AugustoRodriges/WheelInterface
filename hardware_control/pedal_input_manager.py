from pyfirmata import Arduino

class PedalInputManager:

    def __init__(self, board: Arduino):
        self.PEDALS = {
            "acelerator": board.get_pin('a:0:i'), 
            "brake": board.get_pin('a:1:i'), 
            "clutch": board.get_pin('a:2:i')
        }

        self.PEDALS_MIN_VALUE = [0.4027, 0.5347, 0.4282]
        self.PEDALS_MAX_VALUE = [0.4545, 0.5103, 0.4409]

        self.pedals_range = {
            "acelerator": [
                self.PEDALS_MAX_VALUE[0], self.PEDALS_MIN_VALUE[0], self.PEDALS_MAX_VALUE[0] - self.PEDALS_MIN_VALUE[0]
                ], 
                
            "brake": [
                self.PEDALS_MAX_VALUE[1], self.PEDALS_MIN_VALUE[1], self.PEDALS_MAX_VALUE[1] - self.PEDALS_MIN_VALUE[1]
                ], 

            "clutch": [
                self.PEDALS_MAX_VALUE[2], self.PEDALS_MIN_VALUE[2], self.PEDALS_MAX_VALUE[2] - self.PEDALS_MIN_VALUE[2]
                ]
        }
    
    def get_raw_data(self):
        data = {
            "acelerator": self.PEDALS["acelerator"].read(),
            "brake": self.PEDALS["brake"].read(),
            "clutch": self.PEDALS["clutch"].read()
        }

        return data

    def get_map_data(self):
        data = {"acelerator": None, "brake": None, "clutch": None}

        def read_and_map_pedal(pin, pedal_range):
            value = pin.read()
            if value is None:
                return None
            return int(abs(max(0, min(abs((value - pedal_range[1]) / pedal_range[2]) * 100, 100)) - 100))

        data["acelerator"] = read_and_map_pedal(self.PEDALS["acelerator"], self.pedals_range["acelerator"])
        data["brake"] = read_and_map_pedal(self.PEDALS["brake"], self.pedals_range["brake"])
        data["clutch"] = read_and_map_pedal(self.PEDALS["clutch"], self.pedals_range["clutch"])

        return data
