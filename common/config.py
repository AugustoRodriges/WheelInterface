from prompt_toolkit.styles import Style

# Range of the axes
TARGET_MIN = 0x1
TARGET_MAX = 0x8000

# Devices Id's
VJOY_ID = 1
ARDUINO_PORT = "COM4"
BPS = 115200  

# UI styles
STYLES = Style.from_dict({
    'title': '#032cfc bold',
    'sub': '#008000 bold',
    'text': '#032cfc italic',
    'bar': '#008000',
})