# dump properties

import os
from pdb import main
import sys
import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.scaletools import scale_clone


prog= os.path.basename(sys.argv[0])

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="scale a selected object",
        epilog=f"""
Example: 
    {prog} basf
    {prog} 1.1,1.1,1.3
    {prog} list
"""
    )

    parser.add_argument(
        "key_pattern",
        nargs="?",
        default=None,
        help=""
    )

    parser.add_argument(
        "-stl", "--export_stl", action="store_true",
        help="Export the scaled object to STL format in the same directory as the FreeCAD document"
    )

    # parser.add_argument(
    #     "-ep", "--extendedProperty", action="store_true",
    #     help="include extended properties (spreadsheet alias, sketch constrait) to dump."
    # )

    # parser.add_argument(
    #     "-un", "--useName", action="store_true",
    #     help="Use object names instead of labels"
    # )

    try:
        args = parser.parse_args()
    except Exception as e:
        print(f"Error parsing arguments: {e}")
        return None

    return args

def main():
    args = parse_args()

    if not args:
        return
    
    if args.key_pattern is None:
        print("key_pattern is required argument.")
        return

    doc = App.ActiveDocument
    if doc is None:
        raise RuntimeError("No active document found")

    # get the selected object in the GUI
    selections = Gui.Selection.getSelection()
    if not selections:
        raise RuntimeError("No object selected")

    if len(selections) > 1:
        raise RuntimeError("Multiple objects selected. Please select only one object to scale.")
    
    obj = selections[0]
    scale_clone(obj, args.key_pattern, export_stl=args.export_stl)

if __name__ == "__main__":
    main()
