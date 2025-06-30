import threading

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

    def stop(self, in_the_thread=False):
        if not self.thread or not self.thread.is_alive():
            return

        self.to_stop = True

        if not in_the_thread:
            self.thread.join()

    def loop(self):
        while self.macro.started and not self.to_stop:
            self.func()

        self.to_stop = False
        self.thread = None