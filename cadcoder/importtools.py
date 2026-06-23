import re
import json
from cadcoder.matchtools import match_key_startswith
from cadcoder.doctools import diff_docs, recreate_tmp_doc
from cadcoder.objtools import get_obj_pythonSource, skip_objTypeIdNamePattern
import traceback
import FreeCAD as App
import FreeCADGui as Gui


def get_top_callsheets_using_import(doc):
    '''
    top callsheets are callsheets whose pythonSource's importerInstanceName is empty
    '''
    top_callsheets = []
    for obj in doc.Objects:
        if obj.TypeId == 'Spreadsheet::Sheet' and 'callsheet' in obj.Label:
            pythonSource_str = getattr(obj, 'pythonSource', '{}')
            pythonSource = json.loads(pythonSource_str)
            importerInstanceName = pythonSource.get('importerInstanceName', None)
            if not importerInstanceName:
                # print(f"pythonSource = {pythonSource}")
                # print(f"importerInstanceName = {importerInstanceName}")
                top_callsheets.append(obj)
    return top_callsheets

def get_top_classsName_using_import(doc):
    top_callsheets = get_top_callsheets_using_import(doc)
    if not top_callsheets:
        return doc.Label
    else:
        top_callsheet = top_callsheets[0]
        pythonSource_str = getattr(top_callsheet, 'pythonSource', '{}')
        pythonSource = json.loads(pythonSource_str)
        topClassName = pythonSource.get('className', None)
        if not topClassName:
            return doc.Label
        else:
            return topClassName
    
importInfo_by_doc = {}

def map_importInfo(doc, 
                   topClassName: str=None, 
                   printDetail: bool=False,
                   keyPattern: str=None,
                   )->dict:
    
    # because we create tmp docs with same Name but different id,
    # we need to use doc id to distinguish different docs with same Name
    docKey = f"{doc.Name},{id(doc)}"
    if docKey in importInfo_by_doc:
        return importInfo_by_doc[docKey]

    if topClassName is None:
        topClassName = get_top_classsName_using_import(doc)
    print(f"Using topClassName={topClassName} to map doc import")

    import_by_key = {
        'directlyImportedObjs': [],
        'indirectlyImportedObjs': [],
        'notImportedObjs': [],
        'directlyImportedObjs_by_instName': {},
        'indirectlyImportedObjs_by_instName': {},
        'directlyImportedInstInfo_by_InstName': {},
        'indirectlyImportedInstInfo_by_InstName': {},
        'importedObjs_by_instChain': {},
        'importedDescendants_by_instChain': {},
        'importedDescendantCallsheets_by_instChain': {},
        'importerCallParams_by_instChain': {},
        'className_by_instChain': {},
        'moduleName_by_instChain': {},
        'objPrefix_by_instChain': {},
        'importedObjNames': [],
        'instanceName_by_objName': {},
        'importedInstChain_by_objName': {},
        'directlyImportedInstanceChains': set(),
        'directlyImportedCallsheet_by_instName': {},
        'directlyImportedCallsheetCallParamValues_by_instName': {},
    }

    for obj in sorted(doc.Objects, key=lambda o: o.Name):
        if not hasattr(obj, 'pythonSource'):
            import_by_key['notImportedObjs'].append(obj)
            continue

        pythonSource = json.loads(obj.pythonSource)
        className = pythonSource['className']
        try:
            importerCallParams = pythonSource['importerCallParams']
        except:
            importerCallParams = "{}"
        importerClassName = pythonSource['importerClassName']
        instanceName = pythonSource['instanceName']
        instanceChain = pythonSource['instanceChain']

        if instanceChain not in import_by_key['importerCallParams_by_instChain']:
            # import_by_key['importerCallParams_by_instChain'][instanceChain] = json.loads(importerCallParams)
            import_by_key['importerCallParams_by_instChain'][instanceChain] = importerCallParams
            # print(f"Found importerCallParams for instanceChain={instanceChain}: {importerCallParams}")

        if instanceChain not in import_by_key['className_by_instChain']:
            import_by_key['className_by_instChain'][instanceChain] = className
        if instanceChain not in import_by_key['moduleName_by_instChain']:
            import_by_key['moduleName_by_instChain'][instanceChain] = pythonSource['moduleName']
        if instanceChain not in import_by_key['objPrefix_by_instChain']:
            import_by_key['objPrefix_by_instChain'][instanceChain] = pythonSource['objPrefix']

        import_by_key['instanceName_by_objName'][obj.Name] = instanceName
        # print(f"mapped obj Name={obj.Name} to instanceName={instanceName}")
        if instanceChain not in import_by_key['importedObjs_by_instChain']:
            import_by_key['importedObjs_by_instChain'][instanceChain] = []
        import_by_key['importedObjs_by_instChain'][instanceChain].append(obj)

        # add obj to importedDescendants_by_instChain at current chain and each parent chain
        chain = instanceChain
        while chain != '':
            if chain not in import_by_key['importedDescendants_by_instChain']:
                import_by_key['importedDescendants_by_instChain'][chain] = []
            import_by_key['importedDescendants_by_instChain'][chain].append(obj)
            if chain not in import_by_key['importedDescendantCallsheets_by_instChain']:
                import_by_key['importedDescendantCallsheets_by_instChain'][chain] = []
            if obj.TypeId == 'Spreadsheet::Sheet' and 'callsheet' in obj.Label:
                import_by_key['importedDescendantCallsheets_by_instChain'][chain].append(obj)
            if '.' in chain:
                chain = '.'.join(chain.split('.')[:-1])
            else:
                chain = ''

        if className is None or className == '' or className == topClassName:
            import_by_key['notImportedObjs'].append(obj)
        else:
            if className.lower() == topClassName.lower():
                raise RuntimeError(f"obj Label={obj.Label}'s className={className} matches topClassName={topClassName} but has wrong case.")
            import_by_key['importedObjNames'].append(obj.Name)
            import_by_key['importedInstChain_by_objName'][obj.Name] = instanceChain

            if importerClassName == topClassName:
                import_by_key['directlyImportedObjs'].append(obj)
                if instanceName not in import_by_key['directlyImportedObjs_by_instName']:
                    import_by_key['directlyImportedObjs_by_instName'][instanceName] = []
                import_by_key['directlyImportedObjs_by_instName'][instanceName].append(obj)

                import_by_key['directlyImportedInstInfo_by_InstName'][instanceName] = pythonSource

                import_by_key['directlyImportedInstanceChains'].add(instanceChain)    

                if obj.Name.endswith('callsheet') and obj.TypeId == 'Spreadsheet::Sheet':
                    import_by_key['directlyImportedCallsheet_by_instName'][instanceName] = obj
                    from cadcoder.callsheettools import get_callParamValues
                    callParamValues = get_callParamValues(obj)
                    import_by_key['directlyImportedCallsheetCallParamValues_by_instName'][instanceName] = callParamValues
            else:
                import_by_key['indirectlyImportedObjs'].append(obj)
                if instanceName not in import_by_key['indirectlyImportedObjs_by_instName']:
                    import_by_key['indirectlyImportedObjs_by_instName'][instanceName] = []
                import_by_key['indirectlyImportedObjs_by_instName'][instanceName].append(obj)
                
                import_by_key['indirectlyImportedInstInfo_by_InstName'][instanceName] = pythonSource
                
    importInfo_by_doc[docKey] = import_by_key

    if printDetail:
        print(f"doc Label={doc.Label}, Name={doc.Name}, topClassName={topClassName}")
        
        def print_obj(obj, indentCount=0):
            try:
                pythonSource = json.loads(obj.pythonSource)
                className = pythonSource.get('className', None)
                importerClassName = pythonSource.get('importerClassName', None) 
            except:
                className = None
                importerClassName = None
            print(f"{'    ' * indentCount}Label={obj.Label}, Name={obj.Name}, TypeId={obj.TypeId}, className={className}, importerClassName={importerClassName}")

        def print_info(info, indentCount=0):
            for key in sorted(info.keys()):
                print(f"{'    ' * indentCount}{key}: {info[key]}")

        def print_objNames(objNames, indentCount=0):
            objs = [ doc.getObject(objName) for objName in objNames ]
            for obj in sorted(objs, key=lambda obj: obj.Label):
                print_obj(obj, indentCount=indentCount)

        for key in sorted(import_by_key.keys()):
            if keyPattern is not None and not re.search(keyPattern, key, re.IGNORECASE):
                continue

            print(f"{key}:")
            value = import_by_key[key]

            if re.search('objs$', key, re.IGNORECASE):
                # list of objects
                objects = value
                for obj in sorted(objects, key=lambda obj: obj.Label):
                    print_obj(obj, indentCount=1)
            elif re.search('objs_by_', key, re.IGNORECASE):
                # dict of objects
                for key2 in sorted(value.keys()):
                    objects = value[key2]
                    print(f"    {key2}:")
                    for obj in sorted(objects, key=lambda obj: obj.Label):
                        print_obj(obj, indentCount=2)
            elif re.search('info_by_', key, re.IGNORECASE):
                # dict of info
                for key2 in sorted(value.keys()):
                    info = value[key2]
                    print(f"    {key2}")
                    print_info(info, indentCount=2)
            elif re.search('objnames$', key, re.IGNORECASE):
                print_objNames(value, indentCount=1)
            elif re.search('_by_objName$', key, re.IGNORECASE):
                objNames = value.keys()
                objs = [doc.getObject(objName) for objName in objNames]
                for obj in sorted(objs, key=lambda obj: obj.Label):
                    print(f"    obj Label={obj.Label}, Name={obj.Name}, {value[obj.Name]}")
            else:
                print(f"    {key}: {value}")
            print()

    return import_by_key
            
def get_importedDescendants_by_instanceChain(doc, instanceChain):
    import_by_key = map_importInfo(doc)
    importedDescendants_by_instChain = import_by_key['importedDescendants_by_instChain']
    return importedDescendants_by_instChain[instanceChain]

def compare_import_with_default(doc, obj=None, instanceChain=None, instanceName = None,
                                    allObjects=False, # all objs in the instanceChain of the obj (above)
                                    diffOnly=False, commOnly=False, skipImport=False,
                                    callParamValues=None, 
                                    # dict of callParam key and value to use for import.
                                    # if not given, get it from pythonSource, ie, import_by_key['importerCallParams_by_instChain']
                                     objTypeIdPattern=None, 
                                     propNamePattern=None,
                                     objLabelPattern=None, 
                                     printDetail=False,
                                     printExpOnly=False,
                                     debug=0):
    '''
    given a doc, 
    if obj is given, use it and find its instanceChain.
    else if instanceChain is given, use it to find an obj on this instanceChain level (not deeper descendants).
    else if instanceName is given, treat it as directly imported instance, use it to find an obj on this instance.
    else, neither obj nor instanceChain is given, find the selected obj.
        the selection should be a single obj.
        if selected objs > 1, raise error.
    get the obj's importCallParams, className, moduleName, instanceChain, instanceName
    collect all objs in this doc belongs to this instanceChain.
    create a tmp doc. import with 
        importCallParams['doc'] = tmpdoc
        from moduleName import className
        instanceName = className(importCallParams)
    compare the collected obs with tmpdoc
    '''

    import_by_key = map_importInfo(doc)

    selectedLabels = None
    if obj:
        if not allObjects:
            selectedLabels = [obj.Label]
            print(f"compare_import_with_default() 1 obj.Label={obj.Label}")
        else:
            print(f"compare_import_with_default() allObjects=True, comparing all objects in the same instanceChain with obj.Label={obj.Label}")
    elif instanceChain:
        # get a 'top' level obj of this instanceChain, so that we can get importerCallParams
        importedObjs_by_instChain = import_by_key['importedObjs_by_instChain']
        importedObjs = importedObjs_by_instChain[instanceChain]
        obj = importedObjs[0]
        print(f"compare_import_with_default() 1 instanceChain={instanceChain}, got obj.Label={obj.Label} for this instanceChain")
    elif instanceName:
        # print(f"compare_import_with_default() 1 instanceName={instanceName}")
        directlyImportedObjs_by_instName = import_by_key['directlyImportedObjs_by_instName']
        if instanceName not in directlyImportedObjs_by_instName:
            raise ValueError(f"instanceName={instanceName} is not found in directlyImportedObjs_by_instName keys: {list(directlyImportedObjs_by_instName.keys())}")
        importedObjs = directlyImportedObjs_by_instName[instanceName]
        obj = importedObjs[0]
        print(f"compare_import_with_default() 1 instanceName={instanceName}, got obj.Label={obj.Label} for this instanceName")
    else:
        #  obj is None and instanceChain is None and instanceName is None:
        selection = Gui.Selection.getSelection()
        if len(selection) != 1:
            raise ValueError("Please select exactly one object.")
        
        # make sure selected obj is in doc
        if selection[0].Document != doc:
            raise ValueError(f"Selected object is not in the specified document, doc.Label={doc.Label}.")
        
        obj = selection[0]
        if not allObjects:
            selectedLabels = sorted([obj.Label for obj in selection])
            print(f"compare_import_with_default() 1 selected obj.Label={obj.Label}")
        else:
            print(f"compare_import_with_default() allObjects=True, comparing all objects in the same instanceChain with selected obj.Label={obj.Label}")

    pythonSource = get_obj_pythonSource(obj)
    if pythonSource == {}:
        raise ValueError(f"Selected object, Label={obj.Label}, Name={obj.Name} does not have valid pythonSource.")
    
    instanceChain = pythonSource['instanceChain']
    print(f"instanceChain={instanceChain}")

    if '.' not in instanceChain:
        raise ValueError(f"instanceChain={instanceChain} does not have '.' therefore, it is not an imported instance.")

    directlyImportedInstanceChain = '.'.join(instanceChain.split('.')[0:2])
    print(f"directlyImportedInstanceChain={directlyImportedInstanceChain}")

    directlyImportedInstanceName = instanceChain.split('.')[1]
    print(f"instanceChain={instanceChain}, directlyImportedInstanceName={directlyImportedInstanceName}")

    importerCallParams0 = import_by_key['importerCallParams_by_instChain'][directlyImportedInstanceChain]
    if callParamValues is None:
        importerCallParams0 = import_by_key['importerCallParams_by_instChain'][directlyImportedInstanceChain]
    else:
        importerCallParams = callParamValues.copy()
        importerCallParams['instanceName'] = importerCallParams0['instanceName']
        importerCallParams['objPrefix'] = importerCallParams0['objPrefix']
        
    print(f"importerCallParams={importerCallParams}")

    className = import_by_key['className_by_instChain'][directlyImportedInstanceChain]
    print(f"className={className}")

    moduleName = import_by_key['moduleName_by_instChain'][directlyImportedInstanceChain]
    print(f"moduleName={moduleName}")

    objPrefix = import_by_key['objPrefix_by_instChain'][directlyImportedInstanceChain]
    print(f"objPrefix={objPrefix}")
    
    # tested with npt_fxf's b_npt_f_npt_m_callsheet:
    # 17:25:40  instanceChain=myInstance.b_npt_f_instance.npt_m_instance
    # 17:25:40  directlyImportedInstanceChain=myInstance.b_npt_f_instance
    # 17:25:40  instanceChain=myInstance.b_npt_f_instance.npt_m_instance, directlyImportedInstanceName=b_npt_f_instance
    # 17:25:40  importerCallParams={'diaExpansion': '0.03 in', 'doc': 'doc_placeholder', 'femaleOD_wall': '0.08 in', 'female_height': '0.5 in', 'importer': 'importer_placeholder', 'instanceName': 'b_npt_f_instance', 'nominalID': '`2', 'objPrefix': 'b_npt_f_', 'useLabel': True}
    # 17:25:40  className=npt_f
    # 17:25:40  moduleName=parts.npt_f
    # 17:25:40  objPrefix=b_npt_f_
    
    importedDescendants_by_instChain = import_by_key['importedDescendants_by_instChain']
    importedDescendants = importedDescendants_by_instChain[instanceChain]
    
    tmpdoc = create_tmpdoc_and_import(moduleName, className, importerCallParams, debug=debug)

    diff_result = diff_docs(doc1=doc, doc2=tmpdoc, objList1=importedDescendants,
              selectedLabels=selectedLabels,
              diffOnly=diffOnly, commOnly=commOnly, skipImport=skipImport,
              objTypeIdPattern=objTypeIdPattern, 
              propNamePattern=propNamePattern,
              objLabelPattern=objLabelPattern,
              ignoreImporter=True,
              printDetail=printDetail,
              printExpOnly=printExpOnly,
              debug=debug)
    
    return diff_result


def exec_in_doc(doc, source_code):
    exec(source_code, {'doc': doc, '__name__': '__main__'})

def fix_obj_import_callparam(doc, obj, ignoreClass: str=None, printDetail: bool=False):
    '''
    fix the callParam of the given obj in the given doc
    '''
    pythonSource = get_obj_pythonSource(obj)
    try:
        className = pythonSource['className']
    except Exception as e:
        print(f"obj Label={obj.Label}, Name={obj.Name} does not have className in pythonSource. Skipping. Error: {e}")
        return
    
    if ignoreClass is not None and re.search(ignoreClass, className, re.IGNORECASE):
        print(f"obj Label={obj.Label}, Name={obj.Name} className={className} matches ignoreClass={ignoreClass}. Skipping.")
        return
    
    moduleName = pythonSource['moduleName']
    importerCallParams = pythonSource.get('importerCallParams', {})
    if not isinstance(importerCallParams, dict):
        print(f"obj Label={obj.Label}, Name={obj.Name} has invalid importerCallParams={importerCallParams}, resetting to empty dict")
        importerCallParams = {}
        print()

    print(f"Fixing obj Label={obj.Label}, Name={obj.Name}, className={className}, moduleName={moduleName}")
    fixedCallParamDict = import_fix_callParam(importerCallParams, className, moduleName)

    if fixedCallParamDict != importerCallParams:
        # save it back to obj.pythonSource
        pythonSource['importerCallParams'] = fixedCallParamDict
        obj.pythonSource = json.dumps(pythonSource)
        print(f"  Fixed importerCallParams for obj Label={obj.Label}, Name={obj.Name}")
    else:
        print(f"  No change needed for obj Label={obj.Label}, Name={obj.Name}")
    return fixedCallParamDict

def import_fix_callParam(callParamDict:dict, className:str, moduleName:str):
    # parse the str and make it into a python Dict
    callParamDictStr = f"{callParamDict}"
    print(f"callParamDict before fix: {callParamDictStr}")

    # get the contructor signature
    import importlib
    module = importlib.import_module(moduleName)
    cls = getattr(module, className)
    from inspect import signature
    sig = signature(cls.__init__)

    print(f"Constructor signature: {sig}")

    # check each param in callParamDict
    #     if param not in sig.parameters, remove it
    fixedCallParamDict = {}
    changed = 0
    for paramName, paramValue in callParamDict.items():
        if paramName in sig.parameters:
            fixedCallParamDict[paramName] = paramValue
        else:
            print(f"  Removing invalid param: {paramName}={paramValue}")
            changed += 1
    if changed == 0:
        print("  No invalid params found.")
    else:
        print(f"callParamDict after fix: {fixedCallParamDict}")
    return fixedCallParamDict

def get_directlyImportedInstChain_by_objName(doc, objName):
    # directlyImportedInstanceChain is the first two parts of instanceChain, 
    # which is the instanceChain of directly imported instance.
    import_by_key = map_importInfo(doc)
    importedInstChain_by_objName = import_by_key['importedInstChain_by_objName']
    instanceChain = importedInstChain_by_objName[objName]
    directlyImportedInstanceChain = '.'.join(instanceChain.split('.')[:2])
    return directlyImportedInstanceChain

def get_directlyImportedInstanceName_by_objName(doc, objName):
    directlyImportedInstanceChain = get_directlyImportedInstChain_by_objName(doc, objName)
    if '.' not in directlyImportedInstanceChain:
        obj = doc.getObject(objName)
        raise ValueError(f"obj.Name={obj.Name}, obj.Label={obj.Label}, directlyImportedInstanceChain={directlyImportedInstanceChain} does not have '.' therefore, it is not an imported instance.")
    directlyImportedInstanceName = directlyImportedInstanceChain.split('.')[1]
    return directlyImportedInstanceName

def create_tmpdoc_and_import(moduleName, className, importerCallParams, debug=0):
    # save active doc and selected objs
    saved_active_doc = App.ActiveDocument
    saved_selected_objs= Gui.Selection.getSelection()

    def restore_active_doc_and_selection():
        # restore active doc and selected objs
        App.setActiveDocument(saved_active_doc.Name)
        Gui.Selection.clearSelection()
        for obj in saved_selected_objs:
            Gui.Selection.addSelection(obj)

    tmpdoc = recreate_tmp_doc(debug=debug)

    # import className from moduleName
    import importlib
    module = importlib.import_module(moduleName)

    cls = getattr(module, className)

    importerCallParams2 = importerCallParams.copy()
    importerCallParams2.update({'doc': tmpdoc})

    try_again = 0
    print(f"Trying to import with importerCallParams={importerCallParams2}")
    
    try:
        inst = cls(**importerCallParams2)      
    except TypeError as e:
        # try again with default params
        print()
        print(f"TypeError: {e}. Trying again with default params.")
        print()
        try_again = 1
    except Exception as e:
        print(f"Failed to import with given importerCallParams. Error: {e}")
        traceback.print_exc()
        restore_active_doc_and_selection()
        raise e
    
    if try_again:
        instanceName = importerCallParams['instanceName']
        objPrefix = importerCallParams['objPrefix']
        try:
            inst = cls(doc=tmpdoc, instanceName=instanceName, objPrefix=objPrefix)
        except Exception as e:
            print(f"Failed to import with default params. Error: {e}")
            traceback.print_exc()
            restore_active_doc_and_selection()
            raise e

    # assign the instance to instanceName in tmpdoc's global namespace
    # exec(f"{instanceName} = inst", {'inst': inst})

    tmpdoc.recompute()

    restore_active_doc_and_selection()

    return tmpdoc

defaultInfo_by_key_type = {}

def get_defaultInfo(moduleName, className, importerCallParams, useLabel=False, debug=0, refreshCache=False):
    key = f"{moduleName}.{className},{importerCallParams['instanceName']}"
    if key in defaultInfo_by_key_type and not refreshCache:
        return defaultInfo_by_key_type[key]
    
    # get default propInfo and expInfo by creating a tmp doc and importing the class to get the default instance
    tmpdoc = create_tmpdoc_and_import(moduleName, className, importerCallParams, debug=debug)

    from cadcoder.expressiontools import get_doc_all_expInfo
    expInfo_by_objProp = get_doc_all_expInfo(tmpdoc, useLabel=False, includeGrounded=True, refreshCache=False)
    defaultInfo_by_key_type[key]['expInfo'] = expInfo_by_objProp

    from cadcoder.proptools import get_docObjPropDict
    propInfo_by_objProp = get_docObjPropDict(tmpdoc, useLabel=useLabel, includeGrounded=True, refreshCache=False)
    defaultInfo_by_key_type[key]['propInfo'] = propInfo_by_objProp

    return defaultInfo_by_key_type[key]


# defaultExpInfo_by_directInstanceChain_objProp = {}

# def compare_import_with_default_exp(doc, obj, 
#                                           useLabel=False,
#                                         #   instanceChain=None, instanceName = None,
#                                    diffOnly=False, commOnly=False, 
#                                 #    skipImport=False,
#                                      objTypeIdPattern=None, 
#                                      expPattern=None,
#                                      objLabelPattern=None, 
#                                      debug=0):
#     '''
#     similar to compare_import_with_default(), but only compare the expressions.
#     '''
#     directlyImportedInstanceChain = get_directlyImportedInstChain_by_objName(doc, obj.Name)
#     print(f"directlyImportedInstanceChain={directlyImportedInstanceChain}")

#     # get an obj in the directly imported instance, 
#     # so that we can get importerCallParams, className, moduleName
#     import_by_key = map_importInfo(doc)
#     directlyImportedObjs_by_instChain = import_by_key['importedObjs_by_instChain']
#     directlyImportedObjs = directlyImportedObjs_by_instChain[directlyImportedInstanceChain]
#     directlyImportedObj = directlyImportedObjs[0]
#     pythonSource = get_obj_pythonSource(directlyImportedObj)
#     className = pythonSource['className']
#     moduleName = pythonSource['moduleName']
#     objPrefix = pythonSource['objPrefix']
#     instanceName = pythonSource['instanceName']
#     importerCallParams = pythonSource.get('importerCallParams', {})
#     importerCallParams.update({'instanceName': instanceName, 'objPrefix': objPrefix})

#     tmpdoc = create_tmpdoc_and_import(moduleName, className, importerCallParams, debug=debug)

#     from cadcoder.expressiontools import get_doc_all_expInfo, get_obj_all_expInfo
#     if directlyImportedInstanceChain not in defaultExpInfo_by_directInstanceChain_objProp:
#         # get all expressions info in tmpdoc and save it to defaultExpInfo_by_directInstanceChain_objProp
#         print(f"loading defaultExpInfo for directInstanceChain={directlyImportedInstanceChain}...")
#         defaultExpInfo_by_directInstanceChain_objProp[directlyImportedInstanceChain] = get_doc_all_expInfo(tmpdoc, useLabel, includeGrounded=True, refreshCache=False)
#         # print(f"defaultExpInfo_by_directInstanceChain_objProp={defaultExpInfo_by_directInstanceChain_objProp}")
#         print()

#     importExpInfo_by_propName = get_obj_all_expInfo(doc, obj, useLabel, includeGrounded=True, refreshCache=False)
#     importExpInfo_by_objProp = {}
#     for propName, expInfo in importExpInfo_by_propName.items():
#         objProp = f"{obj.Name}.{propName}"
#         importExpInfo_by_objProp[objProp] = expInfo

#     defaultExpInfo_by_objProp = defaultExpInfo_by_directInstanceChain_objProp[directlyImportedInstanceChain]
#     defaultObjProps = set(defaultExpInfo_by_objProp.keys())
#     objKey = f"{obj.Name}" if not useLabel else f"{obj.Label}"
#     # filter out other objs by objKey
#     defaultObjProps = set(filter(lambda objProp: objProp.startswith(f"{objKey}."), defaultObjProps))
#     importObjProps = set(importExpInfo_by_objProp.keys())
#     combinedObjProps = sorted(defaultObjProps.union(importObjProps))

#     result = {}

#     for objProp in combinedObjProps:
#         if expPattern is not None and not re.search(expPattern, objProp, re.IGNORECASE):
#             continue

#         # print(f"checking objProp={objProp}")

#         if objProp not in defaultObjProps:
#             if not commOnly:
#                 print(f"added:")
#                 print(f"  importExpInfo={importExpInfo_by_objProp[objProp]}")
#                 print()
#             continue

#         if objProp not in importObjProps:
#             if not commOnly:
#                 print(f"removed:")
#                 print(f"  defaultExpInfo={defaultExpInfo_by_objProp[objProp]}")
#                 print()
#             continue

#         defaultExpInfo = defaultExpInfo_by_objProp[objProp]
#         importExpInfo = importExpInfo_by_objProp[objProp]
        
#         # print()
#         # print(f"  defaultExpInfo={defaultExpInfo}")
#         # print(f"  importExpInfo={importExpInfo}")
     

#         defaultRawExp = defaultExpInfo['rawExpression']
#         importRawExp = importExpInfo['rawExpression']

#         if defaultRawExp != importRawExp:
#             if not commOnly:
#                 print(f"Difference found in objProp={objProp}:")
#                 print(f"  defaultRawExp={defaultRawExp}")
#                 print(f"  importRawExp={importRawExp}")
#                 print()
#         else:
#             if not diffOnly:
#                 print(f"Same expression in objProp={objProp}:")
#                 print(f"  rawExpression={defaultRawExp}")
#                 print()
