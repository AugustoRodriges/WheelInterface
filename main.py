from hardware_control.arduino_controller import ArduinoController
from joystick import VJoyInterface
from ui.steering_wheel_app import SteeringWheelApp
from ui.containers import pedals_bar
import threading
import time

arduino = ArduinoController() # Arduino
joystick = VJoyInterface(arduino)

bar = pedals_bar.PedalsBar()
app = SteeringWheelApp([1315, 173], bar.create_window_pedals_content({'acelerator': 0, 'brake': 0, 'clutch': 0}))

def background():
    while True:
        pedals_content = joystick.set_pedal_axis()
        bar.update_pedals_bar_content(pedals_content)
        app.invalidate()
        time.sleep(0.01)

back = threading.Thread(target=background)
back.start()

app.run()