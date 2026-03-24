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
        'importerCallParams_by_instChain': {},
        'importedObjNames': [],
        'instanceName_by_objName': {},
        'instanceChain_by_objName': {},
        'directlyImportedInstanceChains': set(),
    }

    for obj in doc.Objects:
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

        import_by_key['instanceName_by_objName'][obj.Name] = instanceName
        if instanceChain not in import_by_key['importedObjs_by_instChain']:
            import_by_key['importedObjs_by_instChain'][instanceChain] = []
        import_by_key['importedObjs_by_instChain'][instanceChain].append(obj)

        # add obj to importedDescendants_by_instChain at current chain and each parent chain
        chain = instanceChain
        while chain != '':
            if chain not in import_by_key['importedDescendants_by_instChain']:
                import_by_key['importedDescendants_by_instChain'][chain] = []
            import_by_key['importedDescendants_by_instChain'][chain].append(obj)
            if '.' in chain:
                chain = '.'.join(chain.split('.')[:-1])
            else:
                chain = ''

        if className is None or className == '':
            import_by_key['notImportedObjs'].append(obj)
        elif className == topClassName:
            import_by_key['notImportedObjs'].append(obj)
        else:
            if className.lower() == topClassName.lower():
                raise RuntimeError(f"obj Label={obj.Label}'s className={className} matches topClassName={topClassName} but has wrong case.")
            import_by_key['importedObjNames'].append(obj.Name)
            import_by_key['instanceChain_by_objName'][obj.Name] = instanceChain

            if importerClassName == topClassName:
                import_by_key['directlyImportedObjs'].append(obj)
                if instanceName not in import_by_key['directlyImportedObjs_by_instName']:
                    import_by_key['directlyImportedObjs_by_instName'][instanceName] = []
                import_by_key['directlyImportedObjs_by_instName'][instanceName].append(obj)

                import_by_key['directlyImportedInstInfo_by_InstName'][instanceName] = pythonSource

                import_by_key['directlyImportedInstanceChains'].add(instanceChain)              
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
                                   diffOnly=False, commOnly=False, skipImport=False,
                                     objTypeIdPattern=None, propNamePattern=None,
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

    if obj:
        pass
    elif instanceChain:
        # get a 'top' level obj of this instanceChain, so that we can get importerCallParams
        importedObjs_by_instChain = import_by_key['importedObjs_by_instChain']
        importedObjs = importedObjs_by_instChain[instanceChain]
        obj = importedObjs[0]
    elif instanceName:
        # print(f"compare_import_with_default() 1 instanceName={instanceName}")
        directlyImportedObjs_by_instName = import_by_key['directlyImportedObjs_by_instName']
        importedObjs = directlyImportedObjs_by_instName[instanceName]
        obj = importedObjs[0]
    else:
        #  obj is None and instanceChain is None and instanceName is None:
        selection = Gui.Selection.getSelection()
        if len(selection) != 1:
            raise ValueError("Please select exactly one object.")
        
        # make sure selected obj is in doc
        if selection[0].Document != doc:
            raise ValueError(f"Selected object is not in the specified document, doc.Label={doc.Label}.")
        
        obj = selection[0]

    pythonSource = get_obj_pythonSource(obj)
    className = pythonSource['className']
    instanceName = pythonSource['instanceName']
    instanceChain = pythonSource['instanceChain']
    moduleName = pythonSource['moduleName']
    objPrefix = pythonSource['objPrefix']
  
    if 'importerCallParams' in pythonSource:
        importerCallParams = pythonSource['importerCallParams']
    else:
        importerCallParams = {}

    # import className from moduleName
    import importlib
    module = importlib.import_module(moduleName)

    cls = getattr(module, className)
    
    importedDescendants_by_instChain = import_by_key['importedDescendants_by_instChain']
    importedDescendants = importedDescendants_by_instChain[instanceChain]
    
    # save active doc and selected objs
    saved_active_doc = App.ActiveDocument
    saved_selected_objs= Gui.Selection.getSelection()

    tmpdoc = recreate_tmp_doc(debug=debug)

    try_again = 0
    try:
        inst = cls(doc=tmpdoc, instanceName=instanceName, objPrefix=objPrefix, **importerCallParams)
    except TypeError as e:
        # try again with default params
        print()
        print(f"TypeError: {e}. Trying again with default params.")
        print()
        try_again = 1
    
    if try_again:
        inst = cls(doc=tmpdoc, instanceName=instanceName, objPrefix=objPrefix)

    # assign the instance to instanceName in tmpdoc's global namespace
    # exec(f"{instanceName} = inst", {'inst': inst})

    tmpdoc.recompute()

    # restore active doc and selected objs
    App.setActiveDocument(saved_active_doc.Name)
    Gui.Selection.clearSelection()
    for obj in saved_selected_objs:
        Gui.Selection.addSelection(obj)

    diff_props = diff_docs(doc1=doc, doc2=tmpdoc, objList1=importedDescendants,
              diffOnly=diffOnly, commOnly=commOnly, skipImport=skipImport,
              objTypeIdPattern=objTypeIdPattern, propNamePattern=propNamePattern,
              ignoreImporter=True,
              debug=debug)
    
    return diff_props

def compare_import_with_default_using_exec(doc, obj=None, instanceChain=None, instanceName = None,
                                   diffOnly=False, commOnly=False, skipImport=False,
                                     objTypeIdPattern=None, propNamePattern=None,
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

    if obj:
        pass
    elif instanceChain:
        # get a 'top' level obj of this instanceChain, so that we can get importerCallParams
        importedObjs_by_instChain = import_by_key['importedObjs_by_instChain']
        importedObjs = importedObjs_by_instChain[instanceChain]
        obj = importedObjs[0]
    elif instanceName:
        # print(f"compare_import_with_default() 1 instanceName={instanceName}")
        directlyImportedObjs_by_instName = import_by_key['directlyImportedObjs_by_instName']
        importedObjs = directlyImportedObjs_by_instName[instanceName]
        obj = importedObjs[0]
    else:
        #  obj is None and instanceChain is None and instanceName is None:
        selection = Gui.Selection.getSelection()
        if len(selection) != 1:
            raise ValueError("Please select exactly one object.")
        
        # make sure selected obj is in doc
        if selection[0].Document != doc:
            raise ValueError(f"Selected object is not in the specified document, doc.Label={doc.Label}.")
        
        obj = selection[0]

    pythonSource = get_obj_pythonSource(obj)
    # print(f"pythonSource={pythonSource}")
    className = pythonSource['className']
    instanceName = pythonSource['instanceName']
    instanceChain = pythonSource['instanceChain']
    moduleName = pythonSource['moduleName']
    objPrefix = pythonSource['objPrefix']

    # print(f"compare_import_with_default() 2 instanceName={instanceName}")

    importerCallParams_str_default = f'{{"doc": doc, "instanceName": "{instanceName}", "objPrefix": "{objPrefix}"}}'
    
    if 'importerCallParams' in pythonSource:
        importerCallParams = pythonSource['importerCallParams']
        importerCallParams_str = f"{importerCallParams}"
        importerCallParams_str = importerCallParams_str.replace('"doc_placeholder"', 'doc').replace('"importer_placeholder"', 'None')
        # importerCallParams_str = re.sub(r'\btrue\b', 'True', importerCallParams_str)
        # importerCallParams_str = re.sub(r'\bfalse\b', 'False', importerCallParams_str)
        importCode = f'''
from {moduleName} import {className}
tryagain = 0
try:
    {instanceName} = {className}(**{importerCallParams_str})
except TypeError as e:
    # try again with default params
    print(f"TypeError: {{e}}")
    tryagain = 1
if tryagain:
    {instanceName} = {className}(**{importerCallParams_str_default})
'''
    else:
        importerCallParams_str = importerCallParams_str_default
        importCode = f'''
from {moduleName} import {className}
{instanceName} = {className}(**{importerCallParams_str})
'''
    
    importedDescendants_by_instChain = import_by_key['importedDescendants_by_instChain']
    importedDescendants = importedDescendants_by_instChain[instanceChain]

#     importCode = f'''
# from {moduleName} import {className}
# {instanceName} = {className}(**{importerCallParams_str})
# '''
    if debug:
        print(f"importCode=\n{importCode}\n")
    
    # save active doc and selected objs
    saved_active_doc = App.ActiveDocument
    saved_selected_objs= Gui.Selection.getSelection()

    tmpdoc = recreate_tmp_doc(debug=debug)

    exec_in_doc(tmpdoc, importCode)

    tmpdoc.recompute()

    # restore active doc and selected objs
    App.setActiveDocument(saved_active_doc.Name)
    Gui.Selection.clearSelection()
    for obj in saved_selected_objs:
        Gui.Selection.addSelection(obj)

    diff_props = diff_docs(doc1=doc, doc2=tmpdoc, objList1=importedDescendants,
              diffOnly=diffOnly, commOnly=commOnly, skipImport=skipImport,
              objTypeIdPattern=objTypeIdPattern, propNamePattern=propNamePattern,
              ignoreImporter=True,
              debug=debug)
    
    return diff_props

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
