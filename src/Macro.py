from Utils import Convert, Screen, Path, Movement, Task

class Macro():
    def __init__(self):
        self.started = False
        self.paths = {}

        self.path = Path.Path(self)
        self.convert = Convert.Convert(self)
        self.screen = Screen.Screen(self)
        self.movement = Movement.Movement(self)
        self.task = Task.Task(self)

    def start(self):
        self.path.start()

    def restart(self):
        self.path.end()
        self.movement.align_spawn()
        self.task.start()
        print(self.path.current)