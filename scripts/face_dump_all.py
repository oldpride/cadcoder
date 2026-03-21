# dump properties

from pdb import main
import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.subelementtools import dump_all_seNames


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Dump face info of a selected object",
        epilog="Example: face_dump.py"
    )

    parser.add_argument(
        "sortBy",
        nargs="?",
        default='name',
        help="Sort faces by 'name', 'index', 'area', 'x', 'y', 'z', default is 'name'"
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
        print(f"name={sel.Name}, label={sel.Label}, typeId={sel.TypeId}")
        dump_all_seNames(sel, seType='Face', by=args.sortBy)

if __name__ == "__main__":
    main()
