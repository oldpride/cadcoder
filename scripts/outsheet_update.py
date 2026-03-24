# dump properties

from pdb import main
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.objtools import print_obj
from cadcoder.outsheettools import update_doc_outsheets


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Dump edge info of a selected object",
        epilog="Example: edge_dump.py"
    )

    parser.add_argument(
        "-l",
        "--link",
        action="store_true",
        help="Link outsheets after updating"
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

    update_doc_outsheets(doc, link=args.link)

if __name__ == "__main__":
    main()
