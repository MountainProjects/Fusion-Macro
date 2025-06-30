from time import *
import var

class Convert():
    def __init__(self):
        pass

    def start(self):
        movement_lib = var.macro.movement
        screen_lib = var.macro.screen

        movement_lib.walk("w", 1.2)
        movement_lib.tap_key("e")
        while not screen_lib.is_backpack_empty():
            sleep(0.5)

        sleep(2)