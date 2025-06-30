import os
import var

class Pattern():
    def __init__(self, macro):
        self.macro = macro
        self.current = None

    def __call__(self):
        def decorator(Pattern):
            if not Pattern.name:
                raise ValueError("Pattern class must have a 'name' attribute")

            if Pattern.name in self.macro.paths:
                raise ValueError(f"Pattern with name '{Pattern.name}' already exists")
            
            Pattern.macro = self.macro
            Pattern.__repr__ = lambda self: f"<Macro Path '{Pattern.name}'>"
            Pattern.__str__ = lambda self: f"<Macro Path '{Pattern.name}'>"
            Pattern.__bool__ = lambda _: self.current is not None and self.current.name == Pattern.name

            self.macro.patterns[Pattern.name] = Pattern()
            return self.macro.patterns[Pattern.name]

        return decorator

    def start(self):
        directory = os.fsencode("src/Patterns")
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = f"Patterns.{filename[:-3]}"
                __import__(module_name, fromlist=[''])
    
    def end(self):
        if self.current is None:
            return
        
        self.current.end()

    def set(self, name=None):
        if not name:
            self.current = None
            return

        self.current = self.macro.patterns[name]

    def run_current(self):
        screen = var.macro.screen

        repeats = 0

        print("РАНЮ ПАТЕРН")

        while not screen.is_backpack_full():
            print("НЕ ЗАПОЛНИЛСЯ Я ЕЩЕ")
            if repeats >= self.current.realign_repeats:
                print("РЕ АЛАЙНЮСЬ А ТО ПИЗДА БУДЕТ")
                repeats = 0
                self.current.realign()
                continue
            self.current.pattern()
            print("ИДУ ПО ПАТЕРНУ")
            repeats += 1
