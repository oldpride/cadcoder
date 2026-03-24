import FreeCAD as App
import FreeCADGui as Gui    
from cadcoder.importtools import fix_obj_import_callparam
from cadcoder.objtools import get_obj_str, skip_obj


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='fix import call parameters')
    parser.add_argument('-ic', '--ignoreClass', type=str, default=None, help='ignore class name, eg, Prism_polygon')
    # parser.add_argument('-topClassName', type=str, default=None, help='top class name')
    # parser.add_argument('-kp', '--keyPattern', type=str, default=None, help='key pattern, eg, directlyImportedInstanceChains')
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
    
    selection = Gui.Selection.getSelection()
    if not selection:
        selection = doc.Objects
    
    for obj in sorted(selection, key=lambda o: o.Label):
        print(get_obj_str(obj))
        if skip_obj(obj):
            print("  Skipped")
        else:
            fix_obj_import_callparam(doc, obj=obj, ignoreClass=args.ignoreClass, printDetail=True)
        print("")

if __name__ == "__main__":
    main()
