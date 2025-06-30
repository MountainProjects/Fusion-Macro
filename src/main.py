import sys
import os

from Macro import Macro
import var

current_path = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.dirname(current_path)

sys.path.append(project_root)

var.macro = Macro()
var.macro.start()

var.macro.path.set("bebil")
var.macro.restart()
