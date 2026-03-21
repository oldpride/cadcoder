# dump properties

from pdb import main
import re
import FreeCAD as App
import FreeCADGui as Gui
import os
import sys
from pdfclib.objtools import get_obj_str
from pdfclib.proptools import dump_obj_props


prog= os.path.basename(sys.argv[0])

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Dump attributes of selected FreeCAD object(s) in the active document",
        epilog=f"""Example: 
        {prog} 
        {prog} -m state
        """
    )

    parser.add_argument(
        "-match", "--match", type=str,
        default=None,
        help="Regex pattern to filter attribute names to dump, case-insensitive"
    )

    parser.add_argument(
        '-ip', '--includeProperities', action='store_true',
        help="Include properties in the dump. By default, only non-property attributes are dumped."
    )

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

    doc = App.ActiveDocument
    if doc is None:
        raise RuntimeError("No active document found")

    # get the selected object in the GUI
    selections = Gui.Selection.getSelection()
    if not selections:
        raise RuntimeError("No object selected")
    
    for sel in selections:
        print(get_obj_str(sel))
        
        for attr in dir(sel):
            if args.match and not re.search(args.match, attr, re.IGNORECASE):
                continue

            propNames = sel.PropertiesList
            if not args.includeProperities:
                if attr in propNames:
                    continue

            try:
                value = getattr(sel, attr)
            except Exception as e:
                value = f"<Error getting value: {e}>"
            print(f"{attr}: {value}")
            print()
if __name__ == "__main__":
    main()
