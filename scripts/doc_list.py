import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.doctools import list_docs

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="List all open FreeCAD documents")
    # parser.add_argument('-full', action='store_true', help='Dump full relations, including Origin, Axes, Planes')
    # parser.add_argument('-useName', action='store_true', help='Use object Name instead of Label')
    
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
    
    list_docs()
 

if __name__ == "__main__":
    main()
