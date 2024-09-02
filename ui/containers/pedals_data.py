from prompt_toolkit import HTML
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.widgets import Label, Button
import json
from hardware_control.serial_communication import ArduinoWheel
from common.utils import create_progress_bar
from . import Data


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

    def __init__(self, text: str, board: ArduinoWheel, position: int):
        self.board = board
        self._text = text
        super().__init__(text=text, handler= lambda: self._change_pedal_calibration_value(position))
    
    def _change_json_var(self, var, new_value, position):
        with open('F:\\GitHub\WheelInterface\\hardware_control\\calib_data.json', 'r') as file:
            data = json.load(file)
            calib = data[var]
            calib[position] = new_value
            data[var] = calib
        
        with open('F:\\GitHub\WheelInterface\\hardware_control\\calib_data.json', 'w') as file:
            json.dump(data, file, indent=4)
    
    def _change_pedal_calibration_value(self, position):
        self.board.get_data()
        if 'min' in self._text.lower():
            self._change_json_var('pedals_min_value', self.board.pedals_data[position], position)

        elif 'max' in self._text.lower():
            self._change_json_var('pedals_max_value', self.board.pedals_data[position], position)


class PedalsData(Data):

    def __init__(self, board: ArduinoWheel):
        self.board = board

    def _buttons_layout(self, position: int):
        return VSplit([
            PedalMButton('min', self.board, position), 
            Window(char=' ', width=42),
            PedalMButton('max', self.board, position)
        ])

    def create_container(self):
        self.acelerator = PedalPercentageLabel('Acelerator', 0)
        self.brake = PedalPercentageLabel("Brake", 0, "     ")
        self.clutch = PedalPercentageLabel("Clutch  ", 0, "  ")

        win = HSplit([
            self.acelerator,
            self._buttons_layout(0),
            self.brake,
            self._buttons_layout(1),
            self.clutch,
            self._buttons_layout(2),
        ])

        return win

    def update_container_content(self, pedals: dict):
        try:
            self.acelerator.update_content(pedals["acelerator"])
            self.brake.update_content(pedals["brake"])
            self.clutch.update_content(pedals["clutch"])
        except TypeError:
            pass
