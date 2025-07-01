from time import *
import var

@var.macro.task()
class TaskHandler():
    name = "Convert"
    def __init__(self):
        pass

    def start(self):
        movement_lib = var.macro.movement
        screen_lib = var.macro.screen

        movement_lib.move("w", 1.05)
        movement_lib.tap_key("e")
        print("Converting...")
        while not screen_lib.is_backpack_empty() and var.macro.started:
            sleep(0.5)
        if not var.macro.started:
            return
        sleep(2)