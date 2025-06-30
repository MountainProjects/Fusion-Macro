from time import *
import var

@var.macro.path()
class PathHandler:
    name = "cedar_cannon"

    def __init__(self):
        print(self)

    def start(self):
        camera_rotate = var.macro.movement.camera_rotate
        walk = var.macro.movement.move
        jump = var.macro.movement.jump
        press = var.macro.movement.tap_key

        check_image = var.macro.screen.find_image_on_region

        camera_rotate(106)
        walk("w", 0.6)
        jump()
        walk("w", 1)
        jump()
        walk("w", 0.5)
        press("e")
        sleep(0.95)
        jump()
        sleep(8)
        jump()
        walk("w", 2)
        accuracy = check_image("src/assets/CorrectPos_Cedar.png", (555, 260, 10,10))
        if accuracy < 0.5:
            return False
        sleep(1)
        camera_rotate(158)
        walk("w", .9)
        return True

    def end(self):
        pass