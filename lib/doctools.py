import json
import os
import traceback
import FreeCAD as App
import FreeCADGui as Gui
import re

def recreate_tmp_doc(tmpDocName="tmpDocNoSave", debug=0):
    '''
    close all docs with names starting with tmpDocName
    create new tmp doc
    return the doc
    '''
    # close all docs with names starting with docName
    for d in App.listDocuments().values():
        if d.Name.startswith(tmpDocName):
            if debug:
                print(f"Closing doc Name={d.Name}")
            App.closeDocument(d.Name)
    
    # create new tmp doc
    doc = App.newDocument(tmpDocName)
    return doc

def reorganize_doc(doc):
    '''
    at the end, recompute and set view
    '''
    print("errors seen above (if any) may be temporary due to incomplete object definitions.")
    print("-----------------------------------------------------")
    print("errors seen below (if any) are real errors.")
    doc.recompute() # type: ignore
    
    straighten_doc(doc)
    print("Finished executing script: " + __file__)

def straighten_doc(doc):
    # print doc type and class
    # print(f"Straightening document: {doc.Name}, type={type(doc)}, class={doc.__class__}")
    # Straightening document: tmpDocNoSave, type=<class 'App.Document'>, class=<class 'App.Document'>

    # make this doc active
    # App.setActiveDocument(doc.Name)

    guiDoc = Gui.getDocument(doc.Name)
    try:
        guiDoc.ActiveView.viewIsometric() 

    except Exception as e:
        msg = f"Error setting view for document {doc.Name}: {type(e).__name__}: {e}"
        print(msg)

    try:
        guiDoc.ActiveView.fitAll()
    except Exception as e:
        msg = f"Error fitting view for document {doc.Name}: {type(e).__name__}: {e}"
        print(msg)

# skip_objTypeIdNamePattern = [
#     # seen these in PartDesign Body. we don't need them because they are auto-created with new Body.
#     # TypeId, Name Prefix
#     'App::Line,X_Axis.*',
#     'App::Line,Y_Axis.*',
#     'App::Line,Z_Axis.*',
#     'App::Plane,XY_Plane.*',
#     'App::Plane,XZ_Plane.*',
#     'App::Plane,YZ_Plane.*',
#     'App::Origin,Origin.*',
#     'App::FeaturePython,trigger',
# ]

def diff_docs(doc1, doc2, 
              objList1=None, objList2=None, diffOnly=False, commOnly=False, skipImport=False,
              objTypeIdPattern=None,  # eg, PartDesign::.*
              propNamePattern=None, # eg, Placement
              ignoreImporter=True,  # ignore importerInstanceName when comparing because it is likely always different.
              debug = 0,
              ):
    '''
    compare two docs 
    - first compare list of object labels
      object names may be auto-renamed, not controlled by user.
      object labels are controlled by user. 
    - if object labels match, then compare properties of each object
    '''

    # traceback.print_stack()

    print(f"Comparing documents: doc1={doc1.Label} and doc2={doc2.Label}")

    # place the two docs in standard position
    straighten_doc(doc1)
    straighten_doc(doc2)

    # import here to avoid circular import
    from pdfclib.objtools import map_obj_name_label, get_obj_pythonSource, skip_objTypeIdNamePattern
    from pdfclib.proptools import get_prop_info, print_prop_info
    objName_by_label1 = map_obj_name_label(doc1)['name_by_label']
    objName_by_label2 = map_obj_name_label(doc2)['name_by_label']

    if objList1 is None:
        objList1 = doc1.Objects
    if objList2 is None:
        objList2 = doc2.Objects

    # filter out objects matching skip patterns
    objList1 = [obj for obj in objList1 if not any(re.match(pattern, f"{obj.TypeId},{obj.Name}") for pattern in skip_objTypeIdNamePattern)]
    objList2 = [obj for obj in objList2 if not any(re.match(pattern, f"{obj.TypeId},{obj.Name}") for pattern in skip_objTypeIdNamePattern)]

    if objTypeIdPattern is not None:
        objList1 = [obj for obj in objList1 if re.search(objTypeIdPattern, obj.TypeId)]
        objList2 = [obj for obj in objList2 if re.search(objTypeIdPattern, obj.TypeId)]

    labels1 = [obj.Label for obj in objList1]
    labels2 = [obj.Label for obj in objList2]

    print(f"doc1 Labels: {sorted(labels1)}")
    print(f"doc2 Labels: {sorted(labels2)}")

    diff_props = []

    combined_labels = sorted(set(labels1) | set(labels2))
    for label in combined_labels:
        if label not in labels1:
            if not commOnly:
                print(f"> obj Label='{label}' only in doc2 '{doc2.Label}'")
                print()
        elif label not in labels2:
            if not commOnly:
                print(f"< obj Label='{label}' only in doc1 '{doc1.Label}'")
                print()
        else: 
            # check whether obj TypeId matches first
            objName1 = objName_by_label1[label]
            objName2 = objName_by_label2[label]
            obj1 = doc1.getObject(objName1)
            obj2 = doc2.getObject(objName2)

            pythonSource1 = get_obj_pythonSource(obj1)
            pythonSource2 = get_obj_pythonSource(obj2)

            importInstanceName1 = pythonSource1.get("importerInstanceName", None)
            importInstanceName2 = pythonSource2.get("importerInstanceName", None)
            if importInstanceName1 is not None or importInstanceName2 is not None:
                if importInstanceName1 != importInstanceName2 and not ignoreImporter:
                    if not commOnly:
                        print(f"> obj Label='{label}' importer={importInstanceName1} in doc2 '{doc2.Label}'")
                        print(f"< obj Label='{label}' importer={importInstanceName2} in doc1 '{doc1.Label}'")
                        print() 
                else:
                    if not diffOnly:
                        print(f"common obj Label='{label}' in both documents")
                        print() 

            if skipImport and (importInstanceName1 is not None or importInstanceName2 is not None):
                continue
 
            if obj1.TypeId != obj2.TypeId:
                if not commOnly:
                    print(f"> obj Label='{label}' TypeId='{obj2.TypeId}' in doc2 '{doc2.Label}'")
                    print(f"< obj Label='{label}' TypeId='{obj1.TypeId}' in doc1 '{doc1.Label}'")
                    print() 
                continue

            if not diffOnly:
                print(f"common obj Label='{label}' in both documents")
            # compare properties
            propNames1 = set(obj1.PropertiesList)
            propNames2 = set(obj2.PropertiesList)
            combined_props = sorted(propNames1 | propNames2)

            if propNamePattern is not None:
                combined_props = [propName for propName in combined_props if re.search(propNamePattern, propName)]

            for propName in sorted(combined_props):
                # skip some properties that are known to be different but not important
                if propName in [
                    # 'Placement', 
                    '_Body',
                    'Shape', 'BoundBox', 'pythonSource', 'pythonFeature'
                    ]:
                    continue

                info1 = get_prop_info(doc1, obj1, propName, objectlist=objList1)
                info2 = get_prop_info(doc2, obj2, propName, objectlist=objList2)
                if propName not in propNames1:
                    if not commOnly:
                        print(f"    > prop <<{label}>>.{propName} only in doc2 '{doc2.Label}'")
                        print_prop_info(info2, indent="    "*2)
                        print()
                    diff_props.append({
                        'obj': obj1,
                        'propName': propName,
                        'action': 'deleted',  # obj2 is the default
                        'pythonSource': pythonSource1,
                        'propInfo': info1,
                    })
                elif propName not in propNames2:
                    if not commOnly:
                        print(f"    < prop <<{label}>>.{propName} only in doc1 '{doc1.Label}'")
                        print_prop_info(info1, indent="    "*2)
                        print()
                    diff_props.append({
                        'obj': obj1,
                        'propName': propName,
                        'action': 'added', # obj2 is the default
                        'pythonSource': pythonSource1,
                        'propInfo': info1,
                    })
                else:
                    # if info1['valueClassTree'] == info2['valueClassTree'] and info1['valuePython'] == info2['valuePython']:
                    if info1['valueClassTree'] == info2['valueClassTree'] and similar_strings(info1['valuePython'], info2['valuePython']):
                        if not diffOnly:
                            print(f"    common prop <<{label}>>.{propName} identical in both documents")
                            print_prop_info(info1, indent="    "*2)
                            print()
                    else:
                        if not commOnly:
                            print(f"    > prop <<{label}>>.{propName} in doc2 '{doc2.Label}':")
                            if debug:
                                print_prop_info(info2, indent="    "*2)
                            print(f"    < prop <<{label}>>.{propName} in doc1 '{doc1.Label}':")
                            if debug:
                                print_prop_info(info1, indent="    "*2)
                            print()

                            if debug:
                                str1 = reduce_string(info1['valuePython'])
                                str2 = reduce_string(info2['valuePython'])
                                # print(f"str1==str2? {str1 == str2}")
                                # print(f"str1={str1}")
                                # print(f"str2={str2}")
                                diff_string(str1, str2)
                        diff_props.append({
                            'obj': obj1,
                            'propName': propName,
                            'action': 'modified',
                            'pythonSource': pythonSource1,
                            'propInfo': info1,
                        })
    print("Finished comparing documents: " + doc1.Label + " and " + doc2.Label)
    print()
    return diff_props

def reduce_string(str1):
    # reduce hex address'at 0x[0-9a-zA-Z]+' with 'at 0x'
    str1 = re.sub(r'at 0x[0-9a-zA-Z]+', 'at 0x', str1)

    # round float numbers to 4 decimal places
    str1 = re.sub(r'\d+\.\d+', lambda x: str(round(float(x.group()), 4)), str1)

    # 6.275484e-16, 1e-6, ..., if abs(value) < 1e-4, should be considered as 0
    str1 = re.sub(r'[-+]?\d+(\.\d+)?e[-]?[1-9]\d*', lambda x: '0' if abs(float(x.group())) < 1e-4 else x.group(), str1)
    
    # -0.000 and 0.000 are considered similar, reduce them to '0'
    str1 = re.sub(r'\b0.0+\b', '0', str1)
    str1 = re.sub(r'-0\b', '0', str1)

    # doc.getObject('Origin002') should be reduced to doc.getObject('Origin')
    str1 = re.sub(r"doc\.getObject\('([A-Za-z_]+)\d+'\)", r"doc.getObject('\1')", str1)

    return str1

def similar_strings(str1, str2):
    '''
    compare two strings, return True if they are similar
    - if only difference is addresses, return True
        eg, 
        <pdfclib.triggertools.TriggeringFeature object at 0x000002296F1A4D50>
        <pdfclib.triggertools.TriggeringFeature object at 0x000002296A7EE410>
        are similar
    '''

    if str1 == str2:
        return True

    return reduce_string(str1) == reduce_string(str2)

def diff_string(str1, str2):
    '''
    return the 1st index where the two strings differ, or -1 if they are the same.
    and print the index and the differing characters.
    '''
    for i, (c1, c2) in enumerate(zip(str1, str2)):
        if c1 != c2:
            # we preserve the spaces and newlines, so that console's auto-formatting 
            # does not affect the alignment.
            # replace other characters with '^'
            carret_str = re.sub(r'[^ \n]', '^', str1[:i]) 
            print()
            print(f"str1={str1}")
            print(f"str2={str2}")
            print(f"     {carret_str}")
            print()
            print(f"Strings differ at index {i}: '{c1}' != '{c2}'")
            print()
            return i
    if len(str1) != len(str2):
        print(f"Strings differ in length: len(str1)={len(str1)}, len(str2)={len(str2)}")
        return min(len(str1), len(str2))
    
    print("Strings are identical")
    return -1

def list_docs():
    for docName in App.listDocuments():
        doc = App.getDocument(docName)
        print(f"Document Label='{doc.Label}', Name='{doc.Name}', Path='{doc.FileName}'")
