from common.utils import map_range
from hardware_control.arduino_controller import ArduinoController
from pyvjoystick.vjoy import VJoyDevice, HID_USAGE
from common.config import TARGET_MAX, TARGET_MIN, VJOY_ID

class VJoyInterface():

    def __init__(self, arduino: ArduinoController):
        self.joystick = VJoyDevice(VJOY_ID)
        self.arduino = arduino

        self.pedals_axis_rotation = [None, None, None]

        self.wheel_axis_rotation = None
    
    def _set_wheel_axis(self) -> int:
        wheel = int(self.arduino.wheel_manager.get_map_data())

        wheel_axis = map_range(wheel, -450, 450, TARGET_MIN, TARGET_MAX)
        self.joystick.set_axis(HID_USAGE.X, wheel_axis)

        return wheel

    def _set_pedal_axis(self) -> list:
        """
        Configure each pedal to control a different axis on the joystick.

        Returns:
            list: Pedals reading mapped to a range of 1 to 100.
        """
        try:
            pedals = self.arduino.pedal_manager.get_map_data() # Get pedals data

            # Map pedals data to the axis range
            self.pedals_axis_rotation[0] = map_range(pedals["acelerator"], 0, 100, TARGET_MIN, TARGET_MAX)
            self.pedals_axis_rotation[1] = map_range(pedals["brake"], 0, 100, TARGET_MIN, TARGET_MAX)
            self.pedals_axis_rotation[2] = map_range(pedals["clutch"], 0, 100, TARGET_MIN, TARGET_MAX)

            # Map each pedal to an axis on the joystick
            self.joystick.set_axis(HID_USAGE.RX, self.pedals_axis_rotation[0])
            self.joystick.set_axis(HID_USAGE.RY, self.pedals_axis_rotation[1])
            self.joystick.set_axis(HID_USAGE.RZ, self.pedals_axis_rotation[2])

            pedals["acelerator"] = int(pedals["acelerator"])
            pedals["brake"] = int(pedals["brake"])
            pedals["clutch"] = int(pedals["clutch"])

            return pedals

        except TypeError:
            return None
    
    def set_joystick(self):
        self.arduino.board.get_data()

        pedals = self._set_pedal_axis()
        wheel = self._set_wheel_axis()

        return pedals, wheel
        