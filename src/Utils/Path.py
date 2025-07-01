import os
import var

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

    def get_from_type(self, type=None):
        """
        Возвращает путь по типу хождения.
        """

        if not type:
            type = var.movementPath

        current_field = self.macro.interface.selectedField.get()
        if not current_field:
            raise ValueError("No field selected")
        
        field = self.macro.field.database.getByQuery({"name": current_field})
        if not field:
            raise ValueError(f"No field found for type '{type}'")
        
        field = field[0]
        for path in field.paths:
            if path["type"] == type:
                return self.macro.paths[path["id"]]
            
    def set_from_type(self, type=None):
        """
        Устанавливает путь по типу хождения.
        """

        if not type:
            type = var.movementPath

        current_field = self.macro.interface.selectedField.get()
        if not current_field:
            raise ValueError("No field selected")
        
        field = self.macro.field.database.getByQuery({"name": current_field})
        if not field:
            raise ValueError(f"No field found for type '{type}'")
        
        field = field[0]
        for path in field.paths:
            if path["type"] == type:
                self.set(path["id"])
                return

    def set(self, name=None):
        if not name:
            self.current = None
            return

        self.current = self.macro.paths[name]