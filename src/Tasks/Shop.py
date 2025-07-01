import var
from time import *

@var.macro.task()
class TaskHandler():
    name = "Shop"

    def __init__(self):
        pass

    def start(self):
        
        
        result = var.macro.paths["shop_cannon"].start() ## TODO shop_cannon -> var.stock.current_path

        if not result:
            print("Farm path failed, restarting...")
            var.macro.restart()
            return
        
        var.macro.movement.tap_key("e")
        sleep(0.5)
        for i in range(10):
            ## TODO GET_CURRENT_STOCK_ITEM on screen
            ## TODO IF ITEM IN SETTINGS: BUY ITEM (SCREEN CLICK)
            sleep(0.8)

        var.macro.movement.tap_key("e")
        sleep(0.5)
        