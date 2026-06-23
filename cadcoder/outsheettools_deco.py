import traceback
from cadcoder.spreadsheettools import get_cell_list, set_cellValue_by_propInfo
from cadcoder.triggertools import link_watch_to_target
from cadcoder.objtools import get_obj_by_objKey, map_obj_name_label, sort_objs_by_downstream
from cadcoder.proptools import get_prop_info
import re

row_by_docKey_sheetLabel_varName = {} # {docKey: {sheetLabel: {varName: rowDict}}}

def map_rowDict_by_varName(obj, refreshCache=False, checkParam=False) -> dict:
    '''
    callsheet format
        variableName,value,isCallParam,comment

    we return a dict, keyed by variableName.
    '''

    doc = obj.Document
    docKey = f"{doc.Name},{id(doc)}"

    # make sure obj is a spreadsheet
    if obj.TypeId != 'Spreadsheet::Sheet':
        raise ValueError(f"Object name={obj.Name} label={obj.Label} is not a Spreadsheet::Sheet")
    
    sheetLabel = obj.Label

    # make sure obj's label ends with outsheet
    if not sheetLabel.endswith('outsheet'):
        raise ValueError(f"Spreadsheet {obj.Name} label={obj.Label} label does not end with 'outsheet'")
    
    if docKey not in row_by_docKey_sheetLabel_varName:
        row_by_docKey_sheetLabel_varName[docKey] = {}
        
    if sheetLabel in row_by_docKey_sheetLabel_varName[docKey] and not refreshCache:
        return row_by_docKey_sheetLabel_varName[docKey][sheetLabel]
    
    row_by_docKey_sheetLabel_varName[docKey][sheetLabel] = {}

    cellList = get_cell_list(obj, refreshCache=refreshCache)

    # A column is variableName, 
    # B column is value, 
    # C column is source,

    A_cells = [cell for cell in cellList if re.match(r'^A\d+$', cell)]
    for A_cell_addr in A_cells:
        # skip A1 as it is header
        if A_cell_addr == 'A1':
            continue
        
        rowNum = A_cell_addr[1:]
        B_cell_addr = 'B' + rowNum
        C_cell_addr = 'C' + rowNum

        varName = obj.get(A_cell_addr)
        
        if B_cell_addr in cellList:
            try:
                value = obj.get(B_cell_addr)
            except Exception as e:
                value = None
        else:
            msg = f"varName '{varName}' has no value in {B_cell_addr}"
            print(msg)
            # raise ValueError(msg)

        content = obj.getContents(B_cell_addr)
        alias = obj.getAlias(B_cell_addr)
        
        #alias and varName should be the same
        if varName != alias:
            msg = f"{obj.Label} cell={B_cell_addr} has alias '{alias}' which does not match var name in {A_cell_addr}='{varName}'"
            print(msg)
            raise ValueError(msg)

        if C_cell_addr in cellList:
            source = obj.get(C_cell_addr)
        else:
            source = None
            msg = f"varName '{varName}' has no source in {C_cell_addr}"
            print(msg)
            # traceback.print_stack()
            # raise ValueError(msg)
        
        row_by_docKey_sheetLabel_varName[docKey][sheetLabel][varName] = {
            "rowNum": rowNum,
            "value": value,
            'alias': alias,
            "source": source,
            "content": content,
        }
    return row_by_docKey_sheetLabel_varName[docKey][sheetLabel]

def update_outsheet(outsheetObj, link=False, refreshCache=False):
    '''
    link outsheet based on the source column using trigger
    '''

    doc = outsheetObj.Document

    row_by_varName = map_rowDict_by_varName(outsheetObj, refreshCache=refreshCache)

    map_obj_name_label(doc, refreshCache=refreshCache)

    updated = 0
    for varName, rowDict in row_by_varName.items():
        source = rowDict['source']
        sourceObjRaw, sourcePropName = source.split('.')
        if sourceObjRaw.startswith('<<'):
            # this is a obj label
            sourceObjLabel = sourceObjRaw[2:-2]
            sourceObj = get_obj_by_objKey(doc, sourceObjLabel, useLabel=True)
        else:
            # this is a obj name
            sourceObjName = sourceObjRaw
            sourceObj = get_obj_by_objKey(doc, sourceObjName, useLabel=False)
        if sourceObj is None:
            msg = f"Cannot find source object for outsheet {outsheetObj.Label} varName={varName} source='{source}'"
            print(msg)
            raise ValueError(msg)
        
        # for update only, we only set the value, not trigger the link
        try:
            source_propInfo = get_prop_info(doc, sourceObj, sourcePropName)
        except Exception as e:
            msg = f"Failed to get value from source={source}"
            print(msg)
            traceback.print_exc()
            raise RuntimeError(msg)  
        
        source_value = source_propInfo['propValue']
        address_B = 'B' + rowDict['rowNum']

        try:
            current_cell_value = outsheetObj.get(address_B)
        except Exception as e:
            current_cell_value = None
        if current_cell_value != source_value:
            print(f"Updating outsheet {outsheetObj.Label} varName={varName} cell={address_B} from '{current_cell_value}' to '{source_value}', source={source}")
            set_cellValue_by_propInfo(outsheetObj, address_B, source_propInfo)
            updated += 1

        if not link:
            continue
        else:
            updated += link_watch_to_target(doc, sourceObj, sourcePropName, outsheetObj, varName, useLabel=True)
    if not updated:
        print(f"No update needed for outsheet={outsheetObj.Label}")
    else:
        print(f"recompute doc after updating")
        doc.recompute()
    return updated

def update_doc_outsheets(doc, link=False, refreshCache=False):
    '''
    link all outsheets in the doc
    '''
    # first sort objects by dependency, so that we link outsheets after the source objects are ready
    result = sort_objs_by_downstream(doc, 
                                     objList = doc.Objects, # all objs of the doc. default is selected object.
                                     useLabel=True, refreshCache=refreshCache)

    updated = 0
    for objLabel in result['ready_list']:
        obj = get_obj_by_objKey(doc, objLabel, useLabel=True)
        if obj.TypeId == 'Spreadsheet::Sheet' and obj.Label.endswith('outsheet'):
            updated += update_outsheet(obj, link=link, refreshCache=refreshCache)

    if not updated:
        print("No outsheet update needed.")
    return updated
