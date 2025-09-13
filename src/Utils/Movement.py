import time
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import ctypes
import var

var.keyboard = KeyboardController()
var.mouse = MouseController()

class Movement():
    def __init__(self, Macro):
        self.Macro = Macro

    def force_release_all(self):
        keys = [
            Key.esc, Key.shift_l, Key.shift_r, Key.tab, Key.ctrl_l, Key.ctrl_r, 
            Key.alt_l, Key.alt_r, Key.enter, Key.space,
            "w", "a", "s", "d", "e", "r", "к"
        ]

        for key in keys:
            try:
                var.keyboard.release(key)
            except:
                pass

    def correct(self):
        klid = ctypes.windll.user32.LoadKeyboardLayoutW("00000409", 1)
        ctypes.windll.user32.ActivateKeyboardLayout(klid, 0)
        var.keyboard = KeyboardController()
        var.mouse = MouseController()
        var.mouse.scroll(0, 5)

    def align_spawn(self):
        correct = False

        while not correct:
            self.reset_character()
            time.sleep(3)
            correct = self.Macro.screen.isCorrectStartPos()
        
            if correct:
                print("Aligned")
                self.camera_rotate(-15.6)
                self.align_spawn_position()
                break

        

    def align_spawn_position(self):
        self.move("w", 4)
        self.move("d", 3)

        var.keyboard.press("w")
        var.keyboard.press("d")
        time.sleep(2)
        var.keyboard.release("w")
        var.keyboard.release("d")

    def stop_movement(self):
        var.keyboard.release("w")
        var.keyboard.release("a")
        var.keyboard.release("s")
        var.keyboard.release("d")

    def reset_character(self):
        self.correct()
        self.force_release_all()
        print("Reset character")

        var.keyboard.press(Key.esc)
        time.sleep(0.05)
        var.keyboard.release(Key.esc)
        time.sleep(0.1)

        var.keyboard.press('r')
        time.sleep(0.05)
        var.keyboard.release('r')
        time.sleep(0.1)

        var.keyboard.press(Key.enter)
        time.sleep(0.05)
        var.keyboard.release(Key.enter)
        time.sleep(0.1)

        # Исправлено: для буквенных клавиш используем строки, для специальных - Key.*
        for key in ["w", "a", "s", "d", Key.space]:
            var.keyboard.press(key)
            time.sleep(0.03)
            var.keyboard.release(key)
            time.sleep(0.02)

    def tap_key(self, key):
        var.keyboard.press(key)
        time.sleep(0.08)
        var.keyboard.release(key)

    def jump(self):
        var.keyboard.press(Key.space)
        time.sleep(0.08)
        var.keyboard.release(Key.space)

    def shiftlock(self):
        var.keyboard.press(Key.shift_l)
        time.sleep(0.08)
        var.keyboard.release(Key.shift_l)

    def move(self, key, duration):
        buffs = var.macro.screen.speed_buff or 0
        base_speed = var.movespeed
        new_speed = base_speed + 3 * buffs
        mult = 32 / new_speed
    
        var.keyboard.press(key)
        time.sleep(duration * mult)
        var.keyboard.release(key)

    def hold_mouse(self):
        var.mouse.press(Button.left)

    def release_mouse(self):
        var.mouse.release(Button.left)

    def camera_rotate(self, degree):
        hold_time = abs(degree) / 117.65
        if degree < 0:
            var.keyboard.press(Key.left)
            time.sleep(hold_time)
            var.keyboard.release(Key.left)
        else:
            var.keyboard.press(Key.right)
            time.sleep(hold_time)
            var.keyboard.release(Key.right)