from Utils import Convert, Screen, Path, Movement

class Macro():
    def __init__(self):
        self.started = False
        self.paths = {}
        self.current_path = None

        self.path = Path.Path(self)
        self.convert = Convert.Convert(self)
        self.screen = Screen.Screen(self)
        self.movement = Movement.Movement(self)

    def get_path(self):
        return self.paths[self.current_path]

    def start(self):
        self.path.start()

    def reset_path(self):
        if self.current_path is None:
            raise ValueError("No path is currently set.")
        
        self.paths[self.current_path].end()
        self.current_path = None
        
    def restart(self):
        print("сделать бебильно тут чтоб рестарт был")
        print(self.current_path)