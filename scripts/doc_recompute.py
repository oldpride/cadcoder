import FreeCAD as App
import FreeCADGui as Gui
import os
import sys

from cadcoder.objtools import recompute_doc

prog = os.path.basename(sys.argv[0])

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        description="recompute active document till all objects are not touched.",
        epilog=f'''Example: 
        {prog}
        {prog} -max 20
        '''
        )
    # parser.add_argument('-full', action='store_true', help='Dump full relations, including Origin, Axes, Planes')
    parser.add_argument('-max', '--max', type=int, default=10, help='max number of recomputes')
    parser.add_argument('-f', '--force', action='store_true', help='force a recompute even there is no touched object')
    parser.add_argument('-n', '--dryrun', action='store_true', help='dry run, do not actually recompute the document')

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
    
    recompute_doc(doc, max_recompute=args.max, force=args.force, dryrun=args.dryrun)

if __name__ == "__main__":
    main()
