import FreeCAD as App
import FreeCADGui as Gui    
from cadcoder.importtools import compare_import_with_default_exp


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="compare current import object's expressions with default import object's expressions")
    # parser.add_argument('docLabels', nargs='+', help='Document labels to compare')
    parser.add_argument('-ndiff', action='store_true', help='show not only difference. default is difference only')
    parser.add_argument('-comm', action='store_true', help='show common only')
    # parser.add_argument('-si', action='store_true', help='skip import')
    parser.add_argument('-d', '-debug', '--debug', action='store_true', help='enable debug mode')
    parser.add_argument('-op', '--objLabelPattern', type=str, help='match obj labels to this pattern (regex)')
    parser.add_argument('-ep', '--expPattern', type=str, help='match expression to this pattern (regex)')

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
    
    doc = App.ActiveDocument

    if doc is None:
        raise RuntimeError("No active document found")
    
    selections = Gui.Selection.getSelection()
    if not selections:
        raise RuntimeError("No object selected. Please select an object to compare its expressions with the default import object's expressions.")
    
    if len(selections) > 1:
        raise RuntimeError("Multiple objects selected. Please select only one object.")
    
    obj = selections[0] # take the first selected object
    
    compare_import_with_default_exp(doc, 
                                    obj,
                                diffOnly=not args.ndiff, 
                                # diffOnly=False,
                                commOnly=args.comm, 
                                # skipImport=args.si, 
                                # debug=args.debug, 
                                objLabelPattern=args.objLabelPattern,
                                expPattern=args.expPattern,
                                )

if __name__ == "__main__":
    main()
