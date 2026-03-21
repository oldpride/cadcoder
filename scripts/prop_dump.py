# dump properties

from pdb import main
import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.proptools import dump_obj_props

'''
optional positional argument:
    prop name pattern (regex) to filter properties to dump
'''

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Dump properties of selected FreeCAD object(s) in the active document",
        epilog="Example: dump_props.py ^Placement$"
    )

    parser.add_argument(
        "propPattern",
        nargs="?",
        default=None,
        help="Regex pattern to filter property names to dump"
    )

    parser.add_argument(
        "-ea", "--extraAttrs", type=str,
        default=None,
        help="List of extra attributes to dump, eg, -ea Expression,dir"
    )

    parser.add_argument(
        "-ep", "--extendedProperty", action="store_true",
        help="include extended properties (spreadsheet alias, sketch constrait) to dump."
    )

    parser.add_argument(
        "-un", "--useName", action="store_true",
        help="Use object names instead of labels"
    )

    try:
        args = parser.parse_args()
    except Exception as e:
        print(f"Error parsing arguments: {e}")
        return None

    return args

def main():
    args = parse_args()
    useLabel = not args.useName

    if not args:
        return

    doc = App.ActiveDocument
    if doc is None:
        raise RuntimeError("No active document found")

    # get the selected object in the GUI
    selections = Gui.Selection.getSelection()
    if not selections:
        raise RuntimeError("No object selected")

    for sel in selections:
        print("--------------------------------------")
        dump_obj_props(doc, sel, useLabel, 
                       propPattern=args.propPattern, 
                       extraAttrs=args.extraAttrs,
                       extended=args.extendedProperty,
                       )

if __name__ == "__main__":
    main()
