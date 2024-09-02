import sys
import os
sys.path.append(os.path.abspath('C:\\Users\\augus\Documentos\\GitHub\\WheelInterface\\ui\\containers'))
from typing import Sequence
from prompt_toolkit.widgets import Label, Box, Dialog, Button
from prompt_toolkit.layout.containers import VSplit, HSplit
from prompt_toolkit.widgets.base import Button
from ui.containers.pedals_data import PedalsData
from ui.containers.wheel_data import WheelData

class Root(Dialog):
    
    def __init__(self, pedals_bar_container: PedalsData, wheel_container: WheelData):
        self.pedals_bar_container = pedals_bar_container
        self.wheel_container = wheel_container
        super().__init__(title="DIY Steering Wheel", with_background=True, body=self._body())
    
    def _body(self):
        body = HSplit([
            self.wheel_container,
            self.pedals_bar_container
        ])

        return Box(body=body)
    