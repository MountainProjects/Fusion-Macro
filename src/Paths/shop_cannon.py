from time import *
import var

@var.macro.path()
class PathHandler:
    name = "shop_cannon"

    def __init__(self):
        pass

    def start(self):
        camera_rotate = var.macro.movement.camera_rotate
        walk = var.macro.movement.move
        jump = var.macro.movement.jump
        press = var.macro.movement.tap_key

        check_image = var.macro.screen.find_image_on_region

        var.macro.paths["cannon_default"].start()
        camera_rotate(150)
        press("e")
        
        sleep(1.5)

        jump()
        sleep(0.5)
        jump()
        sleep(0.2)
        jump()
        walk("w", 1.5)
        
        return True

    def end(self):
        pass
