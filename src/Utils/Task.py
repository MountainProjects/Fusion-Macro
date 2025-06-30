import var
import os

class Task():
    def __init__(self, Macro):
        self.macro = Macro
        self.current = None

    def get(self):
        screen_lib = var.macro.screen
        
        if screen_lib.is_backpack_full():
            return "Convert"
        return "Farm"
    
    def set(self, task):
        self.current = task

        directory = os.fsencode("src/Tasks")
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = f"Paths.{filename[:-3]}"
                __import__(module_name, fromlist=[''])