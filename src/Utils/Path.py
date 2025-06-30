import os

class Path():
    def __init__(self, macro):
        self.macro = macro
        self.current = None

    def __call__(self):
        def decorator(Path):
            if not Path.name:
                raise ValueError("Path class must have a 'name' attribute")

            if Path.name in self.macro.paths:
                raise ValueError(f"Path with name '{Path.name}' already exists")
            
            Path.macro = self.macro
            Path.__repr__ = lambda self: f"<Macro Path '{Path.name}'>"
            Path.__str__ = lambda self: f"<Macro Path '{Path.name}'>"
            Path.__bool__ = lambda _: self.current is not None and self.current.name == Path.name

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
    
    def end(self):
        if self.current is None:
            return
        
        self.current.end()

    def set(self, name=None):
        if not name:
            self.current = None
            return

        self.current = self.macro.paths[name]