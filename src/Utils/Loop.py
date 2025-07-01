import threading
import ctypes
import time

class Loop():
    def __init__(self, macro):
        self.macro = macro
        self.thread = None

        self.to_stop = False
        self.func = None
         
    def __call__(self):
        def decorator(func):
            self.func = func

        return decorator

    def start(self):
        if self.thread:
            self.stop()

        self.thread = threading.Thread(target=self.loop)
        self.thread.start()

    def stop(self):
        if not self.thread or not self.thread.is_alive():
            return

        self.to_stop = True

        if threading.current_thread() != self.thread:
            self._terminate(self.thread)

    def loop(self):
        while self.macro.started and not self.to_stop:
            self.func()

        self.to_stop = False
        self.thread = None

    def _terminate(self, thread):
        if not thread.is_alive():
            return
        
        tid = ctypes.c_long(thread.ident)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(SystemExit))

        if res == 0:
            raise ValueError("Invalid thread ID")
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")