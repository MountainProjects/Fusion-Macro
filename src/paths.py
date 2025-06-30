from utils import *

def cedar_cannon():
    camera_rotate(106)
    walk("w", 0.6)
    jump()
    walk("w", 1)
    jump()
    walk("w", 0.5)
    press("e")
    sleep(0.83)
    jump()
    sleep(8)
    jump()
    walk("w", 2)
    sleep(1)
    camera_rotate(158)
    walk("w", .9)
