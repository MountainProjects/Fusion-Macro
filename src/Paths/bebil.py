import var

@var.macro.path()
class PathHandler:
    name = "bebil"

    def __init__(self):
        print(self)

    def start(self):
        movement = var.macro.movement
        movement.walk("w", 4) # Бебильная ходьба нахрен!!!!!!!