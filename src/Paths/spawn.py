from time import *
import var

@var.macro.path()
class PathHandler:
    name = "spawn"

    def __init__(self):
        pass

    def start(self):
        walk = var.macro.movement.move

        walk("a", 0.75)
        walk("s", 4.15)

        return True

    def end(self):
        pass
