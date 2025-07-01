from time import *
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

import py_win_keyboard_layout
import ctypes
import var

keyboard = KeyboardController()
mouse = MouseController()

import pynput

class Movement():
    def __init__(self, Macro):
        self.Macro = Macro

    def correct(self):
        klid = ctypes.windll.user32.LoadKeyboardLayoutW("00000409", 1)

        ctypes.windll.user32.ActivateKeyboardLayout(klid, 0)
        keyboard = KeyboardController()
        mouse = MouseController()

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
        print("Reset character")
        keyboard.tap(Key.esc)
        sleep(0.2)
        keyboard.tap("r")
        keyboard.tap("к")
        sleep(0.2)
        keyboard.tap(Key.enter)

        #Расклик клавиатуры,
        keyboard.tap("w")
        keyboard.tap("a")
        keyboard.tap("s")
        keyboard.tap("d")
        keyboard.tap(Key.space)

    def tap_key(self, key:Key):
        keyboard.tap(key)

    def jump(self):
        keyboard.press(Key.space)
        sleep(0.05)
        keyboard.release(Key.space)

    def shiftlock(self):
        keyboard.press(Key.shift_l)
        sleep(0.05)
        keyboard.release(Key.shift_l)

    def move(self, key, duration):
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