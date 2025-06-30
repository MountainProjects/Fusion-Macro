from utils import *

def cedar_default():
    walk("w", 0.463)
    walk("a", 0.116)
    walk("s", 0.463)
    walk("a", 0.116)
    walk("w", 0.463)
    walk("a", 0.116)
    walk("s", 0.463)
    walk("a", 0.116)
    walk("w", 0.463)
    walk("d", 0.463)
    walk("s", 0.463)

def cedar_default_realign():
    walk("s", 2)
    sleep(0.5)
    walk("w", 0.925)