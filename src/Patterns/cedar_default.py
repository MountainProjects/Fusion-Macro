from time import *
import var

@var.macro.pattern()
class PatternHandler:
    name = "cedar_default"

    def __init__(self):
        self.realign_repeats = 5

    def pattern(self):
        walk = var.macro.movement.move

        walk("w", 0.463)
        walk("a", 0.116)
        walk("s", 0.463)
        walk("a", 0.116)
        walk("w", 0.463)
        walk("a", 0.116)
        walk("s", 0.463)
        walk("a", 0.116)
        walk("w", 0.463)
        walk("d", 0.463)
        walk("s", 0.463)

    def realign(self):
        walk = var.macro.movement.move
        
        walk("s", 2)
        sleep(0.5)
        walk("w", 0.925)