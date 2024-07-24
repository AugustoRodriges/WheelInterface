from prompt_toolkit import HTML
from prompt_toolkit.layout.containers import Window, HSplit
from prompt_toolkit.widgets import Label
from common.utils import create_progress_bar

class PedalPercentageLabel(Label):

    def __init__(self, pedal: str, percentage:int):
        self.pedal = pedal
        self.percentage = percentage
        super().__init__(text=self._format_content())

    def _format_content(self):
        return HTML(f'<text>{self.pedal}:</text> <bar>{create_progress_bar(self.percentage)}%</bar>')

    def update_content(self, percentage):
        self.percentage = percentage
        self.text = self._format_content()


class PedalsBar():
    def __init__(self):
        pass

    def create_window_pedals_content(self, pedals: dict):
        self.acelerator = PedalPercentageLabel('Acelerator', pedals['acelerator'])
        self.brake = PedalPercentageLabel("Brake", pedals['brake'])
        self.clutch = PedalPercentageLabel("Clutch  ", pedals['clutch'])

        win = HSplit([
            self.acelerator,
            self.brake,
            self.clutch,
        ])

        return win

    def update_pedals_bar_content(self, pedals: dict):
        self.acelerator.update_content(pedals['acelerator'])
        self.brake.update_content(pedals["brake"])
        self.clutch.update_content(pedals["clutch"])
