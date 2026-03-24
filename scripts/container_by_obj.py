import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.containertools import get_container_by_objName
from cadcoder.objtools import get_obj_str


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="get container object by contained object")
    # parser.add_argument('-full', action='store_true', help='Dump full relations, including Origin, Axes, Planes')
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


    for obj in sorted_objects:
        container = get_container_by_objName(doc, obj.Name)
        print(f"Object: {get_obj_str(obj)}")       
        print(f"Container: {get_obj_str(container)}")
        print()
       

if __name__ == "__main__":
    main()
