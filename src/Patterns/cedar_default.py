from time import *
import var

#SETTINGS:
w_duration = 1.253
side_duration = 0.275

repeats = 3

@var.macro.pattern()
class PatternHandler:
    name = "cedar_default"

    def __init__(self):
        self.realign_repeats = 6

    def pattern(self):
        walk = var.macro.movement.move

        for i in range(repeats):
            walk("w", w_duration)
            walk("a", side_duration)
            walk("s", w_duration)
            walk("a", side_duration)
            
        walk("d", side_duration * (repeats * 2))

    def realign(self):
        walk = var.macro.movement.move
        
        walk("s", 5)
        sleep(0.5)
        walk("a", 0.5)
        sleep(0.2)
        walk("s", 4)
        walk("w", 2.4)