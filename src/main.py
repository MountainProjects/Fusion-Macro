import sys
import os
import time

from Macro import Macro
import var

current_path = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.dirname(current_path)

sys.path.append(project_root)

if __name__ == "__main__":
    var.macro = Macro()
    var.macro.initialize()