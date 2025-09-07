from Utils import Screen, Path, Movement, Task, Interface, Loop, Pattern, Field
import win32gui
from pynput.keyboard import Listener
import var

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
        try:
            hwnd = win32gui.GetForegroundWindow()
            if not hwnd:
                return False

            if not win32gui.IsWindowVisible(hwnd) or not win32gui.IsWindowEnabled(hwnd):
                return False

            title = win32gui.GetWindowText(hwnd)

            return title == "Roblox"
        except Exception as e:
            print(f"[Window Check Failed] {e}")
            return False

    def start(self):
        var.loopStarted = 0
        self.field.start()
        self.task.start()
        self.path.start()
        self.pattern.start()
        self.interface.start()

    def end(self):
        self.started = False
        
        self.movement.stop_movement()
        self.movement.release_mouse()

        self.path.end()
        self.loop.stop()

    def restart(self):
        self.end()
        self.started = True
        
        self.loop.start()
        