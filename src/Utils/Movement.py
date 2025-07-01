from time import *
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

import py_win_keyboard_layout
import ctypes
import var

var.keyboard = KeyboardController()
var.mouse = MouseController()

import pynput

class Movement():
    def __init__(self, Macro):
        self.Macro = Macro

    def correct(self):
        klid = ctypes.windll.user32.LoadKeyboardLayoutW("00000409", 1)

        ctypes.windll.user32.ActivateKeyboardLayout(klid, 0)
        var.keyboard = KeyboardController()
        var.mouse = MouseController()

        var.mouse.scroll(0, 5)

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
            self.correct()

            sleep(4.5)

    def stop_movement(self):
        var.keyboard.release("w")
        var.keyboard.release("a")
        var.keyboard.release("s")
        var.keyboard.release("d")

    def reset_character(self):
        print("Reset character")
        var.keyboard.tap(Key.esc)
        sleep(0.2)
        var.keyboard.tap("r")
        var.keyboard.tap("к")
        sleep(0.2)
        var.keyboard.tap(Key.enter)

        #Расклик клавиатуры,
        var.keyboard.tap("w")
        var.keyboard.tap("a")
        var.keyboard.tap("s")
        var.keyboard.tap("d")
        var.keyboard.tap(Key.space)

    def tap_key(self, key:Key):
        var.keyboard.tap(key)

    def jump(self):
        var.keyboard.press(Key.space)
        sleep(0.05)
        var.keyboard.release(Key.space)

    def shiftlock(self):
        var.keyboard.press(Key.shift_l)
        sleep(0.05)
        var.keyboard.release(Key.shift_l)

    def move(self, key, duration):
        mult = 32 / var.movespeed
        var.keyboard.press(key)
        sleep(duration * mult)
        var.keyboard.release(key)

    def hold_mouse(self):
        var.mouse.press(Button.left)

    def release_mouse(self):
        var.mouse.release(Button.left)

    def camera_rotate(self, degree):
        hold_time = abs(degree) / 117.65
        if degree < 0:
            var.keyboard.press(Key.left)
            sleep(hold_time)
            var.keyboard.release(Key.left)
        else:
            var.keyboard.press(Key.right)
            sleep(hold_time)
            var.keyboard.release(Key.right)