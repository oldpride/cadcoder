import traceback
import FreeCAD as App
import re

import Part
from FreeCAD import Vector, Placement, Rotation
import Sketcher
from pprint import pformat

from pdfclib.matchtools import match_key_startswith
from pdfclib.objtools import normalize_label

'''
how to get the property details in UI so that we can use them in our script?
    https://forum.freecad.org/viewtopic.php?style=5&t=98185
    for example, we want to find Binder.Support in UI is linked to Helix.
    to find the corresponding script code:
    select on Binder in the 3D view.
    Control+shift+P, this dumps the code into python console, commented out.
        >>> # doc = App.getDocument("o2p_test_partdesign_1_input")
        >>> # obj = doc.getObject("Binder")
        >>> # shp = obj.Shape
        >>> ### End command Std_SendToPythonConsole
    then we copy and paste to run the code:
        >>> doc = App.getDocument("o2p_test_partdesign_1_input")
        >>> obj = doc.getObject("Binder")
        >>> obj.Support
        [(<Part::PartFeature>, ('',))]
        >>> obj.Support[0]
        (<Part::PartFeature>, ('',))
        >>> obj.Support[0][0]
        <Part::PartFeature>
        >>> obj.Support[0][0].Name
        'Helix'
'''

def float2str(f):
    # reduce float precision to 4 decimal places so that comparison is easier
    return '{:.4f}'.format(f)

def rotation2str(r):
    # x, y, z, angle
    return(f"Rotation({float2str(r.Q[0])}, {float2str(r.Q[1])}, {float2str(r.Q[2])}, {float2str(r.Q[3])})")
    # return f'{r}'
    
def vec2str(v):
    return f'Vector({float2str(v.x)}, {float2str(v.y)}, {float2str(v.z)})'

def shape2str(shape):
    try:
        volume = float2str(shape.Volume)
    except:
        volume = "N/A"

    try:
        area = float2str(shape.Area)
    except:
        area = "N/A"

    # make mutable copy of shape to transform
    shape2 = shape.copy()
    try:
        # reset to original placement, so that bounds and centerOfMass are comparable
        shape2.transformShape(shape2.Placement.inverse().toMatrix(), True)
        bb = shape2.BoundBox
        bb_str = f"BoundBox({float2str(bb.XMin)}, {float2str(bb.YMin)}, {float2str(bb.ZMin)}) - ({float2str(bb.XMax)}, {float2str(bb.YMax)}, {float2str(bb.ZMax)})"
        centerOfMass = vec2str(shape2.CenterOfMass)
    except:
        bb_str = "N/A"
        centerOfMass = "N/A"

    # delete the mutable copy
    del shape2

    return f"# volume={volume}, area={area}, reset_bounds={bb_str}, reset_CenterOfMass={centerOfMass}"


def get_obj_varname(obj, useLabel):
    '''
    obj.Label vs obj.Name
        - obj.Name is the internal name of the object, it is unique in the document.
          it can be used to get the object via doc.getObject('Name').
          it cannot have spaces or special characters.

          reasons to use obj.Name:
            - expressionEngine uses obj.Name internally. 
        - obj.Label is the user-visible name of the object, it can be changed by user.
          it is not unique in the document.
          it can have spaces or special characters.
    '''

    # big decision here
    if useLabel:
        l = obj.Label

        # if we use obj.Name, then we don't need to replace forbidden characters.
        l = normalize_label(l)
    else:
        l = obj.Name
    
    return l

def objClassTree(obj, level=0):
    # max level to avoid infinite recursion
    if level > 5:
        print(f"Max recursion level reached at level {level}, obj={obj}")
        return
    
    # we only keep unique class names
    branches = set()
    myClassName = obj.__class__.__name__

    if isinstance(obj, list) or isinstance(obj, tuple):
        for o in obj:
            subBranches = objClassTree(o, level+1)
            for sb in subBranches:
                branch = f"{myClassName}/{sb}"
                branches.add(branch)
    
    if not branches:
        branches.add(myClassName)

    return branches

no_prefix_types = [
    # seen these in PartDesign Body. we don't need them because they are auto-created with new Body.
    # TypeId, Name Prefix
    ('App::Line', 'X_Axis'),
    ('App::Line', 'Y_Axis'),
    ('App::Line', 'Z_Axis'),
    ('App::Plane', 'XY_Plane'),
    ('App::Plane', 'XZ_Plane'),
    ('App::Plane', 'YZ_Plane'),
    ('App::Origin', 'Origin'),
]

def propValue2python(propValue, objectlist=None)->dict:
    # the propValue can be an FreeCAD object, a primitive type, a list, a tuple.

    # if thing is a property's value, it will have TypeId attribute
    TypeId = getattr(propValue, 'TypeId', None)
    className = propValue.__class__.__name__

    # print(f"obj2python: obj={obj}, TypeId={TypeId}, class={obj.__class__.__name__}")

    if objectlist is None:
        objectlist = []

    if propValue in objectlist:
        # if thing is a FreeCAD object, return the object reference
        normal = f"doc.getObject('{propValue.Name}')"
        
        if match_key_startswith(no_prefix_types, (propValue.TypeId, propValue.Name)):
            prefixed = f"doc.getObject('{propValue.Name}')"
        else:
            prefixed = f"doc.getObject(self.addPrefix('{propValue.Name}'))"

        return {'normal': normal, 'prefixed': prefixed}

    # how can I test if type(obj) is Base.Quantity ?
    if hasattr(propValue, 'Value') and hasattr(propValue, 'Unit'):
        normal = str(propValue.Value)
        return {'normal': normal, 'prefixed': normal}

    if isinstance(propValue, str):
        normal = f"'{propValue}'"
        return {'normal': normal, 'prefixed': normal}
    
    if isinstance(propValue, bool):
        normal = 'True' if propValue else 'False'
        return {'normal': normal, 'prefixed': normal}

    if isinstance(propValue, int):
        normal = str(propValue)
        return {'normal': normal, 'prefixed': normal}

    if isinstance(propValue, float):
         normal = float2str(propValue)
         return {'normal': normal, 'prefixed': normal}

    if TypeId == "Materials::Material":
        normal = f"App.Materials.getMaterial('{propValue.Name}')"
        prefixed = f"App.Materials.getMaterial(self.addPrefix('{propValue.Name}'))"
        return {'normal': normal, 'prefixed': prefixed}
        
    if isinstance(propValue, App.Matrix):
        normal = f'App.Matrix({propValue.A11}, {propValue.A12}, {propValue.A13}, {propValue.A14}, {propValue.A21}, {propValue.A22}, {propValue.A23}, {propValue.A24}, {propValue.A31}, {propValue.A32}, {propValue.A33}, {propValue.A34}, {propValue.A41}, {propValue.A42}, {propValue.A43}, {propValue.A44})'
        return {'normal': normal, 'prefixed': normal}
    
    if TypeId == "App::Line": # GeoFeature object
        # print(f"TypeId={TypeId}, Name={obj.Name}, Placement={obj.Placement}")
        normal = f'App.Line({propValue2python(propValue.Placement)["normal"]})'
        return {'normal': normal, 'prefixed': normal}
     
    if TypeId == "App::Plane": # GeoFeature object
        normal = f'App.Plane({propValue2python(propValue.Placement)["normal"]})'
        return {'normal': normal, 'prefixed': normal}
    
    if isinstance(propValue, Part.ArcOfEllipse):
        normal = f'Part.ArcOfEllipse({propValue2python(propValue.Ellipse)["normal"]}, {propValue.FirstParameter}, {propValue.LastParameter})'
        return {'normal': normal, 'prefixed': normal}
    if isinstance(propValue, Part.ArcOfParabola):
        normal = f'Part.ArcOfParabola({propValue2python(propValue.Parabola)["normal"]}, {propValue.FirstParameter}, {propValue.LastParameter})'
        return {'normal': normal, 'prefixed': normal}
    if isinstance(propValue, Part.ArcOfHyperbola):
        normal = f'Part.ArcOfHyperbola({propValue2python(propValue.Hyperbola)["normal"]}, {propValue.FirstParameter}, {propValue.LastParameter})'
        return {'normal': normal, 'prefixed': normal}
    if isinstance(propValue, Part.ArcOfCircle):
        normal = f'Part.ArcOfCircle({propValue2python(propValue.Circle)["normal"]}, {propValue.FirstParameter}, {propValue.LastParameter})'
        return {'normal': normal, 'prefixed': normal}

    if isinstance(propValue, Part.BSplineCurve):
        poles = ''
        komma = False
        for p in propValue.getPoles():
            if komma:
                poles += ', '
            poles += vec2str(p)
            komma = True

        normal = f'Part.BSplineCurve([{poles}])'
        return {'normal': normal, 'prefixed': normal}
    
    if isinstance(propValue, Sketcher.Constraint):
        args = []
        for attr in ["First", "FirstPos", "Second", "SecondPos", 
                    "Third", "ThirdPos", "Fourth", "FourthPos"]:
            if hasattr(propValue, attr):
                val = getattr(propValue, attr)
                if val != -1:
                    args.append(str(val))
        
        if hasattr(propValue, "Value"):
            args.append(str(propValue.Value))

        normal = f'Sketcher.Constraint("{propValue.Type}", {", ".join(args)})'
        return {'normal': normal, 'prefixed': normal}
    
    if isinstance(propValue, Part.Circle):
        normal = f'Part.Circle({vec2str(propValue.Center)}, {propValue.Axis}, {float2str(propValue.Radius)})'
        return {'normal': normal, 'prefixed': normal}
    if isinstance(propValue, Part.Ellipse):
        # normal = f'Part.Ellipse({vec2str(propValue.Center)}, {propValue.MajorRadius}, {propValue.MinorRadius})'
        # Part.Ellipse(App.Vector(0.000000, 30.103247, 0.000000), App.Vector(-11.649301, 0.000000, 0.000000), App.Vector(0.000000, 0.000000, 0.000000))
        # MajorRadiusVector, MinorRadiusVector, center

        MajorRadiusVector = propValue.XAxis * propValue.MajorRadius
        MinorRadiusVector = propValue.YAxis * propValue.MinorRadius
        normal = f'Part.Ellipse({vec2str(MajorRadiusVector)}, {vec2str(MinorRadiusVector)}, {vec2str(propValue.Center)})'
        
        return {'normal': normal, 'prefixed': normal}
    
    if isinstance(propValue, Part.Hyperbola):
        normal = f'Part.Hyperbola({vec2str(propValue.Center)}, {propValue.MajorRadius}, {propValue.MinorRadius})'
        return {'normal': normal, 'prefixed': normal}
    if isinstance(propValue, Part.LineSegment):
        normal = f'Part.LineSegment({propValue.StartPoint}, {propValue.EndPoint})'
        return {'normal': normal, 'prefixed': normal}

    if isinstance(propValue, Part.Parabola):
        normal = f'Part.Parabola({vec2str(propValue.Focus)}, {vec2str(propValue.Location)}, {vec2str(propValue.Axis)})'
        return {'normal': normal, 'prefixed': normal}
    
    if isinstance(propValue, Part.Point):
        normal = f'Part.Point(Vector({float2str(propValue.X)}, {float2str(propValue.Y)}, {float2str(propValue.Z)}))'
        return {'normal': normal, 'prefixed': normal}
    # if TypeId in ["Part::Helix", "PartDesign::Body"]:
    if className in ["Body", "Feature", "PrimitivePy", "SketchObject"]:
        normal = f"doc.getObject('{propValue.Name}')"
        prefixed = f"doc.getObject(self.addPrefix('{propValue.Name}'))"
        return {'normal': normal, 'prefixed': prefixed}
    
    if TypeId == "Part::PropertyPartShape" or TypeId == "Part::TopoShape":
        '''
        Part::PropertyPartShape vs Part::TopoShape
            - Part::PropertyPartShape is used as property type of FreeCAD objects, e.g. Shape property of Part::Feature
              Part::PropertyPartShape holds a Part::TopoShape instance as its value.
              obj.getTypeIdOfProperty('Shape') returns 'Part::PropertyPartShape'
            - Part::TopoShape is used as the actual shape object, e.g. returned by obj.Shape.
              Part::TopoShape is C++ implemented.
              obj.getTypeIdOfProperty('Shape').TypeId returns 'Part::TopoShape'
        '''
        normal = shape2str(propValue)
        return {'normal': normal, 'prefixed': normal}
    
    if isinstance(propValue, Placement):
        normal = f'Placement({propValue2python(propValue.Base)["normal"]}, {propValue2python(propValue.Rotation)["normal"]})'
        return {'normal': normal, 'prefixed': normal}
    
    if isinstance(propValue, Rotation):
        normal = rotation2str(propValue)
        return {'normal': normal, 'prefixed': normal}
    
    if isinstance(propValue, Vector):
        normal = vec2str(propValue)
        return {'normal': normal, 'prefixed': normal}

    liststart = ''
    if isinstance(propValue, list):
        liststart = '['
        listend = ']'

    if isinstance(propValue, tuple):
        liststart = '('
        listend = ')'

    if liststart != '':
        # elements = [obj2python(e, objectlist) for e in obj]
        # normal = liststart + ', '.join(elements[0]) + listend
        # prefixed = liststart + ', '.join(elements[1]) + listend
        # return (normal, prefixed)
        normal = liststart
        prefixed = liststart
        n_list = []
        p_list = []
        for e in propValue:
            n= propValue2python(e, objectlist)['normal']
            p= propValue2python(e, objectlist)['prefixed']
            n_list.append(n)
            p_list.append(p)

        normal += ', '.join(n_list) + listend
        prefixed += ', '.join(p_list) + listend
        return {'normal': normal, 'prefixed': prefixed}

    # all the rest
    normal = str(propValue)
    return {'normal': normal, 'prefixed': normal}

# Cf. https://github.com/FreeCAD/FreeCAD/blob/278ce803907ef72548d7ac761613038ac435c481/src/App/Property.h#L60
statuslist = [
        'Immutable', 1,
        'ReadOnly', 2,
        'PropReadOnly', 24,
        'PropOutput', 27,
]

def propIsReadonly(obj, propName, debug=0):
    # AttributeError: Property container has no property 'AngularDeflection'
    statusnums = obj.getPropertyStatus(propName)
    for status in statuslist:
        if status in statusnums:
            return True
    return False

propInfo_by_doc_obj_propname = {}

def get_prop_info(doc,
                  obj, 
                  propName, 
                  objectlist=None, # feed to obj2python to avoid recursion
                  extraAttrs=None, # extra attributes of the property to get
                    debug=0,
                    useLabel=True, # use obj.Label instead of obj.Name to represent object
                    refreshCache=False,

                    # whether include extended properties
                    extended = False,
                  ):
    '''
    extraAttrs: list of extra attributes of the property to get.
        note: attributes are not property names.
        default attributes are 
            PropType, valueTypeId, valueObjName, readonly, valuePython, valueClass, valueClass
        extraAttrs can be a string or a list of strings.
            'attr1,attr2'
            ['attr1', 'attr2']


    '''

    # objName = obj.Name
    # Error: 'xxx.ViewProviderSheet' object has no attribute 'Name'
    if hasattr(obj, 'Name'):
        objName = obj.Name
        objId = objName
    else:
        objName = None
        objId = str(id(obj))
    docKey = f"{doc.Name},{id(doc)}"

    if docKey not in propInfo_by_doc_obj_propname:
        propInfo_by_doc_obj_propname[docKey] = {}
    if objId not in propInfo_by_doc_obj_propname[docKey]:
        propInfo_by_doc_obj_propname[docKey][objId] = {}
    if propName in propInfo_by_doc_obj_propname[docKey][objId] and not refreshCache:
        return propInfo_by_doc_obj_propname[docKey][objId][propName]
    
    info = {
        "propName": propName,
    }
    propInfo_by_doc_obj_propname[docKey][objId][propName] = info

    # print(f"Getting property '{propName}' of obj Label='{obj.Label}' in document Label='{doc.Label}'...")

    try:
        if extended:
            propValue = get_extended_prop_by_name(obj, propName)
        else:
            # the following are the same
            propValue = getattr(obj, propName)
            # propValue = obj.getPropertyByName(propName)
    except:
        propValue = None
    info["propValue"] = propValue

    '''
    propType vs valueTypeId
        - propType is get from obj.getTypeIdOfProperty(propName).
          it is FreeCAD property type.
          it is used hold valueTypeId instance.
        - valueTypeId is get from propValue.TypeId.
          sometimes it is C++ class type of the actual value held by the property.
          if valueTypeId is None, then propValue is likely a primitive type (int, float, str, bool).
    '''
    try:
        info["valueTypeId"] = propValue.TypeId
    except:
        info["valueTypeId"] = None

    try:
        info["propType"] = obj.getTypeIdOfProperty(propName)
    except:
        info["propType"] = None

    try:
        info["valueObjName"] = propValue.Name
    except:
        info["valueObjName"] = None

    try:
        info["readonly"] = propIsReadonly(obj, propName)
    except:
        info["readonly"] = None
    
    info["valuePython"] = propValue2python(propValue, objectlist)['normal']
    info["prefixPython"] = propValue2python(propValue, objectlist)['prefixed']

    info["valueClass"] = propValue.__class__.__name__
    info["valueClassTree"] = objClassTree(propValue)

    if extraAttrs is not None:
        if isinstance(extraAttrs, str):
            extraAttrs = extraAttrs.split(',')
        for attr in extraAttrs:
            if attr == 'dir':
                try:
                    info['dir'] = dir(propValue)
                except:
                    info['dir'] = None
                continue
            else:
                try:
                    info[attr] = getattr(propValue, attr)
                except:
                    info[attr] = None

    if obj.TypeId == "Spreadsheet::Sheet":
        # if obj is spreadsheet, get cell content
        try:
            content = obj.getContents(propName)
            info['cellContent'] = content
        except:
            pass
        # also get cell alias
        try:
            alias = obj.getAlias(propName)
            info['cellAlias'] = alias
        except:
            pass
    
    # # get expression if any
    # # get this object's App.Document, 
    # # obj -> Gui.Document -> App.Document
    # doc = obj.Document  # this may be the Gui.Document

    # # if doc is Gui.Document, it will have another 'Document' attribute, to get its App.Document
    # if hasattr(doc, 'Document'):
    #     doc = doc.Document

    # ViewObject does not have Name attribute. therefore, we need to handle exception here.
    if objName is not None:
        objKey = objName if not useLabel else obj.Label
        objPropKey = f"{objKey}.{propName}"
    
        from pdfclib.expressiontools import get_expInfo_by_objPropKey # we import here to avoid circular import
        exprInfo = get_expInfo_by_objPropKey(doc, objPropKey, useLabel=useLabel)
        if exprInfo is not None:
            info['expInfo'] = exprInfo
    
    try:
        propInfo_by_doc_obj_propname[docKey][objId][propName] = info
    except KeyError as e:
        msg = f"KeyError: get_prop_info: doc='{docKey}', objId='{objId}', prop='{propName}'"
        print(msg)
        traceback.print_stack()
        raise RuntimeError(msg)
    return info

def add_intent(s:str, indentcount:int=0, indent=""):
    if not indent:
        indent = '    ' * indentcount
    lines = s.splitlines()
    indented_lines = [indent + line for line in lines]
    return '\n'.join(indented_lines)

def get_prop_info_str(propInfo:dict, indent="", printDetail=False)->str:
    ret_str = ""
    basicKeys = ["propType", "propValue", "valueTypeId", "valueClass", "valueClassTree", "valueObjName", "readonly","valuePython"]
    for key in sorted(basicKeys):   
        if key in propInfo:
            str2 = f"{indent}{key}: {propInfo[key]}"
            ret_str += str2 + "\n"
            if printDetail:
                print(str2)
    for key in sorted(propInfo.keys()):
        if key not in basicKeys:
            if isinstance(propInfo[key], (list, dict)):
                indent_pformat = add_intent(pformat(propInfo[key]), indent=indent+"    "*3)
                str2 = f"{indent}{key}:\n{indent_pformat}"
                ret_str += str2 + "\n"
                if printDetail:
                    print(str2)
            else:
                str2 = f"{indent}{key}: {propInfo[key]}"
                ret_str += str2 + "\n"
                if printDetail:
                    print(str2)
    return ret_str

def print_prop_info(propInfo, indent=""):
    get_prop_info_str(propInfo, indent=indent, printDetail=True)

tmpSuffix = 'TmpDefault'
def cleanTmpObj(doc):
    '''
    remove all temporary default objects created for comparison.
    '''
    toRemove = []
    for obj in doc.Objects:
        if obj.Name.endswith(tmpSuffix):
            toRemove.append(obj.Name)
    
    for name in toRemove:
        # print(f"Removing temporary default object: {name}")
        doc.removeObject(name)

compare_obj_prop_with_default_by_obj = {}

def compare_obj_prop_with_default(
        doc, 
        obj1, 
        useLabel, # use obj.Label instead or obj.Name to represent object
        propPattern=None, 
        extraAttrs=None,

        # whether toremove the temporary default object after comparison.
        # if we need to access the temporary default object's properties later, we should keep it.
        # then we need to clean up later using cleanTmpObj(doc).
        keepTmpObj=False, 

        # whether to include extended properties, e.g. Spreadsheet cell aliases, Sketcher constraints.
        extended = False,        
        ):
    '''
    also check whether the prop is added, ie, not in the default object of the same type.
    '''
    obj_id = id(obj1)    
    try:
        return compare_obj_prop_with_default_by_obj[obj_id]
    except:
        pass


    # create a temp default object so that we can find out which prop is added or modified
    defaultObjName = obj1.Name + tmpSuffix
    obj2 = doc.addObject(obj1.TypeId, defaultObjName)
    allObjs = doc.Objects

    # recompute can trigger errors for some object types, e.g. Pad without linked sketch
    # but they are harmless, though very scary to see.
    # doc.recompute()

    compare_result1 = compare_objects(
        doc, 
        obj1, 
        obj2, 
        propPattern=propPattern, 
        extraAttrs=extraAttrs,
        objectlist=allObjs,
        removeString=tmpSuffix,
        useLabel=useLabel, 
        extended=extended,
    )

    compare_result2 = compare_objects(
        doc, 
        obj1.ViewObject, 
        obj2.ViewObject, 
        propPattern=propPattern, 
        extraAttrs=extraAttrs,
        objectlist=allObjs,
        useLabel=useLabel,
    )

    summary_result = {
        'MainObject': compare_result1,
        'ViewObject': compare_result2,
    }

    if not keepTmpObj:
        doc.removeObject(defaultObjName)

    compare_obj_prop_with_default_by_obj[obj_id] = summary_result

    return summary_result

def compare_objects(
        doc, 
        obj1, 
        obj2, 
        propPattern=None, 
        extraAttrs=None,
        objectlist=None,
        removeString=None, # eg, remove tmpDefault from string comparison
        debug=0,
        useLabel=True, # use obj.Label instead of obj.Name to represent object

        # whether to include extended properties, e.g. Spreadsheet cell aliases, Sketcher constraints.
        extended=False,
        ):
    compare_result = {}

    # list all properties of the body
    if extended:
        propNames1 = get_extended_propNames(obj1)
        propNames2 = get_extended_propNames(obj2)
    else:
        propNames1 = obj1.PropertiesList
        propNames2 = obj2.PropertiesList

    # print(f"{obj.Name} has {len(propNames)} properties:")
    for propName in propNames1:
        if propPattern is not None:
            if not re.search(propPattern, propName, re.IGNORECASE):
                continue
        info1 = get_prop_info(doc, obj1, propName, objectlist, 
                              extraAttrs=extraAttrs, useLabel=useLabel, extended=extended)
        info2 = get_prop_info(doc, obj2, propName, objectlist, 
                              extraAttrs=extraAttrs, useLabel=useLabel, extended=extended)

        OnePropResult = {
            'subStatus': None,
        }

        if propName not in propNames2:
            OnePropResult.update({
                'changeStatus': 'added',
                'info1': info1,
            })
        elif info1['propValue'] == info2['propValue']:
            OnePropResult.update({
                'changeStatus': 'equal',
                'subStatus': 'identical',
                'info1': info1,
            })
        else:
            if removeString is not None:
                for attr in ['propValue', 'valuePython']:
                    if isinstance(info2[attr], str):
                        old = info2[attr]
                        new = old.replace(removeString, '')
                        if old != new:
                            info2[attr] = new
                            if debug:
                                print(f"replaced {obj2.Name}.{propName} {attr} from={old} to={new}")

            if info1['valueClassTree'] == info2['valueClassTree'] and info1['valuePython'] == info2['valuePython']:
            # and str(info1['propValue']) == str(info2['propValue']) and info1['valuePython'] == info2['valuePython']:
                OnePropResult.update({
                    'changeStatus': 'equal',
                    'subStatus': 'different_address',
                    'info1': info1,
                    'info2': info2,
                })
            else:
                OnePropResult.update({
                    'changeStatus': 'modified',
                    'info1': info1,
                    'info2': info2,
                })

        compare_result[propName] = OnePropResult

    # add removed properties
    for propName in propNames2:
        if propPattern is not None:
            if not re.search(propPattern, propName, re.IGNORECASE):
                continue
        if propName not in propNames1:
            info2 = get_prop_info(doc, obj2, propName, objectlist, extraAttrs=extraAttrs)
            OnePropResult = {
                'changeStatus': 'removed',
                'subStatus': None,
                'info2': info2,
            }
            compare_result[propName] = OnePropResult

    return compare_result

def dump_obj_props(doc, obj, useLabel, 
                   propPattern=None, 
                   extraAttrs=None,
                   extended=False,
                   ):
    '''
    dump all properties of obj, comparing with default object of the same type.
    '''
    App.Console.PrintMessage(f"obj Label='{obj.Label}', Name={obj.Name}, TypeId={obj.TypeId}\n")

    compare_result = compare_obj_prop_with_default(
        doc, obj, useLabel=useLabel, 
        propPattern=propPattern, extraAttrs=extraAttrs, 
        keepTmpObj=True, # we will clean up after we using the tmp object's properties.
        extended=extended,
        )
    for typeKey in ['MainObject', 'ViewObject']:
        print(f"{obj.Name} has {len(compare_result[typeKey])} properties:")
        for propName in sorted(compare_result[typeKey].keys()):
            root= compare_result[typeKey][propName]
            indent = '    '
            changeStatus = root['changeStatus']
            subStatus = root['subStatus']
            print(f"{indent}{changeStatus.replace('equal', 'default')}: {typeKey}-{propName}" + (f" ({subStatus})" if subStatus else ""))
            if changeStatus == 'equal' or changeStatus == 'added':
                print(f"{indent}  Object value:")
                print_prop_info(root['info1'], indent*2)
            elif changeStatus == 'removed':
                print(f"{indent}  Default value:")
                print_prop_info(root['info2'], indent*2)
            elif changeStatus == 'modified':
                print(f"{indent}  Object value:")
                print_prop_info(root['info1'], indent*2)
                print(f"{indent}  Default value:")
                print_prop_info(root['info2'], indent*2)
            print()
        print()

    cleanTmpObj(doc)
            

original_props_by_doc_obj = {}
extended_props_by_doc_obj = {}

def get_docObjPropDict(doc, refreshCache=False, extended=False, useLabel=False):
    '''
    get all properties of all objects in doc
    return a dict of objName -> propName -> propInfo
    ---
    useLabel: if True, use object labels instead of names as keys
    '''

    if extended:
        props_by_doc_obj = extended_props_by_doc_obj
    else:
        props_by_doc_obj = original_props_by_doc_obj

    docKey = f"{doc.Name},{id(doc)}"
    if docKey in props_by_doc_obj and not refreshCache:
        return props_by_doc_obj[docKey]
    
    props_by_doc_obj[docKey] = {}

    for obj in doc.Objects:
        if useLabel:
            objKey = obj.Label
        else:
            objKey = obj.Name

        # print(f"objKey={objKey}, TypeId={obj.TypeId}, Label={obj.Label}")

        props_by_doc_obj[docKey][objKey] = get_obj_props(doc, obj, 
                                                          refreshCache=refreshCache,
                                                          extended = extended,
                                                          useLabel=useLabel
                                                          )

    return props_by_doc_obj[docKey]

def diff_docObjPropDicts(docObjPropDict1, docObjPropDict2, 
                      propPattern=None, 
                      propIgnore=None,
                      diffOnly=False,
                      printDetail=False,
                      ):
    allObjKeys = set(docObjPropDict1.keys()).union(set(docObjPropDict2.keys()))
    allObjKeys = sorted(allObjKeys)
    # print(f"allObjKeys={allObjKeys}")

    differences = []

    for objKey in allObjKeys:
        objPropDict1 = docObjPropDict1.get(objKey, None)
        objPropDict2 = docObjPropDict2.get(objKey, None)

        indent = '    '
        if objPropDict1 is None:
            if printDetail:
                print(f"{indent}obj in doc2 but not in doc1: {objKey}")
            diff2 = diff_objPropDicts({}, objPropDict2, propPattern=propPattern, propIgnore=propIgnore, diffOnly=diffOnly, printDetail=printDetail)
            objKey1 = None
            objKey2 = objKey
        elif objPropDict2 is None:
            if printDetail:
                print(f"{indent}obj in doc1 but not in doc2: {objKey}")
            diff2 = diff_objPropDicts(objPropDict1, {}, propPattern=propPattern, propIgnore=propIgnore, diffOnly=diffOnly, printDetail=printDetail)   
            objKey1 = objKey
            objKey2 = None  
        else:
            if printDetail:
                print(f"{indent}comparing obj: {objKey}")
            diff2 = diff_objPropDicts(objPropDict1, objPropDict2, propPattern=propPattern, propIgnore=propIgnore, diffOnly=diffOnly, printDetail=printDetail)
            objKey1 = objKey
            objKey2 = objKey
        # insert objKey into each difference entry
        for d in diff2:
            d['objKey1'] = objKey1
            d['objKey2'] = objKey2
            differences.append(d)
    return differences

def get_obj_props(doc,obj, refreshCache=False, extended=False, useLabel=False):
    '''
    get all properties of obj
    return a dict of propName -> propInfo
    '''
    docKey = f"{doc.Name},{id(doc)}"
    if useLabel:
        objKey = obj.Label
    else:
        objKey = obj.Name

    if extended:
        props_by_doc_obj = extended_props_by_doc_obj
    else:
        props_by_doc_obj = original_props_by_doc_obj

    if docKey not in props_by_doc_obj:
        props_by_doc_obj[docKey] = {}
    if objKey in props_by_doc_obj[docKey] and not refreshCache:
        return props_by_doc_obj[docKey][objKey]
    
    props_by_doc_obj[docKey][objKey] = {}

    # print(f"Getting properties of obj Label='{obj.Label}' in document Label='{doc.Label}'...")

    propDict = {}

    if extended:
        propNames = get_extended_propNames(obj)
    else:
        propNames = obj.PropertiesList

    for propName in propNames:  
        obj_info = get_prop_info(doc, obj, propName, refreshCache=refreshCache, extended=extended)
        propDict[propName] = obj_info

    props_by_doc_obj[docKey][objKey] = propDict # cache it

    return propDict
    

def diff_obj_props(doc1, doc2, obj1, obj2, 
                   propPattern=None, refreshCache=False, diffOnly=False, extended=False, printDetail=True):
    '''
    compare properties of obj1 in doc1 against obj2 in doc2
    '''
    propDict1 = get_obj_props(doc1, obj1, refreshCache=refreshCache, extended=extended)
    propDict2 = get_obj_props(doc2, obj2, refreshCache=refreshCache, extended=extended)

    # print(f"propDict1={pformat(propDict1)}")
    # print(f"propDict2={pformat(propDict2)}")

    return diff_objPropDicts(propDict1, propDict2, propPattern=propPattern, diffOnly=diffOnly, printDetail=printDetail)

def diff_objPropDicts(propDict1, propDict2, 
                      propPattern=None, propIgnore=None, diffOnly=False, printDetail=False):
    allPropNames = set(propDict1.keys()).union(set(propDict2.keys()))
    allPropNames = sorted(allPropNames)

    differences = []

    for propName in allPropNames:
        # print(f"Comparing property: {propName}")
        if propPattern is not None:
            if not re.search(propPattern, propName, re.IGNORECASE):
                continue
        if propIgnore is not None:
            if re.search(propIgnore, propName, re.IGNORECASE):
                continue
        # print(f"propName={propName}")
        obj1_info = propDict1.get(propName, None)
        obj2_info = propDict2.get(propName, None)

        indent = '    '
        if obj1_info is None:
            print(f"{indent}obj1: {propName}")
            if printDetail:
                print_prop_info(obj2_info, indent*2)
            differences.append({'propName': propName, 'changeStatus': 'added', 'info1': None, 'info2': obj2_info})
        elif obj2_info is None:
            print(f"{indent}obj2: {propName}")
            if printDetail:
                print_prop_info(obj1_info, indent*2)
            differences.append({'propName': propName, 'changeStatus': 'removed', 'info1': obj1_info, 'info2': None})
        else:
            # both exist
            if obj1_info['propValue'] == obj2_info['propValue']:
                # identical
                if printDetail and not diffOnly:
                    print(f"{indent}same {propName} (identical address or value):")
                    print_prop_info(obj1_info, indent*2)
                differences.append({'propName': propName, 'changeStatus': 'same', 'info1': obj1_info, 'info2': obj2_info})
            else:
                if obj1_info['propType'] != obj2_info['propType'] or obj1_info.get('valueTypeId', None) != obj2_info.get('valueTypeId', None) or obj1_info.get('valuePython', None) != obj2_info.get('valuePython', None):
                    if printDetail:
                        print(f"{indent}different {propName}")
                        print(f"{indent}  obj1:")
                        print_prop_info(obj1_info, indent*2)
                        print(f"{indent}  obj2:")
                        print_prop_info(obj2_info, indent*2)
                    differences.append({'propName': propName, 'changeStatus': 'modified', 'info1': obj1_info, 'info2': obj2_info})
                else:
                    # now type, dump, ptyhon are all the same

                    if (obj1_info['propType'] is not None
                        and (obj1_info.get('valueTypeId', None) is not None or propName == "Constraints") 
                        and obj1_info.get('valuePython', None) is not None
                        ):
                        # if we have meaningfully propType, valueTypeId, valuePython, 
                        # then they are effectively the same
                        if printDetail and not diffOnly:
                            print(f"{indent}same {propName} (different address):")
                            print_prop_info(obj1_info, indent*2)
                        differences.append({'propName': propName, 'changeStatus': 'same', 'info1': obj1_info, 'info2': obj2_info})
                    # elif obj1_info['propType'] == "Part::PropertyPartShape":
                    #     shape1 = obj1_info['propValue']
                    #     shape2 = obj2_info['propValue']

                    #     # make mutable copy of shapes to transform
                    #     shape1 = shape1.copy()
                    #     shape2 = shape2.copy()
                    #     # Move shapes to a common placement (origin)
                    #     shape1.transformShape(shape1.Placement.inverse().toMatrix(), True)
                    #     shape2.transformShape(shape2.Placement.inverse().toMatrix(), True)

                    #     # Perform a boolean 'common' (intersection) operation
                    #     common_shape = shape1.common(shape2)

                    #     v1 = float3f(shape1.Volume)
                    #     v2 = float3f(shape2.Volume)
                    #     vcommon = float3f(common_shape.Volume)
                    #     print(f"{indent}  obj1 volume: {v1}")
                    #     print(f"{indent}  obj2 volume: {v2}")
                    #     print(f"{indent}  common volume: {vcommon}")

                    #     # Compare the volume of the intersection to the original volume
                    #     if vcommon == v1 and vcommon == v2:
                    #         print(f"{indent}same {propName} (different address/placement):")
                    #         print_prop_info(obj1_info, indent*2)
                    #     else:
                    #         print(f"{indent}different: {propName}")
                    #         print(f"{indent}  obj1:")
                    #         print_prop_info(obj1_info, indent*2)
                    #         print(f"{indent}  obj2:")
                    #         print_prop_info(obj2_info, indent*2)
                    else:
                        if printDetail:
                            print(f"{indent}todo: {propName}")
                            print(f"{indent}  obj1:")
                            print_prop_info(obj1_info, indent*2)
                            print(f"{indent}  obj2:")
                            print_prop_info(obj2_info, indent*2)
                        differences.append({'propName': propName, 'changeStatus': 'todo', 'info1': obj1_info, 'info2': obj2_info})

    return differences
                            
def str_mm_to_in(mm_str: str) -> str:
    '''
    convert a string like '2.032 mm' to '0.08 in'
    '''
    if m := re.match(r'^\s*([0-9.+-eE]+)\s*mm\s*$', str(mm_str)):
        # use str() to handle Base.Quantity type
        mm_value = float(m.group(1))
        in_value = mm_value / 25.4
        in_str = f"{in_value} in"
        return in_str
    else:
        msg = f"str_mm_to_in: cannot parse mm_str={mm_str}. returning original string."
        print(msg)
        return mm_str


def get_param_value(
        propInfo,    # propInfo
        isForFuncParam, # is this used as a function parameter or a cell value
                     # if isFuncParam is True, numberic value should not be quoted.
                     # else, it should be quoted.
        preferInchUnit, # if True, convert Quantity in mm to in
        ) -> str: # always return a string becuase we will use it in generated code (string).
    pass

    '''
    example of a pure number, eg, float
        added: MainObject-B3
            Object value:
            propType: App::PropertyFloat
            propValue: 1.1982
            valueTypeId: None
            valueClass: float
            valueClassTree: {'float'}
            valueObjName: None
            readonly: True
            valuePython: 1.1982
            propName: B3
            prefixPython: 1.1982
            cellContent: 1.1982
            cellAlias: horizontalScale

    example of a Quantity with unit, 
    note that propValue is 2.032 mm while cellContent is =0.08 in.
    '0.08 in' is more desireable as function parameter because it preserves the unit.
        added: MainObject-B5
            Object value:
            propType: Spreadsheet::PropertySpreadsheetQuantity
            propValue: 2.032 mm
            valueTypeId: None
            valueClass: Quantity
            valueClassTree: {'Quantity'}
            valueObjName: None
            readonly: True
            valuePython: 2.032
            propName: B5
            prefixPython: 2.032
            cellContent: =0.08 in
            cellAlias: femaleOD_wall
            expInfo:
                            {'parents': [],
                            'expression': '0.08 in',
                            'grounded': True,
                            'prefixedExp': '0.08 in',
                            'rawExpression': '0.08 in',
                            'source': 'SpreadsheetCell'}
                        
    example of an expression depending on other cells:
        added: MainObject-B6
            Object value:
            propType: Spreadsheet::PropertySpreadsheetQuantity
            propValue: 12.0015 mm
            valueTypeId: None
            valueClass: Quantity
            valueClassTree: {'Quantity'}
            valueObjName: None
            readonly: True
            valuePython: 12.0015
            propName: B6
            prefixPython: 12.0015
            cellContent: =femaleOD_wall * 2 + <<npt_m_spec>>.RealOD
            cellAlias: femaleOD_spec
            expInfo:
                            {'parents': ['npt_f_callsheet.femaleOD_wall', 'npt_m_spec.RealOD'],
                            'expression': 'femaleOD_wall * 2 + <<npt_m_spec>>.RealOD',
                            'grounded': False,
                            'prefixedExp': "femaleOD_wall * 2 + <<{self.addPrefix('npt_m_spec')}>>.RealOD",
                            'rawExpression': 'femaleOD_wall * 2 + <<npt_m_spec>>.RealOD',
                            'source': 'SpreadsheetCell'}
    '''
    valueClass = propInfo['valueClass']
    if valueClass == 'float' or valueClass == 'int' or valueClass == 'bool':
        if isForFuncParam:
            return str(propInfo['propValue'])
        else:
            return f"'{propInfo['propValue']}'"
    elif valueClass == 'str':
        # return f"'{propInfo['propValue']}'"
        # escape single quote
        escaped_propValue = propInfo['propValue'].replace("'", "\\'")
        return f"'{escaped_propValue}'"
    elif valueClass == 'Quantity':
        # Quantity always needs to be quoted, because it has a unit. eg '0.08 in'
        if isForFuncParam:
            equal_sign = ''
        else:
            equal_sign = '='

        if 'cellContent' in propInfo:
            # source is from spreadsheet cell,
            grounded = False
            try:
                expInfo = propInfo['expInfo']
            except KeyError:
                # when running get_obj_all_expInfo() with includeGrounded=False,
                # 'expInfo' will be missing for grounded expression.
                msg = f"propInfo {propInfo['propName']} missing expInfo. likely a grounded expression."
                print(msg)
                grounded = True

            if grounded or propInfo['expInfo']['grounded']:
                # grounded expression, use cellContent, eg, =0.08 in
                # we prefer cellContent over propValue because cellContent preserves the unit.
                # '0.08 in' vs '2.032 mm'
                return f"'{equal_sign}{propInfo['cellContent'].lstrip('=')}'"
            else:
                # ungrounded expression, use propValue,
                # even though it loses unit, but at least it is a static value; it will
                # be overridden later when expression is set.
                if preferInchUnit:
                    in_str = str_mm_to_in(propInfo['propValue'])
                    return f"'{equal_sign}{in_str}'"
                else:
                    return f"'{equal_sign}{propInfo['propValue']}'"
        else:
            # source is not from spreadsheet cell, use propValue
            return f"'{equal_sign}{propInfo['propValue']}'"

def get_extended_prop_by_name(obj, anyName):
    '''
    this is an extended function of obj.getPropertyByName(propName),
    which accepts both property name and property alias (in Spreadsheet object).
    '''
    if anyName in obj.PropertiesList:
        propName = anyName
        return obj.getPropertyByName(propName)
    elif obj.TypeId == "Spreadsheet::Sheet":
        try: 
            propName = obj.getCellFromAlias(anyName)
            return obj.getPropertyByName(propName)
        except Exception:
            propName = None
    elif obj.TypeId == "Sketcher::SketchObject":
        if re.fullmatch(r'Constraints\[\d+\]', anyName):
            # we can get the constraint prop from Contraint property or ExpressionEngine property.
            # using the ExpressionEngine property is easier.
            #    [('Constraints[10]', '<<NPT_M_Dimension_Spreadsheet>>.thread_cutter_side'), 
            #    ('Constraints[11]', '<<NPT_M_Dimension_Spreadsheet>>.thread_start_r')]
            for row in obj.ExpressionEngine:
                varName = row[0]
                if varName == anyName:
                    expression = row[1]
                    return expression

    raise ValueError(f"Cannot find property/alias/constraint='{anyName}' in object '{obj.Name}'")
    

def get_extended_propNames(obj, propPattern=None):
    '''
    this is an extended function of obj.PropertiesList,
    which includes both property names and property aliases (in Spreadsheet object).
    '''
    if propPattern is not None:
        propList = [propName for propName in obj.PropertiesList if re.search(propPattern, propName, re.IGNORECASE)]
    else:
        propList = list(obj.PropertiesList)

    # get Spreadsheet's cell aliases. Cells are already included in PropertiesList.
    if obj.TypeId == "Spreadsheet::Sheet":
        for propName in obj.PropertiesList:
            if not re.fullmatch(r"[A-Z]\d+", propName):
                # only consider cell properties
                continue
            try:
                alias = obj.getAlias(propName)
            except Exception:
                continue 
            if alias is not None:
                if alias in propList:
                    continue
                if propPattern is not None and not re.search(propPattern, alias, re.IGNORECASE):
                    continue
                propList.append(alias)  
    '''
    get Sketcher constraints names that in its ExpressionEngine.
    modified: MainObject-ExpressionEngine
    Object value:
        propType: App::PropertyExpressionEngine
        propValue: [('Constraints[10]', '<<NPT_M_Dimension_Spreadsheet>>.thread_cutter_side'), 
        ('Constraints[11]', '<<NPT_M_Dimension_Spreadsheet>>.thread_start_r')]
        valueTypeId: None
        valueClass: list
        valueClassTree: {'list/tuple/str'}
        valueObjName: None
        readonly: False
        valuePython: [('Constraints[10]', '<<NPT_M_Dimension_Spreadsheet>>.thread_cutter_side'), 
        ('Constraints[11]', '<<NPT_M_Dimension_Spreadsheet>>.thread_start_r')]
        propName: ExpressionEngine
    '''
    if obj.TypeId == "Sketcher::SketchObject":
        for row in obj.ExpressionEngine:
            varName = row[0]
            if m := re.match(r'(Constraints\[\d+\])', varName):
                constraintName = m.group(1)
                if propPattern is not None and not re.search(propPattern, alias, re.IGNORECASE):
                    continue
                propList.append(constraintName)
    return propList

'''
using npt_m_sketch as example

from contraint_dump.py
06:13:21  constraints.append(Sketcher.Constraint('Coincident', 0, 2, 1, 1, -2000, 0, 0.0)) # constraint1
06:13:21  constraints.append(Sketcher.Constraint('Coincident', 1, 2, 2, 1, -2000, 0, 0.0)) # constraint2
06:13:21  constraints.append(Sketcher.Constraint('Coincident', 2, 2, 0, 1, -2000, 0, 0.0)) # constraint3
06:13:21  constraints.append(Sketcher.Constraint('PointOnObject', 1, 2, 0, -2000, 0, 0.0)) # constraint4
06:13:21  constraints.append(Sketcher.Constraint('DistanceY', 1, 1, 1, 2, -2000, 0, App.Units.Quantity('2.787950382608695 mm'))) # constraint5
06:13:21  constraints.append(Sketcher.Constraint('DistanceX', 1, 1, 2, -2000, 0, App.Units.Quantity('24.78491959518692 mm'))) # constraint6
06:13:21  constraints.append(Sketcher.Constraint('Vertical', 1, 0, -2000, 0, -2000, 0, 0.0)) # constraint7
06:13:21  constraints.append(Sketcher.Constraint('Angle', 2, 2, 1, -2000, 0, App.Units.Quantity('30.000070153049904 deg'))) # constraint8
06:13:21  constraints.append(Sketcher.Constraint('Angle', 0, 1, 2, 2, -2000, 0, App.Units.Quantity('60.00014030609981 deg'))) # constraint9

from prop_dump.py
06:14:42      modified: MainObject-Constraints
06:14:42        Object value:
06:14:42          propType: Sketcher::PropertyConstraintList
06:14:42          propValue: [<Constraint 'Coincident'>, <Constraint 'Coincident'>, <Constraint 'Coincident'>, <Constraint 'PointOnObject' (1,-1)>, <Constraint 'DistanceY'>, <Constraint 'DistanceX'>, <Constraint 'Vertical' (1)>, <Constraint 'Angle'>, <Constraint 'Angle'>]
06:14:42          readonly: False
06:14:42          valueClass: list
06:14:42          valueClassTree: {'list/Constraint'}
06:14:42          valueObjName: None
06:14:42          valuePython: [<Constraint 'Coincident'>, <Constraint 'Coincident'>, 
                                <Constraint 'Coincident'>, <Constraint 'PointOnObject' (1,-1)>, 
                                <Constraint 'DistanceY'>, <Constraint 'DistanceX'>, 
                                <Constraint 'Vertical' (1)>, <Constraint 'Angle'>, 
                                <Constraint 'Angle'>]
06:14:42          valueTypeId: None
06:14:42          prefixPython: [<Constraint 'Coincident'>, <Constraint 'Coincident'>, 
                                <Constraint 'Coincident'>, <Constraint 'PointOnObject' (1,-1)>, 
                                <Constraint 'DistanceY'>, <Constraint 'DistanceX'>, 
                                <Constraint 'Vertical' (1)>, <Constraint 'Angle'>, 
                                <Constraint 'Angle'>]
06:14:42          propName: Constraints
06:14:42        Default value:
06:14:42          propType: Sketcher::PropertyConstraintList
06:14:42          propValue: []
06:14:42          readonly: False
06:14:42          valueClass: list
06:14:42          valueClassTree: {'list'}
06:14:42          valueObjName: None
06:14:42          valuePython: []
06:14:42          valueTypeId: None
06:14:42          prefixPython: []
06:14:42          propName: Constraints
06:14:42  
06:14:42      added: MainObject-Constraints[4]
06:14:42        Object value:
06:14:42          propType: None
06:14:42          propValue: <<npt_m_callsheet>>.thread_cutter_side
06:14:42          readonly: None
06:14:42          valueClass: str
06:14:42          valueClassTree: {'str'}
06:14:42          valueObjName: None
06:14:42          valuePython: '<<npt_m_callsheet>>.thread_cutter_side'
06:14:42          valueTypeId: None
06:14:42          expInfo:
                    {'comment': 'ExpressionEngine expressions are all ungrounded',
                     'expression': '<<npt_m_callsheet>>.thread_cutter_side',
                     'grounded': False,
                     'parents': ['npt_m_callsheet.thread_cutter_side'],
                     'prefixedExp': "<<{self.addPrefix('npt_m_callsheet')}>>.thread_cutter_side",
                     'rawExpression': '<<npt_m_callsheet>>.thread_cutter_side',
                     'source': 'ExpressionEngine',
                     'varName': 'Constraints[4]'}
06:14:42          prefixPython: '<<npt_m_callsheet>>.thread_cutter_side'
06:14:42          propName: Constraints[4]

from geometry_dump.py
06:18:15    EndPoint: Vector(24.7849, -2.7880, 0.0000)
06:18:15    StartPoint: Vector(22.3705, -1.3940, 0.0000)
06:18:15    TypeId: Part::GeomLineSegment
06:18:15  
06:18:15    EndPoint: Vector(24.7849, 0.0000, 0.0000)
06:18:15    StartPoint: Vector(24.7849, -2.7880, 0.0000)
06:18:15    TypeId: Part::GeomLineSegment
06:18:15  
06:18:15    EndPoint: Vector(22.3705, -1.3940, 0.0000)
06:18:15    StartPoint: Vector(24.7849, 0.0000, 0.0000)
06:18:15    TypeId: Part::GeomLineSegment

from sketcher_dump.py
06:32:30  geo0 = npt_m_sketch.addGeometry(Part.LineSegment(Vector (22.37049056648515, -1.393975191304347, 0.0), Vector (24.78491959518692, -2.787950382608695, 0.0)))
06:32:30  geo1 = npt_m_sketch.addGeometry(Part.LineSegment(Vector (24.78491959518692, -2.787950382608695, 0.0), Vector (24.78491959518692, 0.0, 0.0)))
06:32:30  geo2 = npt_m_sketch.addGeometry(Part.LineSegment(Vector (24.78491959518692, 0.0, 0.0), Vector (22.37049056648515, -1.3939751913043474, 0.0)))
06:32:30  npt_m_sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 2, geo1, 1))
06:32:30  npt_m_sketch.addConstraint(Sketcher.Constraint('Coincident', geo1, 2, geo2, 1))
06:32:30  npt_m_sketch.addConstraint(Sketcher.Constraint('Coincident', geo2, 2, geo0, 1))
06:32:30  npt_m_sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo1, 2, -1))
06:32:30  npt_m_sketch.addConstraint(Sketcher.Constraint('DistanceY', geo1, 1, geo1, 2, 2.7880))
06:32:30  npt_m_sketch.addConstraint(Sketcher.Constraint('DistanceX', -1, 1, geo1, 2, 24.7849))
06:32:30  npt_m_sketch.addConstraint(Sketcher.Constraint('Vertical', geo1))
06:32:30  npt_m_sketch.addConstraint(Sketcher.Constraint('Angle', -1, 2, geo2, 1, 0.5236))
06:32:30  npt_m_sketch.addConstraint(Sketcher.Constraint('Angle', geo0, 1, geo2, 2, 1.0472))

ideally our extended prop for constraints should use sketcher_dump.py's style.
'''
