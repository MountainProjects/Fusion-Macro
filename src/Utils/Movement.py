from time import *
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

import py_win_keyboard_layout
import ctypes
import var

keyboard = KeyboardController()
mouse = MouseController()

class Movement():
    def __init__(self, Macro):
        self.Macro = Macro

    def correct(self):
        py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x04090409)
        mouse.scroll(0, 5)
        #TODO ДЕТЕКТ ШИФТ ЛОКА И ШИФТ ЛОК

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
        sleep(0.2)
        keyboard.tap("r")
        keyboard.tap("к")
        sleep(0.2)
        keyboard.tap(Key.enter)

    def tap_key(self, key:Key):
        keyboard.tap(key)

    def jump(self):
        keyboard.press(Key.space)
        sleep(0.05)
        keyboard.release(Key.space)

    def move(self, key, duration):
        print("Иду нахрен")
        mult = var.movespeed / 100
        keyboard.press(key)
        sleep(duration * mult)
        keyboard.release(key)

    def hold_mouse(self):
        mouse.press(Button.left)

    def release_mouse(self):
        mouse.release(Button.left)

    def camera_rotate(self, degree):
        hold_time = abs(degree) / 117.65
        if degree < 0:
            keyboard.press(Key.left)
            sleep(hold_time)
            keyboard.release(Key.left)
        else:
            keyboard.press(Key.right)
            sleep(hold_time)
            keyboard.release(Key.right)