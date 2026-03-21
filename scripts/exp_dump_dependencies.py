import re
import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.expressiontools import dump_all_upstream_expObjPropKeys, is_objProp_expression
from pdfclib.proptools import get_extended_propNames

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Dump selected objects' properties' expressions' upstream dependencies")
    # optional -debug flag
    parser.add_argument('-debug', action='count', default=0, help='Enable debug output')
    parser.add_argument('-un', '--useName', action='store_true', help='Use object names instead of labels')
    parser.add_argument('-ne', '--nonexpression', action='store_true', help='include non-expression properties')
    # Optional regex pattern to filter property names
    parser.add_argument('propPattern', nargs='?', default=None, help='Optional regex pattern to filter property names')
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
    selections = Gui.Selection.getSelection()

    if not selections:
        selections = sorted(doc.Objects, key=lambda o: o.Name)
    
    for obj in selections:
        print(f"Selected object Name={obj.Name}, TypeId={obj.TypeId}, Label={obj.Label}, useLabel={useLabel}")
        indent = '    '

        extPropList = sorted(get_extended_propNames(obj))
        print(f"{indent}Extended property list: {extPropList}")

        for propName in extPropList:
            if args.propPattern and re.search(args.propPattern, propName) is None:
                continue

            print(f"{indent}Extended Property: {propName}")
            dump_all_upstream_expObjPropKeys(doc, obj, propName, debug=args.debug, indentCount=1, useLabel=useLabel)
            print()

if __name__ == "__main__":
    main()
    
