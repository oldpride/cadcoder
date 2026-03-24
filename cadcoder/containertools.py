
from pprint import pformat
import re
import traceback
from cadcoder.objtools import get_obj_str


container_by_doc_objName = {}
container_by_doc_label = {}
objs_by_doc_containerName = {}
objs_by_doc_containerLabel = {}

def map_container(doc, refreshCache=False):
    # use doc id to distinguish different docs with same Name because we may have tmp docs with same Name
    docKey = f"{doc.Name},{id(doc)}" 
    docLabel = doc.Label

    if refreshCache or docKey not in container_by_doc_objName:
        container_by_doc_objName[docKey] = {}
        container_by_doc_label[docLabel] = {}
        objs_by_doc_containerName[docKey] = {}
        objs_by_doc_containerLabel[docLabel] = {}

    for obj in doc.Objects:
        if not obj.isDerivedFrom("PartDesign::Body"):
            continue
        container = obj

        Group = container.Group
        for obj2 in Group:
            container_by_doc_objName[docKey][obj2.Name] = container
            container_by_doc_label[docLabel][obj2.Label] = container
    
            if container.Name not in objs_by_doc_containerName[docKey]:
                objs_by_doc_containerName[docKey][container.Name] = [] 
            if container.Label not in objs_by_doc_containerLabel[docLabel]:
                objs_by_doc_containerLabel[docLabel][container.Label] = []
            objs_by_doc_containerName[docKey][container.Name].append(obj2)
            objs_by_doc_containerLabel[docLabel][container.Label].append(obj2)

    return

def get_container_by_objName(doc, objName, refreshCache=False):
    map_container(doc, refreshCache)
    docKey = f"{doc.Name},{id(doc)}"
    try:
        container = container_by_doc_objName[docKey][objName]
        return container
    except KeyError:
        return None

def get_container_by_objLabel(doc, objLabel, refreshCache=False):
    map_container(doc, refreshCache)
    docKey = f"{doc.Name},{id(doc)}"
    try:
        container = container_by_doc_label[docKey][objLabel]
        return container
    except KeyError:
        return None

def get_objs_by_containerName(doc, containerName, refreshCache=False):
    map_container(doc, refreshCache)
    docKey = f"{doc.Name},{id(doc)}"
    try:
        objs = objs_by_doc_containerName[docKey][containerName]
        return objs
    except KeyError:
        return None

def get_objs_by_containerLabel(doc, containerLabel, refreshCache=False):
    map_container(doc, refreshCache)
    docKey = f"{doc.Name},{id(doc)}"
    try:
        objs = objs_by_doc_containerLabel[docKey][containerLabel]
        return objs
    except KeyError:
        return None 

def print_container(doc, container):
    print(f"container: {get_obj_str(container)}")
    for obj in container.Group:
        print(f"    obj: {get_obj_str(obj)}")

def get_containers(doc, refreshCache=False, printDetail=False, useLabel=False):
    map_container(doc, refreshCache)

    docKey = f"{doc.Name},{id(doc)}"
    containerNames = objs_by_doc_containerName[docKey].keys()
    containers = []
    if printDetail:
        for containerName in sorted(containerNames):
            container = doc.getObject(containerName)
            print_container(doc, container)
            containers.append(container)
    
    return containers
            
def extend_container_with_objects(container, objs:list, debug=0):
    if not objs:
        return
    
    group = container.Group
    group.extend(objs)
    container.Group = group

    '''
    if the obj has a shape, we need to set the container's Tip to the obj;
    otherwise we get errors like:
    06:20:53  b_npt_f_boolean: Tool shape is null
    06:20:53  s_npt_f_boolean: Tool shape is null
    '''
    # get the last obj with a shape
    for obj in reversed(objs):
        # if hasattr(obj, "Shape") and obj.Shape is not None and not obj.Shape.isNull():
        if hasattr(obj, "Shape") and re.search(r"PartDesign::", obj.TypeId):
            # only PartDesign feature can be set to Tip; otherwise get error:
            #     Linked object is not a PartDesign feature
            if debug:
                print(f"set container.Tip: ")
                print(f"    container {get_obj_str(container)}")
                print(f"    tip obj {get_obj_str(obj)}")
            container.Tip = obj
            break
    return

LCS_by_doc_containerName = {}

def get_LCS_map(doc, container, refreshCache=False, debug=0):
    '''
    LCS - Local Coordinate System
    Origin...
    X-Axis...
    Y-Axis...
    Z-Axis...
    XY-Plane...
    XZ-Plane... 
    YZ-Plane...
    '''

    # check whether container is actually a container
    if not container.isDerivedFrom("PartDesign::Body"):
        msg = f"get_LCS_map: obj is not a container - PartDesign::Body"
        print(msg)
        print(f"    {get_obj_str(container)}")
        traceback.print_stack()
        raise RuntimeError(msg)

    docKey = f"{doc.Name},{id(doc)}" # use doc id to distinguish different docs with same Name
    if docKey not in LCS_by_doc_containerName or refreshCache:
        LCS_by_doc_containerName[docKey] = {}

    containerName = container.Name
    if containerName in LCS_by_doc_containerName[docKey]:
        return LCS_by_doc_containerName[docKey][containerName]
    
    LCS_by_prefix = {}
    for obj in container.OutList:
        if obj.TypeId == "App::Origin":
            prefix = re.sub(r"\d+$", "", obj.Name)
            LCS_by_prefix[prefix] = obj
            for obj2 in obj.OutList:
                prefix = None
                if obj2.TypeId in ["App::Line", "App::Plane"]:
                    # XZ-plane001 -> XZ-plane
                    prefix = re.sub(r"\d+$", "", obj2.Name)
                    LCS_by_prefix[prefix] = obj2
            break

    LCS_by_doc_containerName[docKey][containerName] = LCS_by_prefix
    if debug:
        print(f"Cached LCS map for container: {get_obj_str(container)}")
        print(f"    {pformat(LCS_by_prefix)}")
    return LCS_by_prefix

def get_LCS_by_prefix(doc, container, prefix):
    lcs_by_prefix = get_LCS_map(doc, container)
    lcs = lcs_by_prefix[prefix]
    return lcs

LCS_prefixes = ["Origin", "X_Axis", "Y_Axis", "Z_Axis", "XY_Plane", "XZ_Plane", "YZ_Plane"]
def get_LCS_prefixes():
    return LCS_prefixes



'''
21:42:49      modified: MainObject-AttachmentSupport
21:42:49        Object value:
21:42:49          propType: App::PropertyLinkSubList
21:42:49          propValue: [(<GeoFeature object>, ('',))]
21:42:49          readonly: False
21:42:49          valueClass: list
21:42:49          valueClassTree: {'list/tuple/GeoFeature', 'list/tuple/tuple/str'}
21:42:49          valueObjName: None
21:42:49          valuePython: [(doc.getObject('XZ_Plane'), (''))]
21:42:49          valueTypeId: None
21:42:49          prefixPython: [(doc.getObject('XZ_Plane'), (''))]
21:42:49          propName: AttachmentSupport

old: npt_m_sketch.AttachmentSupport = [(doc.getObject('XZ_Plane'), (''))]
new:
    npt_m_sketch.AttachmentSupport = self.get_AttachmentSupport(npt_m_sketch, ['XZ_Plane'])

'''
def get_AttachmentSupport(doc, obj, oldLcsNames:list):
    prefixes = []
    for name in oldLcsNames:
        prefix = re.sub(r"\d+$", "", name)
        prefixes.append(prefix)

    container = get_container_by_objName(doc, obj.Name, 
                                        #  refreshCache=True
                                            )
    print(f"object {get_obj_str(obj)}")
    print(f"    container {get_obj_str(container)}")

    AttachmentSupport = []
    for prefix in prefixes:
        lcsObj = get_LCS_by_prefix(doc, container, prefix)
        if lcsObj is not None:
            AttachmentSupport.append((lcsObj, ('',)))

    print(f"AttachmentSupport from '{oldLcsNames}' to {pformat(AttachmentSupport)}")
    return AttachmentSupport
