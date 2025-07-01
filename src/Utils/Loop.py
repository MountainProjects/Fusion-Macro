import multiprocessing
import multiprocessing.process

class Loop():
    def __init__(self, macro):
        self.macro = macro
        self.process = None

        self.to_stop = False
        self.func = None
         
    def __call__(self):
        def decorator(func):
            self.func = func
            return func

        return decorator

    def start(self):
        if self.process:
            self.stop()

        self.process = multiprocessing.Process(target=self.func, args=())
        self.process.start()

    def stop(self):
        if not self.process or not self.process.is_alive():
            return

        self.process.terminate()
        self.process.join()
        self.process = None

    def loop(self):
        while self.macro.started:
            self.func()

        self.process = None