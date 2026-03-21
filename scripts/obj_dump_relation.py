import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.objtools import get_obj_relations, get_obj_str


def parse_args():
    '''
    use argparser to the following args:
        -full: dump full relations, including Origin, Axes, Planes. Default is to skip them.
    '''
    import argparse
    parser = argparse.ArgumentParser(description="Dump object relations in FreeCAD document")
    # parser.add_argument('-full', action='store_true', help='Dump full relations, including Origin, Axes, Planes')
    
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

    for obj in sorted(objects, key=lambda x: x.Label):
        # print(get_obj_str(obj))
        get_obj_relations(obj, useLabel=True, printDetail=True)

if __name__ == "__main__":
    main()
