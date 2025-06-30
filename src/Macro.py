from Utils import Convert, Screen

class Macro():
    def path(self, name):
        def decorator(Path):
            return Path(self)

        return decorator

    def __init__(self):
        self.started = False
        self.paths = {}

        self.convert = Convert.Convert(self)
        self.screen = Screen.Screen(self)

    def start(self):
        print("я макросю")
        