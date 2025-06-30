import var

@var.macro.path()
class PathHandler:
    name = "bebil"

    def __init__(self):
        print(self)

    def start(self):
        var.macro.movement.move("w", 2)
        pass

    def end(self):
        pass