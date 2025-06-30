from Utils import Convert, Screen, Path

class Macro():
    def __init__(self):
        self.started = False
        self.paths = {}
        self.current_path = None

        self.path = Path.Path(self)
        self.convert = Convert.Convert(self)
        self.screen = Screen.Screen(self)

    def start(self):
        self.path.start()
        print("я макросю")
        