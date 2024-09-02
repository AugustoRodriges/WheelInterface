# ui/containers/__init__.py
from typing import Callable
from prompt_toolkit.layout.containers import WindowAlign
from prompt_toolkit.widgets import Label

class Data():

    def create_container(self):
        raise NotImplementedError
    
    def update_container_content(self):
        raise NotImplementedError

class CustomLabel(Label):
    def __init__(self):
        super().__init__(text='')
    
    def update_content(self, text):
        self.text = text
        