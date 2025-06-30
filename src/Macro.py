from Utils import Convert, Screen, Path, Movement, Task, Interface
import threading

class Macro():
    def __init__(self):
        self.started = False
        self.thread = None
        self.paths = {}

        self.path = Path.Path(self)
        self.convert = Convert.Convert(self)
        self.screen = Screen.Screen(self)
        self.movement = Movement.Movement(self)
        self.task = Task.Task(self)
        self.interface = Interface.Interface(self)

    def start(self):
        self.task.start()
        self.path.start()
        self.interface.start()

    def loop(self):
        while self.started:
            print("гдр в дебри")

    def restart(self):
        if self.thread:
            #гдр не знает дебрей
            pass
        self.path.end()
        self.movement.align_spawn()
        self.task.set()
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()
        