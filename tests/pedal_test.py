from hardware_control.arduino_controller import ArduinoController

arduino = ArduinoController()

while True:
    print(arduino.pedal_mannager.get_raw_data())