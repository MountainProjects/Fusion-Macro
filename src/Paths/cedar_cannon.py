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

        camera_rotate(106)
        walk("w", 2.80032)
        jump()
        walk("w", 4.6656)
        walk("a", 0.046656)
        jump()
        walk("w", 3.03456)
        press("e")
        sleep(0.9)
        jump()
        sleep(8)
        jump()
        walk("w", 14.0068) 
        accuracy = check_image("src/assets/CorrectPos_Cedar.png", (555, 260, 10,10))
        if accuracy < 0.2:
            return False
        sleep(1)
        camera_rotate(158)
        walk("w", 4.204)
        return True


    def end(self):
        pass