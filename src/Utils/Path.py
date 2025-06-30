import os

class Path(): # https://cdn.discordapp.com/attachments/1254571495167098941/1313681768574091275/copy_84877E2E-E21A-463A-AA2D-A728D047E8FE.gif?ex=6863e5bc&is=6862943c&hm=f546bc786a746e31bc973262fd56d13602c58972343f781a950e482050d91378&
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
            Path.__bool__ = lambda self: self.current and self.current.name == Path.name

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
        self.current = None

    def set(self, name):
        if not name:
            raise ValueError("Path name cannot be empty")
        
        self.current = self.macro.paths[name]