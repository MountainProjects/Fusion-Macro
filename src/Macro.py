from Utils import Screen, Path, Movement, Task, Interface, Loop, Pattern, Field
import win32gui

class Macro():
    def __init__(self):
        self.started = False
        self.thread = None

        self.paths = {}
        self.tasks = {}
        self.patterns = {}
        self.fields = {}

        self.path = Path.Path(self)
        self.screen = Screen.Screen(self)
        self.movement = Movement.Movement(self)
        self.task = Task.Task(self)
        self.interface = Interface.Interface(self)
        self.loop = Loop.Loop(self)
        self.pattern = Pattern.Pattern(self)
        self.field = Field.Field(self)

        @self.loop()
        def main_loop():
            if not self.IsRobloxFocused():
                return

            self.movement.align_spawn()
            self.task.set()

    def IsRobloxFocused(self) -> bool:
        hwnd = win32gui.GetForegroundWindow()
        class_name = win32gui.GetClassName(hwnd)
        return class_name == "Roblox"

    def start(self):
        self.field.start()
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
        