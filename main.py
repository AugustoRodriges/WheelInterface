from hardware_control.arduino_controller import ArduinoController
from joystick_control.joystick import VJoyInterface
from ui.steering_wheel_app import SteeringWheelApp
from ui.containers import pedals_data, root
from prompt_toolkit.layout import Layout
import threading
import time

arduino = ArduinoController() # Arduino
joystick = VJoyInterface(arduino)

bar = pedals_data.PedalsData()
bar_container = bar.create_container({'acelerator': 0, 'brake': 0, 'clutch': 0}, arduino.pedal_mannager.PEDALS)

root_container = root.Root(bar_container)

app = SteeringWheelApp(root_container)

def main():
    def wheel_background():
        while True:
            pedals_content = joystick.set_pedal_axis()
            bar.update_container_content(pedals_content)
            app.invalidate()
            time.sleep(0.01)

    back = threading.Thread(target=wheel_background)
    back.start()

    app.run()

if __name__ == "__main__":
    main()
    