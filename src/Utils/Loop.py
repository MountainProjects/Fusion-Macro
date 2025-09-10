import threading
import ctypes
import time

class Loop():
    def __init__(self, macro):
        self.macro = macro
        self.thread = None
        self.to_stop = False
        self.func = None
        self._lock = threading.Lock()
         
    def __call__(self):
        def decorator(func):
            self.func = func
            return func
        return decorator

    def start(self):
        with self._lock:
            if self.thread and self.thread.is_alive():
                print("Loop already running, skipping start")
                return

            self.to_stop = False
            self.thread = threading.Thread(target=self.loop, daemon=True)
            self.thread.start()
            print("Loop started")

    def stop(self):
        if threading.current_thread() == self.thread:
            print("Cannot stop loop from within the loop thread! Setting stop flag...")
            self.to_stop = True
            # ОБНУЛЯЕМ thread СРАЗУ
            self.thread = None
            return
            
        with self._lock:
            if not self.thread or not self.thread.is_alive():
                return

            print("Stopping loop...")
            self.to_stop = True
            
            if threading.current_thread() != self.thread:
                self.thread.join(timeout=2.0)
                
                if self.thread and self.thread.is_alive():
                    print("Force terminating loop thread...")
                    self._terminate(self.thread)
                
                self.thread = None
                print("Loop stopped")

    def loop(self):
        try:
            while self.macro.started and not self.to_stop:
                if self.func:
                    self.func()
                time.sleep(0.1)
        except Exception as e:
            print(f"Loop error: {e}")
        finally:
            self.to_stop = False
            self.thread = None
            print("Loop finished")

    def _terminate(self, thread):
        if not thread or not thread.is_alive():
            return
        
        try:
            tid = ctypes.c_long(thread.ident)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(SystemExit))
            
            if res == 0:
                print("Invalid thread ID for termination")
            elif res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                print("Thread termination failed")
        except Exception as e:
            print(f"Termination error: {e}")