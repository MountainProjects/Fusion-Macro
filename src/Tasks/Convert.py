from time import *
import var
import requests

webhook = "https://discord.com/api/webhooks/1390001812979060886/4BnQpkmeAwldCGqciUFiRcY6kqeHBDPESZmoW-a6cyAvFpV2jYVMwb-DnSxM1gFcMj_N"

@var.macro.task()
class TaskHandler():
    name = "Convert"
    def __init__(self):
        pass

    def start(self):
        movement_lib = var.macro.movement
        screen_lib = var.macro.screen

        movement_lib.move("a", 0.75)
        movement_lib.move("s", 0.85)
        movement_lib.tap_key("e")
        print("Converting...")
        while not screen_lib.is_backpack_empty():
            sleep(0.5)
        
        if not var.macro.started:
            return
        
        if var.loopStarted != 0:
            completed_in = time() - var.loopStarted
            print(f"Completed farm cycle in {completed_in}")
            var.loopStarted = 0

            payload = {
                "content": f"Цикл выполнен за {completed_in} секунд. ({completed_in/60} минут)"
            }

            requests.post(webhook, json=payload)
        sleep(2)