import var

@var.macro.task()
class TaskHandler():
    name = "Farm"

    def __init__(self):
        pass

    def start(self):
        current_path = var.macro.path.current
        if not current_path:
            return
        
        result = current_path.start()
        if not result:
            print("Farm path failed, restarting...")
            var.macro.restart()
            return
        
        print("Starting farm...")
        var.macro.movement.hold_mouse()
        var.macro.pattern.set("cedar_default")
        var.macro.pattern.run_current()