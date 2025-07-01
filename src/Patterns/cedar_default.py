from time import *
import var

#SETTINGS:
w_duration = 2.16
side_duration = 0.5616

repeats = 3

@var.macro.pattern()
class PatternHandler:
    name = "cedar_default"

    def __init__(self):
        self.realign_repeats = 5

    def pattern(self):
        walk = var.macro.movement.move

        for i in range(repeats):
            walk("w", w_duration)
            walk("a", side_duration)
            walk("s", w_duration)
            walk("a", side_duration)
        walk("d", side_duration * repeats * 2)

    def realign(self):
        walk = var.macro.movement.move
        
        walk("s", 9.3)
        sleep(0.5)
        walk("w", 2.04)