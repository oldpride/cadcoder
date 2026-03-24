import json
import os
from pprint import pformat
import re
import traceback
from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui

import inspect
from cadcoder.objtools import get_obj_str, map_obj_name_label
# from cadcoder.callsheettools import set_varName, get_expObjNames_string, get_impInsts_string
from cadcoder.containertools import extend_container_with_objects
from cadcoder.subelementtools import update_doc_seName
# from cadcoder.subelementtools import update_obj_seName

class baseClass:
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None):
        self.doc = doc
        self.objPrefix = objPrefix
        self.useLabel = useLabel
        self.importer = importer

        self.exportObj_by_objName = {}
        self.exportObjs = []

        # self.importObj_by_inst_objName = {}
        self.importInst_by_instName = {}
        
        self.className = self.__class__.__name__  # returns child class name
        self.moduleName = f"parts.{self.className}" # hardcoded module name
 
        # print(f"\n\nclassName={self.className}\n\n")
        self.instanceId = id(self)
        self.instanceName = instanceName

        self.callsheet = None  # to be set later

        self.lastObj = None
        self.lastShapeObj = None
        self.lastImportInstance = None

        if self.importer is not None:
            if isinstance(self.importer, dict):
                self.importerClassName = self.importer['className']
                self.importerInstanceId = self.importer['instanceId']
                self.importerInstanceChain = self.importer['instanceChain']
                self.importerInstanceName = self.importer['instanceName']
            else:  
                self.importerClassName = self.importer.className
                self.importerInstanceId = self.importer.instanceId 
                self.importerInstanceChain = self.importer.instanceChain
                self.importerInstanceName = self.importer.instanceName
        else:
            self.importerClassName = ""
            self.importerInstanceId = ""
            self.importerInstanceChain = ""
            self.importerInstanceName = ""
        
        if self.importerInstanceChain is None or self.importerInstanceChain == "":
            self.instanceChain = self.instanceName
        else:
            self.instanceChain = f"{self.importerInstanceChain}.{self.instanceName}"
        
        # get the call signature of our child (caller) class's caller
        # traceback.print_stack()
        import_call_frame = inspect.currentframe().f_back
        import_call_argvalues = inspect.getargvalues(import_call_frame)
        # print(f"Caller name: {import_call_frame.f_code.co_name}")
        # print(f"Arguments passed to caller: {import_call_argvalues.locals}")
        # {'self': <__main__.Npt_f object at 0x000001C36AF25550>, 'instanceName': 'myInstance', 
        # 'doc': <Document object at 000001C34CF738A0>, 'objPrefix': '', 'useLabel': True, 
        # 'importer': None, 'femaleOD_wall_spec': '0.08 in', 'female_height_spec': '0.9 in', 
        # 'holeDiaExpansion_spec': '0.03 in', 'horizontalScale': 1.1982, 'nominalID': '`1/4', 
        # 'verticalScale': 1.261, 'Npt_m': <class 'parts.Npt_m.Npt_m'>, 
        # '__class__': <class '__main__.Npt_f'>}
        
        import_call_params = import_call_argvalues.locals.copy()

        if 'importer' in import_call_params:
            del import_call_params['self']
            del import_call_params['__class__']
            if self.className in import_call_params:
                del import_call_params[self.className]
            import_call_params['doc'] = 'doc_placeholder'
            import_call_params['importer'] = 'importer_placeholder'
    
            # using json vs using repr
            #     we use json when we save the whole pythonSource into a property.
            #     but for individual parameters, we use repr to get the string 
            #     representation for easier use.
            # the following is using json.
            #     self.importerCallParams = json.dumps(import_call_params,
            #                                     #  indent=4, # this will break json to multiple lines.
            #                                      sort_keys=True)
            # the following is using repr.
            # self.importerCallParams = ", ".join([f"'{k}': {repr(import_call_params[k])}" for k in sorted(import_call_params.keys())])
            # self.importerCallParams = "{" + self.importerCallParams + "}"
            # the following using original python
            self.importerCallParams = import_call_params
            
        else:
            self.importerCallParams = {}

    def addPrefix(self, mystring):
        return f"{self.objPrefix}{mystring}"

    def get_objKey(self, obj):
        return obj.Label if self.useLabel else obj.Name
        
    def addPrefix(self, mystring):
        return f"{self.objPrefix}{mystring}"

    def get_objKey(self, obj):
        return obj.Label if self.useLabel else obj.Name

    def get_varName_in_caller(self, obj, caller_locals_items=None):
        # note: varName-to-obj may not have one-to-one mapping
        # for example, if caller creates multiple objects in a loop, this is 1-to-many mapping.
        # if caller reuses the same variable name to assign different objects, this is many-to-1 mapping.

        if caller_locals_items is None:
            frame = inspect.currentframe()
            caller_locals = frame.f_back.f_locals
            caller_locals_items = caller_locals.items()

        objVarName = None
        for varName, varObj in caller_locals_items:
            if varObj is obj:
                objVarName = varName
                break
        if objVarName is None:
            for varName, varObj in caller_locals_items:
                if isinstance(varObj, dict):
                    for k, v in varObj.items():
                        if v is obj:
                            objVarName = f"{varName}['{k}']"
                            break
        return objVarName
    
    def post_new_obj(self, obj, 
                    canConvertToPython=True, 
                    # some python-generated objects cannot be converted back to python 
                    # by our current implementation. For themn, we need to set False here.
                    objVarName=None, # when generating the class first time, callsheet is created at the end.
                                      # In this situation, objVarName will be set by update_callsheet().
                    
                     ):
        map_obj_name_label(self.doc, refreshCache=True) # ensure name-label map is up-to-date
        # print(f"map after adding obj: {pformat(map)}")
        
        frame = inspect.currentframe()
        caller_locals = frame.f_back.f_locals

        if objVarName is None:
            objVarName = self.get_varName_in_caller(obj, caller_locals.items())
            if objVarName is None:
                msg ="Cannot find obj variable name in caller's context"
                traceback.print_stack()
                print(f"obj name={obj.Name}, label={obj.Label}, TypeId={obj.TypeId}")
                print(msg)
                raise RuntimeError(msg)

        objKey = self.get_objKey(obj)
        obj.addProperty('App::PropertyString', 'pythonSource', 'Base', '')   
            
        info = {
            'canConvertToPython': canConvertToPython,
            'className':self.className, 
            'importerClassName': self.importerClassName,
            'importerInstanceId': self.importerInstanceId,
            'importerInstanceName': self.importerInstanceName,
            'importerCallParams': self.importerCallParams,
            'instanceId': f"{hex(self.instanceId)}",
            'instanceChain': self.instanceChain,
            'instanceName': self.instanceName,
            'moduleName':self.moduleName, 
            'objKey':objKey,
            'objName':obj.Name,
            'objLabel':obj.Label,
            'objVarName':objVarName,
            'objPrefix':self.objPrefix,        
            }
        # convert dict to json string
        
        obj.pythonSource = json.dumps(info, indent=4, sort_keys=True)        
        
        obj.setEditorMode('pythonSource', 0)  # 0: visible + editable, 1: hidden, 2: read-only (grayed out)
        self.exportObj_by_objName[obj.Name] = obj
        self.exportObjs.append(obj)

        self.lastObj = obj

        if hasattr(obj, "Shape"):
            self.lastShapeObj = obj
     

    def update_pythonFeature(self, obj, propDict:dict):
        '''
        add pythonFeature prop is it is not there.
        pythonFeature is the json of propDict - keyvalues.
        '''
        if not hasattr(obj, "pythonFeature"):
            obj.addProperty('App::PropertyString', 'pythonFeature', 'Base', '')
            pythonFeature = {}
        else:
            pythonFeature = json.loads(obj.pythonFeature)
            
        pythonFeature.update(propDict)
        obj.pythonFeature = json.dumps(pythonFeature, indent=4, sort_keys=True)

    def update_callsheet(self):
        if self.callsheet is None:
            # create callsheet spreadsheet
            callsheetName = self.addPrefix(f"{self.className.lower()}_callsheet")
            self.callsheet = self.doc.addObject("Spreadsheet::Sheet", callsheetName)
            self.post_new_obj(self.callsheet, objVarName=callsheetName)

        # set_varName(self.callsheet, 'ImportInsts', get_impInsts_string(self.importInst_by_instName), 'N', 'imported instances, info only, not control', alias='ImportInsts', refreshCache=True)
        # set_varName(self.callsheet, 'ExportObjs', get_expObjNames_string(self.exportObj_by_objName), 'N', 'exported objs, info only, not control', alias='ExportObjs', refreshCache=True)
        # set_varName(self.callsheet, 'Class', self.className, 'N', 'className, info only, not control', alias='Class', refreshCache=True)
        self.doc.recompute()
        # update_doc_seName(self.doc, refreshCache=True)
        
    # exposed methods
    def get_objs(self):
        return self.exportObj_by_objName.values()
    
    def get_objMap(self):
        return self.exportObj_by_objName
    
    top_objects = None
    def get_top_objects(self):
        if self.top_objects is not None:
            return self.top_objects
        from cadcoder.objtools import get_group_top_objects
        self.top_objects = get_group_top_objects(objList=self.exportObj_by_objName.values(), visibleOnly=False)
        return self.top_objects

    def update_imports(self, instance):
        # instanceId = id(instance)
        instanceName = instance.instanceName
        # self.importObj_by_inst_objName[instanceName] = {}

        # for k, v in instance.exportObj_by_objName.items(): 
        #     self.importObj_by_inst_objName[instanceName][k] = v

        self.importInst_by_instName[instanceName] = {
            'className': instance.className,
            'moduleName': instance.moduleName,
            'objPrefix': instance.objPrefix,
        }
        # {"npt_m_instance": {"className": "Npt_m", "moduleName": "parts.Npt_m", "objPrefix": ""}}
        # {"npt_f_instance": {"className": "Npt_f", "moduleName": "parts.Npt_f", "objPrefix": ""}}

        if self.lastObj is None:
            # only let import overwrite current lastObj when lastObj is None
            if instance.lastObj is not None:
                self.lastObj = instance.lastObj

        if self.lastShapeObj is None:
            # only let import overwrite current lastShapeObj when lastShapeObj is None
            if instance.lastShapeObj is not None:
                self.lastShapeObj = instance.lastShapeObj

        self.lastImportInstance = instance

    def container_append_object(self, container, obj):
        extend_container_with_objects(container, [obj])

    # def update_seNames(self):
    #     for obj in self.exportObjs:
    #         update_obj_seName(obj) # this triggers doc.recompute()
