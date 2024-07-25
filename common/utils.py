import json
import os

class CacheValidation:
    
    def __init__(self, file_name:str):
        self.file_name = file_name
        with open(file_name, 'r') as file:
            self.data = json.load(file)
        self.last_update = os.path.getmtime(self.file_name)
    
    def update(self):
        last_update = os.path.getmtime(self.file_name)
        if last_update != self.last_update:
            self.last_update = last_update
            with open(self.file_name, 'r') as file:
                self.data = json.load(file)

    def get_data(self):
        self.update()
        return self.data


def map_range(value: int | float, from_min: int | float, from_max: int | float, to_min: int, to_max: int) -> int:
    """
    Map a value from one range to another range.

    Args:
        value (int or float): The number to be converted.
        from_min (int or float): The minimum value of the original range.
        from_max (int or float): The maximum value of the original range.
        to_min (int): The minimum value of the target range.
        to_max (int): The maximum value of the target range.
    
    Returns:
        int: The mapped value in the target range.
    """

    # Convert the value to the target range
    mapped_value = (value - from_min) / (from_max - from_min) * (to_max - to_min) + to_min
    
    # Ensure the result is within the target range
    return int(max(to_min, min(mapped_value, to_max)))

def create_progress_bar(percentage: int):
    total = 50  
    progress = int(total * (percentage / 100))
    bar = '▆' * progress + ' ' * (total - progress)
    return f'{bar} {percentage}'

