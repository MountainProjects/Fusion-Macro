from time import *
import var

@var.macro.path()
class PathHandler:
    name = "cannon_default"

    def __init__(self):
        pass

    def start(self):
        camera_rotate = var.macro.movement.camera_rotate
        walk = var.macro.movement.move
        jump = var.macro.movement.jump

        camera_rotate(106)
        walk("w", 1.625)
        jump()
        walk("w", 2.7)
        walk("a", 0.027)
        jump()
        walk("w", 1.76)
        return True

    def end(self):
        pass
