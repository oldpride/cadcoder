import FreeCAD as App
import FreeCADGui as Gui    
from cadcoder.importtools import compare_import_with_default


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="compare current import object's properties with default import object's properties")
    # parser.add_argument('docLabels', nargs='+', help='Document labels to compare')
    parser.add_argument('-ndiff', action='store_true', help='show not only difference. default is difference only')
    parser.add_argument('-comm', action='store_true', help='show common only')
    parser.add_argument('-si', action='store_true', help='skip import')
    parser.add_argument('-d', '-debug', '--debug', action='store_true', help='enable debug mode')
    parser.add_argument('-op', '--objLabelPattern', type=str, help='match obj labels to this pattern (regex)')
    parser.add_argument('-pp', '--propNamePattern', type=str, help='match propName to this pattern (regex)')
    parser.add_argument('-a', '--allObjects', action='store_true', help='compare all objects, if not set, only compare the selected object in the GUI')

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
    allObjects = args.allObjects
    
    doc = App.ActiveDocument

    if doc is None:
        raise RuntimeError("No active document found")
    
    result = compare_import_with_default(doc,
                                allObjects=allObjects,
                                diffOnly=not args.ndiff, 
                                commOnly=args.comm, skipImport=args.si, debug=args.debug, 
                                objLabelPattern=args.objLabelPattern,
                                propNamePattern=args.propNamePattern,
                                printDetail=True,
                                printExpOnly=True,
                                )
    
if __name__ == "__main__":
    main()
