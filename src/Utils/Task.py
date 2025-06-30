import var
import os

class Task():
    def __init__(self, Macro):
        self.macro = Macro
        self.current = None
        self.tasks = {}

    def __call__(self):
        def decorator(Task):
            if not Task.name:
                raise ValueError("Task class must have a 'name' attribute")

            if Task.name in self.tasks:
                raise ValueError(f"Task with name '{Task.name}' already exists")
            
            Task.macro = self.macro
            Task.__repr__ = lambda self: f"<Macro Task '{Task.name}'>"
            Task.__str__ = lambda self: f"<Macro Task '{Task.name}'>"
            Task.__bool__ = lambda _: self.current and self.current.name == Task.name

            self.tasks[Task.name] = Task()
            return self.tasks[Task.name]

        return decorator
    
    def start(self):
        directory = os.fsencode("src/Tasks")
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = f"Tasks.{filename[:-3]}"
                __import__(module_name, fromlist=[''])

    def get(self):
        screen_lib = var.macro.screen
        
        if screen_lib.is_backpack_full():
            return "Convert"
        return "Farm"
    
    def set(self, task=None):
        task = task or self.get()
        print(self.tasks)
        try:
            self.tasks[task]
        except ValueError:
            raise ValueError(f"No task {task} in macro's tasks list.")
        self.current = task
        self.tasks[task].start()