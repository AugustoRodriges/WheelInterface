from prompt_toolkit import HTML
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.widgets import Label
from common.utils import create_progress_bar
from . import Data, CustomLabel

class WheelAngleLabel(Label):
    def __init__(self, sum_angle: int):
        self.sum_angle = sum_angle
        self.mult = 100 / (self.sum_angle * 2) 
        self.angle_per = self.sum_angle * self.mult + 1
        
        super().__init__(text=self._format_content)
    
    def _format_content(self):
        return HTML(create_progress_bar(self.angle_per, show_percentage=False, total=100))

    def update_content(self, angle):
        self.angle_per = (angle + self.sum_angle) * self.mult + 1
        self.text = self._format_content()


class WheelData(Data):
    def __init__(self, sum_angle: int):
        self.angle = CustomLabel()
        self.bar = WheelAngleLabel(sum_angle)

        self.l1 = CustomLabel()

    def create_container(self):
        win = HSplit([
            VSplit([
                Window(char=' ', width=44),
                Label("Wheel Angle:"),
                Window(char=' ', width=44),
            ]),
            self.bar,
            VSplit([
                self.l1,
                self.angle,
                Window(char=' ', width=49),
            ])
        ])

        return win

    def update_container_content(self, angle: int):
        self.bar.update_content(angle)
        self.l1.update_content(' ' * (49 - len(str(angle))))
        self.angle.update_content(f'{angle}°')
