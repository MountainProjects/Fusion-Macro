from time import *
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import var

keyboard = KeyboardController()
mouse = MouseController()

class Movement():
    def __init__(self, Macro):
        self.Macro = Macro

    def align_spawn(self):
        """
        Резетает персонажа до тех пор пока не будет правильная позиция спавна и камеры
        """
        correct = self.Macro.screen.isCorrectStartPos()
        if correct:
            return

        while not correct:
            aligned = self.Macro.screen.isCorrectStartPos()
            if aligned:
                break

            self.reset_character()
            sleep(4.5)

    def stop_movement(self):
        keyboard.release("w")
        keyboard.release("a")
        keyboard.release("s")
        keyboard.release("d")

    def reset_character(self):
        keyboard.tap(Key.esc)
        keyboard.tap("r")
        keyboard.tap("к")
        keyboard.tap(Key.enter)

    def tap_key(self, key:Key):
        keyboard.tap(key)

    def move(self, key, duration):
        mult = var.movespeed/100
        keyboard.press(key)
        sleep(time*mult)
        keyboard.release(key)