from multiprocessing.util import debug
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.doctools import diff_docs
import os

program = os.path.basename(__file__)
usage_help = f'''
usage: 
    {program} docLabel2    # compare active document with doc2
    {program} docLable1 docLabel2

compare two FreeCAD documents

if doc is not found in open documents, try to open from current working directory.

    -diff      show difference only
    -comm      show common only
    -si        skip import

'''


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="compare two FreeCAD documents")
    parser.add_argument('docLabels', nargs='+', help='Document labels to compare')
    parser.add_argument('-diff', action='store_true', help='show difference only')
    parser.add_argument('-comm', action='store_true', help='show common only')
    parser.add_argument('-si', action='store_true', help='skip import')   
    parser.add_argument('-debug', action='count', default=0, help='Enable debug output') 

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
    docLabels = args.docLabels

    if len(docLabels) == 1:
        doc1 = App.ActiveDocument
        if doc1 is None:
            raise RuntimeError("No active document found")
        docLabel2 = docLabels[0]
        if debug:
            print(f"searching doc Name or Label='{docLabel2}' among open documents...")
        doc2 = None
        for docName, doc in App.listDocuments().items():
            if docName == docLabel2 or doc.Label == docLabel2:
                doc2 = doc
                if debug:
                    print(f"found document: Name='{doc.Name}', Label='{doc.Label}'")
                break
            
        # doc2 = App.getDocument(docLabel2) if docLabel2 in App.listDocuments() else None
        if doc2 is None:
            # # try to open from current working directory
            # filepath2 = os.path.join(os.getcwd(), f"{docLabel2}.FCStd")

            # try to open from parts directory
            filepath2 = os.path.join(os.path.dirname(__file__), f"parts/{docLabel2}.FCStd")
            if os.path.exists(filepath2):
                print(f"Opening document from file: {filepath2}")
                doc2 = App.openDocument(filepath2)
            else:
                raise RuntimeError(f"Document '{docLabel2}' not found among open documents, and file '{filepath2}' does not exist.")
            
            # opening a new doc changes active document, therefore, we restore active document
            App.setActiveDocument(doc1.Name)
    
    else:
        docLabel1 = docLabels[0]
        docLabel2 = docLabels[1]
        doc1 = App.getDocument(docLabel1) if docLabel1 in App.listDocuments() else None
        if doc1 is None:
            # try to open from current working directory
            filepath1 = os.path.join(os.getcwd(), f"{docLabel1}.FCStd")
            if os.path.exists(filepath1):
                print(f"Opening document from file: {filepath1}")
                doc1 = App.openDocument(filepath1)
            else:
                raise RuntimeError(f"Document '{docLabel1}' not found among open documents, and file '{filepath1}' does not exist.")
        
        doc2 = App.getDocument(docLabel2) if docLabel2 in App.listDocuments() else None
        if doc2 is None:
            # try to open from current working directory
            filepath2 = os.path.join(os.getcwd(), f"{docLabel2}.FCStd")
            if os.path.exists(filepath2):
                print(f"Opening document from file: {filepath2}")
                doc2 = App.openDocument(filepath2)
            else:
                raise RuntimeError(f"Document '{docLabel2}' not found among open documents, and file '{filepath2}' does not exist.")

    diff_docs(doc1, doc2, diffOnly=args.diff, commOnly=args.comm, skipImport=args.si)

if __name__ == "__main__":
    main()
