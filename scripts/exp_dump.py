'''
dump some properties of the selected object

Usage:
    dump_prop_dependencies.py propPattern
'''

from pprint import pformat
import re
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.expressiontools import get_doc_all_expInfo, get_obj_all_expInfo

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Dump properties of the selected object.')
    # optional -debug flag
    parser.add_argument('-debug', action='count', default=0, help='Enable debug output')
    parser.add_argument('-un', '--useName', action='store_true', help='Use object names instead of labels')
    # Optional regex pattern to filter property names
    # parser.add_argument('propPattern', nargs='?', default=None, help='Optional regex pattern to filter property names')
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

    includeGrounded=True
    selection = Gui.Selection.getSelection()
    if not selection:
        expr_by_objProp = get_doc_all_expInfo(doc, useLabel=useLabel,
                                            includeGrounded=includeGrounded,
                                            )
        print(f"All expressions in document '{doc.Name}', useLabel={useLabel}:\n{pformat(expr_by_objProp)}")
    else:
        for obj in sorted(selection, key=lambda o: o.Label):
            expr_by_objProp = get_obj_all_expInfo(doc, obj, useLabel=useLabel,
                                                includeGrounded=includeGrounded,
                                                )
            print(f"Expressions for object '{obj.Name}', label={obj.Label}, useLabel={useLabel}, exps=\n{pformat(expr_by_objProp)}")

if __name__ == "__main__":
    main()
    
