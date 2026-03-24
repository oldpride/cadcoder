import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.objtools import expand_objects

description='''
expand selected objects into all downstream objects so that 
they are self-contained set of objects.
we can then export them together.
'''

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description=description)
    # parser.add_argument('-full', action='store_true', help='Dump full relations, including Origin, Axes, Planes')
    parser.add_argument('-useName', action='store_true', help='Use object Name instead of Label')
    
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
    
    useLabel = not args.useName

    doc = App.ActiveDocument

    if doc is None:
        raise RuntimeError("No active document found")
    
    expand_objects(doc, useLabel, printDetail=True)

if __name__ == "__main__":
    main()
