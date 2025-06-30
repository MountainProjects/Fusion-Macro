import var

class Farm():
    def __init__(self):
        pass

    def start(self):
        current_path = var.macro.path.current
        if not current_path:
            return
        
        current_path.start()