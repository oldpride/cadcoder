import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.objtools import get_obj_all_downstreams


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Dump object relations in FreeCAD document")
    # parser.add_argument('-full', action='store_true', help='Dump full relations, including Origin, Axes, Planes')
    parser.add_argument('-useName', action='store_true', help='Use object Name instead of Label')
    
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
    
    useLabel = not args.useName

    doc = App.ActiveDocument

    if doc is None:
        raise RuntimeError("No active document found")

    selection = Gui.Selection.getSelection()
    if selection:
        objects = selection
    else:
        objects = doc.Objects

    # if useLabel:
    #     sorted_objects = sorted(objects, key=lambda o: o.Label)
    # else:
    #     sorted_objects = sorted(objects, key=lambda o: o.Name)

    sorted_objects = sorted(objects, key=lambda o: o.Label)

    i = 0
    for obj in sorted_objects:
        get_obj_all_downstreams(doc, obj, useLabel=useLabel, printDetail=True, prefix=str(i))
        print()
        i += 1

if __name__ == "__main__":
    main()
