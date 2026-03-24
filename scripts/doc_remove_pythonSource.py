import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.objtools import remove_obj_pythonSource

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
    
    objects = doc.Objects

    for obj in sorted(objects, key=lambda obj: obj.Label):
        print(f"Removing pythonSource from Label={obj.Label}, Name={obj.Name}, TypeId={obj.TypeId}")
        remove_obj_pythonSource(obj)
    doc.recompute()
    print(f"completed")

 

if __name__ == "__main__":
    main()
