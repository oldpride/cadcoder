import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.objtools import get_obj_shape


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Dump object shape information")
    
    try:
        args = parser.parse_args()
        return args
    except SystemExit:
        print("Argument parsing failed.")
        return None
    
def main():
    args = parse_args()
    if args is None:
        return

    doc = App.ActiveDocument

    if doc is None:
        raise RuntimeError("No active document found")

    selection = Gui.Selection.getSelection()
    if selection:
        objects = selection
    else:
        objects = doc.Objects

    for obj in objects:
        get_obj_shape(obj, printDetail=True)

if __name__ == "__main__":
    main()
