from prompt_toolkit import HTML
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.widgets import Label, Button
import json
from pyfirmata import Pin
from common.utils import create_progress_bar


class PedalPercentageLabel(Label):

    def __init__(self, pedal: str, percentage:int, custom_text: str=''):
        self._text = pedal + custom_text
        self.percentage = percentage
        super().__init__(text=self._format_content())

    def _format_content(self):
        return HTML(f'{self._text}: {create_progress_bar(self.percentage)}%')

    def update_content(self, percentage):
        self.percentage = percentage
        self.text = self._format_content()


class PedalMButton(Button):

    def __init__(self, text: str, pedal: Pin, position: int):
        self.pedal = pedal
        self._text = text
        super().__init__(text=text, handler= lambda: self.change_pedal_calibration_value(position))
    
    def _change_json_var(self, var, new_value, position):
        with open('C:\\Users\\augus\\Documentos\\GitHub\WheelInterface\\hardware_control\\calib_data.json', 'r') as file:
            data = json.load(file)
            calib = data[var]
            calib[position] = new_value
            data[var] = calib
        
        with open('C:\\Users\\augus\\Documentos\\GitHub\WheelInterface\\hardware_control\\calib_data.json', 'w') as file:
            json.dump(data, file, indent=4)
    
    def change_pedal_calibration_value(self, position):
        if 'min' in self._text.lower():
            self._change_json_var('pedals_min_value', self.pedal.read(), position)

        elif 'max' in self._text.lower():
            self._change_json_var('pedals_max_value', self.pedal.read(), position)


class PedalsData():

    def __init__(self):
        pass

    def buttons_layout(self, pin: Pin, position: int):
        return VSplit([
            PedalMButton('min', pin, position), 
            Window(char=' ', width=42),
            PedalMButton('max', pin, position)
        ])

    def create_container(self, pedals_content: dict, pedals_pins):
        self.acelerator = PedalPercentageLabel('Acelerator', pedals_content['acelerator'])
        self.brake = PedalPercentageLabel("Brake", pedals_content['brake'], "     ")
        self.clutch = PedalPercentageLabel("Clutch  ", pedals_content['clutch'], "  ")

        win = HSplit([
            self.acelerator,
            self.buttons_layout(pedals_pins["acelerator"], 0),
            self.brake,
            self.buttons_layout(pedals_pins["brake"], 1),
            self.clutch,
            self.buttons_layout(pedals_pins["clutch"], 2),
        ])

        return win

    def update_container_content(self, pedals: dict):
        try:
            self.acelerator.update_content(pedals['acelerator'])
            self.brake.update_content(pedals["brake"])
            self.clutch.update_content(pedals["clutch"])
        except TypeError:
            pass
