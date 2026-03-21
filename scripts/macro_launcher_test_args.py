# dump command line arguments

import FreeCAD as App
import FreeCADGui as Gui
import sys
from pprint import pformat

print(f"Command line arguments={pformat(sys.argv)}")
