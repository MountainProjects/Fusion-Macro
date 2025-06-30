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

    def start(self):
        self.path.start()
        self.movement.reset_character() # А ВОТ ВСЕ РЕЗЕТАЮ ТЕБЯ
        