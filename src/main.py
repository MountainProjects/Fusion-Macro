import sys
import os

current_path = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.dirname(current_path)

sys.path.append(project_root)

from Macro import Macro
import var

var.macro = Macro()
var.macro.start()