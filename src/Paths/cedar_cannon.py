from time import *
import var

@var.macro.path()
class PathHandler:
    name = "cedar_cannon"

    def __init__(self):
        print(self)

    def start(self):
        camera_rotate = var.macro.movement.camera_rotate
        walk = var.macro.movement.move
        jump = var.macro.movement.jump
        press = var.macro.movement.tap_key

        camera_rotate(106)
        walk("w", 0.6)
        jump()
        walk("w", 1)
        jump()
        walk("w", 0.5)
        press("e")
        sleep(0.95)
        jump()
        sleep(8)
        jump()
        walk("w", 2)
        sleep(1)
        camera_rotate(158)
        walk("w", .9)

    def end(self):
        pass