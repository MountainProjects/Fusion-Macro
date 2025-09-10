from Utils import Screen, Path, Movement, Task, Interface, Loop, Pattern, Field
import win32gui
from pynput.keyboard import Listener
import var
import time
import traceback

class Macro():
    def __init__(self):
        self.started = False
        self.thread = None
        self.is_restarting = False 

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
                time.sleep(1)
                return

            self.movement.align_spawn()
            self.task.set()
            time.sleep(0.5)

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

    def initialize(self):
        self.field.start()
        self.task.start() 
        self.path.start()
        self.pattern.start()
        self.interface.start()
        self.screen.start_speed_thread()

    def start(self): 
        print("Starting macro...")
        self.started = True
        var.loopStarted = 0
        self.loop.start()
        print("Macro started!")

    def end(self):
        if not self.started:
            return
            
        self.started = False
        self.movement.stop_movement()
        self.movement.release_mouse()
        self.loop.stop()
        print("Macro stopped!")

    def restart(self):
        if self.is_restarting:
            print("Already restarting, skipping...")
            return
            
        self.is_restarting = True
        try:
            print("Restarting macro...")
            self.end()
            time.sleep(2)
            self.start()
        finally:
            self.is_restarting = False
        