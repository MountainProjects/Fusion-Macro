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
        sleep_time = 0
        while not screen_lib.is_backpack_empty() and var.macro.started:
            sleep(0.5)
            sleep_time += 0.5
            if sleep_time == 5 and screen_lib.is_backpack_full():
                print("Macro is not converting, restarting...")
                var.macro.restart()
        if not var.macro.started:
            return
        sleep(2)