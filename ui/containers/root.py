from typing import Sequence
from prompt_toolkit.widgets import Label, Box, Dialog, Button
from prompt_toolkit.layout.containers import VSplit, HSplit
from prompt_toolkit.widgets.base import Button
from pedals_data import PedalsData

class Root(Dialog):
    
    def __init__(self, pedals_bar_container: PedalsData):
        self.pedals_bar_container = pedals_bar_container
        super().__init__(title="DIY Steering Wheel", with_background=True, body=self.body())
    
    def body(self):
        body = VSplit([
            self.pedals_bar_container
        ])

        return Box(body=body)
    