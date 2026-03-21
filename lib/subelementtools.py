import re
import Part
from pdfclib.objtools import sort_objs_by_downstream, get_obj_by_objKey


attr_by_seType = {
    'Edge': 'Length',
    'Face': 'Area',
}

seInfo_by_docKey_objName_seType_posType_posName = {}

def map_seInfo_by_posName(obj, seType, posType, printDetail=False, debug=False, refreshCache=False):
    '''
    get subelement name for given position Name, eg, top1, front2, ...

    position types:
        'top': max z value
        'bottom': min z value
        'left': min x value
        'right': max x value
        'front': min y value
        'back': max y value

    when order by Z, if multiple edges have same value Z, return the one with max length
    '''

    doc = obj.Document
    docKey = f"{doc.Name},{id(doc)}"
    objName = obj.Name

    if docKey not in seInfo_by_docKey_objName_seType_posType_posName:
        seInfo_by_docKey_objName_seType_posType_posName[docKey] = {}
        
    if objName not in seInfo_by_docKey_objName_seType_posType_posName[docKey]:
        seInfo_by_docKey_objName_seType_posType_posName[docKey][objName] = {}

    if seType not in seInfo_by_docKey_objName_seType_posType_posName[docKey][objName]:
        seInfo_by_docKey_objName_seType_posType_posName[docKey][objName][seType] = {}

    if posType not in seInfo_by_docKey_objName_seType_posType_posName[docKey][objName][seType] or refreshCache:
        seInfo_by_docKey_objName_seType_posType_posName[docKey][objName][seType][posType] = {}
    else:
        return seInfo_by_docKey_objName_seType_posType_posName[docKey][objName][seType][posType]

    if posType == 'top':
        by = 'z'
        reverse = True
    elif posType == 'bottom':
        by = 'z'
        reverse = False
    elif posType == 'left':
        by = 'x'
        reverse = False
    elif posType == 'right':
        by = 'x'
        reverse = True
    elif posType == 'front':
        by = 'y'
        reverse = False
    elif posType == 'back':
        by = 'y'
        reverse = True
    else:
        raise RuntimeError(f"Unsupported posType: {posType}")
    
    sorted_infos = sort_seInfos(obj, seType, by, reverse=reverse, printDetail=printDetail|debug, indentCount=1, refreshCache=refreshCache)
    
    # get the top group
    top_group = []
    for info in sorted_infos:
        rounding_error = 0.0001
        if abs(info[by] - sorted_infos[0][by]) < rounding_error:
            top_group.append(info)
        else:
            break

    # sort the top group by attr, and name the top group as 'front1', 'front2', etc.
    attr = attr_by_seType.get(seType, None)
    info_by_posName = {}
    if attr is not None:
        top_group = sorted(top_group, key=lambda v: v[attr], reverse=True) # prefer the larger attr value
    for i, info in enumerate(top_group):
        posName = f"{posType}{i + 1}"
        info_by_posName[posName] = info
        # seName = info['name']
        if printDetail:
            print("")
            print(f"{posName}: {get_seInfo_string(seType, info)}")
            print("")

    seInfo_by_docKey_objName_seType_posType_posName[docKey][objName][seType][posType] = info_by_posName
    return info_by_posName

def get_seInfo_by_posName(obj, seType, posName, debug=False, refreshCache=False, printDetail=False):
    posType = re.sub(r'\d+$', '', posName)
    seInfo_by_posName = map_seInfo_by_posName(obj, seType, posType, debug=debug, refreshCache=refreshCache, printDetail=printDetail)
    try:
        seInfo = seInfo_by_posName[posName]
    except KeyError:
        msg = print(f"KeyError: posName={posName} not found in seInfo_by_posName")
        print(msg)
        print(f"obj Label={obj.Label} posName={posName} seInfo_by_posName={seInfo_by_posName}: ")
        # for pn in sorted(seInfo_by_posName.keys()):
        #     seInfo = seInfo_by_posName[pn]
        #     print(f"    {pn}, {seInfo['name']}")
        raise RuntimeError(msg)
        

    return seInfo

def get_seName_by_posName(obj, seType, posName, debug=False, refreshCache=False, printDetail=False):
    seInfo = get_seInfo_by_posName(obj, seType, posName, debug=False, refreshCache=refreshCache, printDetail=printDetail)
    seName = seInfo['name']
    print(f"seType={seType} posName={posName} points to {seName}")
    return seName

def get_all_seNames(obj, seType, printDetail=False):
    shape = obj.Shape
    # Edge -> Edges
    # Face -> Faces
    subElements = getattr(shape, f"{seType}s")
    seNames = []
    for i, subElement in enumerate(subElements):
        seName = f"{seType.capitalize()}{i + 1}"
        seNames.append(seName)
        if printDetail:
            print(f"{seName:7s}: {get_se_string(subElement)}")
    return seNames

def get_se_string(subElement)->str:
    '''
    print length and center of mass of edge in 4 decimal places
    default output:
    Length=242.3767000295222, CenterOfMass=Vector (1.8493236204696625e-13, 7.36782318912216e-16, 0.0)
    '''

    # edge_string = f'{edgeInfo["name"]:7s} Length={edgeInfo["length"]:10.4f}, CenterOfMass=Vector ({edgeInfo["x"]:10.4f}, {edgeInfo["y"]:10.4f}, {edgeInfo["z"]:10.4f})'
    if isinstance(subElement, Part.Edge):
        subElement_string = f'Length={subElement.Length:10.4f}, CenterOfMass=Vector ({subElement.CenterOfMass.x:10.4f}, {subElement.CenterOfMass.y:10.4f}, {subElement.CenterOfMass.z:10.4f})'
    elif isinstance(subElement, Part.Face):
        subElement_string = f'Area={subElement.Area:10.4f}, CenterOfMass=Vector ({subElement.CenterOfMass.x:10.4f}, {subElement.CenterOfMass.y:10.4f}, {subElement.CenterOfMass.z:10.4f})'
    return subElement_string

def get_seInfo_string(seType, seInfo):
    attr = attr_by_seType[seType]
    return f"{seInfo['name']:7s}: {attr}={seInfo[attr]:10.4f}, CenterOfMass=Vector({seInfo['x']:10.4f}, {seInfo['y']:10.4f}, {seInfo['z']:10.4f})"


seInfo_by_docKey_objName_seType_seName = {}

def map_obj_seInfo_by_seName(obj, seType, refreshCache=False):
    doc = obj.Document
    docKey = f"{doc.Name},{id(doc)}"
    objName = obj.Name
    if docKey not in seInfo_by_docKey_objName_seType_seName:
        seInfo_by_docKey_objName_seType_seName[docKey] = {}
    if objName not in seInfo_by_docKey_objName_seType_seName[docKey]:
        seInfo_by_docKey_objName_seType_seName[docKey][objName] = {}
    if seType in seInfo_by_docKey_objName_seType_seName[docKey][objName] and not refreshCache:
        return seInfo_by_docKey_objName_seType_seName[docKey][objName][seType]
    
    seInfo_by_docKey_objName_seType_seName[docKey][objName][seType] = {}

    # print(f"updating seInfo_by_docKey_objName_seType_seName[{docKey}][{objName}][{seType}]")
    
    seInfo_by_seName = {}
    shape = obj.Shape
    attr = attr_by_seType[seType]
    for i, subElement in enumerate(getattr(shape, f"{seType}s")):
        # print(f"Mapping subelement info for docKey={docKey}, objName={objName}, seType={seType}, subElement index={i}")
        seName = f"{seType}{i + 1}"
        seInfo = {
            'name': seName,
            'index': i,
            attr: getattr(subElement, attr),
            'x': subElement.CenterOfMass.x,
            'y': subElement.CenterOfMass.y,
            'z': subElement.CenterOfMass.z,
        }
        seInfo_by_seName[seName] = seInfo

    seInfo_by_docKey_objName_seType_seName[docKey][objName][seType] = seInfo_by_seName
    return seInfo_by_seName

def get_seInfo_by_seName(obj, seType, seName, refreshCache=False):
    seInfo_by_seName = map_obj_seInfo_by_seName(obj, seType, refreshCache=refreshCache)
    if seName not in seInfo_by_seName:
        raise RuntimeError(f"Subelement name '{seName}' not found in object '{obj.Name}'")
    return seInfo_by_seName[seName]

def sort_seInfos(obj, seType:str, by:str, reverse:bool=False, printDetail:bool=False, indentCount=0, refreshCache=False)->list:
    '''
    sort edges by 'name', 'index', 'length', 'x', 'y', 'z'
    return sorted list of edge names
    '''
    seInfo_by_seName = map_obj_seInfo_by_seName(obj, seType, refreshCache=refreshCache)
    # print(f"{obj.Name} {obj.Label} seInfo_by_seName = {seInfo_by_seName}")
    attr = attr_by_seType[seType]
    if by not in ['name', 'index', attr, 'x', 'y', 'z']:
        raise RuntimeError(f"Unsupported sort by: {by}")
    if by == 'name':
        by2 = 'index'
    else:
        by2 = by
    sorted_seInfos = sorted(seInfo_by_seName.values(), key=lambda v: v[by2], reverse=reverse)
    if printDetail:
        for seInfo in sorted_seInfos:
            print(f"obj={obj.Name}, seType={seType}, sortBy={by}, {get_seInfo_string(seType, seInfo)}")
    return sorted_seInfos
    
def dump_pos(seType, objects:list):
    for obj in objects:
        print(f"name={obj.Name}, label={obj.Label}, typeId={obj.TypeId}")
        for posType in [ 'top', 'bottom', 'left', 'right', 'front', 'back' ]:
            i = 0
            max=100
            while i<=max:
                i += 1
                posName = f"{posType}{i}"
                # seInfo = get_seInfo_by_posName(sel, seType, posName)
                try:                   
                    seInfo = get_seInfo_by_posName(obj, seType, posName)
                except Exception as e:
                    # traceback.print_stack()
                    # print(f"failed to get {seType} {posName}")
                    break

                seName = seInfo['name']
                print(f"{posName:7s}, {seName:7s}, {get_seInfo_string(seType, seInfo)}")
            print()

def map_seName_by_posName_in_all_posType(obj, seType, printDetail=False, debug=False, refreshCache=False):
    seName_by_posName = {}
    posNames_by_seName = {}
    for posType in [ 'top', 'bottom', 'left', 'right', 'front', 'back' ]:
        seInfo_by_posName = map_seInfo_by_posName(obj, seType, posType, printDetail=False, debug=False, refreshCache=refreshCache)
        # print(f"{posType}, seInfo_by_posName={seInfo_by_posName}")
        for posName, seInfo in seInfo_by_posName.items():
            seName = seInfo['name']
            seName_by_posName[posName] = seName
            if seName not in posNames_by_seName:
                posNames_by_seName[seName] = [posName]
            else:
                posNames_by_seName[seName].append(posName)
    # print(f"posNames_by_seName={posNames_by_seName}")
    return seName_by_posName, posNames_by_seName

def get_posNames_by_seName(obj, seName, refreshCache=False):
    seType = re.sub(r'\d+$', '', seName)
    seName_by_posName, posNames_by_seName = map_seName_by_posName_in_all_posType(obj, seType, refreshCache=refreshCache)
    if seName not in posNames_by_seName:
        return []
    else:
        return posNames_by_seName[seName]

def get_index_from_name(name:str)-> int:
    # Edge123 -> 123
    if m := re.search(r'(\d+)', name):
        index = int(m.group(1))
        return index
    else:
        msg = f"name={name} is not correct format, eg, Edge123, top123"
        raise RuntimeError(msg)
    

def get_posName_by_seName(obj, seName, refreshCache=False):
    if not seName:
        msg = f"seName='{seName}' is empty or None"
        raise RuntimeError(msg)
    posNames = get_posNames_by_seName(obj, seName, refreshCache=refreshCache)

    if not posNames:
        return None
    
    # pick the smallest index
    min_posName = posNames[0]
    min_index = get_index_from_name(min_posName)
    for posName in posNames[1:]:
        index = get_index_from_name(posName)
        if index < min_index:
            min_index = index
            min_posName = posName

    return min_posName

def dump_all_seNames(obj, seType, by):
    sorted_seInfos = sort_seInfos(obj, seType, by)
    for seInfo in sorted_seInfos:
        seName = seInfo['name']
        posNames = get_posNames_by_seName(obj, seName)
        min_posName = get_posName_by_seName(obj, seName)
        print(f"{get_seInfo_string(seType, seInfo)}, {posNames}, min={min_posName}")       
        
def update_obj_seName(obj, refreshCache=False):
    '''
    update Edge name, Face name, ... after modifying the Base or AttachmentSupport.
    get the stored prop, seType, posName from pythonFeature
    '''

    from pdfclib.objtools import get_obj_prop_jsonDict
    jsonDict = get_obj_prop_jsonDict(obj, 'pythonFeature')

    # return if jsonDict is empty
    if not jsonDict:
        return
    
    propNames = ['AttachmentSupport', 'Base']

    for propName in propNames:
        if propName in jsonDict:
            old_propValue = getattr(obj, propName)
            print(f"obj Label={obj.Label}, old {propName}={old_propValue}") 
                
            if propName == 'AttachmentSupport':
                # old prop value: npt_m_hole_bottom_sketch.AttachmentSupport = [(npt_m_hole_top, ('Face45'))]
                # pythonFeature jsonDict: {"AttachmentSupport": {"seType": "Face", "posName": "bottom1"}}
                
                # parse old propValue     
                baseObj, old_seName_tuple = old_propValue[0]
                old_seName = old_seName_tuple[0]

                # parse jsonDict from pythonFeature
                seType = jsonDict[propName]['seType']
                posName = jsonDict[propName]['posName']       

                new_seName = get_seName_by_posName(baseObj, seType, posName, refreshCache=refreshCache)
                
                if old_seName == new_seName:
                    print(f"obj Label={obj.Label}, {propName}, no change, old_seName=new_seName={new_seName}.")
                else:
                    print(f"obj Label={obj.Label}, {propName}, updating, old_seName={old_seName}, new_seName={new_seName}")
                    obj.AttachmentSupport = [(baseObj, (new_seName,))]

                    # recompute whole doc after subelement change
                    # obj.recompute() # recomputing obj is not enough
                    doc = obj.Document
                    doc.recompute()
            elif propName == 'Base':
                # old prop value: npt_fxf_chamfer_top.Base = (npt_fxf_instance.npt_fxf_boolean, ['Edge1'])
                # pythonFeature jsonDict: {"Base": [{"seType": "Edge", "posName": "bottom1"}, {"seType": "Edge", "posName": "top1"}]}
                
                # parse old propValue     
                baseObj, old_seNames = old_propValue

                # parse pythonFeature jsonDict
                new_seNames = set()
                for d in jsonDict[propName]:
                    seType = d['seType']
                    posName = d['posName']
                    new_seName = get_seName_by_posName(baseObj, seType, posName, refreshCache=refreshCache)
                    new_seNames.add(new_seName)
                
                if set(old_seNames) == new_seNames:
                    print(f"obj Label={obj.Label}, {propName}, no change, old_seNames=new_seNames={new_seNames}.")
                else:
                    print(f"obj Label={obj.Label}, {propName}, updating, old_seNames={old_seNames}, new_seNames={new_seNames}")
                    obj.Base = (baseObj, new_seNames )

                    # recompute whole doc after subelement change
                    # obj.recompute() # recomputing obj is not enough
                    doc = obj.Document
                    doc.recompute()

def update_objs_seName(objs, refreshCache=False):
    for obj in objs:
        update_obj_seName(obj, refreshCache=refreshCache)

def update_doc_seName(doc, refreshCache=False, debug=0):
    '''
    first sort all objects by dependency
    '''
    result = sort_objs_by_downstream(doc, useLabel=True, 
                                     objList=doc.Objects, # all objects. default to active obj only
                                     printDetail=debug,
                                     refreshCache=refreshCache,
                                     )
    for objLabel in result['ready_list']:
        obj = get_obj_by_objKey(doc, objLabel, useLabel=True) 
        update_obj_seName(obj, refreshCache=refreshCache)
