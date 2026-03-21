import re
import FreeCAD as App
import FreeCADGui as Gui
import os
import sys

from pdfclib.expressiontools import sort_objs_exp_dependency
from pdfclib.proptools import diff_objPropDicts, get_docObjPropDict, diff_docObjPropDicts

# from pdfclib.objtools import recompute_doc

prog = os.path.basename(sys.argv[0])

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        description="show the last transactions in the active document.",
        epilog=f'''Example: 
        {prog}
        {prog} -n 20
        '''
        )
    # parser.add_argument('-full', action='store_true', help='Dump full relations, including Origin, Axes, Planes')
    parser.add_argument('-n', '--number', type=int, default=10, help='upto how many transactions to show')
    parser.add_argument('-pp', '--propPattern', type=str, default=None, help='property pattern to filter the changed properties, eg, "Placement|Shape"')
    parser.add_argument('-pi', '--propIgnore', type=str, default='Shape|Geometry|ExternalGeo|^B[0-9]+$', help='property pattern to ignore, eg, "Label|Name"')
    parser.add_argument('-debug', '--debug', action='store_true', help='print debug information')

    try:
        args = parser.parse_args()
        return args
    except SystemExit:
        print("Argument parsing failed.")
        return None

def get_obj_by_label(doc, label):
    for obj in doc.Objects:
        if obj.Label == label:
            return obj    
    return None
  
def main():
    args = parse_args()
    if args is None:
        return
    
    # useLabel = not args.useName

    doc = App.ActiveDocument

    if doc is None:
        raise RuntimeError("No active document found")
    
    '''
    dir(doc): ['ActiveObject', 'Comment', 'Company', 'Content', 'CreatedBy', 
    'CreationDate', 'DependencyGraph', 'FileName', 'HasPendingTransaction', 
    'Id', 'Importing', 'InList', 'Label', 'LastModifiedBy', 'LastModifiedDate', 
    'License', 'LicenseURL', 'Material', 'MemSize', 'Meta', 'Module', 'Name', 
    'Objects', 'OldLabel', 'OutList', 'Partial', 'PropertiesList', 
    'RecomputesFrozen', 'Recomputing', 'RedoCount', 'RedoNames', 
    'Restoring', 'RootObjects', 'RootObjectsIgnoreLinks', 'ShowHidden',
    'Temporary', 'Tip', 'TipName', 'TopologicalSortedObjects', 'Transacting',
    'TransientDir', 'TypeId', 'Uid', 'UndoCount', 'UndoMode', 'UndoNames', 
    'UndoRedoMemSize', 'UnitSystem', 'UseHasher', '__class__', '__delattr__',
    '__dir__', '__doc__', '__eq__', '__format__', '__ge__', 
    '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', 
    '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', 
    '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', 
    '__str__', '__subclasshook__', 'abortTransaction', 'addObject', 
    'addProperty', 'clearDocument', 'clearUndos', 'commitTransaction', 
    'copyObject', 'dumpContent', 'dumpPropertyContent', 'exportGraphviz', 
    'findObjects', 'getAllDerivedFrom', 'getDependentDocuments', 
    'getDocumentationOfProperty', 'getEditorMode', 'getEnumerationsOfProperty', 
    'getFileName', 'getGroupOfProperty', 'getLinksTo', 'getObject', 
    'getObjectsByLabel', 'getProgramVersion', 'getPropertyByName', 
    'getPropertyStatus', 'getPropertyTouchList', 'getTempFileName', 
    'getTypeIdOfProperty', 'getTypeOfProperty', 'importLinks', 'isClosable', 
    'isDerivedFrom', 'isSaved', 'isTouched', 'load', 'mergeProject', 
    'moveObject', 'mustExecute', 'openTransaction', 'purgeTouched', 
    'recompute', 'redo', 'removeObject', 'removeProperty', 'restore', 
    'restoreContent', 'restorePropertyContent', 'save', 'saveAs', 'saveCopy', 
    'setClosable', 'setDocumentationOfProperty', 'setEditorMode', 
    'setGroupOfProperty', 'setPropertyStatus', 'supportedTypes', 'undo']
    '''
    # 
    undo_stack = doc.UndoNames
    if undo_stack is None or len(undo_stack) == 0:
        print("No undo/redo history available")
        return
    
    undo_stack_length = len(undo_stack)
    print(f"Undo stack length: {undo_stack_length}")
    num_transactions = min(args.number, undo_stack_length)
    print(f"Last {num_transactions} transactions:")

    # objLabel = None
    for i in range(num_transactions):
        undo_name = undo_stack[i]  # get the last i-th transaction
        print(f"{i+1}. {undo_name}")

        # if objLabel is None:
        #     if m := re.match(r"Edit\s+(\S+)", undo_name):
        #         objLabel = m.group(1)

    '''
    19:52:23  Undo stack size: 5
    19:52:23  Last 5 transactions:
    19:52:23  5. Edit cylinder_pad
    19:52:23  4. Edit cylinder_pad
    19:52:23  3. Edit top_Body001.Placement
    19:52:23  2. Placement
    19:52:23  1. Edit cutter_cylinder_pad
    '''

    if undo_stack_length > 0:
        doc.undo()  # undo the last transaction to show the change in the document
        doc.recompute()  # recompute the document to update the changes
        docObjPropDict1 = get_docObjPropDict(doc, refreshCache=True, 
                                     # to include extended properties, eg, sketch constraints, spreadsheet aliass.
                                     extended=True, 
                                     useLabel=True, 
                                     )
        
        # print(f"keys1={list(docObjPropDict1.keys())}")
        # print()

        doc.redo()  # redo the undone transaction to restore the document state
        doc.recompute()  # recompute the document to update the changes 
        docObjPropDict2 = get_docObjPropDict(doc, refreshCache=True, 
                                       extended=True, 
                                       useLabel=True)
        # print(f"keys2={list(docObjPropDict2.keys())}")
        # print()
        
        differences = diff_docObjPropDicts(docObjPropDict1, docObjPropDict2, 
                          propPattern=args.propPattern,
                          propIgnore=args.propIgnore,
                        diffOnly=True,
                        printDetail=args.debug,
                        )
        
        affected_objProps = []
        for diff in differences:
            propName = diff['propName']
            changeStatus = diff['changeStatus']
            info1 = diff['info1']
            info2 = diff['info2']
            objKey1 = diff['objKey1']
            objKey2 = diff['objKey2']

            if changeStatus in ['added', 'modified', 'todo']:
                objProp = f"{objKey2}.{propName}"
                print(f"{objProp} {changeStatus}")
                affected_objProps.append(objProp)
            elif changeStatus == 'removed':
                objProp = f"{objKey1}.{propName}"
                print(f"{objProp} {changeStatus}")
            elif changeStatus == 'same':
                if args.debug:
                    objProp = f"{objKey2}.{propName}"
                    print(f"{objProp} {changeStatus}")
            else:
                objProp = f"{objKey2}.{propName}"
                raise RuntimeError(f"Unknown changeStatus: {changeStatus} for objProp={objProp}")
        
    '''
    11:15:33  cutter_cylinder_callsheet.cylinder_height modified
    11:15:33  cutter_cylinder_callsheet.cylinder_height_spec modified
    11:15:33  cutter_cylinder_pad.Length modified
    11:15:33  cylinder_callsheet.cylinder_height modified
    11:15:33  cylinder_callsheet.cylinder_height_spec modified
    11:15:33  cylinder_pad.Length modified
    11:15:33  npt_extension_callsheet.cylinder_height_spec modified
    11:15:33  top_npt_f.Placement modified
    '''
    sort_exps_result = sort_objs_exp_dependency(doc, useLabel=True, objList=doc.Objects, debug=args.debug, printDetail=1)
    failure_reasons = ['delayed_set', 
                       'external_other_set'
                       ]
    for fr in failure_reasons:
        if sort_exps_result[fr]:
            msg = f"Error: some expressions could not be sorted, reason={fr} is not empty"
            print(msg)
            raise RuntimeError(msg)
        
    first_affected_objProp = None
    for objPropKey in sort_exps_result['ready_list']:
        if objPropKey in affected_objProps:
            print(f"objPropKey={objPropKey} is the 1st affected property")
            first_affected_objProp = objPropKey
            break

    if first_affected_objProp is None:
        print("No affected property found in the sorted ready_list")
         
if __name__ == "__main__":
    main()
