
import json
import re
import traceback
from pdfclib.expressiontools import is_exp_grounded
from pdfclib.proptools import get_param_value, get_prop_info
from pdfclib.spreadsheettools import get_cell_list, find_next_row, get_content_by_cellAddr
from pdfclib.matchtools import match_key_startswith
from pprint import pformat

            
row_by_docKey_sheetLabel_varName = {}

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

    # make sure obj's label contains 'callsheet'
    if 'callsheet' not in sheetLabel:
        raise ValueError(f"Spreadsheet {obj.Name} label={obj.Label} label does not contain 'callsheet'")
    
    if docKey not in row_by_docKey_sheetLabel_varName:
        row_by_docKey_sheetLabel_varName[docKey] = {}
        
    if sheetLabel in row_by_docKey_sheetLabel_varName[docKey] and not refreshCache:
        return row_by_docKey_sheetLabel_varName[docKey][sheetLabel]
    
    row_by_docKey_sheetLabel_varName[docKey][sheetLabel] = {}

    cellList = get_cell_list(obj, refreshCache=refreshCache)

    # A cells are variableNames, 
    # B cells are values, 
    # C cells are isCallParam,
    # D cells are comments
    # loop through all A cells
    A_cells = [cell for cell in cellList if re.match(r'^A\d+$', cell)]
    for A_cell_addr in A_cells:
        # skip A1 as it is header
        if A_cell_addr == 'A1':
            continue
        
        rowNum = A_cell_addr[1:]
        B_cell_addr = 'B' + rowNum
        C_cell_addr = 'C' + rowNum
        D_cell_addr = 'D' + rowNum

        varName = obj.get(A_cell_addr)
        
        if B_cell_addr in cellList:
            try:
                value = obj.get(B_cell_addr)
            except Exception as e:
                value = ''
            content = obj.getContents(B_cell_addr)
            alias = obj.getAlias(B_cell_addr)
            
            #alias and varName should be the same
            if varName != alias:
                msg = f"{obj.Label} cell={B_cell_addr} has alias '{alias}' which does not match var name in {A_cell_addr}='{varName}'"
                print(msg)
                raise ValueError(msg)
        else:
            msg = f"varName '{varName}' has no value in {B_cell_addr}"
            print(msg)
            raise ValueError(msg)

        if C_cell_addr in cellList:
            isCallParam = obj.get(C_cell_addr)
        else:
            isCallParam = None

        if checkParam:
            if isCallParam == 'Y':
                if not is_exp_grounded(content):
                    msg = f"Call parameter '{varName}' in {obj.Label} cell={B_cell_addr} is not grounded: {content}"
                    print(msg)
                    traceback.print_stack()
                    raise ValueError(msg)
        if D_cell_addr in cellList:
            comment = obj.get(D_cell_addr)
        else:
            comment = None

        row_by_docKey_sheetLabel_varName[docKey][sheetLabel][varName] = {
            "rowNum": rowNum,
            "value": value,
            'alias': alias,
            "isCallParam": isCallParam,
            "content": content,
            "comment": comment,
        }
    return row_by_docKey_sheetLabel_varName[docKey][sheetLabel]

def get_rowDict_by_varName(sheet, varName, refreshCache=False, checkParam=False)->dict:
    row_by_varName = map_rowDict_by_varName(sheet, refreshCache=refreshCache, checkParam=checkParam)
    if varName in row_by_varName:
        return row_by_varName[varName]
    return None

def get_rowNum_by_varName(sheet, varName, refreshCache=False, checkParam=False)->int:
    rowDict = get_rowDict_by_varName(sheet, varName, refreshCache=refreshCache, checkParam=checkParam)
    if rowDict:
        return int(rowDict["rowNum"])
    return None


callParams_by_sheetName = {}
def get_callParams(sheet, refreshCache=False, checkParam=False):
    sheetName = sheet.Name
    if sheetName in callParams_by_sheetName:
        return callParams_by_sheetName[sheetName]
    rowDict_by_varName = map_rowDict_by_varName(sheet, refreshCache=refreshCache, checkParam=checkParam)
    callParams = []
    for varName in sorted(rowDict_by_varName.keys()):
        rowDict = rowDict_by_varName[varName]
        if rowDict.get("isCallParam") == "Y":
            callParams.append(varName)
    callParams_by_sheetName[sheetName] = callParams
    return callParams

def is_callParam(sheet, varName, refreshCache=False, checkParam=False):
    rowDict = get_rowDict_by_varName(sheet, varName, refreshCache=refreshCache, checkParam=checkParam)
    if rowDict:
        return rowDict.get("isCallParam") == "Y"
    return False

def parse_keyvalue(input_str:str ) ->dict:
    '''
    input_str=optioanl;condition=notNone
    ret={
    'optional' : True,
    'condition' : 'notNone',
    }
    '''

    ret = {}
    for pair in input_str.split(';'):
        pair = pair.strip()
        if '=' in pair:
            key, value = pair.split('=', 1)
            ret[key.strip()] = value.strip()
        elif pair:
            # if no '=', treat as boolean flag
            ret[pair] = True
        return ret
    
    return ret

parent_by_doc_child = {}
children_by_doc_parent = {}
callsheets_by_doc = {}
callsheetNames_by_doc = {}

def map_callsheets_relations_using_exp(doc, refreshCache=False):
    '''
    find top-level callsheets using expression analysis.
    if a callsheet's expression refers to another callsheet, then it is not a top-level callsheet.
    '''
    # we use docKey to distinguish different docs with same Name because we may have tmp docs with same Name.
    docKey = f"{doc.Name},{id(doc)}"
    if docKey in parent_by_doc_child and not refreshCache:
        return
    parent_by_child = {}
    children_by_parent = {}

    callsheet_objs = [obj for obj in doc.Objects if obj.TypeId == 'Spreadsheet::Sheet' and 'callsheet' in obj.Label]    
    callsheet_objNames = [obj.Name for obj in callsheet_objs]

    from pdfclib.expressiontools import get_obj_all_expInfo
    for child_callsheet in callsheet_objs:
        expInfo_by_objProp = get_obj_all_expInfo(doc, 
                                                child_callsheet, 
                                                useLabel=False, # use objName because our other mappings are by obj.Name
                                                # includeGrounded=False, # skip grounded expressions, eg, =10, =tan(1.7899)
                                                )
        for objProp in expInfo_by_objProp.keys():
            expInfo = expInfo_by_objProp[objProp]
            # print(f"    {objProp} expInfo={expInfo}")

            parentsObjNameProps = expInfo['parents']

            for parentObjNameProp in parentsObjNameProps:
                parentObjName, parentProp = parentObjNameProp.split('.', 1)

                if parentObjName not in callsheet_objNames:
                    # parent is not a callsheet, skip
                    continue

                if parentObjName == child_callsheet.Name:
                    # self-reference, skip
                    continue

                parent_by_child[child_callsheet.Name] = parentObjName
                if parentObjName not in children_by_parent:
                    children_by_parent[parentObjName] = []
                children_by_parent[parentObjName].append(child_callsheet.Name)

    parent_by_doc_child[docKey] = parent_by_child
    children_by_doc_parent[docKey] = children_by_parent
    callsheets_by_doc[docKey] = callsheet_objs
    callsheetNames_by_doc[docKey] = callsheet_objNames

    # print(f"Mapped callsheet relations for doc {doc.Name}:")
    # print(f"    parent_by_doc_child[{docKey}] = {pformat(parent_by_child)}")

    return

def get_top_callsheets_using_exp(doc):
    '''
    top callsheets are callsheets whose parent is None.
    using expression
    pro: removes the dependence on pythonSource.
    con: need stricter expression relationship - tree structure.
    '''
    map_callsheets_relations_using_exp(doc)
    docKey = f"{doc.Name},{id(doc)}"
    parent_by_child = parent_by_doc_child[docKey]
    callsheets = callsheets_by_doc[docKey]
    top_callsheets = []
    for callsheet in callsheets:
        if callsheet.Name not in parent_by_child:
            # this callsheet has no parent, it is a top callsheet
            top_callsheets.append(callsheet)
    return top_callsheets

def link_parent_child_callsheets(parentSheet, childSheet):
    '''
    for each call parameter in childSheet, 
        if parentSheet doesn't have the call parameter
            add it into parentSheet, with objPrefix.
        link the call parameter in childSheet to the corresponding call parameter in parentSheet
            using parentSheet's label.
    '''
    doc = childSheet.Document
    child_call_params = get_callParams(childSheet)
    parent_call_params = get_callParams(parentSheet)

    child_pythonSource_str = childSheet.pythonSource
    child_pythonSource = json.loads(child_pythonSource_str)

    child_objPrefix = child_pythonSource['objPrefix']

    for callParam in child_call_params:
        call_value = childSheet.get(callParam)
        profixedCallParam = f"{child_objPrefix}{callParam}"
        child_propInfo = get_prop_info(doc, childSheet, callParam)
        child_valueClass = child_propInfo['valueClass']
        child_row = get_rowNum_by_varName(childSheet, callParam)
        try:
            child_comment = childSheet.get(f'D{child_row}')
        except Exception as e:
            # print(f"Failed to get comment for {callParam} at D{child_row}: {e}. skipped D{child_row}")
            child_comment = ""

        if profixedCallParam not in parent_call_params:
            parent_row = find_next_row(parentSheet)
            parentSheet.set(f'A{parent_row}', profixedCallParam)

            if child_valueClass == 'Quantity':
                parentSheet.set(f'B{parent_row}', f'={call_value}')
            else:
                parentSheet.set(f'B{parent_row}', f'{call_value}')

            parentSheet.set(f'C{parent_row}', 'Y')

            if child_objPrefix or child_comment:
                parentSheet.set(f'D{parent_row}', f"{child_comment}")
                # print(f"set comment={child_objPrefix} {child_comment}")
            parentSheet.setAlias(f'B{parent_row}', profixedCallParam)
            parentSheet.recompute()  # recompute after setting new values; otherwise other obj won't know its existence.
         
            print(f'linking {childSheet.Label}.{callParam} at B{child_row} to <<{parentSheet.Label}>>.{profixedCallParam}')
            childSheet.set(f'B{child_row}', f'=<<{parentSheet.Label}>>.{profixedCallParam}')
            childSheet.recompute()
        else:
            parent_row = get_rowNum_by_varName(parentSheet, profixedCallParam)
            expected_expr_by_label = f'=<<{parentSheet.Label}>>.{profixedCallParam}'
            expected_expr_by_name = f'=<<{parentSheet.Name}>>.{profixedCallParam}'
            current_expr = get_content_by_cellAddr(childSheet, f'B{child_row}')
            if current_expr not in [expected_expr_by_label, expected_expr_by_name]:
                print(f'mismatched expr in {childSheet.Label}: call_param={callParam} at B{child_row}: expected_expressions={expected_expr_by_label} or {expected_expr_by_name}, current_expression={current_expr}')
            else:
                print(f'expression matches expectation in {childSheet.Label}: call_param={callParam} at B{child_row}: expression={current_expr}')

    