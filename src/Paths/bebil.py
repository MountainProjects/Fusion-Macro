import var

@var.macro.path()
class PathHandler:
    name = "bebil"

    def __init__(self):
        print(self)

    def start(self):
        var.macro.movement.walk("w", 2)
        pass

    def end(self):
        pass