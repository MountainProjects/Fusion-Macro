import sys
import os

current_path = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.dirname(current_path)

sys.path.append(project_root)

from Macro import Macro

macro = Macro()
macro.start()

@macro.path(name="bebil")
class bebil:
    def __init__(self, Macro):
        print("bebil started", self, Macro)