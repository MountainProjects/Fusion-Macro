import var


@var.macro.task()
class TaskHandler():
    name = "Farm"

    def __init__(self):
        pass

    def start(self):
        print(self.macro.paths)
        current_path = self.macro.paths['cedar_cannon']
        if current_path is None:
            print("No path.")
            return
        
        result = current_path.start()
        if not result:
            print("Farm path failed, restarting...")
            var.macro.restart()
            return
        
        print("Starting farm...")
        var.macro.movement.hold_mouse()
        #var.macro.pattern.set(var.macro.pattern.current)
        var.macro.pattern.run_current()