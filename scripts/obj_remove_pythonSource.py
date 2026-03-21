import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.objtools import get_target_objs, remove_obj_pythonSource

description='''
remove pythonSource from selected objects or all objects in the document
'''

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description=description)
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
    
    objects = get_target_objs(doc)

    for obj in objects:
        print(f"Removing pythonSource from {obj.Name}, Label={obj.Label}, TypeId={obj.TypeId}")
        remove_obj_pythonSource(obj)
    print(f"Removed pythonSource from {len(objects)} objects")

if __name__ == "__main__":
    main()
