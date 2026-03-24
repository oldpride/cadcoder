from pprint import pformat
import re
import traceback
import FreeCAD as App
import FreeCADGui as Gui


# from cadcoder.objtools import get_obj_by_objKey, get_obj_str, map_obj_name_label

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


triggerVersion = 1.0 
# compatibility check:
# if the triggerVersion in code (here) is different from the triggerVersion in the trigger object, 
# then we have a compatibility issue.

class TriggeringFeature:
    def __init__(self, obj):
        '''
        self is python object.
        obj is the FreeCAD object.
        '''
        obj.Proxy = self  # set the proxy to this python object
        # self.doc = obj.Document # don't store doc reference as it cannot be serialized into json.

        # for obj.TypeId == 'App::FeaturePython', we store data in the obj.Proxy directly,
        # no need to store it in a dedicated property.
        # We can only store simple data types in obj.Proxy, such as int, float, str, dict, list, 
        # but not FreeCAD objects or complex data structures, because obj.Proxy needs to be 
        # serializable into json for it to be saved in the document.

        self.docName = obj.Document.Name
        # self.Object = obj  # Store reference back to object
        self.info_by_watchObjPropName_targetObjPropName = {}
        self.triggerVersion = triggerVersion
        
        
    def execute(self, obj):
        print("running TriggeringFeature.execute()")
        doc = obj.Document

        if self.info_by_watchObjPropName_targetObjPropName:
            # refresh obj_name_label map
            map_obj_name_label(doc, refreshCache=True)

        for watchObjPropName, info_by_targetObjPropName in self.info_by_watchObjPropName_targetObjPropName.items():  
            for targetObjPropName, info in info_by_targetObjPropName.items()    : 
                watchObjKey, watchPropName = watchObjPropName.split('.', 1)
                targetObjKey = info['targetObjKey']
                useLabel = info['useLabel']
                watchObj = get_obj_by_objKey(doc, watchObjKey, useLabel=useLabel)
                targetObj = get_obj_by_objKey(doc, targetObjKey, useLabel=useLabel)
                targetPropName = info['targetPropName']
                oldWatchValueStr = info['valueStr']

                newWatchValue = get_prop_value(watchObj, watchPropName)
                targetValue = get_prop_value(targetObj, targetPropName)
                newWatchValueStr = f"{newWatchValue}"
                if newWatchValueStr != oldWatchValueStr:
                    print(f'Triggered by change in {watchObjPropName} from {oldWatchValueStr} to {newWatchValueStr}')
                    info['valueStr'] = newWatchValueStr
                if newWatchValue != targetValue:
                    print(f'Setting {targetObjKey}.{targetPropName} to {newWatchValue}')
                    set_prop_value(targetObj, targetPropName, newWatchValue)
                
'''
triggerObj vs watchObj vs targetObj
- trigger obj is the object that will be recomputed when a watched property changes.
- watch obj is the object whose property is being watched for changes.
- target obj, if present, is the object that will be modified when the watched property changes.

trigger obj is an independent object in a document.
there only need on trigger object per document.
'''

triggerObj_by_doc = {}

def get_triggerObj(doc, triggerName="trigger", create=True):
    docName = doc.Name 
    docKey = f"{docName},{id(doc)}"
    # because for tmp document, the doc object may be different each time, even though the doc.Name is the same,
    # we need to use doc's obj address as key.
    docKey = f"{docName},{id(doc)}"
    if docKey in triggerObj_by_doc:
        triggerObj = triggerObj_by_doc[docKey]
    else:
        triggerObj_by_doc[docKey] = None # placeholder, prevent from repeated searchs

        # try to find an existing trigger object
        # there should be only one trigger object per document, 
        #    - obj type is App::FeaturePython,
        #    - named 'trigger'.
        triggerObj = None
        for obj in doc.Objects:
            if obj.TypeId == 'App::FeaturePython' and obj.Label == 'trigger':
                triggerObj = obj
                break
        if triggerObj is not None:
            triggerObj_by_doc[docKey] = triggerObj
            # check trigger version compatibility
            versionInObj = getattr(triggerObj.Proxy, 'triggerVersion', None)
            if versionInObj != triggerVersion:
                raise RuntimeError(f"Trigger version mismatch. versionInCode={triggerVersion}, versionInObject={getattr(triggerObj.Proxy, 'triggerVersion', None)}. need to regenerate the document from python.")
        elif create:
            if triggerName is None or triggerName == "":
                triggerName = 'trigger'
            triggerObj = doc.addObject('App::FeaturePython', triggerName)
            triggerObj_by_doc[docKey] = triggerObj
            # infos_by_doc_triggerPropName[docName] = {}
            TriggeringFeature(triggerObj)
        else:
            triggerObj = None
    return triggerObj

def link_watch_to_target(doc, watchObj, watchPropName, targetObj, targetPropName, useLabel):
    targetObjKey = targetObj.Label if useLabel else targetObj.Name
    watchObjKey = watchObj.Label if useLabel else watchObj.Name

    watchObjPropName = f'{watchObjKey}.{watchPropName}'
    watchPropValue = get_prop_value(watchObj, watchPropName)
    watchPropType = watchObj.getTypeIdOfProperty(watchPropName)

    triggerObj = get_triggerObj(doc)

    updated = 0

    if watchObjPropName not in triggerObj.Proxy.info_by_watchObjPropName_targetObjPropName:
        updated = 1
        triggerObj.Proxy.info_by_watchObjPropName_targetObjPropName[watchObjPropName] = {}
        triggerPropName = watchObjPropName.replace('.', '_')
        triggerObj.addProperty(watchPropType, triggerPropName, "Base", f"trigger for {watchObjPropName}")
        triggerObj.setExpression(triggerPropName, watchObjPropName)
        triggerObj.setEditorMode(triggerPropName, 0)  # Make the property editable in the property editor

    targetObjPropName = f'{targetObjKey}.{targetPropName}'
    try:
        # targetPropValue = getattr(targetObj, targetPropName)
        targetPropValue = get_prop_value(targetObj, targetPropName)
    except Exception as e:
        targetPropValue = None

    '''
    triggerObj.Proxy.info_by_watchObjPropName_targetObjPropName must be serializable into json, 
    so we cannot store the actual watchPropValue if it's not json serializable, such as Quantity.

    This is why we have
        'valueStr': f"{watchPropValue}",
    instead of
        'value': watchPropValue,

    otherwise, we will get error like below when try to save the doc.

    19:11:59  PropertyPythonObject::toString(): failed for <class 'cadcoder.triggertools.TriggeringFeature'>
    19:11:59  pyException: Traceback (most recent call last):
    File "C:\Program Files\FreeCAD 1.0\bin\Lib\json\__init__.py", line 231, in dumps
        return _default_encoder.encode(obj)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "C:\Program Files\FreeCAD 1.0\bin\Lib\json\encoder.py", line 200, in encode
        chunks = self.iterencode(o, _one_shot=True)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "C:\Program Files\FreeCAD 1.0\bin\Lib\json\encoder.py", line 258, in iterencode
        return _iterencode(o, 0)
            ^^^^^^^^^^^^^^^^^
    File "C:\Program Files\FreeCAD 1.0\bin\Lib\json\encoder.py", line 180, in default
        raise TypeError(f'Object of type {o.__class__.__name__} '
    <class 'TypeError'>: Object of type Quantity is not JSON serializable

    '''

    if targetObjPropName not in triggerObj.Proxy.info_by_watchObjPropName_targetObjPropName[watchObjPropName]:
        updated = 1
        triggerObj.Proxy.info_by_watchObjPropName_targetObjPropName[watchObjPropName][targetObjPropName]={
            'valueStr': f"{watchPropValue}", # convert to string to make it json serializable, 
            'useLabel': useLabel,
            'watchObjKey': watchObjKey,
            'watchObjName': watchObj.Name,
            'watchObjLabel': watchObj.Label,
            'watchPropName': watchPropName,
            'watchPropType': watchPropType,
            'targetObjKey': targetObjKey,
            'targetObjName': targetObj.Name,
            'targetObjLabel': targetObj.Label,
            'targetPropName': targetPropName,   
        }
    else:
        print(f"Link already exists for watchObjPropName={watchObjPropName} targetObjPropName={targetObjPropName}")

    if watchPropValue != targetPropValue:
        print(f'watch={watchObjKey}.{watchPropName}={watchPropValue} not match target={targetObjKey}.{targetPropName}={targetPropValue}')
        print(f"set target value to match watch value, {targetObjKey}.{targetPropName}={watchPropValue}")
        set_prop_value(targetObj, targetPropName, watchPropValue)
        # doc.recompute() # don't recompute for now as it may cause undesired side effects.
    return updated

def sync_link(doc):
    # sync the value from the watch object to the target object.
    # the values can be out of sync if the target object was modified directly.
    docName = doc.Name
    triggerObj = get_triggerObj(doc)
    for triggerPropName, infos in triggerObj.Proxy.infos_by_triggerPropName.items():
        for info in infos:
            if 'targetObjKey' not in info:
                continue
            if info['opt']['linkType'] != 'simple':
                continue
            watchObjKey = info['watchObjKey']
            useLabel = info['useLabel']
            watchObj = get_obj_by_objKey(doc, watchObjKey, useLabel=useLabel)
            watchPropName = info['watchPropName']
            targetObjKey = info['opt']['targetObjKey']
            targetPropName = info['opt']['targetPropName']
            targetObj = get_obj_by_objKey(doc, targetObjKey, useLabel=useLabel)
            # watchValue = getattr(watchObj, watchPropName)
            # targetValue = getattr(targetObj, targetPropName)
            watchValue = get_prop_value(watchObj, watchPropName)
            targetValue = get_prop_value(targetObj, targetPropName)
            if watchValue != targetValue:
                print(f'watch={watchObj.Name}.{watchPropName}={watchValue} not match target={targetObj.Name}.{targetPropName}={targetValue}')
                print(f"set target value to match watch value, {targetObj.Name}.{targetPropName}={watchValue}")
                set_prop_value(targetObj, targetPropName, watchValue)

def get_prop_value(obj, propName):
    objType = obj.TypeId
    if objType == 'Spreadsheet::Sheet':
        if re.match(r'^[A-Z]\d+$', propName):
            # this is a cell address. 
            # propValue = getattr(obj, propName) # getattr() does not work for cell address like 'B2'
            try:
                propValue = obj.get(propName)
            except Exception as e:
                propValue = None
            return propValue
        elif not hasattr(obj, propName):
            # this is an alias
            cellAddr = obj.getCellFromAlias(propName)
            try:
                propValue = obj.get(cellAddr)
            except Exception as e:
                propValue = None
            return propValue
        # now this is a regular property, we will handle it like other normal objects using getattr().
    
    try:
        propValue = getattr(obj, propName)
    except Exception as e:
        propValue = None
    return propValue

def set_prop_value(obj, propName, value):
    objType = obj.TypeId
    if objType == 'Spreadsheet::Sheet': 
        if re.match(r'^[A-Z]\d+$', propName):
            # this is a cell address
            obj.set(propName, f"{value}")
            return
        elif not hasattr(obj, propName):
            # this is an alias, we need to get the cell address first
            cellAddr = obj.getCellFromAlias(propName)
            if not cellAddr:
                msg=f"{get_obj_str(obj)} does not have a property or a cell alias named '{propName}'"
                print(msg)
                raise ValueError(msg)
            # setattr(obj, cellAddr, value) will not work.
            #     AttributeError: 'Spreadsheet.Sheet' object has no attribute 'B2'
            # because setattr() only works on existing properties. 
            # To add new property, we need obj.addProperty() first.
            # For Spreadsheet obj, Spreadsheet.set() will insert new cell and set value at the same time.
            obj.set(cellAddr, f"{value}")
            return
        # now this is a regular property, we can set it directly.
        # we will handle it like other normal objects using setattr().

    try:
        setattr(obj, propName, value)
    except TypeError as e:
        propType = obj.getTypeIdOfProperty(propName)
        propValue = getattr(obj, propName)
        msg = f" (property type: {propType}, propValue old={propValue}, new={value})"
        traceback.print_stack()
        print(f"TypeError: {msg}")
        raise TypeError(f"Cannot set property {propName} of type={propType} to value={value}")
    except ValueError as e:
        traceback.print_stack()
        propType = obj.getTypeIdOfProperty(propName) 
        if propType == 'App::PropertyEnumeration':
            validValues = obj.getEnumerationsOfProperty(propName)
            print(f"propName={propName}, propType={propType}, validValues={validValues}, you entered value={value}") 
            raise ValueError(f"Invalid value for enumeration property {propName}")
        else:
            raise ValueError(f"Cannot set property {propName} of type={propType} to value={value}")

def get_trigger_info(doc):
    triggerObj = get_triggerObj(doc, create=False)
    if triggerObj is None:
        return {}   
    return triggerObj.Proxy.info_by_watchObjPropName_targetObjPropName
    
    
def dump_trigger_info(doc):
    info_by_watchObjPropName_targetObjPropName = get_trigger_info(doc)
    print("Trigger Infos:")
    print(pformat(info_by_watchObjPropName_targetObjPropName)) 

def trigger_fix_objNames(doc, dryrun=False):
    '''
    if trigger infos are stored using obj Names, but the obj name can be changed 
    when user modifies the document. Normally the obj Label is more stable.
    Therefore, from time to time, we need to set the obj Names to real obj Names in the document.
    - targetObjName
    - watchObjName
    {'npt_m_callsheet.nominalOD': [{'targetObjKey': 'npt_m_spec',
                                'targetObjLabel': 'npt_m_spec',
                                'targetObjName': 'Spreadsheet001',
                                'targetPropName': 'nominalOD',
                                'useLabel': True,
                                'value': '`3/4',
                                'watchObjKey': 'npt_m_callsheet',
                                'watchObjLabel': 'npt_m_callsheet',
                                'watchObjName': 'Spreadsheet',
                                'watchPropName': 'nominalOD',
                                'watchPropType': 'App::PropertyString'}]}
    '''

    triggerObj = get_triggerObj(doc, create=False)
    if triggerObj is None:
        print("No trigger object found.")
        return
    
    info_by_watchObjPropName_targetObjPropName = triggerObj.Proxy.info_by_watchObjPropName_targetObjPropName
    for watchObjPropName, info_by_targetObjPropName in info_by_watchObjPropName_targetObjPropName.items():
        for targetObjPropName, info in info_by_targetObjPropName.items():
            useLabel = info['useLabel']
            watchObjLabel = info['watchObjLabel']
            targetObjLabel = info['targetObjLabel']
            watchObj = get_obj_by_objKey(doc, watchObjLabel, useLabel=True)
            targetObj = get_obj_by_objKey(doc, targetObjLabel, useLabel=True)
            if watchObj is not None:
                old_watchObjName = info['watchObjName']
                new_watchObjName = watchObj.Name
                if old_watchObjName != new_watchObjName:
                    if not dryrun:
                        info['watchObjName'] = new_watchObjName
                        print(f"Updated watchObjName from {old_watchObjName} to {new_watchObjName}")
                    else:
                        print(f"[dryrun] Would update watchObjName from {old_watchObjName} to {new_watchObjName}")
                else:
                    print(f"watchObjName={old_watchObjName} is up to date.")
            if targetObj is not None:
                old_targetObjName = info['targetObjName']
                new_targetObjName = targetObj.Name
                if old_targetObjName != new_targetObjName:
                    if not dryrun:
                        info['targetObjName'] = new_targetObjName
                        print(f"Updated targetObjName from {old_targetObjName} to {new_targetObjName}")
                    else:
                        print(f"[dryrun] Would update targetObjName from {old_targetObjName} to {new_targetObjName}")
                else:
                    print(f"targetObjName={old_targetObjName} is up to date.")

def main():
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()

    useLabel = True

    
    # Example usage of setTrigger method
    watchObj = doc.addObject('PartDesign::Body', 'WatchObject')
    watchObj.addProperty('App::PropertyFloat', 'MyProperty', 'Base', 'MyDescription')
    watchObj.MyProperty = 10.0
    
    targetObj = doc.addObject('PartDesign::Body', 'TargetObject')
    targetObj.addProperty('App::PropertyFloat', 'MyTargetProp', 'Base', 'MyDescription')
    targetObj.MyTargetProp = 0.0

    link_watch_to_target(doc, watchObj, 'MyProperty',  targetObj, 'MyTargetProp', useLabel)
    
    # Simulate a change in the watch object's property
    watchObj.MyProperty = 20.0
    
    doc.recompute()
 
if __name__ == "__main__":
    main()
