# dump properties

from pdb import main
from pprint import pformat
import traceback
import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.subelementtools import dump_pos


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Dump edge info of a selected object",
        epilog="Example: edge_dump.py"
    )

    # parser.add_argument(
    #     "edgePattern",
    #     nargs="?",
    #     default=None,
    #     help="Regex pattern to filter edge pos names to dump"
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

    doc = App.ActiveDocument
    if doc is None:
        raise RuntimeError("No active document found")

    # get the selected object in the GUI
    selections = Gui.Selection.getSelection()
    if not selections:
        raise RuntimeError("No object selected")

    dump_pos('Face', selections)
           

if __name__ == "__main__":
    main()
