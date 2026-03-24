import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.containertools import get_container_by_objName, get_LCS_map, get_LCS_prefixes
from cadcoder.objtools import get_obj_str


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="dump container LCS - Local Coordinate System")
    parser.add_argument('-debug', action='store_true', help='Enable debug output')
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
    
    # useLabel = not args.useName

    doc = App.ActiveDocument

    if doc is None:
        raise RuntimeError("No active document found")

    selection = Gui.Selection.getSelection()
    if selection:
        objects = selection
    else:
        objects = doc.Objects


    sorted_objects = sorted(objects, key=lambda o: o.Label)


    for container in sorted_objects:
        lcs_map = get_LCS_map(doc, container, debug=args.debug)
        print(f"LCS Map for Container: {get_obj_str(container)}")
        for prefix in get_LCS_prefixes():
            lcsObj = lcs_map[prefix]
            print(f"  {prefix}: {get_obj_str(lcsObj)}")
        print()

       

if __name__ == "__main__":
    main()
