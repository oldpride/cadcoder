from pprint import pformat
import re
import traceback
import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.objtools import get_obj_by_objKey

infos_by_doc_triggerPropName = {}

class TriggeringFeature:
    def __init__(self, obj):
        obj.Proxy = self
        # self.doc = obj.Document # don't store doc reference as it cannot be serialized into json.
        self.docName = obj.Document.Name
        # self.Object = obj  # Store reference back to object
        
    def execute(self, obj):
        print("running TriggeringFeature.execute()")
        doc = obj.Document

        need_recompute = False
        for triggerPropName, infos in infos_by_doc_triggerPropName[self.docName].items():  
            for info in infos: 
                watchObjKey = info['watchObjKey']
                useLabel = info['useLabel']
                watchObj = get_obj_by_objKey(doc, watchObjKey, useLabel=useLabel)
                watchPropName = info['watchPropName']
                oldValue = info['value']
                newValue = getattr(watchObj, watchPropName)
                if newValue != oldValue:
                    need_recompute = True
                    print(f'Triggered by change in {watchObjKey}.{watchPropName} from {oldValue} to {newValue}')
                    info['value'] = newValue
                    info['triggerFunc'](doc, info, oldValue) 
        if need_recompute:
            print('Triggering recompute')

        sync_link(doc)
                
'''
triggerObj vs watchObj vs targetObj
- trigger obj is the object that will be recomputed when a watched property changes.
- watch obj is the object whose property is being watched for changes.
- target obj, if present, is the object that will be modified when the watched property changes.

trigger obj is an independent object in a document.
there only need on trigger object per document.
'''
triggerObj_by_doc = {}

def get_triggerObj(doc, triggerName=""):
    docName = doc.Name
    if docName in triggerObj_by_doc:
        triggerObj = triggerObj_by_doc[docName]
    else:
        if triggerName is None or triggerName == "":
            triggerName = 'trigger'
        triggerObj = doc.addObject('App::FeaturePython', triggerName)
        triggerObj_by_doc[docName] = triggerObj
        infos_by_doc_triggerPropName[docName] = {}
        TriggeringFeature(triggerObj)
    return triggerObj
    

def set_trigger(doc, watchObj, watchPropName, triggerFunc, useLabel, **opt):
    triggerObj = get_triggerObj(doc)
    watchObjKey = watchObj.Label if useLabel else watchObj.Name
    watchObjPropName = f'{watchObjKey}.{watchPropName}'
    triggerPropName = f'{watchObjKey}____{watchPropName}'
    # triggerPropName = watchObjPropName

    watchPropValue = getattr(watchObj, watchPropName)
    watchPropType = watchObj.getTypeIdOfProperty(watchPropName)
    triggerObjName = triggerObj.Name
    docName = doc.Name
    if triggerPropName not in infos_by_doc_triggerPropName[docName]:
        infos_by_doc_triggerPropName[docName][triggerPropName] = []
        triggerObj.addProperty(watchPropType, triggerPropName, 'Base', 'Trigger property')
        triggerObj.setExpression(triggerPropName, watchObjPropName)
        triggerObj.setEditorMode(triggerPropName, 0)  # Make the property editable in the property editor
    infos_by_doc_triggerPropName[docName][triggerPropName].append({
        'value': watchPropValue,
        'useLabel': useLabel,
        'watchObjKey': watchObjKey,
        'watchPropName': watchPropName,
        'watchPropType': watchPropType,
        'triggerPropName': triggerPropName,
        'triggerObjName': triggerObjName,
        'triggerFunc': triggerFunc,
        'opt': opt,
    })
    

def triggerFunc_set_target_value(doc, info, oldValue):
    targetObjKey = info['opt']['targetObjKey']
    targetPropName = info['opt']['targetPropName']
    useLabel = info['useLabel']
    targetObj = get_obj_by_objKey(doc, targetObjKey, useLabel=useLabel)
    value = info['value']
    print(f'Setting {targetObjKey}.{targetPropName} to {value}')
    set_prop_value(targetObj, targetPropName, value)

def link_watch_to_target(doc, watchObj, watchPropName, targetObj, targetPropName, useLabel):
    targetObjKey = targetObj.Label if useLabel else targetObj.Name
    watchObjKey = watchObj.Label if useLabel else watchObj.Name
    set_trigger(doc, watchObj, watchPropName, triggerFunc_set_target_value, useLabel, 
                # we have to convert obj to key because App::FeaturePython cannot
                # store objects in its properties - cannot serialize objects into json.             
                targetObjKey=targetObjKey, 
                targetPropName=targetPropName,
                linkType = 'simple',
                )
    watchValue = getattr(watchObj, watchPropName)
    targetValue = getattr(targetObj, targetPropName)
    if watchValue != targetValue:
        print(f'watch={watchObjKey}.{watchPropName}={watchValue} not match target={targetObjKey}.{targetPropName}={targetValue}')
        print(f"set target value to match watch value, {targetObjKey}.{targetPropName}={watchValue}")
        set_prop_value(targetObj, targetPropName, watchValue)
        # doc.recompute() # don't recompute for now as it may cause undesired side effects.

def sync_link(doc):
    # sync the value from the watch object to the target object.
    # the values can be out of sync if the target object was modified directly.
    docName = doc.Name
    for triggerPropName, infos in infos_by_doc_triggerPropName[docName].items():
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
            watchValue = getattr(watchObj, watchPropName)
            targetValue = getattr(targetObj, targetPropName)
            if watchValue != targetValue:
                print(f'watch={watchObj.Name}.{watchPropName}={watchValue} not match target={targetObj.Name}.{targetPropName}={targetValue}')
                print(f"set target value to match watch value, {targetObj.Name}.{targetPropName}={watchValue}")
                set_prop_value(targetObj, targetPropName, watchValue)

def set_prop_value(obj, propName, value):
    objType = obj.TypeId
    if objType == 'Spreadsheet::Sheet' and re.match(r'^[A-Z]\d+$', propName):
        obj.set(propName, value)
    else:
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

def parse_triggerPropName(triggerPropName):
    '''
    triggerPropName = f'{watchObjKey}____{watchPropName}'
    
    parse triggerPropName into watchObjKey, watchPropName.

    use the last occurrence of '____' to split the triggerPropName.
    '''
    parts = triggerPropName.rsplit('____', 1)
    watchObjKey = parts[0]
    watchPropName = parts[1]
    return watchObjKey, watchPropName

def parse_trigger_settings(doc, useLabel):
    '''
    return a dict of infos_by_triggerPropName
    '''
    docName = doc.Name
    infos_by_triggerPropName = {}
    # there should be only one trigger object per document, 
    #    - obj type is App::FeaturePython,
    #    - named 'trigger'.
    triggerObj = None
    for obj in doc.Objects:
        if obj.TypeId == 'App::FeaturePython' and obj.Label == 'trigger':
            triggerObj = obj
            break
    if triggerObj is None:
        return infos_by_triggerPropName
    
    triggerObjKey = triggerObj.Label if useLabel else triggerObj.Name
    
    from pdfclib.expressiontools import get_expInfo_by_objPropKey
    for propName in triggerObj.PropertiesList:
        # triggerProp is an expression
        expInfo = get_expInfo_by_objPropKey(doc, f'{triggerObjKey}.{propName}')
        if expInfo is not None:
            watchObjKey, watchPropName = parse_triggerPropName(propName)
            infos_by_triggerPropName[propName] = {
                'watchObjKey': watchObjKey,
                'watchPropName': watchPropName,
                'value': getattr(triggerObj, propName),
                'triggerFunc': triggerFunc_set_target_value,
                'opt': {
                    'targetObjKey': expInfo['objKey'],
                    'targetPropName': expInfo['propName'],
                    'linkType': 'simple',
                },
            }

def main():
    from pdfclib.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()

    useLabel = True
    
    def triggerFunc(doc, info, oldValue):
        print(f'Trigger function called, oldValue={oldValue}, info={pformat(info)}')
    
    # Example usage of setTrigger method
    watchObj = doc.addObject('PartDesign::Body', 'WatchObject')
    watchObj.addProperty('App::PropertyFloat', 'MyProperty', 'Base', 'MyDescription')
    watchObj.MyProperty = 10.0
    set_trigger(doc, watchObj, 'MyProperty', triggerFunc, useLabel)
    
    # Simulate a change in the watch object's property
    watchObj.MyProperty = 20.0
    
    doc.recompute()
 
if __name__ == "__main__":
    main()
