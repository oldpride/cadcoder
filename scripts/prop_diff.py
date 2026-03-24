usage = '''
find the difference in properties between 2 selected objects

if no document is specified, 
    if 2 two objects are specified on the command line, 
        search the active document first, for the two objects.
        for any object not found in the active document, 
            we search all open documents in order of document name.
        the two objects can be spefied by their name patterns (regex).
        eg: -obj1 Pad -obj2 Pad001
    if no objects are specified,
        we expect exactly 2 objects selected across all open documents in tree view.
            note: App.Gui.Selection.getSelection() only returns unique object names,
                  therefore, if 2 objects with the same name are selected in different documents,
                  only one of them will be returned - name overlapping.
        therefore, if App.Gui.Selection.getSelection() only returns 1 object, we will try
            to find the other object by looking for the same name in other open documents.
        if more than 2 objects are selected, an error is raised.

if two document names are specified on the command line, 
    they are specified by their name patterns (regex).
    eg: -doc1  test.* -doc2 Unamed.*

    if no objects are specified on command line, 
        we expect one selected object in each document in tree view.
    if two objects are specified on command line,
        we find each of them in the corresponding document.

if other number of documents or objects are specified on the command line, an error is raised.
'''

from pprint import pformat
import re
from typing import Tuple, Union
import FreeCAD as App
from cadcoder.proptools import diff_obj_props
import argparse

def find_object_in_doc_by_objNamePattern(doc, name_pattern):
    pattern = re.compile(name_pattern, re.IGNORECASE)
    objects = sorted(doc.Objects, key=lambda x: x.Name)
    for obj in objects:
        if pattern.search(obj.Name):
            return obj
    return None

def find_object_in_doc_by_labelPattern(doc, label_pattern):
    pattern = re.compile(label_pattern, re.IGNORECASE)
    objects = sorted(doc.Objects, key=lambda x: x.Name)
    for obj in objects:
        if pattern.search(obj.Label):
            return obj
    return None

'''
if no document is specified, 
    if no objects are specified,
        we expect exactly 2 objects selected across all open documents in tree view.
            note: App.Gui.Selection.getSelection() only returns unique object names,
                  therefore, if 2 objects with the same name are selected in different documents,
                  only one of them will be returned - name overlapping.
        therefore, if App.Gui.Selection.getSelection() only returns 1 object, we will try
            to find the other object by looking for the same name in other open documents.
'''

def find_selected_objs_without_specified_docs() -> Union[None, Tuple[App.DocumentObject, App.DocumentObject]]:
    selections = App.Gui.Selection.getSelection()
    print(f"Selections: {[sel.Label + ' in ' + sel.Document.Label for sel in sorted(selections, key=lambda x: x.Label)]}")

    if len(selections) == 0:
        return None
    
    if len(selections) == 1:
        '''
        If we select 1 object in 2 different documents in 3D view, 
        and if the object has the same name,
        the selection will only contain one of them, because
        App.Gui.Selection.getSelection() returns a list of unique names.
        '''
        sel1 = selections[0]
        sel2 = None

        sel1Name = sel1.Name
        sel1Label = sel1.Label
        if sel1Name: # awlays true. 
            for doc in sorted(App.listDocuments().values(), key=lambda x: x.Name):
                if doc.Name != sel1.Document.Name:
                    obj = find_object_in_doc_by_objNamePattern(doc, f"^{re.escape(sel1Name)}$")
                    # obj = find_object_in_doc(doc, f"^{sel1.Name}$")
                    if obj is not None:
                        sel2 = obj
                        break
        if sel2 is None:
            # try finding by Label
            for doc in sorted(App.listDocuments().values(), key=lambda x: x.Name):
                if doc.Name != sel1.Document.Name:
                    obj = find_object_in_doc_by_labelPattern(doc, f"^{re.escape(sel1Label)}$")
                    if obj is not None:
                        print("Found matching object by Label:", obj.Name, "in document", doc.Name)
                        sel2 = obj
                        break
        if sel2 is None:
            print("Only one object selected, and no matching object found in other documents.")
            return None
        return (sel1, sel2)
    
    if len(selections) == 2:
        return (selections[0], selections[1])
    
    print("More than 2 objects selected. Please select exactly 2 objects.")
    return None

'''
if no document is specified, 
    if 2 two objects are specified on the command line, 
        search the active document first, for the two objects.
        for any object not found in the active document, 
            we search all open documents in order of document name.
        the two objects can be spefied by their name patterns (regex).
        eg: -obj1 Pad -obj2 Pad001
'''
def find_specified_objs_without_specfied_docs(
        obj1_name_pattern: str, 
        obj2_name_pattern: str
        ) -> Union[None, Tuple[App.DocumentObject, App.DocumentObject]]:
    activeDoc = App.ActiveDocument
    obj1 = find_object_in_doc_by_objNamePattern(activeDoc, obj1_name_pattern)
    obj2 = find_object_in_doc_by_objNamePattern(activeDoc, obj2_name_pattern)

    openDocs = sorted(App.listDocuments().values(), key=lambda x: x.Name)
    if obj1 is None:
        for d in openDocs:
            if d.Name != activeDoc.Name:
                obj1 = find_object_in_doc_by_objNamePattern(d, obj1_name_pattern)
                if obj1 is not None:
                    break

    if obj2 is None:
        for d in openDocs:
            if d.Name != activeDoc.Name:
                obj2 = find_object_in_doc_by_objNamePattern(d, obj2_name_pattern)
                if obj2 is not None:
                    break

    if obj1 is None or obj2 is None:
        return None

    return (obj1, obj2)

'''
if two document names are specified on the command line, 
    they are specified by their name patterns (regex).
    eg: -doc1  test.* -doc2 Unamed.*

    if no objects are specified on command line, 
        we expect one selected object in each document in tree view.

'''
def find_selected_objs_in_specified_docs(
        doc1_name_pattern: str, 
        doc2_name_pattern: str
        ) -> Union[None, Tuple[App.DocumentObject, App.DocumentObject]]:
    obj1 = None
    obj2 = None

    # because selection's name overlapping, the mapping from doc name to document is 1-to-many,
    selections = App.Gui.Selection.getSelection()
    openDocs = sorted(App.listDocuments().values(), key=lambda x: x.Name)

    # find the two documents
    for sel in selections:
        for doc in openDocs:
            if obj1 is None:
                if re.search(doc1_name_pattern, doc.Name, re.IGNORECASE):
                    if doc.getObject(sel.Name) is not None:
                        obj1 = sel
            if obj2 is None:
                if re.search(doc2_name_pattern, doc.Name, re.IGNORECASE):
                    if doc.getObject(sel.Name) is not None:
                        obj2 = sel

            if obj1 is not None and obj2 is not None:
                return (obj1, obj2)

'''
if two document names are specified on the command line, 
    they are specified by their name patterns (regex).
    eg: -doc1  test.* -doc2 Unamed.*

    if two objects are specified on command line,
        we find each of them in the corresponding document.
'''

def find_specified_objs_in_specified_docs(
        doc1_name_pattern: str, 
        doc2_name_pattern: str, 
        obj1_name_pattern: str, 
        obj2_name_pattern: str) -> Union[None, Tuple[App.DocumentObject, App.DocumentObject]]:
    obj1 = None
    obj2 = None

    openDocs = sorted(App.listDocuments().values(), key=lambda x: x.Name)

    # find obj1 in doc1
    for doc in openDocs:
        if re.search(doc1_name_pattern, doc.Name, re.IGNORECASE):
            obj1 = find_object_in_doc_by_objNamePattern(doc, obj1_name_pattern)
            if obj1 is not None:
                break

    # find obj2 in doc2
    for doc in openDocs:
        if re.search(doc2_name_pattern, doc.Name, re.IGNORECASE):
            obj2 = find_object_in_doc_by_objNamePattern(doc, obj2_name_pattern)
            if obj2 is not None:
                break

    if obj1 is None or obj2 is None:
        return None

    return (obj1, obj2)

def parse_args():
    parser = argparse.ArgumentParser(description=usage, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-doc1", type=str, help="name pattern (regex) of document 1")
    parser.add_argument("-doc2", type=str, help="name pattern (regex) of document 2")
    parser.add_argument("-obj1", type=str, help="name pattern (regex) of object 1")
    parser.add_argument("-obj2", type=str, help="name pattern (regex) of object 2")
    
    # propPattern is a positional argument
    parser.add_argument("propPattern", nargs="?", default=None, help="name pattern (regex) of property")

    # parse_args can call exit() which will terminate the whole FreeCAD process.
    # therefore, we catch SystemExit exception here.
    try:
        args = parser.parse_args()
    except SystemExit:
        print("Argument parsing error.")
        return None
    return args

def main():
    args = parse_args()

    if args is None:
        return

    doc1_pattern = args.doc1
    doc2_pattern = args.doc2
    obj1_pattern = args.obj1
    obj2_pattern = args.obj2
    propPattern = args.propPattern

    # docs and objects must come in pairs
    if (doc1_pattern is None) != (doc2_pattern is None):
        print("Both document patterns must be specified.")
        return
    if (obj1_pattern is None) != (obj2_pattern is None):
        print("Both object patterns must be specified.")
        return

    obj_pair = None

    if doc1_pattern is None and doc2_pattern is None:
        # no documents specified
        if obj1_pattern is None and obj2_pattern is None:
            # no objects specified
            obj_pair = find_selected_objs_without_specified_docs()
        else:
            # 2 objects specified
            obj_pair = find_specified_objs_without_specfied_docs(obj1_pattern, obj2_pattern)
    else:
        # 2 documents specified
        if obj1_pattern is None and obj2_pattern is None:
            # no objects specified
            obj_pair = find_selected_objs_in_specified_docs(doc1_pattern, doc2_pattern)
        else:
            # 2 objects specified
            obj_pair = find_specified_objs_in_specified_docs(doc1_pattern, doc2_pattern, obj1_pattern, obj2_pattern)

    if obj_pair is None:
        print("Could not find the two specified objects.")
        return

    obj1, obj2 = obj_pair
    doc1 = obj1.Document
    doc2 = obj2.Document
    print(f"Comparing obj.Label='{obj1.Label}' in doc.Label='{doc1.Label}'")
    print(f"      and obj.Label='{obj2.Label}' in doc.Label='{doc2.Label}'")

    diff_obj_props(doc1, doc2, obj1, obj2, propPattern=propPattern)

if __name__ == "__main__":
    main()
