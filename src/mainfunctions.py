from utils import *
import paths
import patterns

def convert():
    walk("w", 1.1)
    press("e")
    while not is_backpack_empty():
        sleep(0.5)

    sleep(2)

    start_macro()
def start_macro():
    sleep(2)
    align()

    if is_backpack_full():
        convert()
        return

    paths.cedar_cannon()
    start_clicking()
    repeats = 0
    while True:
        if repeats == 5:
            repeats = 0
            patterns.cedar_default_realign()
            continue

        if is_backpack_full():
            align()
            convert()
            break
        patterns.cedar_default()
        repeats += 1