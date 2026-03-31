# -*- coding: utf-8 -*-

__Version__ = '0.9'
__Date__ = '2025-12-29'
__License__ = 'LGPL-3.0-or-later'
__Web__ = ''
__Wiki__ = 'README.md'
__Name__ = 'doc to python class'
__Comment__ = 'export FreeCAD document objects to python class code'
__Author__ = 'Tian'
__Icon__ = ''
__Help__ = 'README.md'
__Status__ = 'Alpha'
__Requires__ = 'FreeCAD >= 1.02'
__Communication__ = ''
__Files__ = ''

from logging import config
import os
import re
import sys
import inspect
import traceback

import FreeCAD as App
import FreeCADGui as Gui
import Part
from FreeCAD import Vector, Placement

import json
from PySide2 import QtWidgets, QtCore
from pprint import pformat
from cadcoder.callsheettools import is_callParam
from cadcoder.importtools import map_importInfo,  compare_import_with_default
from cadcoder.containertools import get_LCS_map, get_LCS_prefixes, get_container_by_objName
from cadcoder.expressiontools import get_expInfo_by_objPropKey, sort_objs_exp_dependency
from cadcoder.logtools import prefix_stack
from cadcoder.matchtools import match_key_startswith
from cadcoder.objtools import expand_objects, get_obj_by_objKey, sort_objs_by_downstream, get_obj_str
from cadcoder.proptools import compare_obj_prop_with_default, get_prop_info, normalize_label, propIsReadonly, get_obj_varname, get_param_value
from cadcoder.sketchtools import sketch2python
from cadcoder.spreadsheettools import is_cell_in_sheet
from cadcoder.subelementtools import get_posName_by_seName
from cadcoder.uitools import TextDialog
import pdb

debug = 0
dialog = None

'''
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
    Unlike Name, Label is not guaranteed to be unique by FreeCAD, 
    although FreeCAD's default behavior often 
    appends numbers to ensure uniqueness if duplicate labels 
    are created. The Label is what users typically interact 
    with in the graphical interface.

when applying mapping, we need do it in order. Therefore, use list.
for example, if we have mappings:
     ('Body001', 'Body'),
     ('Body002', 'Body001'),

we need to apply mappings in order on (Body001, Body002) to get (Body, Body001). correct.
    ie, Body001 -> Body
    Body002 -> Body001
if we apply them in reverse order, we will get (Body, Body). wrong.
    ie, Body001 -> Body
    Body002 -> Body001 -> Body
'''
nameMapping = [
    # (oldName, newName)
]


def main_part1():
    # main_part1
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()

def main_part2(doc, myInstance):
    # main_part2
    from pprint import pformat
    print(f"myInstance.exportObj_by_objName= {pformat(myInstance.exportObj_by_objName)}")

    top_objects = myInstance.get_top_objects()
    print(f"myInstance.top_objects=")
    for obj in top_objects:
        print(f"    name={obj.Name}, label={obj.Label}")

    from cadcoder.doctools import reorganize_doc
    reorganize_doc(doc) 

delayed_expression_by_objProp = {}  # properties with expression need adding in order.
top_directly_imported_objs = set()
objProp_already_set_with_call_param = set()
importCallInfo_by_instanceName = {}
added_prefixedObjNames = {}
added_sourceObjNames = set()
varname_by_objName = {}
useVarName = True
import_by_key = None
importCode_by_instanceName = {}

def add_imports(doc, useLabel: bool, import_by_key):
    # handle imported objects first, as they have no dependency and others may depend on them.
    # for example, boolean operation depends on top imported bodies's placement, etc.
    add_method_line('')
    add_method_line('# import classes and create instances for directly imported objects')
    # directlyImportedInstanceChains = import_by_key['directlyImportedInstanceChains']
    directlyImportedInstInfo_by_InstName = import_by_key['directlyImportedInstInfo_by_InstName']
    directlyImportedInstanceNames = directlyImportedInstInfo_by_InstName.keys()
    print(f"Directly imported instance names: {directlyImportedInstanceNames}")
    # exit(0)
    for instanceName in directlyImportedInstanceNames:
        instInfo = directlyImportedInstInfo_by_InstName[instanceName]
        className = instInfo['className']
        moduleName = instInfo['moduleName']
        objPrefix = instInfo['objPrefix']

        add_method_line(f"import_placeholder_{instanceName}")

        # add_method_line(f'from {moduleName} import {className}')
        importCode_by_instanceName[instanceName] = f'from {moduleName} import {className}\n'
        # import method-1: use placeholder parameter for callsheet parameters. later set the parameters' values.
        # add_method_line(f"{instanceName} = {className}('{instanceName}', doc, objPrefix=self.objPrefix + '{objPrefix}', useLabel={useLabel}, importer=self, import_placeholder_{instanceName})")
        
        importCode_by_instanceName[instanceName] += f"        {instanceName} = {className}('{instanceName}', doc, objPrefix=self.objPrefix + '{objPrefix}', useLabel={useLabel}, importer=self, params_placeholder_{instanceName})"
        # import method-2: we can also use default values for parameters when importing instance 
        # because we will set properties's links later anyway.
        # add_method_line(f'{instanceName} = {className}('{instanceName}', doc, objPrefix={param_objPrefix}, useLabel={useLabel}), importer=self')

        add_method_line(f'self.{instanceName} = {instanceName} # expose as instance variable')
        add_method_line(f'self.update_imports({instanceName}) # update import info for the instance')
        
        print(f"Comparing imports for instance: {instanceName}")
        diff_props = compare_import_with_default(doc, instanceName=instanceName, 
                                                 diffOnly=True, commOnly=False, skipImport=False,
                                     objTypeIdPattern=None, propNamePattern='Placement|Visibility')
                                     
        for dp in diff_props:
            obj = dp['obj']
            propName = dp['propName']
            action = dp['action']
            pythonSource = dp['pythonSource']
            propInfo = dp['propInfo']
            full_objVarName = get_full_objVarName(obj) # instanceName.shortVarName
            prefixPython = propInfo['prefixPython']
            if action in ['modified', 'added']:
                add_method_line(f'{full_objVarName}.{propName} = {use_varname_in_prefixPython( doc, prefixPython )}  # adjust imported object')
            elif action in ['deleted']:
                add_method_line(f'# need to handle deleted property {propName} for object {full_objVarName}')
        
        # add_method_line(f'# fix edge name or face name for imported objects')
        # add_method_line(f'# update_objs_seName(self.exportObjs, refreshCache=True)')
        # add_method_line(f'update_doc_seName(doc, refreshCache=True)')
        # add_method_line(f'')

def add_expressions(doc, useLabel: bool, selection: list, topCallsheetObjs):
    add_method_line('')
    add_method_line("# add expressions to object properties based on expression dependencies")
    print()
    print(f"useLabel={useLabel} sorting expressions by dependency")
    print()
    sort_exps_result = sort_objs_exp_dependency(doc, useLabel, objList=selection, debug=debug, printDetail=1)
    failure_reasons = ['delayed_set', 
                       'external_other_set'
                       ]
    for fr in failure_reasons:
        if sort_exps_result[fr]:
            msg = f"Error: some expressions could not be sorted, reason={fr} is not empty"
            print(msg)
            raise RuntimeError(msg)

    topCallsheetObjKeys = []
    for topCallsheetObj in topCallsheetObjs:
        if useLabel:
            topCallsheetObjKeys.append(topCallsheetObj.Label)
        else:
            topCallsheetObjKeys.append(topCallsheetObj.Name)
    
    instanceChain_by_objName = import_by_key['instanceChain_by_objName']

    directlyImportedCallsheetObjKeys = set()
    for obj in import_by_key['directlyImportedObjs']:
        if obj.TypeId != 'Spreadsheet::Sheet':
            continue
        if 'callsheet' in obj.Label:
            if useLabel:
                directlyImportedCallsheetObjKeys.add(obj.Label)
            else:
                directlyImportedCallsheetObjKeys.add(obj.Name)

    for objPropKey in sort_exps_result['ready_list']:
        # print(f"processing expression for objPropKey={objPropKey}")
        if objPropKey in objProp_already_set_with_call_param:
            if debug:
                print(f"  skipping expression for objPropKey={objPropKey} already set with call parameter")
            continue

        objKey, propName = objPropKey.rsplit('.', 1)
        obj = get_obj_by_objKey(doc, objKey, useLabel)        
        expInfo = get_expInfo_by_objPropKey(doc, objPropKey, useLabel)

        # skip expressions for indirectly imported objects
        if obj in import_by_key['indirectlyImportedObjs']:
            if debug:
                print(f"skipping expression for indirectly imported objKey={objKey} propName={propName}")
            continue

        # skip trigger object's expressions. will be handled separately.
        if obj.TypeId == 'App::FeaturePython' and obj.Label == 'trigger':
            # print(f"skipping expression for trigger object objKey={objKey} propName={propName}")
            continue

        if obj in import_by_key['directlyImportedObjs']:
            # this is an directly imported object. connect its callsheet with topCallsheet.

            # if this expression 
            #     depends on the current callsheet, 
            #     or, owned by an directly imported obj and depends on directly imported callsheet from another imported instance - inter-import,
            # then we need to set it via topCallsheet.
            # otherwise, skip it.
            # print(f"objKey={objKey} is imported, exp={expInfo['expression']}")
            depend_on_topCallsheets = False
            for parent in expInfo['parents']:
                parent_objKey = parent.rsplit('.', 1)[0]
                # if parent_objKey == topCallsheetObjKey0:
                if parent_objKey in topCallsheetObjKeys:
                    depend_on_topCallsheets = True
                    break
            if not depend_on_topCallsheets: 
                if debug:            
                    print(f"expression for directly imported objKey={objKey} propName={propName}, not depend on topCallsheet, parents={expInfo['parents']}")
                # check if any parent is from another directly imported callsheet object - inter-import
                inter_direct_import_dependent = False
                placement_of_driect_import_obj = False
                for parent in expInfo['parents']:
                    parent_objKey = parent.rsplit('.', 1)[0]
                    if parent_objKey in directlyImportedCallsheetObjKeys:
                        if propName == 'Placement':
                            # if the expression is for Placement in a directly imported object, we need it.
                            placement_of_driect_import_obj = True   
                            break
                        myInstanceChain = instanceChain_by_objName[obj.Name]
                        parent_obj = get_obj_by_objKey(doc, parent_objKey, useLabel)
                        parentInstanceChain = instanceChain_by_objName[parent_obj.Name]
                        if myInstanceChain != parentInstanceChain:
                            inter_direct_import_dependent = True
                            break
                if not inter_direct_import_dependent and not placement_of_driect_import_obj:
                    if debug:            
                        print(f"expression for directly imported objKey={objKey} propName={propName}, is not inter_direct_import_dependent, parents={expInfo['parents']}. Skipping it.")
                    continue # skip this expression
                else:
                    if debug:
                        print(f"expression for directly imported objKey={objKey} propName={propName}, is inter_direct_import_dependent, parents={expInfo['parents']}. Will connect.")
            else:
                if debug:
                    print(f"expression for directly imported objKey={objKey} propName={propName}, depends on topCallsheet, parents={expInfo['parents']}. Will connect.")
            instanceName = import_by_key['instanceName_by_objName'][obj.Name]
            instanceChain = import_by_key['instanceChain_by_objName'][obj.Name]

            if debug:
                print(f"connecting directly imported objKey={objKey} propName={propName} expression={expInfo['expression']} parents={expInfo['parents']} to topCallsheet")
            
            # if need_callInfo:
            # extract callsheet parameter name and set it via callsheet parameter
            # npt_m_callsheet.set("B3", f"=<<{addPrefix('npt_f_callsheet')}>>.horizontalScale")
            # if the expression is from spreadsheet cell, we need to find its alias as call parameter.
            if expInfo["source"] == 'SpreadsheetCell':
                # if exp source is SpreadsheetCell, the propName is a cell address, eg, B3.
                # find cell alias - it must have an alias so that others can refer to it.
                # otherwise, it is useless.
                try:
                    alias = obj.getAlias(propName)
                except:
                    alias = None
                if alias is None or alias == '':
                    msg = f"Error: imported spreadsheet cell {obj.Label}.{propName} is set by topCallsheet, but has no alias defined."
                    print(msg)
                    traceback.print_stack()
                    raise RuntimeError(msg)
                call_param_key = alias
            else:
                # for non-spreadsheet-cell property, we use propName as call parameter name.
                call_param_key = propName

            propInfo = get_prop_info(doc, obj, propName)    
            importerCallParams = import_by_key['importerCallParams_by_instChain'][instanceChain]
            # if propName != 'Placement': 
            if call_param_key in importerCallParams.keys():
                importCallInfo = {
                    'call_param_key': call_param_key,
                    'propInfo': propInfo,
                }

                if not instanceName in importCallInfo_by_instanceName:
                    importCallInfo_by_instanceName[instanceName] = []
                importCallInfo_by_instanceName[instanceName].append(importCallInfo)  
                if debug:
                    print(f"added call_param_key={call_param_key} (propName={propName}) importCallInfo for instanceName={instanceName}")
            else:
                if debug:
                    print(f"skipping adding call_param_key={call_param_key} (propName={propName}) to instanceName={instanceName}'s importCallInfo because it is not in part of it.")

            # instanceName = import_by_key['instanceName_by_objName'][obj.Name]
            pythonSource = json.loads(obj.pythonSource)
            varName_in_importedInstance = pythonSource['objVarName']
            if 'callsheet' in varName_in_importedInstance and re.match(r'B[0-9]+', propName):
                # a cell property in callsheet spreadsheet can be a call parameter
                alias = obj.getAlias(propName)
                if alias is None:
                    add_method_line(f"{instanceName}.{varName_in_importedInstance}.set('{propName}', f\"=" + expInfo['prefixedExp'] + f"\")")
                else:
                    add_method_line(f"{instanceName}.{varName_in_importedInstance}.set({instanceName}.{varName_in_importedInstance}.getCellFromAlias('{alias}'), f\"=" + expInfo['prefixedExp'] + f"\")")
            else:
                # print(f"expInfo={pformat(expInfo)}")
                expVarName = expInfo['varName']
                prefixedExp = expInfo['prefixedExp']
                add_method_line(f"{instanceName}.{varName_in_importedInstance}.setExpression('{expVarName}', f\"{prefixedExp}\")")
            continue
        # we are done with (directly and indirectly) imported objects's expressions.

        # now we handle top (current) class's objects' expressions.
        prefixedExp = expInfo['prefixedExp']
        objVarName = get_obj_varname(obj, useLabel)
        
        if expInfo["source"] == 'SpreadsheetCell':
            # if expression is from spreadsheet cell, we need to set it via spreadsheet cell.
            # mention its alias in comment for easier debugging.
            alias = obj.getAlias(propName)
            if alias is None:
                add_method_line(f'{objVarName}.set("{propName}", f"={prefixedExp}")')
            else:
                add_method_line(f'{objVarName}.set({objVarName}.getCellFromAlias("{alias}"), f"={prefixedExp}")')
        elif expInfo["source"] == 'SpreadsheetAlias':
            pass  # do nothing, already handled when setting static value.
        else:
            expVarName = expInfo['varName']
            add_method_line(f'{objVarName}.setExpression("{expVarName}", f"{prefixedExp}")')

            '''
            if this is spreadsheet and is for a configuration table, we need to recompute
                NPT_M_Thread_Spreadsheet.setExpression('.nominalOD.Enum', 'cells[<<A3:|>>]')
                doc.recompute()
                NPT_M_Thread_Spreadsheet.setExpression('.cells.Bind.B2.I2', 'tuple(.cells; <<B>> + str(hiddenref(nominalOD) + 3); <<I>> + str(hiddenref(nominalOD) + 3))')
                doc.recompute()
            without recompute, we may get error:
                Error: '1 / 2' is not part of the enumeration
                Error: Property 'RealOD' not found. 
                note that the property RealOD is not even related to the configuration table. very hard to debug.
            '''
            if obj.TypeId == 'Spreadsheet::Sheet' and (expVarName.startswith('.cells.Bind') or expVarName.endswith('.Enum')):
                # add_method_line('doc.recompute() # recompute after setting configuration-table expression; otherwise error: Property ... not found.')
                add_method_line(f'{objVarName}.recompute() # recompute after setting configuration-table expression; otherwise error: Property ... not found.')
                # objs_waiting_for_recompute.clear()

def add_triggers(doc):
    add_method_line('')
    add_method_line("# add trigger objects' expressions")
    from cadcoder.triggertools import get_trigger_info, triggerVersion
    trigger_info = get_trigger_info(doc)
    info_by_watchObjPropName_targetObjPropName = trigger_info.get('info_by_watchObjPropName_targetObjPropName', {})
    info_by_watchObjPropName_targetObjFuncArgs = trigger_info.get('info_by_watchObjPropName_targetObjFuncArgs', {})
    if info_by_watchObjPropName_targetObjPropName:
        imported_triggertools = False
        for watchObjPropName, info_by_targetObjPropName in info_by_watchObjPropName_targetObjPropName.items():
            watchObjKey, watchPropName = watchObjPropName.rsplit('.', 1)
            for targetObjPropName, info in info_by_targetObjPropName.items():
                useLabel2 = info['useLabel']
                # only import trigger with watchObj in in added_objNames
                watchObj = get_obj_by_objKey(doc, watchObjKey, useLabel2)
                if watchObj.Name not in added_sourceObjNames:
                    print(f"skipping trigger for watchObj.Name={watchObj.Name} Label={watchObj.Label} not in added objects={added_prefixedObjNames}.")
                    continue
                if not imported_triggertools:
                    add_method_line('from cadcoder.triggertools import link_watch_to_target')
                    imported_triggertools = True
                watchObjName = info['watchObjName']
                targetObjName = info['targetObjName']
                targetPropName = info['targetPropName']
                watchObjPython = f"doc.getObject(self.addPrefix('{watchObjName}'))"
                targetObjPython = f"doc.getObject(self.addPrefix('{targetObjName}'))"
                watchObjPython = use_varname_in_prefixPython(doc, watchObjPython)
                targetObjPython = use_varname_in_prefixPython(doc, targetObjPython)
                add_method_line(f"link_watch_to_target(doc, {watchObjPython}, '{watchPropName}', {targetObjPython}, '{targetPropName}', useLabel)")

def export_doc(doc, useLabel: bool, topClassName: str):
    global import_by_key
    # global rowDict_by_varName
    print(f"Exporting objects in document: {doc.Name}, useLabel={useLabel}")

    add_script_line('from FreeCAD import Vector, Placement, Rotation')
    add_script_line('import Sketcher')
    add_script_line('import Part')
    add_script_line('import FreeCAD as App')
    add_script_line('import FreeCADGui as Gui')
    add_script_line('from cadcoder.baseClass import baseClass')
    add_script_line('from cadcoder.containertools import get_LCS_by_prefix')
    add_script_line('from cadcoder.objtools import update_obj_prop_jsonDict')
    add_script_line('from cadcoder.subelementtools import update_objs_seName, update_doc_seName, get_seName_by_posName')

    # selection is a subset of doc.Objects, 
    selection = Gui.Selection.getSelection()
    allObjects = sorted(doc.Objects, key=lambda obj: obj.Name)

    if not selection:
        print(f"No objects selected, exporting all {len(allObjects)} objects in the document.")
        selection = allObjects
    else:
        # extend selection to make it a self-complete set.
        selection = expand_objects(doc, useLabel, objects=selection, printDetail=True)

    topCallsheetObj0 = None
    for obj in allObjects:
        if obj.TypeId == 'Spreadsheet::Sheet' and obj.Label == 'callsheet':
            topCallsheetObj0 = obj
            break

    topCallsheetObjs = []
    for obj in allObjects:
        if obj.TypeId == 'Spreadsheet::Sheet' and obj.Label.startswith('callsheet'):
            topCallsheetObjs.append(obj)
    
    if topCallsheetObj0 is not None:
        if topClassName is None:
            if hasattr(topCallsheetObj0, 'pythonSource'):
                # 1st try to use pythonSource's className if available
                try:
                    pythonSource = json.loads(topCallsheetObj0.pythonSource)
                    topClassName = pythonSource['className']
                    print(f"topCallsheetObj has pythonSource, using its className={topClassName} as topClassName")
                except Exception as e:
                    print(f"Error: failed to parse pythonSource for topCallsheetObj.Name={topCallsheetObj0.Name} Label={topCallsheetObj0.Label}. Error: {e}")
                    traceback.print_exc()
                    topClassName = normalize_label(doc.Name)
                    print(f"Using doc.Name={doc.Name} as topClassName")
            else:
                topClassName = normalize_label(doc.Name)
        # else: we have both callsheetObj and topClassName. we are good.
    else: # topCallsheetObj0 is None:   
        if topClassName is None:
            # if at this point, we still cannot figure out current class name, we use doc.Name
            topClassName = normalize_label(doc.Name)
            print(f"As no callsheet found, we use doc.Name={doc.Name} as topClassName")
        # else: we have topClassName but no callsheetObj. we will add a new callsheet at the end.
    print(f"summary: topClassName={topClassName}, topCallsheetObj0 Label={topCallsheetObj0.Label if topCallsheetObj0 else None}")
    
    # now that we have topClassName, we can define the class interface
    add_script_line('') 
    add_script_line(f'class {topClassName}(baseClass):')
    add_body_line('def init_placeholder')
    add_method_line('')
    add_method_line('super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)')

    added_objects = set() # use this to keep track of added objects

    # handle import first because others may depend on them.
    import_by_key = map_importInfo(doc, topClassName, 
                                   printDetail=debug,
                                   )
    add_imports(doc, useLabel, import_by_key)

    # add imported objects to added_objects
    for key in ['directlyImportedObjs', 'indirectlyImportedObjs']:
        for obj in import_by_key[key]:
            if useLabel:
                objKey = obj.Label
            else:
                objKey = obj.Name
            added_objects.add(objKey)

    # now add objects that not part of import
    '''
    strategy to handle dependencies:
    
    There are two types of dependencies:
    1. object dependencies: object A depends on object B, ie, A refers to B in its properties.
       we need to create B before A.
    2. expression dependencies: object A's property P1 has an expression that refers to object B's property P2.

    Therefore, we do two passes:

    1. We first create skeleton bodies based on object dependencies and
    set properties' resolved values first, no expressions yet.
    This basically gives us a static snapshot of the document.

    2. Then we add expressions according to expression dependencies.
    This allows us to maintain the dynamic relationships between object properties.

    At last, we add some end of file codes.
    '''

    sort_objs_result = sort_objs_by_downstream(doc, useLabel, objList=selection, debug=debug, printDetail=1)
    failure_reasons = ['delayed_set', 
                       'external_other_set'
                       ]
    
    for fr in failure_reasons:
        if sort_objs_result[fr]:
            msg = f"Error: some objects could not be sorted, reason={fr} is not empty"
            print(msg)
            raise RuntimeError(msg)
    
    sorted_objKeyList = sort_objs_result['ready_list']
    added_objects.update(set(sort_objs_result['skip_set']))  # set of objPropKey.

    add_method_line('')
    add_method_line("# add objects and add static value to objects' properties based on object dependencies")
    for objKey in sorted_objKeyList:
        obj = get_obj_by_objKey(doc, objKey, useLabel)
   
        if (obj.TypeId, obj.Name) in added_objects:
            print(f"object Name={obj.Name} TypeId={obj.TypeId} Label={obj.Label} already added.")
            continue
        if obj.TypeId == 'App::FeaturePython':
            if obj.Label == 'trigger':
                print(f"skipping trigger object Name={obj.Name} TypeId={obj.TypeId} Label={obj.Label}. will be handled separately.")           
            else:
                print(f"ERROR: skipping object Name={obj.Name} TypeId={obj.TypeId} Label={obj.Label} because FeaturePython not supported yet.")
            continue

        if hasattr(obj, 'pythonSource'):
            pythonSource = json.loads(obj.pythonSource)
            importClassName = pythonSource['className']
            importInstanceName = pythonSource['instanceName']

            # some objects generated from Python but we don't know how to convert them
            # back to Python.
            canConvertToPython = pythonSource.get('canConvertToPython', True)
            if not canConvertToPython:
                add_method_line(f'# object {obj.Name} of type {obj.TypeId} is generated from Python but cannot be converted back to Python. We will skip it, but you may need to handle it manually.')
                add_method_line(f"raise NotImplementedError('object {obj.Name} of type {obj.TypeId} cannot be converted back to Python. Please handle it manually.')")
                
                msg = f"Error: object {obj.Name} of type {obj.TypeId} is generated from Python but cannot be converted back to Python. We will skip it, but you may need to handle it manually."
                print(msg)
                raise NotImplementedError(msg)
            
            if importInstanceName in import_by_key['directlyImportedObjs_by_instName']:
                # this obj is part of the direct import. we have already imported this object above.
                added_objects.add((obj.TypeId, obj.Name))
                continue
            elif importClassName != topClassName:
                # this class must be recursively imported by other imported class - indirectly imported.
                # we mark it as ready and skip it.
                print(f"objKey={objKey}'s className={importClassName} is not in import list, neiterher current class, skipping it.")
                # indirectly_imported_objKeys.add(objKey)
                added_objects.add((obj.TypeId, obj.Name))
                continue
            # else:
                # current class's object with pythonSource, we still need to create it.

        # now the object is not part of import, we need to create it.
        objVarName = add_object(doc, obj, useLabel, selection)
        added_objects.add((obj.TypeId, obj.Name))

        # if the object belongs to a container, we need to add it to the container.
        # handling container is the same as handling Group property. so we will
        # skip handling Group property later.
        container = get_container_by_objName(doc, obj.Name, useLabel)
        if container is not None:
            # containerVarName = varname_by_objName[container.Name]
            containerVarName = get_varName(doc, container.Name)
            add_method_line(f'self.container_append_object({containerVarName}, {objVarName})')

        add_static_prop(doc, obj, objVarName, useLabel, selection, topCallsheetObjs)

        # recompute after adding object
        if obj.TypeId in ['PartDesign::Boolean']:
            # 'PartDesign::Boolean' needs recomputing whole doc
            add_method_line(f'doc.recompute() # recompute whole document for {obj.TypeId}')
        else:
            # recompute this object only, saving time compared to recomputing the whole document.
            add_method_line(f'{objVarName}.recompute()  # recompute after adding object')
        add_method_line("")
        
    add_method_line('# add delayed static property values')
    for (obj, vname, propName, info) in delayed_prop_static_values:
        prefixPython = use_varname_in_prefixPython( doc, info['prefixPython'] )
        add_method_line(f'{vname}.{propName} = {prefixPython}')

    add_expressions(doc, useLabel, selection, topCallsheetObjs)

    add_triggers(doc)

    add_method_line('')
    add_method_line('# add delayed expression property values - values, not expressions, eg, enum value')
    if delayed_prop_exp_values:
        for (obj, vname, propName, info) in delayed_prop_exp_values:
            # if obj == topCallsheetObj0 and not is_cell_in_sheet(propName, obj) and info.get('expInfo', None) is not None:
            if obj in topCallsheetObjs and not is_cell_in_sheet(propName, obj) and info.get('expInfo', None) is not None:
                # a non-cell property in callsheet spreadsheet can be a call parameter if it is an expression
                # skip if propName is an alias         
                call_param_name = propName
                callsheet_params.append( (obj, vname, propName, info, call_param_name) )
                add_method_line(f'{vname}.{propName} = {call_param_name}')
            else:
                prefixPython = use_varname_in_prefixPython(doc, info['prefixPython'] )
                add_method_line(f'{vname}.{propName} = {prefixPython}')

    add_method_line('')
    add_method_line(f'# now we have rebuilt the original {topClassName} doc. Now we apply dynmic call parameters')
    add_method_line(f'print("there can be temporary errors when we applying dynamic call parameters that change original {topClassName}\'s shape.")')
    add_method_line(f'print("ignore temporary errors, if any, below.")')
    for line in callsheet_call_param_lines:
        add_method_line(line)
    add_method_line('doc.recompute()')
    add_method_line('update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.')
    add_method_line(f'print("ignore temporary errors, if any, above.")')

    target_callsheet_vname = 'callsheet'
    if topCallsheetObj0 is None:
        # if the class has no callsheet yet, create an empty callsheet 
        add_method_line('')
        add_method_line(f'# create empty callsheet spreadsheet label and varname={target_callsheet_vname}')
        add_method_line(f'{target_callsheet_vname} = doc.addObject("Spreadsheet::Sheet", self.addPrefix("{target_callsheet_vname}"))')
        add_method_line(f'self.{target_callsheet_vname} = {target_callsheet_vname}')
        add_method_line(f"{target_callsheet_vname}.Label = self.addPrefix('{target_callsheet_vname}')")
        add_method_line(f'self.post_new_obj({target_callsheet_vname})')
        # add header row
        add_method_line(f'{target_callsheet_vname}.set("A1", "variableName")')
        add_method_line(f'{target_callsheet_vname}.set("B1", "value")')
        add_method_line(f'{target_callsheet_vname}.set("C1", "isCallParam")')
        add_method_line(f'{target_callsheet_vname}.set("D1", "comment")')
        add_method_line(f'{target_callsheet_vname}.recompute() # recompute sheet to make new cells available')

    # update callsheet parameters
    add_method_line('')
    add_method_line(f"self.update_callsheet()")

    add_script_line('')
    add_script_line('')
    add_script_line(f'def main():')
    func2lines(main_part1, indent=1)
    
    # sort callsheet param by vname, to make the output deterministic and easier to compare
    # 2nd field is vname.
    sorted_callsheet_params = sorted(callsheet_params, key=lambda x: x[4])

    callsheet_param_values_str = ""
    for (obj, vname, propName, info, call_param_name) in sorted_callsheet_params:
        param_value = get_param_value(info, isForFuncParam=True, preferInchUnit=True)
        callsheet_param_values_str += f"{call_param_name}={param_value}, "
    
    add_body_line('')
    add_body_line(f'# create instance of {topClassName}')
    add_body_line(f'myInstance = {topClassName}("myInstance", doc, objPrefix="", useLabel=True, importer=None, {callsheet_param_values_str})')

    add_body_line('')
    func2lines(main_part2, indent=1)
    
    add_script_line('')
    add_script_line('')
    add_script_line("if __name__ == '__main__':")
    add_body_line('main()')
    add_script_line('') # add a final newline

    # clear dialog textEdit and reprint with placeholders replaced
    dialog.form.textEdit.clear()

    print("reprint script, replacing placeholders in script lines")
    for line in script_lines:
        if re.search(r'^\s*def init_placeholder', line):
            dialog.form.textEdit.append(f'    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, {callsheet_param_values_str} ):')
            for (obj, vname, propName, info, call_param_name) in sorted_callsheet_params:
                dialog.form.textEdit.append(f'        self.{call_param_name} = {call_param_name}')
        elif m := re.search(r'import_placeholder_(.+?)$', line):
            instanceName = m.group(1)

            if instanceName not in importCallInfo_by_instanceName:
                # if no import call info, just leave empty, meaning to let imported instance use default parameters.
                print(f"importCallInfo_by_instanceName = \n{pformat(importCallInfo_by_instanceName)}")
                print(f"instanceName={instanceName} not in importCallInfo_by_instanceName.")
                print(f"import {instanceName} with default parameters; leave call parameters empty.")
                importCode_by_instanceName[instanceName] = importCode_by_instanceName[instanceName].replace(f'params_placeholder_{instanceName}', '')
            else:
                callParams_str = ""
                for importCallInfo in sorted(importCallInfo_by_instanceName[instanceName], key=lambda x: x['call_param_key']):
                    call_param_key = importCallInfo['call_param_key']
                    param_value = get_param_value(importCallInfo['propInfo'], isForFuncParam=True, preferInchUnit=True)
                    callParams_str += f"{call_param_key}={param_value}, "
                importCode_by_instanceName[instanceName] = importCode_by_instanceName[instanceName].replace(f'params_placeholder_{instanceName}', callParams_str)
            # print(f"importCode_by_instanceName[{instanceName}] = {importCode_by_instanceName[instanceName]}")
            
            line = line.replace(f'import_placeholder_{instanceName}', importCode_by_instanceName[instanceName])
            dialog.form.textEdit.append(line)
        else:
            dialog.form.textEdit.append(line)


out_line_number = 0
script_lines = []
def add_script_line(line, indent=0):
    global out_line_number

    # when useLabel is True, nameMapping is empty.
    # when useLabel is False, we may have nameMapping to apply.
    for old, new in nameMapping:
        # must match whole word and case-sensitive
        line = re.sub(r'\b' + re.escape(old) + r'\b', new, line)

    # remove newlines - make multi-line code into single line
    line = line.replace('\n', ' ')

    out_line_number += 1
    spaces = ' ' * 4 * indent
    prefix_stack(f"{out_line_number}: " + spaces + line, debug=debug)
    dialog.form.textEdit.append(spaces + line)
    script_lines.append(spaces + line)

def add_body_line(line, indent=1):
    add_script_line(line, indent)

def add_method_line(line, indent=2):
    add_script_line(line, indent)

def func2source(func):
    import inspect
    source_lines = inspect.getsourcelines(func)[0]
    # remove the first line (def ...)
    source_lines = source_lines[1:]
    # dedent
    dedented_lines = []
    for line in source_lines:
        dl = line[4:] if line.startswith('    ') else line
        dl = dl.rstrip('\n')
        dedented_lines.append(dl)
    return dedented_lines

def func2lines(func, indent=1):
    lines = func2source(func)
    for line in lines:
        add_body_line(line, indent)

'''
Binder.Context
    propType: App::PropertyXLink
    propValue: (<body object>, 'Binder.')
    valueTypeId: None
    valueClass: tuple
    valueClassTree: {'tuple/str', 'tuple/Body'}
    valueObjName: None
    readonly: False
    valuePython: (doc.getObject('Body'), 'Binder.')
    propName: Context
    prefixPython: (doc.getObject(self.addPrefix('Body')), 'Binder.')

later, instead of setting Binder.Context = (doc.getObject(self.addPrefix('Body')), 'Binder.')
we set Binder.Context = (Binder, 'Binder.')
so we need to have a mapping from object name to variable name.

the replacement makes code more readable.
'''

def use_varname_in_prefixPython(doc, prefixPython:str) -> str:
    '''
    replace Binder.Context = (doc.getObject(self.addPrefix('Body')), 'Binder.')
    with   Binder.Context = (npm_m, 'Binder.')
    '''
    if not useVarName:
        return prefixPython
    
    string_by_atom = {}
    atom_idx = 0
    
    '''
    we need to match patterns like:
        doc.getObject(self.addPrefix('Body'))
        doc.getObject('XZ_Plane')
    '''
    # while m := re.search(r"(doc\.getObject\(self\.addPrefix\('([^']+)'\)\))", prefixPython):
    while m := re.search(r"(doc\.getObject\((?:self\.addPrefix\('([^']+)'\)|'([^']+)')\))", prefixPython):
        # print(f"found objName={m.group(1)} in prefixPython={prefixPython}")
        doc_get_obj_str = m.group(1)
        objName = m.group(2) if m.group(2) is not None else m.group(3)
        try:
            varname = get_varName(doc, objName)
            prefixPython = prefixPython.replace(doc_get_obj_str, varname)
            # print(f"replaced with varname={varname}, new prefixPython={prefixPython}")
        except:
            print(f"object Name={objName} cannot be replaced with varname.")
            atom = f"__ATOM_{atom_idx}__"
            string_by_atom[atom] = doc_get_obj_str
            prefixPython = prefixPython.replace(doc_get_obj_str, atom)
            atom_idx += 1

    # restore unreplaceable strings from atoms
    for atom, original_str in string_by_atom.items():
        prefixPython = prefixPython.replace(atom, original_str)

    return prefixPython

def get_varName(doc, objName):
    if objName in varname_by_objName:
        return varname_by_objName[objName]
    
    obj = doc.getObject(objName)
    if obj in import_by_key['directlyImportedObjs'] or obj in import_by_key['indirectlyImportedObjs']:
        return get_full_objVarName(obj)
    
    msg = f"obj Label={obj.Label}, Name={obj.Name}, is not in top class or in any directly imported instance"
    print(msg)
    traceback.print_stack()
    raise RuntimeError(msg)

def get_full_objVarName(obj):
    '''
    full object variable name is like npt_m_instance.npt_m_callsheet
    '''
    if hasattr(obj, 'pythonSource'):
        pythonSource = json.loads(obj.pythonSource)
        objVarName = pythonSource['objVarName']
        shortObjVarName = objVarName
        # instanceName = import_by_key['instanceName_by_objName'][obj.Name]
        # instanceName = pythonSource['instanceName']
        # fullObjVarName = f"{instanceName}.{shortObjVarName}"
        instanceChain = pythonSource['instanceChain']
        # since the code will be in the current instance, we remove the 1st element of the instanceChain
        instanceChain2 = '.'.join(instanceChain.split('.')[1:])
        fullObjVarName = f"{instanceChain2}.{shortObjVarName}"
    else:
        print(f"object Name={obj.Name} TypeId={obj.TypeId} has no pythonSource, using shortObjVarName as fullObjVarName")
        fullObjVarName = shortObjVarName
    return fullObjVarName


def add_object(doc, obj, useLabel, objectList)-> str:
    '''
    add object to the doc.
    add its props with static values only.
    '''
    objVarName = get_obj_varname(obj, useLabel)
    objVarNameUseLabel = get_obj_varname(obj, True)

    # prefixedObjName = f"self.addPrefix('{obj.Name}')"    # name-based
    prefixedObjName = f"self.addPrefix('{objVarName}')"    # label-based

    if prefixedObjName in added_prefixedObjNames:
        # we need this check if use label-based varname because obj labels can be duplicate.
        old_obj = added_prefixedObjNames[prefixedObjName]
        msg = f"Error: prefixedObjName={prefixedObjName} already added. Likely dup labels. Rename one label first."
        print(msg)
        print(f"old: {get_obj_str(old_obj)}")
        print(f"new: {get_obj_str(obj)}")
        raise RuntimeError(msg)
    added_prefixedObjNames[prefixedObjName] = obj
    added_sourceObjNames.add( obj.Name )

    TypeIds_need_recompute = [
        "PartDesign::Chamfer",
    ]

    if obj.TypeId in TypeIds_need_recompute:
        add_method_line(f'doc.recompute() # recompute before adding {obj.TypeId} to avoid error')

    add_method_line(f"{objVarName} = doc.addObject('{obj.TypeId}', {prefixedObjName} )")
    varname_by_objName[obj.Name] = objVarName

    add_method_line(f"{objVarName}.Label = self.addPrefix('{obj.Label}')")
    add_method_line(f"self.{objVarNameUseLabel} = {objVarName}")
    add_method_line(f"self.post_new_obj({objVarName})")

    # if object is a container, we also assign vars to its LCS - Local Coordinate System, eg, Origin, X_Axis, XY_Plane, etc.
    if obj.TypeId == "PartDesign::Body":
        LCS_by_prefix = get_LCS_map(doc, obj)
        for lcsPrefix in get_LCS_prefixes():
            if lcsPrefix in LCS_by_prefix:
                LCS_obj = LCS_by_prefix[lcsPrefix]
                LCS_objVarName = f"{objVarName}_{lcsPrefix}"
                add_method_line(f"{LCS_objVarName} = get_LCS_by_prefix(doc, {objVarName}, '{lcsPrefix}')")           
                varname_by_objName[LCS_obj.Name] = LCS_objVarName
        for lcsPrefix in get_LCS_prefixes():
            LCS_obj = LCS_by_prefix[lcsPrefix]
            LCS_objVarName = f"{objVarName}_{lcsPrefix}"
            add_method_line(f"self.{LCS_objVarName} = {LCS_objVarName}")
        for lcsPrefix in get_LCS_prefixes():
            LCS_obj = LCS_by_prefix[lcsPrefix]
            LCS_objVarName = f"{objVarName}_{lcsPrefix}"
            add_method_line(f"self.post_new_obj({LCS_objVarName})")
    return objVarName

ready_expKeys = set()  # objKey.propName that are ready
delayed_prop_static_values = []  # store lines to be added later
delayed_prop_exp_values = []  # store lines to be added later
callsheet_params = []
callsheet_call_param_lines = []

def add_static_prop(doc, obj, objVarName, useLabel, objectList, topCallsheetObjs):
    skipProperties = [
        'Label', # label is handled eariler
        'Shape', 'Proxy',
        'AddSubShape', 'FullyConstrained', 'VisualLayerList',
        'InternalShape', 'ShapeMaterial', 'ShapeAppearance', 'MaterialName',
        'SuppressedShape',
        'ExpressionEngine',  # handled separately

        # handled separately
        'pythonSource', 
        'pythonFeature',
    ]

    skipTypeProp = [
        ('Sketcher::SketchObject', 'Geometry'),    # done by addSketch()
        ('Sketcher::SketchObject', 'Constraints'), # done by setExpressions()
        ('PartDesign::Body', 'Origin'),        # auto-created with new Body.

        # these two are handled by we handle container
        ('PartDesign::Body', 'Tip'),      
        ('PartDesign::Body', 'Group'),   
    ]

    delayedTypeProp = [
        # some properties need to be added after all objects are created.

        # these two are handled by we handle container
        # ('PartDesign::Body', 'Tip'),
        # ('PartDesign::Body', 'Group'), 
    ]

    needReadOnlyObjTypeProp = [
        # we don't need readonly properties generally, except these:
        # by object.TypeId, propertyName
        ('PartDesign::SubShapeBinder', 'Support'),
    ]

    extraTypePropHandlers = {
        # "PartDesign::Boolean,Group": {
        #     # after boolean, we need to make the group objects invisible
        #     'after': handle_boolean_group_prop,
        # },
    }

    specialTypePropHandlers = {
        # special handlers for some (TypeId, propName)
        "PartDesign::Chamfer,Base": handle_chamfer_base_prop, 
        # "Sketcher::SketchObject,AttachmentSupport": handle_sketcher_attachmentSupport,
    }

    specialPropHandlers = {
        # special handlers for some (propName) 
        "AttachmentSupport": handle_attachmentSupport,
    }

    if obj.TypeId == 'Sketcher::SketchObject':
        sketch_lines = sketch2python(obj, objVarName, objectList)
        for line in sketch_lines:
            add_method_line(line)
    # varname is object's name or label based on useLabel.
    # add new properties - properties that are not in default
    compare_result = compare_obj_prop_with_default(doc, obj, useLabel, propPattern=None, extraAttrs=None)
    for typeKey in ['MainObject', 'ViewObject']:
        propNames = sorted(compare_result[typeKey].keys())
        if typeKey == 'ViewObject':
            obj2 = obj.ViewObject
            objVarName2 = objVarName + '.ViewObject'
        else:
            obj2 = obj
            objVarName2 = objVarName
        for propName in propNames:
            # print(f"considering adding property {typeKey}/{propName} for object {obj.Name} TypeId={obj.TypeId}")
            if propName in skipProperties:
                continue
            # if (obj2.TypeId, propName) in skipObjProp:
            if match_key_startswith(skipTypeProp, (obj2.TypeId, propName)):
                continue

            if propIsReadonly(obj2, propName):
                skip = True

                if propName in [
                    'Label', # we need to set Label even though it is readonly.
                    ]:
                    skip = False
                if obj2.TypeId in [
                    'Spreadsheet::Sheet', # we need to add cells in spreadsheet, even they are readonly.
                    ]:
                    skip = False
                # if matchTuplePattern((obj2.TypeId, propName), needReadOnlyObjTypeProp):
                # if match_key_startswith(needReadOnlyObjTypeProp, (obj2.TypeId, propName)):
                if (obj2.TypeId, propName) in needReadOnlyObjTypeProp:
                    skip = False
                
                if skip:
                    # print(f"({obj.TypeId}, {propName}) of object {obj.Name} is readonly, skipping")
                    continue
            
            OnePropResult = compare_result[typeKey][propName]
            if OnePropResult['changeStatus'] in ['added', 'modified']:
                info1 = OnePropResult['info1']
                # this only defines the property, does not set its value yet. 
                # so we cannot return here. we need to continue to set its value below.

                if obj2.TypeId == 'Spreadsheet::Sheet' and is_cell_in_sheet(propName, obj2):
                    # this property is a cell in the spreadsheet
                    valueClass = info1['valueClass']
                    param_value = get_param_value(
                        info1,
                        isForFuncParam=False,
                        preferInchUnit=True,
                    )
                    add_method_line(f"{objVarName2}.set('{propName}', {param_value})")
                    # objs_waiting_for_recompute.add(objVarName2)

                    alias = obj2.getAlias(propName)
                    if alias is not None:
                        add_method_line(f"{objVarName2}.setAlias('{propName}', '{alias}')")
                        # alias is ready when added.
                        if useLabel:
                            objAliasKey = f"{obj.Label}.{alias}"

                        else:
                            objAliasKey = f"{obj.Name}.{alias}"
                        ready_expKeys.add(objAliasKey) # mark only alias as ready, not the prop itself.

                        # a call parameter is the function call interface. It is given by caller, not derived from spreadsheet.
                        # therefore, it cannot be a grounded expression.
                        #
                        # a cell can be a call parameter if 
                        #    1. the spreadsheet label is 'callsheet' (topCallsheetObj)
                        #    2. the cell is in column 'B' (call parameter column)
                        #    3. it has an alias
                        #    4. if its alias name is not ending with '_const'. eg slope_const=tan(1.7899)
                        #    5. its value is not an expression; or if expression, it is a static value expression.
                        #       static value expression is like: =1 in, =tan(1.7899)
                        if obj2 in topCallsheetObjs and propName.startswith('B'):
                            # # skip if alias that is special reserved names.
                            # if alias in ['ImportObj', 'ExportObj', 'Class', 'ImportParam', 'ImportInstance']:
                            #     continue
                            # skip alias if it is not a callParam
                            if not is_callParam(obj2, alias, checkParam=True):
                                continue

                            # print(f"checking call parameter for cell {propName} alias={alias} in callsheet spreadsheet {obj2.Label}")
                            expInfo = info1.get('expInfo', None)
                            if expInfo is not None and not expInfo['grounded']:
                                pass  # has ungrounded expression, skip
                            elif expInfo is not None and re.match(r'[.]B\d+$', expInfo['expression']):
                                # for grounded expession, only one case is not call parameter.
                                # 'Spreadsheet001.B2': '.B11',      # this is part of spreadsheet config table
                                pass  # has expression, skip
                            else:
                                call_param_name = alias
                                callsheet_params.append( (obj, objVarName2, alias, info1, call_param_name) )
                                valueClass = info1['valueClass']
                        
                                if valueClass == 'float' or valueClass == 'int' or valueClass == 'bool' or valueClass == 'str':   
                                    # eg npt_f_callsheet.set('B6', '12.0015')
                                    # no need to add '=' in front of it.
                                    equal_sign = ''
                                elif valueClass == 'Quantity':
                                    # Quantity property is like '0.03 in', '5.7999 mm', with a unit, need '='.
                                    # eg npt_f_callsheet.set('B10', '=0.03 in')
                                    equal_sign = '='
                                else:
                                    msg = f"Unsupported call parameter cell valueClass={valueClass}"
                                    print(msg)
                                    print(f"for cell {propName} in spreadsheet {obj.Name}")
                                    print(f"info1={pformat(info1)}")
                                    raise RuntimeError(msg)
                                # setting cell always need to quote the value.
                                # add_method_line(f"{objVarName2}.set('{propName}', f'{equal_sign}" + "{" + f"self.{call_param_name}" + "}" + "') # call param")
                                # callsheet_call_param_lines.append(f"{objVarName2}.set('{propName}', f'{equal_sign}" + "{" + f"self.{call_param_name}" + "}" + "')")
                                callsheet_call_param_lines.append(f"{objVarName2}.set({objVarName2}.getCellFromAlias('{alias}'), f'{equal_sign}" + "{" + f"self.{call_param_name}" + "}" + "')")
                                '''
                                if we did as below, which used the value from call parameter::
                                    npt_f_callsheet.set('B10', f'{self.holeDiaExpansion}') # call param
                                then later we should not do below, which is default, when setting expressions:
                                    npt_f_callsheet.set("B10", f"=0.03 in")
                                because the default would wipe out the call parameter (caller provided) value.
                                therefore, we mark the cell as already set with call parameter.
                                '''
                                objProp_already_set_with_call_param.add(f"{objVarName2}.{propName}")
                                
                    continue # done with this cell and its alias if any. therefore, cell and alias are not delayed.

                if OnePropResult['changeStatus'] in ['added']:
                    # for new property, we need to add it first.
                    # this only defines the property, does not set its value yet. 
                    # so we cannot return here. we need to continue to set its value below.
                    add_method_line(f'{objVarName2}.addProperty("{info1["propType"]}", "{propName}")')
    
                expInfo = info1.get('expInfo', None)
                if expInfo is not None and expInfo.get('varType', "") in ['Enum']:
                    # we don't set value to property whose value type is Enum. We don't even need to set it. 
                    # If we did, it actually likely to cause error if we not manage the order of ites expression
                    # precisely. Error is like: 
                    #     ... is not part of the enumeration
                    # but we still need to define the property. (done above)
                    # for now, we delay setting such properties until all expressions are added.
                    delayed_prop_exp_values.append( (obj, objVarName2, propName, info1) )
                    continue                     
                
                # set static value
                if (obj2.TypeId, propName) in delayedTypeProp:
                    # some properties need to be added after all objects are created.
                    delayed_prop_static_values.append( (obj, objVarName2, propName, info1) )
                    continue 

                typeId_propKey = f"{obj2.TypeId},{propName}"

                if typeId_propKey in extraTypePropHandlers:
                    if 'before' in extraTypePropHandlers[typeId_propKey]:
                        extraTypePropHandlers[typeId_propKey]['before'](doc, obj2, objVarName2, propName, info1)

                if typeId_propKey in specialTypePropHandlers:
                    # call special handler
                    handler_func = specialTypePropHandlers[typeId_propKey]
                    print(f"Handling special property: {typeId_propKey} for {objVarName2}.{propName} using {handler_func.__name__}")
                    # print(f"info1: {info1}")
                    handler_func(doc, obj2, objVarName2, propName, info1)
                elif propName in specialPropHandlers:
                    # call special handler
                    handler_func = specialPropHandlers[propName]
                    print(f"Handling special property: {typeId_propKey} for {objVarName2}.{propName} using {handler_func.__name__}")
                    # print(f"info1: {info1}")
                    handler_func(doc, obj2, objVarName2, propName, info1)
                else:
                    prefixPython = use_varname_in_prefixPython(doc, info1['prefixPython'])
                    add_method_line(f'{objVarName2}.{propName} = {prefixPython}')

                if typeId_propKey in extraTypePropHandlers:
                    if 'after' in extraTypePropHandlers[typeId_propKey]:
                        extraTypePropHandlers[typeId_propKey]['after'](doc, obj2, objVarName2, propName, info1)


def handle_attachmentSupport(doc, obj2, objVarName2, propName, info1):
    '''
    from
    npt_m_hole_bottom_sketch.AttachmentSupport = [(npt_m_hole_top, ('Face45'))]
    to
    npt_m_hole_bottom_sketch.AttachmentSupport = [(npt_m_hole_top, (get_seName_by_posName(npt_m_hole_top, 'Face', 'bottom1')))]
        
    '''
    propValue = info1['propValue']
    # [(npt_m_hole_top, ('Face45'))]
    result_string = '['
    for tup in propValue:
        # (npt_m_hole_top, ('Face45'))
        baseObj, subElementNames = tup
        baseObjName = baseObj.Name
        baseObjVarName = get_varName(doc, baseObjName)
        # result_string += f'({objVarName}, ('
        subElement_string_list = []
        for seName in subElementNames:
            if seName == '':
                seType = None
                posName = ''
                subElement_string_list.append("''")
            else:
                seType = re.sub(r'\d+$', '', seName)
                posName = get_posName_by_seName(baseObj, seName)
                subElement_string_list.append(f"get_seName_by_posName({baseObjVarName}, '{seType}', '{posName}')")
        result_string = '(' + baseObjVarName + ', (' + ', '.join(subElement_string_list) + '))'
    add_method_line(f'{objVarName2}.{propName} = {result_string}')
    add_method_line(f'{baseObjVarName}.Visibility = False  # hide base object') 

    if seType is not None:
        jsonDict = {propName: {'seType': seType, 'posName': posName}}
        jsonStr  = json.dumps(jsonDict).replace("\n", "") # 1-liner
        add_method_line(f'update_obj_prop_jsonDict({objVarName2}, "pythonFeature",' + jsonStr + ')')
     
def handle_chamfer_base_prop(doc, obj2, objVarName2, propName, info1):
    ''''
    set the Base property's edge using position name
    from 
        npt_fxf_chamfer_top.Base = (npt_fxf_instance.npt_fxf_boolean, ['Edge1'])
    to
        npt_fxf_chamfer_top.Base = (npt_fxf_instance.npt_fxf_boolean, [get_edgeName_by_position(npt_fxf_instance.npt_fxf_boolean, 'top')])
    '''
    propValue = info1['propValue']
    # (npt_fxf_instance.npt_fxf_boolean, ['Edge1'])
    seType_posName_list = []
    result_string = '('
    obj, subElementNames = propValue
    objName = obj.Name
    objVarName = get_varName(doc, objName)
    subElement_string_list = []
    for seName in subElementNames:
        seType = re.sub(r'\d+$', '', seName)
        posName = get_posName_by_seName(obj, seName)
        seType_posName_list.append({'seType': seType, 'posName': posName})
        se_string = f"get_seName_by_posName({objVarName}, '{seType}', '{posName}')"
        subElement_string_list.append(se_string)
    result_string = '(' + objVarName + ', [' + ', '.join(subElement_string_list) + '])'

    add_method_line(f'{objVarName2}.{propName} = {result_string}') 
    add_method_line(f'{objVarName}.Visibility = False  # hide chamfer base object')  
    jsonDict = {propName: seType_posName_list}
    jsonStr  = json.dumps(jsonDict).replace("\n", "") # 1-liner
    add_method_line(f'update_obj_prop_jsonDict({objVarName2}, "pythonFeature",' + jsonStr + ')')
    
'''
Error:  <Part> ViewProviderExt.cpp(1308): Cannot compute Inventor representation for the shape of tmpDocNoSave#Body: Bnd_Box is void
this is a temporary error due to incomplete object definition. a later recompute will fix it.
'''

def parse_args():
    '''
    use argparser to the following args:
        -d, --debug: incremental debug levels
                    -d -d: more verbose

        -un,--useName  use object.Name instead of object.Label for variable names
                           default is to use object.Label
        
        -sc,--sourceClass: specify the source class name to use in the generated script

        -nuv,--notUseVarName: not use variable names in prefixPython expressions
    '''

    import argparse
    parser = argparse.ArgumentParser(
        description='Objects To Python Macro', 
        exit_on_error=False, # default True will call sys.exit(1), which exits FreeCAD entirely. bad!!!
        # this switch doesn't work in FreeCAD 1.0.2. 
        )
    parser.add_argument('-d', '--debug', action='count', default=0,
                        help='increase debug verbosity level (can be used multiple times)')

    parser.add_argument('-un', '--useName', action='store_true', default=False,
                        help='use object.Name instead of object.Label for variable names')
    
    parser.add_argument('-tc', '--topClassName', type=str, default=None,
                        help='specify the top class name to use in the generated script')
    
    parser.add_argument('-nuv', '--notUseVarName', action='store_true', default=False,
                        help='not use variable names in prefixPython expressions')

    try:
        args = parser.parse_args(sys.argv[1:])
    except SystemExit:
        return None
    
    args = parser.parse_args()
    return args


def main():
    global debug, dialog, useVarName
    args = parse_args()
    if args is None:
        return

    print(f"args={pformat(args)}")

    debug = args.debug
    useLabel = not args.useName
    
    useVarName = not args.notUseVarName

    doc = App.activeDocument()

    if 'tmpDocNoSave' in doc.Label:
        raise RuntimeError(f"doc.Label={doc.Label} is a tmp doc.")
    if 'tmpDocNoSave' in doc.Name:
        raise RuntimeError(f"doc.Name={doc.Name} is a tmp doc. close it and open it again.")
    
    dialog = TextDialog()
        
    export_doc(doc, useLabel=useLabel, topClassName=args.topClassName)
    

if __name__ == '__main__':
    main()
    
