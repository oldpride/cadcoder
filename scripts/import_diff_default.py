import FreeCAD as App
import FreeCADGui as Gui    
from cadcoder.importtools import compare_import_with_default


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='show import condition of active document')
    # parser.add_argument('docLabels', nargs='+', help='Document labels to compare')
    parser.add_argument('-ndiff', action='store_true', help='show not only difference. default is difference only')
    parser.add_argument('-comm', action='store_true', help='show common only')
    parser.add_argument('-si', action='store_true', help='skip import')

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
    
    compare_import_with_default(doc, diffOnly=not args.ndiff, commOnly=args.comm, skipImport=args.si)

if __name__ == "__main__":
    main()
