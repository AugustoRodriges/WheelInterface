
from prompt_toolkit import Application
from prompt_toolkit.layout import Layout, VSplit
from prompt_toolkit.widgets import Label
from common.config import STYLES

class SteeringWheelApp(Application):
    def __init__(self, window_size: list, root_container):
        self.app_window = VSplit([root_container], width=window_size[0], height=window_size[1])
        super().__init__(layout=Layout(self.app_window), style=STYLES, full_screen=False)
