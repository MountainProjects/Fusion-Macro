from Utils import Convert, Screen, Path, Movement, Task, Interface, Loop, Pattern

class Macro():
    def __init__(self):
        self.started = False
        self.thread = None

        self.paths = {}
        self.tasks = {}
        self.patterns = {}

        self.path = Path.Path(self)
        self.convert = Convert.Convert(self)
        self.screen = Screen.Screen(self)
        self.movement = Movement.Movement(self)
        self.task = Task.Task(self)
        self.interface = Interface.Interface(self)
        self.loop = Loop.Loop(self)
        self.pattern = Pattern.Pattern(self)

        @self.loop()
        def main_loop():
            self.movement.correct()
            self.movement.align_spawn()
            self.task.set()

    def start(self):
        self.task.start()
        self.path.start()
        self.pattern.start()
        self.interface.start()

    def end(self):
        self.started = False
        self.path.end()
        self.loop.stop()

    def restart(self):
        self.end()
        self.started = True
        
        self.loop.start()
        