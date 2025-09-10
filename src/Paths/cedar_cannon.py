from time import *
import var

@var.macro.path()
class PathHandler:
    name = "cedar_cannon"

    def __init__(self):
        pass

    def start(self):
        camera_rotate = var.macro.movement.camera_rotate
        walk = var.macro.movement.move
        jump = var.macro.movement.jump
        press = var.macro.movement.tap_key

        check_image = var.macro.screen.find_image_on_region

        var.macro.paths["spawn"].start()
        var.macro.paths["cannon_default"].start()
        press("e")
        sleep(0.83)

        jump()
        sleep(8)
        jump()
        walk("w", 0.624)
        walk("a", 0.3)
        walk("w", 7.5)
        accuracy = check_image("src/assets/CorrectPos_Cedar.png", (555, 260, 10,10))
        if accuracy < 0.2:
            return False
        sleep(1)
        camera_rotate(158)
        walk("w", 2.4)
        sleep(0.3)
        return True

    def end(self):
        pass
