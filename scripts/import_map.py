import FreeCAD as App
import FreeCADGui as Gui    
from cadcoder.importtools import map_importInfo


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='show import condition of active document')
    parser.add_argument('-topClassName', type=str, default=None, help='top class name')
    parser.add_argument('-kp', '--keyPattern', type=str, default=None, help='key pattern, eg, directlyImportedInstanceChains')
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
    
    map_importInfo(doc, topClassName=args.topClassName, keyPattern=args.keyPattern, printDetail=True)

if __name__ == "__main__":
    main()
