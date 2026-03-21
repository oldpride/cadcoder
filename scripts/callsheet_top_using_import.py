import re
import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.importtools import get_top_callsheets_using_import


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="get top-level callsheets using import info from pythonSource property")
    # optional -debug flag
    parser.add_argument('-debug', action='count', default=0, help='Enable debug output')
    # parser.add_argument('-un', '--useName', action='store_true', help='Use object names instead of labels')
    try:
        args = parser.parse_args()
        return args
    except SystemExit:
        return None
    
def main():
    args = parse_args()
    if not args:
        return
    
    # useLabel = not args.useName

    doc = App.ActiveDocument
    top_callsheets = get_top_callsheets_using_import(doc)
    print(f"top_callsheets:")
    for callsheet in top_callsheets:
        print(f"    Label={callsheet.Label}, Name={callsheet.Name}, TypeId={callsheet.TypeId}")

if __name__ == "__main__":
    main()
    
