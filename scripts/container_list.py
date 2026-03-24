import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.containertools import get_containers


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="list containers in FreeCAD document")
    # parser.add_argument('-full', action='store_true', help='Dump full relations, including Origin, Axes, Planes')
    # parser.add_argument('-useLabel', action='store_true', help='Use object Label instead of Name')
    
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
    
    # useLabel = not args.useName

    doc = App.ActiveDocument

    if doc is None:
        raise RuntimeError("No active document found")

    get_containers(doc, printDetail=True)

if __name__ == "__main__":
    main()
