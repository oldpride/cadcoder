import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.expressiontools import sort_objs_exp_dependency


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="dump selected objects' properties' expressions's dependency order")
    # optional -debug flag
    parser.add_argument('-debug', action='count', default=0, help='Enable debug output')
    parser.add_argument('-un', '--useName', action='store_true', help='Use object names instead of labels')
    try:
        args = parser.parse_args()
        return args
    except SystemExit:
        return None
    
def main():
    args = parse_args()
    if not args:
        return
    
    useLabel = not args.useName

    doc = App.ActiveDocument
    sort_objs_exp_dependency(doc, useLabel=useLabel, debug=args.debug, printDetail=True)

if __name__ == "__main__":
    main()
    
