# dump properties

from pdb import main
import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.objtools import print_obj
from pdfclib.subelementtools import update_obj_seName


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Dump edge info of a selected object",
        epilog="Example: edge_dump.py"
    )

    parser.add_argument(
        "sortBy",
        nargs="?",
        default='name',
        help="Sort edges by 'name', 'index', 'length', 'x', 'y', 'z', default is 'name'"
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
        selections = doc.Objects

    for sel in sorted(selections, key=lambda x: x.Label):
        print_obj(sel)
        update_obj_seName(sel)

if __name__ == "__main__":
    main()
