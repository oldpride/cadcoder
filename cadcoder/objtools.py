from pprint import pformat
import re
import traceback
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.matchtools import match_key_startswith
import json

def normalize_label(s: str) -> str:
    forbidden = [' ', '.', ',', '%', '+', '-', '*',
                 '/', '(', ')', '[', ']', '=', '"', "'"]
    
    for f in forbidden:
        s = s.replace(f, '_')

    if s[0].isdigit():
            s = '_' + s
    return s

def get_obj_info(obj):
    '''
    return a string with object details: Name, Label, TypeId
    '''
    info = {}
    for attr in ['Name', 'Label','TypeId', 'Class']:
        if hasattr(obj, attr):
            info[attr] = getattr(obj, attr)
        else:
            info[attr] = None
        
    info['Class'] = obj.__class__.__name__
    info['Id'] = id(obj)
    info['Dir'] = dir(obj)
    return info

def print_obj_info(obj, printDir=False, indent=""):
    info = get_obj_info(obj)
    
    # print basic keys in one line
    print(f"{indent}Name='{info['Name']}', Label='{info['Label']}'")
    print(f"{indent}TypeId='{info['TypeId']}', Class='{info['Class']}'")
    print(f"{indent}Id={info['Id']}")
    if printDir:
        print(f"{indent}Dir: {info['Dir']}")
    print()

"""
Dump all objects in the given document (or active document if None)

object.Name vs object.Label:
    - object.Name: 
        This is the internal, unique identifier of
        an object within a FreeCAD document. 
        It is automatically assigned when an object is created and
        cannot be changed later. The Name is used internally by 
        FreeCAD for referencing objects in formulas and scripts, 
        especially when using methods like doc.getObject(). 
        It is guaranteed to be unique within a document.
    - object.Label: 
        This is the user-facing name displayed in the Tree View. 
        It is a descriptive string that can be freely changed by 
        the user at any time to make the object more understandable. 
        Unlike Name, Label is not guaranteed to be unique within 
        a document, although FreeCAD's default behavior often 
        appends numbers to ensure uniqueness if duplicate labels 
        are created. The Label is what users typically interact 
        with in the graphical interface.
"""

def compareObjects(obj1, obj2):
    '''
    https://forum.freecad.org/viewtopic.php?t=62549

    check whether the two selected vertex are the same object by, from strongest to weakest:
        1. address
        the following compares shapes
        2. isEqual() - share the same TShape, have the same Location and have the same Orientation
        3. isSame() - share the same TShape, have the same Location but may have a different Orientation
        4. isPartner() - Share the same TShape, but may have a different Location and may have a different Orientation
    '''
    # this compares objects
    if obj1 == obj2:
        return True
 
    # apply the shape comparisons only if the methods are available
    try:
        if not obj1.isEqual(obj2):
            print("isEqual failed")
            return False
        if not obj1.isSame(obj2):
            print("isSame failed")
            return False
        if not obj1.isPartner(obj2):
            print("isPartner failed")
            return False
        
        return True
    except Exception as e:
        pass

    try:
        shape1 = obj1.toShape()
        shape2 = obj2.toShape()
        
        if not shape1.isEqual(shape2):
            print("Shape isEqual failed")
            return False
        if not shape1.isSame(shape2):
            print("Shape isSame failed")
            return False
        if not shape1.isPartner(shape2):
            print("Shape isPartner failed")
            return False
        
        return True
    except Exception as e:
        print("Shape comparison failed")
        return False

'''
obj name vs label
-  obj.Name is created by FreeCAD internally, it is unique in the document, not changeable.
-  obj.Label is user friendly name, it can be changed by user, not unique in the document.
here we assume obj.Label is unique in the document. if not, we raise error.
'''
objNameLabel_by_docKey = {}

def map_obj_name_label(doc, refreshCache=False):
    # we use docKey to distinguish different docs with same Name because we may have tmp docs with same Name.
    docKey = f"{doc.Name},{id(doc)}"

    if not refreshCache and docKey in objNameLabel_by_docKey:
        return objNameLabel_by_docKey[docKey]  # already mapped

    label_by_name = {}
    name_by_label = {}

    for obj in doc.Objects:
        if obj.Label in name_by_label:
            raise ValueError(f"Duplicate label found: '{obj.Label}' for objects '{name_by_label[obj.Label]}' and '{obj.Name}'")
        if obj.Name in label_by_name:
            raise ValueError(f"Duplicate name found: '{obj.Name}' for objects '{label_by_name[obj.Name]}' and '{obj.Label}'")
        label_by_name[obj.Name] = obj.Label
        name_by_label[obj.Label] = obj.Name

    objNameLabel_by_docKey[docKey] = {
        'label_by_name': label_by_name,
        'name_by_label': name_by_label
    }
    
    return objNameLabel_by_docKey[docKey]

def get_objRaw_by_objKey(doc, objKey, useLabel):
    objmap = map_obj_name_label(doc)
    direction = 'name_by_label' if useLabel else 'label_by_name'
    if direction not in objmap:
        # print stack trace  
        traceback.print_stack()
        msg = f"missing {direction} in objmap"
        print(msg)
        print(f"objmap=\n{pformat(objmap)}")     
        raise RuntimeError(msg)
    submap = objmap[direction]
    if objKey not in submap:
        traceback.print_stack()
        msg = f"Cannot find objKey='{objKey}' in objmap[{direction}], useLabel={useLabel}, doc={doc.Name}"
        print(msg)
        print(f"objmap[{direction}]=\n{pformat(objmap[direction])}")
        raise RuntimeError(msg)
    return submap[objKey]

def get_name_by_label(doc,objLabel):
    return get_objRaw_by_objKey(doc, objLabel, useLabel=True)

def get_label_by_name(doc, objName):
    return get_objRaw_by_objKey(doc, objName, useLabel=False)

def get_obj_by_objKey(doc, objKey, useLabel):
    if useLabel:
        objName = get_name_by_label(doc, objKey)
    else:
        objName = objKey
    obj = doc.getObject(objName)
    if obj is None:
        msg=f"ERROR: cannot find object with key='{objKey}' (useLabel={useLabel}) objName='{objName}' doc={doc.Name}"
        print(msg)
        if useLabel:
            print(f"Available labels:\n{pformat(list(map_obj_name_label(doc)['name_by_label'].keys()))}")
        else:
            print(f"Available names:\n{pformat(list(map_obj_name_label(doc)['label_by_name'].keys()))}")
        traceback.print_stack()
        raise RuntimeError(msg)
    return obj  

def get_objKey(obj, useLabel):
    return obj.Label if useLabel else obj.Name

def get_objKeyList_by_objList(useLabel, objList):
    objKeyList = []
    for obj in objList:
        objKey = obj.Label if useLabel else obj.Name
        objKeyList.append(objKey)

    return objKeyList

def get_objList_by_objKeyList(doc, useLabel, objKeyList):
    objList = []
    for objKey in objKeyList:
        obj = get_obj_by_objKey(doc, objKey, useLabel)
        objList.append(obj)

    return objList

def get_target_objKeyList(doc, useLabel, objList0=None) -> list:
    objects = get_target_objs(doc, objList0)
    objKeyList = []
    for obj in objects:
        objKey = obj.Label if useLabel else obj.Name
        objKeyList.append(objKey)

    return objKeyList

def get_target_objs(doc, objList=None) -> list:
    if objList is not None:
        return objList

    selection = Gui.Selection.getSelection()
    if selection:
        objects = selection
    else:
        objects = doc.Objects
    return objects

# skip_objects = [
#     # seen these in PartDesign Body. we don't need them because they are auto-created with new Body.
#     # TypeId, Name Prefix
#     ('App::Line', 'X_Axis'),
#     ('App::Line', 'Y_Axis'),
#     ('App::Line', 'Z_Axis'),
#     ('App::Plane', 'XY_Plane'),
#     ('App::Plane', 'XZ_Plane'),
#     ('App::Plane', 'YZ_Plane'),
#     ('App::Origin', 'Origin'),
# ]

skip_objTypeIdNamePattern = [
    # seen these in PartDesign Body. we don't need them because they are auto-created with new Body.
    # TypeId, Name Prefix
    'App::Line,[XYZ]_Axis.*',
    'App::Plane,(XY|XZ|YZ)_Plane.*',
    'App::Origin,Origin.*',
    'App::FeaturePython,trigger',
]

def skip_obj(obj)->bool:
    TypeIdName = f"{obj.TypeId},{obj.Name}"
    for pattern in skip_objTypeIdNamePattern:
        if re.match(pattern, TypeIdName):
            return True
    return False
    
def print_obj(obj, indentCount=0):
    indent = "  " * indentCount
    print(f"{indent}Label={obj.Label}, Name={obj.Name}, TypeId={obj.TypeId}")

all_relations_by_docKey_objKey = {}

def get_all_obj_relations(doc, useLabel=True, refreshCache=False):
    # we use docKey to distinguish different docs with same Name because we may have tmp docs with same Name.
    docKey = f"{doc.Name},{id(doc)}"
    # print(f"Getting all object relations for docKey={docKey}, useLabel={useLabel}, refreshCache={refreshCache}")
    if docKey in all_relations_by_docKey_objKey and not refreshCache:
        return all_relations_by_docKey_objKey[docKey]
    
    all_relations_by_docKey_objKey[docKey] = {}

    allObjects = doc.Objects
    for obj in allObjects:
        # print(f"docKey={docKey}, obj.Label={obj.Label}, processing")
        relations = get_obj_relations(obj, useLabel)
        # print(f"relations={relations}")
        objKey = obj.Label if useLabel else obj.Name
        all_relations_by_docKey_objKey[docKey][objKey] = relations

    # print(f"All object relations for docKey={docKey}: {all_relations_by_docKey_objKey[docKey]}")

    return all_relations_by_docKey_objKey[docKey]

def get_obj_str(obj):
    if obj is None:
        return "None"
    return f"Label={obj.Label}, Name={obj.Name}, TypeId={obj.TypeId}"

def get_obj_relations(obj, useLabel=True, printDetail=False):
    '''
    inList/outList vs Group
    - inList/outList are automatic relationships maintained by FreeCAD when you link objects together.
      they represent the parent-child relationships between objects.
      we cannot directly modify inList/outList. It changes as a result of other operations.
      For example, 
      - the inList/Outlist of Body is updated by Group (below).
      - the inList/Outlist of Pad is updated by Pad.Profile (below).
    - Group is a container, only available to PartDesign::Body, not available to Pad or Sketch.
      Group brings objects into the scope of the Body.
      we can directly modify Group.
    '''
    
    relations = {
        'obj': obj,
        'upstreams': {},
        'downstreams': {},
        'InList': [],
        'OutList': [],
        'Group': [],
        'Source': None,
        'Links': [],
    }

    if printDetail:
        print(f"Object: {get_obj_str(obj)}")
    for parent in sorted(obj.InList, key=lambda o: o.Label):
        parentKey = parent.Label if useLabel else parent.Name
        r = {
            'by': 'InList',
            'obj': parent,
        }
        relations['upstreams'][parentKey] = r
        relations['InList'].append(parentKey)
        if printDetail:
            print(f"    InList (parent, upstream): {get_obj_str(parent)}")
    if hasattr(obj, 'Source'):
        relations['Source'] = obj.Source
        objKey2 = obj.Source.Label if useLabel else obj.Source.Name
        r = {
            'by': 'Source',
            'obj': obj.Source,
        }
        relations['upstreams'][objKey2] = r
        if printDetail:
            print(f"    Source (upstream, parent): {get_obj_str(obj.Source)}")

    if printDetail:
        print()
    if hasattr(obj, 'Links') and obj.Links:
        for link in obj.Links:
            linkKey = link.Label if useLabel else link.Name
            relations['Links'].append(linkKey)
            r = {
                'by': 'Links',
                'obj': link,
            }
            relations['upstreams'][linkKey] = r
            if printDetail:
                print(f"    Links (upstream, parent): {get_obj_str(link)}")
    for child in obj.OutList:
        childKey = child.Label if useLabel else child.Name
        r = {
            'by': 'OutList',
            'obj': child,
        }
        relations['downstreams'][childKey] = r
        relations['OutList'].append(childKey)
        if printDetail:
            print(f"    OutList (child, downstream): {get_obj_str(child)}") 
    if hasattr(obj, 'Group') and obj.Group:
        for grpMember in obj.Group:
            grpMemberKey = grpMember.Label if useLabel else grpMember.Name
            r = {
                'by': 'Group',
                'obj': grpMember,
            }
            relations['Group'].append(grpMemberKey)
            relations['downstreams'][grpMemberKey] = r
            if printDetail:
                print(f"    Group (member, downstream): {get_obj_str(grpMember)}")

    return relations

def get_obj_all_upstreams(doc, obj, useLabel=True, printDetail=False, prefix="0", typePattern=None):
    objKey = obj.Label if useLabel else obj.Name
    return get_objKey_upstreams_recursively(doc, objKey, useLabel, printDetail=printDetail, indentCount=0, prefix=prefix, typePattern=typePattern)

objKey_upstream_stack = []

def get_objKey_upstreams_recursively(doc, objKey, useLabel, level=0, printDetail=False, indentCount=0, prefix="0", typePattern=None):
    if level == 0:
        objKey_upstream_stack.clear()

    if objKey in objKey_upstream_stack:
        msg = f"Detected circular dependency for object '{objKey}'"
        print(msg)
        print(f"Current objKey_upstream_stack: {objKey_upstream_stack}")
        raise RuntimeError(msg)
    
    max_recursion_depth = 50

    if len(objKey_upstream_stack) >= max_recursion_depth:
        msg = f"Exceeded maximum recursion depth ({max_recursion_depth}) for object '{objKey}'"
        print(msg)
        print(f"Current objKey_upstream_stack:")
        i=0
        for key in objKey_upstream_stack:
            print(f"  #{i} {key}")
            i += 1
        raise RuntimeError(msg)
    
    objKey_upstream_stack.append(objKey)
     
    all_relations = get_all_obj_relations(doc, useLabel)

    if objKey not in all_relations:
        msg = f"Object '{objKey}' not found in document relations."
        print(msg)
        print(f"all_relations keys: {sorted(list(all_relations.keys()))}")
        raise RuntimeError(msg)
    
    relations = all_relations[objKey]
    ret = set()

    if printDetail:
        indent = '  ' * indentCount
        typeId = relations['obj'].TypeId
        print(f"{indent}{prefix} Object {objKey} {typeId} upstream relations:")

    i = 0
    for objKey2 in sorted(relations['upstreams'].keys()):
        by2 = relations['upstreams'][objKey2]['by']
        typeId2 = relations['upstreams'][objKey2]['obj'].TypeId
        if typePattern is None or re.search(typePattern, typeId2, re.IGNORECASE):
            if printDetail:
                print(f"{indent}      - parent {prefix}.{i} {objKey2} {typeId2} (by {by2})")
            ret.add(objKey2)

        ret.update(get_objKey_upstreams_recursively(doc, objKey2, useLabel, 
                                                     level=level+1, 
                                                     indentCount=indentCount+1,
                                                     prefix=f"{prefix}.{i}",
                                                     printDetail=printDetail,
                                                     typePattern=typePattern))
        i += 1
    if level == 0 and printDetail:
        indent = '  '
        print(f"{indent}All upstreams of '{objKey}':")
        for item in sorted(ret):
            print(f"{indent*2}{item}")
    objKey_upstream_stack.pop()
    return ret

def get_obj_all_downstreams(doc, obj, useLabel=True, printDetail=False, prefix="0", typePattern=None):  

    # if printDetail:
    #     print(f"{prefix} Object Name={obj.Name}, Label={obj.Label}, TypeId={obj.TypeId}, useLabel={useLabel}")
    objKey = obj.Label if useLabel else obj.Name
    return get_objKey_downstreams_recursively(doc, objKey, useLabel, printDetail=printDetail, indentCount=0, prefix=prefix, typePattern=typePattern)
objKey_downstream_stack = []

def get_objKey_downstreams_recursively(doc, objKey, useLabel, 
                                       level=0, printDetail=False, indentCount=0, 
                                       prefix="0", typePattern=None,
                                       debug = 0,
                                       ):
    if level == 0:
        objKey_downstream_stack.clear()

    if debug:
        print(f"get_objKey_downstreams_recursively(): objKey={objKey}, level={level}, stack={objKey_downstream_stack}")

    if objKey in objKey_downstream_stack:
        msg = f"Detected circular dependency for object '{objKey}'"
        print(msg)
        print(f"Current objKey_downstream_stack: {objKey_downstream_stack}")
        raise RuntimeError(msg)
    
    max_recursion_depth = 50

    if len(objKey_downstream_stack) >= max_recursion_depth:
        msg = f"Exceeded maximum recursion depth ({max_recursion_depth}) for object '{objKey}'"
        print(msg)
        print(f"Current objKey_downstream_stack:")
        i=0
        for key in objKey_downstream_stack:
            print(f"  #{i} {key}")
            i += 1
        raise RuntimeError(msg)
    
    objKey_downstream_stack.append(objKey)
     
    all_relations = get_all_obj_relations(doc, useLabel)

    # print()
    # print(f"all_relations: {all_relations}")
    # print()

    if objKey not in all_relations:
        msg = f"Object '{objKey}' not found in document relations."
        print(msg)
        print(f"all_relations keys: {sorted(list(all_relations.keys()))}")
        raise RuntimeError(msg)
    
    relations = all_relations[objKey]
    obj = relations['obj']
    ret = set()
    
    if printDetail:
        indent = '  ' * indentCount
        if typePattern is None or re.search(typePattern, obj.TypeId, re.IGNORECASE):
            typeId = obj.TypeId
            print(f"{indent}{prefix} Object {objKey} {typeId} downstream relations:")


    i=0
    for objKey2 in sorted(relations['downstreams'].keys()):
        by2 = relations['downstreams'][objKey2]['by']
        typeId2 = relations['downstreams'][objKey2]['obj'].TypeId
        if typePattern is None or re.search(typePattern, typeId2, re.IGNORECASE):
            if printDetail:
                print(f"{indent}      - child {prefix}.{i} {objKey2} {typeId2} (by {by2})")
            ret.add(objKey2)
        ret.update(get_objKey_downstreams_recursively(doc, objKey2, useLabel, 
                                                      level=level+1, 
                                                      indentCount=indentCount+1,
                                                      prefix=f"{prefix}.{i}",
                                                      printDetail=printDetail, 
                                                      typePattern=typePattern))
        i += 1

    if level == 0 and printDetail:
        indent = '  '
        print(f"{indent}All downstreams of '{objKey}':")
        for item in sorted(ret):
            print(f"{indent*2}{item}")
    objKey_downstream_stack.pop()
    return ret


def sort_objs_by_downstream(doc, useLabel, objList=None, 
                            externalReadyList=None, 
                            debug=0, 
                            printDetail=False,
                            refreshCache=False,
                            ) -> dict:
    objList2 = get_target_objs(doc, objList)

    if not objList2:
        raise RuntimeError("No objects to sort")
    
    if debug:
        print(f"Sorting {len(objList2)} objects by downstream dependencies (useLabel={useLabel})")
        for obj in sorted(objList2, key=lambda o: o.Name):
            print(f"    Object Name={obj.Name}, Label={obj.Label}, TypeId={obj.TypeId}")
    
    objKeyList = get_objKeyList_by_objList(useLabel, objList2)

    delayed_set = set(objKeyList.copy())
    ready_list = []   # we use list to preserve order
    pre_ready_set = set()  # objects that are considered pre-ready
    skip_set = set()  # objects that cannot be built because they are automatically created.
    external_other_set = set()  # objects outside objList
    external_ready_set = set()
    external_preready_set = set()

    # first move TypeId=PartDesign::Body to ready_list because they the containers needed by others
    # so with its auto-triggered objects
    pre_ready_TypeIds = [
        'PartDesign::Body', 
    ]
    skip_downstream_typeIds = [
        'App::Origin',
        'App::Line',
        'App::Plane',
    ]

    # print("---------------------------------------------------------")
    # print(f"refreshCache={refreshCache}")
    if refreshCache:
        # print("---------------------------------------------------------------")
        # get_obj_by_objKey cache
        map_obj_name_label(doc, refreshCache=refreshCache)
        all_obj_relations = get_all_obj_relations(doc, useLabel, refreshCache=refreshCache)
        # print()
        # print(f"all_obj_relations: {all_obj_relations}")
        # print()

    for objKey in sorted(delayed_set.copy()):
        obj = get_obj_by_objKey(doc, objKey, useLabel)

        if obj.TypeId in pre_ready_TypeIds:
            ready_list.append(objKey)
            pre_ready_set.add(objKey)
            delayed_set.remove(objKey)
            if debug:
                print(f"Object '{objKey}' is {obj.TypeId} and moved to ready_list first.")

    while delayed_set:
        begin_len = len(delayed_set)
        
        for objKey in sorted(delayed_set.copy()):  # iterate over a copy of the list
            obj = get_obj_by_objKey(doc, objKey, useLabel)
            typeId = obj.TypeId
            if typeId in skip_downstream_typeIds:
                skip_set.add(objKey)
                delayed_set.remove(objKey)
                if debug:
                    print(f"Object '{objKey}' is {typeId} and moved to skip_set.")
                continue

            downstreams = get_objKey_downstreams_recursively(doc, objKey, useLabel, printDetail=False)
            downstreams_ready = True
            if not downstreams:
                ready_list.append(objKey)
                delayed_set.remove(objKey)
                if debug:
                    print(f"Object '{objKey}' has no downstreams and moved to ready_list.")
                continue

            for dsKey in downstreams:
                if dsKey in ready_list or dsKey in skip_set:
                    continue

                if externalReadyList is not None and dsKey in externalReadyList:
                    external_ready_set.add(dsKey)
                    continue

                if dsKey not in delayed_set:
                    dsObj = get_obj_by_objKey(doc, dsKey, useLabel)
                    if dsObj.TypeId in pre_ready_TypeIds:
                        external_preready_set.add(dsKey)
                    elif dsObj.TypeId in skip_downstream_typeIds:
                        skip_set.add(dsKey)
                    else:
                        external_other_set.add(dsKey)
                        if debug:
                            print(f"{objKey} depends on external object '{dsKey}' not in the current set.")
                        downstreams_ready = False
                    continue

                if debug:
                    print(f"{objKey} downstream '{dsKey}' is not ready yet.")
                downstreams_ready = False
                continue   # don't break, we want to collect all missing downstreams

            if downstreams_ready:
                ready_list.append(objKey)
                delayed_set.remove(objKey)
                if debug:
                    print(f"Object '{objKey}' downstreams are all ready and moved to ready_list.")

        if len(delayed_set) == begin_len:
            print("Cannot make further progress in sorting due to unresolved dependencies.")
            break

    ret = {
        'ready_list': ready_list,
        'pre_ready_set': pre_ready_set,
        'skip_set': skip_set,
        'delayed_set': delayed_set,
        'external_other_set': external_other_set,
        'external_ready_set': external_ready_set,
        'external_preready_set': external_preready_set,
    }

    if printDetail:
        print("sort_objs_by_downstream result:")
        for k in ret:
            print(f"{k}:")
            if '_set' in k:
                for k2 in sorted(ret[k]):
                    print(f"    {k2}")
            else:
                # regular list, we preserve order
                for v in ret[k]:
                    print(f"    {v}")
    return ret


def expand_objects(doc, useLabel, objects=None, printDetail=False) -> set:
    '''
    expand the given objects by including all their downstreams.
    this tells the full set of objects needed to build the given objects.
    '''

    objects2 = get_target_objs(doc, objects)
    # print(f"Expanding {len(objects)} from initial objects0 = {objects0}")
    # if printDetail:
    #     print("Initial object set:")
    #     for obj in sorted(objects, key=lambda o: o.Name):
    #         print(f"    Name={obj.Name}, Label={obj.Label}, TypeId={obj.TypeId}")

    expanded_objKey_set = set()
    for obj in objects2:
        objKey = obj.Label if useLabel else obj.Name
        expanded_objKey_set.add(objKey)
        expanded_objKey_set.update(get_obj_all_downstreams(doc, obj, useLabel=useLabel, printDetail=False))

    if printDetail:
        print("Expanded object set:")
        # print(f"expanded_set = {pformat(expanded_set)}")
        for objKey in sorted(expanded_objKey_set):
            obj = get_obj_by_objKey(doc, objKey, useLabel)
            if obj in objects2:
                stauts = "(initial)"
            else:
                stauts = "(expanded)"
            print(f"    objKey={objKey}, Name={obj.Name}, TypeId={obj.TypeId}, {stauts}")

    expanded_objList = get_objList_by_objKeyList(doc, useLabel, list(expanded_objKey_set))

    return expanded_objList

def get_doc_top_objects(doc, objList=None, visibleOnly=False) -> set:
    '''
    if objList is given, find top objects in the given list.
    if objList is None, find top objects in the whole document.
    top objects are those that do not have any upstreams in the given set.
    '''
    objects2 = get_target_objs(doc, objList)
    top_objects = set()
    for obj in objects2:
        # if obj has InList, then it is not top object
        if obj.InList:
            continue
        if visibleOnly:
            if hasattr(obj, 'Visibility') and not obj.Visibility:
                continue
            if hasattr(obj, 'ViewObject'):
                vo = obj.ViewObject
                if hasattr(vo, 'Visibility') and not vo.Visibility:
                    continue
        top_objects.add(obj)
    return list(top_objects)

def get_group_top_objects(objList:set, visibleOnly=False) -> set:
    '''
    from the given set of objects, find top objects that do not have any upstreams in the given set.
    '''
    top_objects = set()
    objSet = set(objList)
    for obj in objList:
        # if obj has InList, and any of its parents is in the given set, then it is not top object
        has_parent_in_set = False
        for parent in obj.InList:
            if parent in objSet:
                has_parent_in_set = True
                break
        if has_parent_in_set:
            continue
        if visibleOnly:
            if hasattr(obj, 'Visibility') and not obj.Visibility:
                continue
            if hasattr(obj, 'ViewObject'):
                vo = obj.ViewObject
                if hasattr(vo, 'Visibility') and not vo.Visibility:
                    continue
        top_objects.add(obj)
    return list(top_objects)

def get_obj_shape(obj, printDetail=False):
    if hasattr(obj, 'Shape'):
        bb = obj.Shape.BoundBox
        if printDetail:
            indent = '    '
            print(f"Object Name={obj.Name}, Label={obj.Label}, TypeId={obj.TypeId}")
            print(f"{indent}Shape BoundBox: {bb}")
            print(f"{indent}Shape Volume: {obj.Shape.Volume}")
            print(f"{indent}Shape Area: {obj.Shape.Area}")
            print(f"{indent}Shape Center of Mass: {obj.Shape.CenterOfMass}")
            print(f"{indent}X: {bb.XMin} to {bb.XMax}, XSize={bb.XLength}, XSizeIn={bb.XLength/25.4}in, XCenter={(bb.XMin+bb.XLength/2)}")
            print(f"{indent}Y: {bb.YMin} to {bb.YMax}, YSize={bb.YLength}, YSizeIn={bb.YLength/25.4}in, YCenter={(bb.YMin+bb.YLength/2)}")
            print(f"{indent}Z: {bb.ZMin} to {bb.ZMax}, ZSize={bb.ZLength}, ZSizeIn={bb.ZLength/25.4}in, ZCenter={(bb.ZMin+bb.ZLength/2)}")
            print(f"{indent}Diagonal: {bb.DiagonalLength}, DiagonalIn={bb.DiagonalLength/25.4}in")
            true_diagonal = (App.Vector(bb.XMax, bb.YMax, bb.ZMax) - 
                 App.Vector(bb.XMin, bb.YMin, bb.ZMin)).Length 
            print(f"{indent}True Diagonal: {true_diagonal}, TrueDiagonalIn={true_diagonal/25.4}in")

        return obj.Shape
    else:
        if printDetail:
            print(f"Object Name={obj.Name}, Label={obj.Label}, TypeId={obj.TypeId} has no Shape property.")
        return None
    

def get_obj_prop_jsonDict(obj, propName, printDetail=False):
    # if hasattr(obj, propName):
    #     jsonDict =  json.loads(getattr(obj, propName))
    # else:
    #     jsonDict = {}
    try:
        propValue = obj.getPropertyByName(propName)
        jsonDict = json.loads(propValue)
    except Exception as e:
        msg = f"{get_obj_str(obj)} does not have property '{propName}'. Returning empty dict."
        print(msg)
        jsonDict = {}

    if printDetail:
        json.dumps(jsonDict, indent=4, sort_keys=True)

    return jsonDict


def update_obj_prop_jsonDict(obj, propName, delta_jsonDict, reset=False):
    # print(f"delta_jsonDict={delta_jsonDict}")
    old_jsonDict = get_obj_prop_jsonDict(obj, propName)

    # print(f"update_obj_prop_jsonDict(obj={obj.Label}, propName={propName}), old_jsonDict={old_jsonDict}")

    if reset:
        new_jsonDict = delta_jsonDict
    else:
        new_jsonDict = old_jsonDict.copy()
        new_jsonDict.update(delta_jsonDict)

    # print(f"update_obj_prop_jsonDict(obj={obj.Label}, propName={propName}), new_jsonDict={new_jsonDict}")

    if new_jsonDict == old_jsonDict:
        print(f"No change in JSON dictionary.")
        return
    
    if not hasattr(obj, propName):
        obj.addProperty("App::PropertyString", propName, "Base", f"JSON property {propName}")
    
    setattr(obj, propName, json.dumps(new_jsonDict))

def remove_obj_prop(obj, propName):
    if hasattr(obj, propName):
        obj.removeProperty(propName)
    else:
        print(f"Property {propName} does not exist on object {obj.Name}.")

def get_obj_pythonSource(obj):
    # if hasattr(obj, 'pythonSource'):
    #     return json.loads(obj.pythonSource)
    # return {}
    return get_obj_prop_jsonDict(obj, "pythonSource")

def set_obj_pythonSource(obj, new_pythonSource):
    # '''
    # if new_pythonSource is the same as the current pythonSource, do nothing.
    # if new_pythonSource is different from the current pythonSource, update the pythonSource property.
    # if pythonSource does not exist, add it.
    # '''
    # old_pythonSource = get_obj_pythonSource(obj)
    # if old_pythonSource == new_pythonSource:
    #     return
    # if not hasattr(obj, 'pythonSource'):
    #     obj.addProperty("App::PropertyString", "pythonSource", "Base", "Python source code")
    # old_pythonSource.update(new_pythonSource)
    # obj.pythonSource = json.dumps(old_pythonSource)
    update_obj_prop_jsonDict(obj, "pythonSource", new_pythonSource, reset=True)
    
def remove_obj_pythonSource(obj):
    # if hasattr(obj, 'pythonSource'):
    #     # del obj.pythonSource # this does not work
    #     obj.removeProperty("pythonSource") # this works
    remove_obj_prop(obj, "pythonSource")

def recompute_doc(doc, max_recompute=10, force=False, dryrun=False):
    '''
    recompute the doc until there is no touched object, or until max_recompute is reached.
    if force is True, will do one more recompute even there is no touched object, to make sure all objects are updated.
    if dryrun is True, will not actually recompute the document, just print the number of touched objects and exit.
    '''    
    recompute_count = 0

    for i in range(max_recompute):
        # check if any object is touched.
        touched_objs = []
        for obj in doc.Objects:
            if "Touched" in obj.State:
                print(f"{get_obj_str(obj)} is still touched. State={obj.State}")
                touched_objs.append(obj)
        if not touched_objs:
            print("No touched objects.")

            if (force):
                print(f"Force a recompute even there is no touched object")
                doc.recompute()
            break
        else:
            if dryrun:
                print(f"Dry run mode, not recomputing document.")
                break

            print(f"Recompute count={recompute_count} of max={max_recompute}.")
            doc.recompute()
            recompute_count += 1
            print()
