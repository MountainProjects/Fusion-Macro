from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

keyboard = KeyboardController()
mouse = MouseController()

class Movement():
    def __init__(self, Macro):
        self.Macro = Macro

    def reset_character():
        keyboard.tap(Key.esc)
        keyboard.tap("r")
        keyboard.tap("к")
        keyboard.tap(Key.enter)