from hardware_control.arduino_controller import ArduinoController
from joystick_control.joystick import VJoyInterface
from ui.steering_wheel_app import SteeringWheelApp
from ui.containers import pedals_data, root, wheel_data
import threading
import time

arduino = ArduinoController() # Arduino
joystick = VJoyInterface(arduino)

pedals_content, wheel_angle = 0, 0

bar = pedals_data.PedalsData(arduino.board)
bar_container = bar.create_container()

wheel_bar = wheel_data.WheelData(450)
wheel_container = wheel_bar.create_container()

root_container = root.Root(bar_container, wheel_container)

app = SteeringWheelApp(root_container)

def main():

    def app_back():
        while True:
            wheel_bar.update_container_content(wheel_angle)
            bar.update_container_content(pedals_content)
            app.invalidate()
            time.sleep(0.05)
            
    def wheel_back():
        global pedals_content, wheel_angle
        while True:
            pedals_content, wheel_angle = joystick.set_joystick()

    wheel_background = threading.Thread(target=wheel_back)
    wheel_background.start()

    app_background = threading.Thread(target=app_back)
    app_background.start()

    app.run()

if __name__ == "__main__":
    main()
    