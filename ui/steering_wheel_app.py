
from prompt_toolkit import Application
from prompt_toolkit.layout import Layout, VSplit
from prompt_toolkit.widgets import Label
from common.config import STYLES

class SteeringWheelApp(Application):
    def __init__(self, root_container):
        super().__init__(layout=Layout(root_container), style=STYLES, full_screen=True, mouse_support=True)
