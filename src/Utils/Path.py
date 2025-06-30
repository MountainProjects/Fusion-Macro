import os

class Path():
    def __init__(self, macro):
        self.macro = macro

    def __call__(self):
        def decorator(Path):
            if not Path.name:
                raise ValueError("Path class must have a 'name' attribute")

            if Path.name in self.macro.paths:
                raise ValueError(f"Path with name '{Path.name}' already exists")
            
            Path.macro = self.macro
            Path.__repr__ = lambda self: f"<Macro Path '{Path.name}'>"
            Path.__str__ = lambda self: f"<Macro Path '{Path.name}'>"
            Path.__bool__ = lambda self: self.macro.current_path == Path.name

            self.macro.paths[Path.name] = Path()
            return self.macro.paths[Path.name]

        return decorator

    def start(self):
        directory = os.fsencode("src/Paths")
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = f"Paths.{filename[:-3]}"
                __import__(module_name, fromlist=[''])
    
    def set(self, name):
        if not name:
            raise ValueError("Path name cannot be empty")
        
        if name in self.macro.paths:
            raise ValueError(f"Path with name '{name}' already exists")
        
        self.macro.current_path = name