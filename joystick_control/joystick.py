from common.utils import map_range
from hardware_control.arduino_controller import ArduinoController
from pyvjoystick.vjoy import VJoyDevice, HID_USAGE
from common.config import TARGET_MAX, TARGET_MIN, VJOY_ID

class VJoyInterface():

    def __init__(self, arduino: ArduinoController):
        self.joystick = VJoyDevice(VJOY_ID)
        self.arduino = arduino

        self.pedals_axis_rotation = [None, None, None]

    def set_pedal_axis(self) -> list | None:
        """
        Configure each pedal to control a different axis on the joystick.

        Returns:
            list: Pedals reading mapped to a range of 1 to 100.
        """
        try:
            pedals = self.arduino.pedal_mannager.get_map_data() # Get pedals data

            # Map pedals data to the axis range
            self.pedals_axis_rotation[0] = map_range(pedals["acelerator"], 0, 100, TARGET_MIN, TARGET_MAX)
            self.pedals_axis_rotation[1] = map_range(pedals["brake"], 0, 100, TARGET_MIN, TARGET_MAX)
            self.pedals_axis_rotation[2] = map_range(pedals["clutch"], 0, 100, TARGET_MIN, TARGET_MAX)

            # Map each pedal to an axis on the joystick
            self.joystick.set_axis(HID_USAGE.RX, self.pedals_axis_rotation[0])
            self.joystick.set_axis(HID_USAGE.RY, self.pedals_axis_rotation[1])
            self.joystick.set_axis(HID_USAGE.RZ, self.pedals_axis_rotation[2])

            return pedals

        except TypeError:
            return None
        