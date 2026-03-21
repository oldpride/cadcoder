import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.objtools import get_doc_top_objects, print_obj_info


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="list top objects in FreeCAD document")
    
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
    if selection:
        objects = selection
    else:
        objects = doc.Objects

    top_objects = get_doc_top_objects(doc)
    print(f"Top-level objects in document '{doc.Name}':")
    for obj in top_objects:
        print_obj_info(obj)

if __name__ == "__main__":
    main()
