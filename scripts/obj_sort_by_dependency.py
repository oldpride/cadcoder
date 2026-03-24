description = '''
order all or selected objects by downstream dependencies
'''

from pprint import pformat
import re
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.objtools import sort_objs_by_downstream


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description=description)
    # optional -debug flag
    parser.add_argument('-debug', action='count', default=0, help='Enable debug output')
    parser.add_argument('-un', '--useName', action='store_true', help='Use object names instead of labels')
    try:
        args = parser.parse_args()
        return args
    except SystemExit:
        return None
    
def main():
    args = parse_args()
    if not args:
        return
    
    useLabel = not args.useName

    doc = App.ActiveDocument

    result = sort_objs_by_downstream(doc, useLabel, debug=args.debug, printDetail=True)

if __name__ == "__main__":
    main()
    
