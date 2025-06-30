import var
import os

class Task():
    def __init__(self, Macro):
        self.macro = Macro
        self.current = None
        self.tasks = {}

        directory = os.fsencode("src/Tasks")
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = f"Tasks.{filename[:-3]}"
                self.tasks[filename[:-3]] = __import__(module_name, fromlist=[''])

    def get(self):
        screen_lib = var.macro.screen
        
        if screen_lib.is_backpack_full():
            return "Convert"
        return "Farm"
    
    def start(self, task=None):
        task = task or self.get()
        print(self.tasks)
        try:
            self.tasks[task]
        except ValueError:
            raise ValueError(f"No task {task} in macro's tasks list.")
        self.current = task
        self.tasks[task].start()