description = '''
dump selected objects' properties' expressions's dependency order
'''

import re
import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.importtools import map_importInfo


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description=description)
    # optional -debug flag
    # parser.add_argument('-debug', action='count', default=0, help='Enable debug output')
    parser.add_argument('-kp', '--keyPattern', action='store', default=None, help='Pattern to filter keys')
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
    map_importInfo(doc, keyPattern=args.keyPattern, printDetail=True)

if __name__ == "__main__":
    main()
    
