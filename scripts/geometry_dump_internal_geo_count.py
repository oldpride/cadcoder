import re
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.geometrytools import get_obj_internalGeometry_count
import Part


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Dump selected Sketch object's geometry's internal")
    # optional -debug flag
    # parser.add_argument('-debug', action='count', default=0, help='Enable debug output')
    # parser.add_argument('-kp', '--keyPattern', action='store', default=None, help='Pattern to filter keys')
    try:
        args = parser.parse_args()
        return args
    except SystemExit:
        return None
    
def main():
    args = parse_args()
    if not args:
        return
    
    # useLabel = not args.useName

    doc = App.ActiveDocument

    selctions = Gui.Selection.getSelection()
    if not selctions:
        print("No object selected. Please select a Sketch object.")
        return

    for obj in selctions:
        if obj.TypeId != "Sketcher::SketchObject":
            print(f"Selected object {obj.Name} is not a Sketch object. Skipping.")
            continue
        get_obj_internalGeometry_count(obj, printDetail=True)

if __name__ == "__main__":
    main()
    
