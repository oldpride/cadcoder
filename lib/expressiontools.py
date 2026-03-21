from pprint import pformat
import re
import traceback
import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.objtools import get_name_by_label, get_label_by_name, get_obj_by_objKey
from pdfclib.proptools import get_extended_prop_by_name

'''
configuration table create a enum property, total needs 3 lines in expression.
their order matters.
    # these must be first 
    NPT_M_Thread_Spreadsheet.setExpression('.nominalOD.Enum', 'cells[<<A3:|>>]') 

    # the following two lines can interchange order
    NPT_M_Thread_Spreadsheet.setExpression('.cells.Bind.B2.I2', 'tuple(.cells; <<B>> + str(hiddenref(nominalOD) + 3); <<I>> + str(hiddenref(nominalOD) + 3))')
    NPT_M_Thread_Spreadsheet.set('A2', '=hiddenref(.nominalOD.String)')

there are also properiies.
    ...
    NPT_M_Thread_Spreadsheet.set('C2', '=.C7')
    NPT_M_Thread_Spreadsheet.set('D2', '=.D7')
    ...
    NPT_M_Thread_Spreadsheet.addProperty("App::PropertyEnumeration", "nominalOD")

    # the nominalOD property must be set after the 3 expression lines (on top) are set 
    # and recompute is done, 
    # because nominalOD depends on the enum property created by the first expression line above.
    NPT_M_Thread_Spreadsheet.nominalOD = '`1 / 2'

added: MainObject-nominalOD
  Object value:
    propType: App::PropertyEnumeration
    propValue: `3 / 4
    valueTypeId: None
    valueClass: str
    valueClassTree: {'str'}
    valueObjName: None
    readonly: False
    valuePython: '`3 / 4'
    propName: nominalOD
    expInfo:
                    {'parents': ['NPT_M_Thread_Spreadsheet.cells[<<A3:|>>]'],
                     'expression': 'cells[<<A3:|>>]',
                     'grounded': False,
                     'rawExpression': 'cells[<<A3:|>>]',
                     'source': 'ExpressionEngine',
                     'varName': '.nominalOD.Enum',
                     'varType': 'Enum'}
'''

        
def token_to_refObjProp(doc, token: str, useLabel: bool, objHint=None, propNameHint:str=None):
    dep = token_to_rawObjProp(token, propNameHint=propNameHint, objHint=objHint)
    if dep is None:
        return None
    rawObjProp, refPropName = dep  # refObjRaw may be obj name or obj label

    if rawObjProp.startswith('<<') and rawObjProp.endswith('>>'):
        # it is an object label reference
        # <<NPT_M_Global_Spreadsheet>>.HoleDiaExansion - obj label
        refObjLabel = rawObjProp[2:-2]
        try:
            refObjName = get_name_by_label(doc, refObjLabel)
        except Exception:
            refObjName = None
    else:
        # refObjKey is obj name
        # Spreadsheet001.HoleDiaExansion - obj name
        refObjName = rawObjProp
        try:
            refObjLabel = get_label_by_name(doc, refObjName)
        except Exception:
            refObjLabel = None

    if refObjName is None or refObjLabel is None:
        msg = f"Cannot resolve reference object's name or label."
        print(msg)
        print(f"   token={token} -> refObjRaw={rawObjProp}, refPropName={refPropName}, useLabel={useLabel}")
        raise RuntimeError(msg)
    
    if useLabel:
        return (refObjLabel, refPropName)
    else:
        return (refObjName, refPropName)

def dump_all_upstream_expObjPropKeys(doc, obj, propName, level=0, indentCount=0, debug=0, useLabel=False) -> set:
    '''
    dump dependencies of an object's property expression.
    '''
    if useLabel:
        objKey = obj.Label
    else:
        objKey = obj.Name

    upstreams = get_all_upstream_expObjPropKeys(doc, objKey, propName, useLabel, level=level, indentCount=indentCount, debug=debug, printDetail=True)
    return upstreams

get_all_upstreams_stack = []

def get_all_upstream_expObjPropKeys(doc, objKey, propName, useLabel, level=0, indentCount=0, debug=0, printDetail=False) -> set:
    # print(f"objKey={objKey}, propName={propName}, level={level}, indentCount={indentCount}, useLabel={useLabel}")
    '''
    dump dependencies of an object's property expression.
    '''
    if level == 0:
        get_all_upstreams_stack.clear()

    objPropKey = f"{objKey}.{propName}"

    get_all_upstreams_stack.append(objPropKey)
    max_level = 20
    if level > max_level:
        raise RuntimeError(f"Exceeded max recursion level {max_level}. stack={get_all_upstreams_stack}")
    
    ret = set()

    indent = '    ' * (indentCount+1)

    obj = get_obj_by_objKey(doc, objKey, useLabel)

    try:
        # propValue = obj.getPropertyByName(propName)
        propValue = get_extended_prop_by_name(obj, propName) # propName can be prop, alias, constraint
    except Exception as e:
        if debug:
            print(f"{indent}exception='{e}' at stack={get_all_upstreams_stack}")
        get_all_upstreams_stack.pop()
        return ret
        
    expInfo = get_expInfo_by_objPropKey(doc, objPropKey, useLabel, debug=debug)
    # print(f"{indent}objPropKey={objPropKey}, useLabel={useLabel}, expInfo={pformat(expInfo)}")

    if expInfo is None:
        if printDetail:
            print(f"{indent}{objPropKey}='{propValue}' (no expression)")
    else:
        if printDetail:
            print(f"{indent}{objPropKey}='{propValue}'")
            print(f"{indent}rawExpression='{expInfo['rawExpression']}'")
            print(f"{indent}expression='{expInfo['expression']}'")
            print(f"{indent}source={expInfo['source']}, grounded={expInfo['grounded']}")
        
        upstreams = expInfo['parents']
        
        if upstreams: 
            if printDetail:
                print(f"{indent}upstreams: {upstreams}")
           
            for upstream in upstreams:
                ret.add(upstream)
                uObjKey, uPropName, *_ = upstream.split('.')
                # objKey2 can be a label, but it is not wrapped with << and >>.
                if useLabel:
                    uObjLabel = uObjKey
                    try:
                        uObjName = get_name_by_label(doc, uObjLabel)
                    except Exception as e:
                        uObjName = None
                else:
                    uObjName = uObjKey
                    try:
                        uObjLabel = get_label_by_name(doc, uObjName)
                    except Exception as e:
                        uObjLabel = None

                if uObjName is None or uObjLabel is None:
                    msg = f"Cannot resolve upstream object's name or label:"
                    print(f"   obj name={obj.Name}, label={obj.Label}")
                    print(f"   upstream={upstream}, useLabel={useLabel}")
                    print(f"   ")
                    raise RuntimeError(msg)
                dObj = doc.getObject(uObjName)
                if not dObj:
                    msg = f"Cannot get upstream object:"
                    print(f"   obj name={obj.Name}, label={obj.Label}")
                    print(f"   upstream={upstream}, useLabel={useLabel}")
                    print(f"   uObjName={uObjName}, uObjLabel={uObjLabel}")
                    raise RuntimeError(msg)
                ret.update(get_all_upstream_expObjPropKeys(doc, uObjKey, uPropName, useLabel, level=level+1, 
                                indentCount=indentCount+1, debug=debug, 
                                printDetail=printDetail, # printDetail only at debug level.
                                ))
        # summarize at top level
        if level == 0 and printDetail:
            print(f"{indent}All upstreams of {objPropKey}:")
            for item in sorted(ret):
                print(f"{indent}    {item}")
    get_all_upstreams_stack.pop()

    
    return ret

allExp_by_objKey = {}

def get_obj_all_expInfo(doc, obj, useLabel, includeGrounded=True, debug=0):
    '''
    get all expressions information of an object.
    cache by obj.
    '''
    if useLabel:
        objKey = obj.Label
    else:
        objKey = obj.Name
    if objKey in allExp_by_objKey:
        return allExp_by_objKey[objKey]

    info_by_objProp = {}

    # fnd in ExpressionEngine
    try:
        eelist = obj.ExpressionEngine
    except Exception:
        eelist = None
    
    if eelist:
        # [('Base_b', 'Base_a + 1')]
        # [('.nominalOD.Enum', 'cells[<<A3:|>>]')]
        varType = ""
        for row in eelist:
            varName = row[0]
            rawExpression = row[1] # expression can be using obj name of label, or both.
            # ExpressionEngine's var name corresponds to obj's propName

            if not includeGrounded:
                if is_exp_grounded(rawExpression):
                    continue

            # try to extract propName from varName
            propName = varName
            if propName.startswith('.'):
                # in [('.nominalOD.Enum', 'cells[<<A3:|>>]')]
                # .nominalOD.Enum -> nominalOD.Enum
                propName = propName[1:]  # skip leading '.'
            if '.' in propName:
                # nominalOD.Enum -> nominalOD
                # 'cells.Bind.B1.B1' -> 'cells'
                parts = propName.split('.')
                propName = parts[0]  # only keep the first part as propName
                varType = parts[1]  # Enum, Bind, etc.
            objPropKey = f"{objKey}.{propName}"

            info = parse_rawExpression(doc, rawExpression, objKey, propName, useLabel)
            info['varName'] = varName
            info['source'] = 'ExpressionEngine'
            info['grounded'] = False # ExpressionEngine expressions are all ungrounded
            info['comment'] = 'ExpressionEngine expressions are all ungrounded'
            # info['grounded'] = is_exp_grounded(rawExpression)
            if not (varType is None or varType == ""):
                # print(f"objKey={objKey}, row={row} -> varName={varName}, varType={varType}")
                info['varType'] = varType
            info_by_objProp[objPropKey] = info

    '''
    handle 
    ('.nominalOD.Enum', 'cells[<<A3:|>>]')
    'NPT_M_Thread_Spreadsheet..nominalOD.Enum': 'cells[<<A3:|>>]',
    '''
    # find in Spreadsheet cells
    if obj.TypeId == "Spreadsheet::Sheet":
        '''
        cell property vs object property.
            - cell property: A1, B2, etc. its expression is in cell contents, starting with '='.
            - object property: eg, Base_C3. its expression is in ExpressionEngine.
        
        spreadsheet object's ExpressionEngine does not have expressions defined in cell contents.
        Therefore, we don't worry about duplication when adding celle contents and ExpressionEngine.
            
        added: MainObject-B3
        Object value:
            propType: App::PropertyInteger
            propValue: 2
            valueTypeId: None
            valueClass: int
            valueClassTree: {'int'}
            valueObjName: None
            readonly: True
            valuePython: 2
            propName: B3
        added: MainObject-Base_C3
        Object value:
            propType: App::PropertyFloat
            propValue: 0.5
            valueTypeId: None
            valueClass: float
            valueClassTree: {'float'}
            valueObjName: None
            readonly: False
            valuePython: 0.5000
            propName: Base_C3            
        '''
        for propName in obj.PropertiesList:
            # print(f"Checking {obj.Name} propName={propName}")
            # get cell names.
            if re.fullmatch(r"[A-Z]\d+", propName):
                # get cell contents
                content = obj.getContents(propName)
                objPropKey = f"{objKey}.{propName}"
                if content[0] == "=":                
                    rawExpression = content[1:]  # skip '='
                    if not includeGrounded:
                        if is_exp_grounded(rawExpression):
                            continue
                    info = parse_rawExpression(doc, rawExpression, objKey, propName, useLabel)
                    info['source'] = 'SpreadsheetCell'
                    info['varName'] = propName
                    info['grounded'] = is_exp_grounded(rawExpression)
                    info_by_objProp[objPropKey] = info
                # get aliases
                alias = obj.getAlias(propName)
                # print(f"Checking alias for {obj.Name} propName={propName}, alias={alias}")
                if alias:
                    # alias are all ungrounded
                    objPropAlias = f"{objKey}.{alias}"

                    # we can use either obj name or label in expression.
                    # label is more readable, but needs wrapping with << and >>.
                    rawExpression = f"<<{obj.Label}>>.{propName}"

                    info = parse_rawExpression(doc, rawExpression, objKey, alias, useLabel)
                    info['source'] = 'SpreadsheetAlias'
                    info['varName'] = alias
                    info['grounded'] = False # aliases are all ungrounded
                    info_by_objProp[objPropAlias] = info
        
    allExp_by_objKey[objKey] = info_by_objProp
    return info_by_objProp

allExpInfo_by_docKey = {}

def get_doc_all_expInfo(doc, useLabel, includeGrounded=True, debug=0):
    '''
    'raw' means expressions are as-is in ExpressionEngine or cell contents,
    which may contain both object names and labels.
    eg, <<NPT_M_Global_Spreadsheet>>.horizontalScale  # labels are wrapped with << and >>.
        Spreadsheet001.horizontalScale # object names.

    examples from dump_props.py:
    added: MainObject-Base_a
    Object value:
        propType: App::PropertyFloat
        propValue: 0.0
        valueTypeId: None
        valueClass: float
        valueClassTree: {'float'}
        valueObjName: None
        readonly: False
        valuePython: 0.0000
        propName: Base_a
    added: MainObject-Base_b
    Object value:
        propType: App::PropertyFloat
        propValue: 1.0
        valueTypeId: None
        valueClass: float
        valueClassTree: {'float'}
        valueObjName: None
        readonly: False
        valuePython: 1.0000
        propName: Base_b
    modified: MainObject-ExpressionEngine
    Object value:
        propType: App::PropertyExpressionEngine
        propValue: [('Base_b', 'Base_a + 1')]
        valueTypeId: None
        valueClass: list
        valueClassTree: {'list/tuple/str'}
        valueObjName: None
        readonly: False
        valuePython: [('Base_b', 'Base_a + 1')]
        propName: ExpressionEngine
    '''
    
    docKey = f"{doc.Name},{id(doc)}"

    if docKey in allExpInfo_by_docKey:
        return allExpInfo_by_docKey[docKey]
    
    # print stack for debugging
    # traceback.print_stack()
    # print(f"useLabel={useLabel}")
    
    info_by_objProp = {}

    for obj in sorted(doc.Objects, key=lambda o: o.Label):
        objExps = get_obj_all_expInfo(doc, obj, useLabel, includeGrounded=includeGrounded, debug=debug)
        info_by_objProp.update(objExps)    # flatten away objKey level. 
                    
    allExpInfo_by_docKey[docKey] = info_by_objProp
    if debug:
        print(f"get_doc_all_rawExpressions: allExp_by_docKey[{docKey}]={pformat(info_by_objProp)}")

    return info_by_objProp

def parse_rawExpression(doc, rawExpression: str, objKey:str, propName: str, useLabel: bool) -> dict:
    tokens = get_expression_tokens(rawExpression)

    parents = set()

    if useLabel:
        objName = get_name_by_label(doc, objKey)
        obj = doc.getObject(objName)
    else:
        obj = doc.getObject(objKey)

    # we use this map to convert rawExpression to use obj names or labels consistently.
    refObjKey_by_refObjRaw = {}
    prefixedObjKey_by_refObjRaw = {}

    for token in tokens:
        pair = token_to_rawObjProp(token, propNameHint=propName, objHint=obj)
        if pair is None:
            # print(f"parse_rawExpression: cannot parse token='{token}' in rawExpression='{rawExpression}'")
            continue
        refObjRaw, refPropName = pair  # refObjRaw may be obj name or obj label

        if refObjRaw is None or refObjRaw == '':
            # this is a local prop reference without obj, eg, '.Base_a' or 'Base_a'
            # return (objKey, refPropName)

            if propName == refPropName:
                # self reference, skip
                continue

            parents.add(f"{objKey}.{refPropName}")
            continue

        if refObjRaw.startswith('<<') and refObjRaw.endswith('>>'):
            # it is an object label reference
            # <<NPT_M_Global_Spreadsheet>>.HoleDiaExansion - obj label
            refObjLabel = refObjRaw[2:-2]   
            
            try:
                refObjName = get_name_by_label(doc, refObjLabel)
            except Exception:
                refObjName = None
            if not useLabel:
                # if useLabel is False, we need to convert rawExpression to use obj names later.
                # and that will need this mapping.
                refObjKey_by_refObjRaw[refObjRaw] = refObjName
                prefixedObjKey_by_refObjRaw[refObjRaw] = "{self.addPrefix('" + refObjName + "')}"
            else:
                prefixedObjKey_by_refObjRaw[refObjRaw] = "<<{self.addPrefix('" + refObjLabel + "')}>>"
        else:
            # refObjKey is obj name
            # Spreadsheet001.HoleDiaExansion - obj name
            refObjName = refObjRaw
            try:
                refObjLabel = get_label_by_name(doc, refObjName)
            except Exception:
                refObjLabel = None
            if useLabel:
                # if useLabel is True, we need to convert rawExpression to use obj labels later.
                # and that will need this mapping.
                refObjKey_by_refObjRaw[refObjRaw] = f"<<{refObjLabel}>>"
                prefixedObjKey_by_refObjRaw[refObjRaw] = "<<{self.addPrefix('" + refObjLabel + "')}>>"
            else:
                prefixedObjKey_by_refObjRaw[refObjRaw] = "{self.addPrefix('" + refObjName + "')}"

        if refObjName is None or refObjLabel is None:
            msg = f"Cannot parse rawExpression into obj and prop."
            print(msg)
            print(f"   rawExpression={rawExpression}")
            print(f"   token={token} -> refObjRaw={refObjRaw}, refPropName={refPropName}")
            raise RuntimeError(msg)
        if useLabel:
            refObjKey = refObjLabel
        else:
            refObjKey = refObjName


        if propName == refPropName and refObjKey == objKey:
            # self reference, skip
            continue
        parents.add(f"{refObjKey}.{refPropName}")

    # convert rawExpression to use obj names or labels consistently.
    expression = rawExpression
    
    for refObjRaw in reversed(sorted(refObjKey_by_refObjRaw.keys(), key=lambda x: len(x))):
        # need to sort in reverse order to avoid partial replacement.
        refObjKey = refObjKey_by_refObjRaw[refObjRaw]
        expression = expression.replace(refObjRaw, refObjKey)
        
    prefixedExp = rawExpression
    for refObjRaw in reversed(sorted(prefixedObjKey_by_refObjRaw.keys(), key=lambda x: len(x))):
        # need to sort in reverse order to avoid partial replacement.
        prefixedObjKey = prefixedObjKey_by_refObjRaw[refObjRaw]
        prefixedExp = prefixedExp.replace(refObjRaw, prefixedObjKey)
    info = {
        'rawExpression': rawExpression,
        'expression': expression,
        'prefixedExp': prefixedExp,
        'parents': sorted(parents),
    }

    return info


def is_exp_grounded(expression: str) -> bool:

    '''
    ungrounded vs grounded props:

    ungrounded props are not grounded, meaning they depend on others by expressions.
    eg, 
        'Spreadsheet.B10': 'realOD + holeDiaExansion',
        'Spreadsheet.thread_start_r': 'Spreadsheet.B20', 
        'Spreadsheet001.cells': 'tuple(.cells; <<B>> + '
                                                'str(hiddenref(nominalOD) + 3); '
                                            '<<I>> + str(hiddenref(nominalOD) '
                                            '+ 3))',
        
                                            
    grounded props not depending on others by expressions.
    eg,
        'Spreadsheet001.B2': '.B11',      # this is part of spreadsheet config table
        'Spreadsheet001.nominalOD': 'cells[<<A3:|>>]',  # this is part of spreadsheet config table
                                                        # because it cannot resolve to anything else,
                                                        # we consider it grounded.
        'Spreadsheet.B3': 'tan(1.7899)',
        'Spreadsheet.B16': '1.5 in',
          
    '''
    if re.search(r'^[.][A-Z]\d+$', expression):
        # eg, in 'Spreadsheet001.B2': '.B11'
        return True
    
    # eg, 'cells[<<A3:|>>]' or 'cells[<<A2:A3>>]'
    if re.search(r'^cells\[<<[A-Z]\d+:?\|?>>\]$', expression):
        return True
    if re.search(r'^cells\[<<[A-Z]\d+:[A-Z]\d+>>\]$', expression):
        return True
    
    # if no var token in expression refers to other properties, then it is grounded.
    # eg, tan(1.7899), 1.5 in
    tokens = get_expression_tokens(expression)
    found_var = False
    for token in tokens:
        if token in ['in',  # inch
                     'mm',
                    ]:
            continue
        # skip numeric literals
        if re.fullmatch(r'[-+]?[0-9]*\.?[0-9]+', token):
            continue
        found_var = True
        break
    if not found_var:
        return True
    
    return False

def is_objProp_expression(doc, objPropKey:str, useLabel) -> bool:
    '''
    check whether an objProp is an expression.
    '''
    exprInfo_by_objProp = get_doc_all_expInfo(doc, useLabel)
        
    if objPropKey in exprInfo_by_objProp:
        return True
    return False

'''
we need find the dependency among the expressions.

examples:
    'Cone.Radius1': 'Spreadsheet.cone_bottom_small_r',
    'Cone.Radius2': 'Spreadsheet.cone_top_big_r',
    'Helix.Angle': '1.7899',
    'Helix.Height': 'Spreadsheet.helix_height',
    'Helix.Pitch': 'Spreadsheet.pitch',
    'Helix.Radius': 'Spreadsheet.helix_r',
    'Sketch.Constraints[10]': '<<NPT_M_Dimension_Spreadsheet>>.thread_cutter_side',
    'Sketch.Constraints[11]': '<<NPT_M_Dimension_Spreadsheet>>.thread_start_r',
    'Spreadsheet.B10': 'realOD + holeDiaExansion',
    'Spreadsheet.B11': 'specOD / 2',
    'Spreadsheet.B12': 'expandedOD * 0.5',
    'Spreadsheet.B13': 'cone_top_big_r_spec - slope * '
                        'male_height_spec',
    'Spreadsheet.B14': 'cone_bottom_small_r_spec * '
                        '<<NPT_M_Global_Spreadsheet>>.horizontalScale',
    'Spreadsheet.B15': '<<NPT_M_Thread_Spreadsheet>>.TPI',
    'Spreadsheet.B16': '1 in / TPI * '
                        '<<NPT_M_Global_Spreadsheet>>.verticalScale',
    'Spreadsheet.B17': 'cone_height + 0.1 in',
    'Spreadsheet.B18': 'cone_bottom_small_r',
    'Spreadsheet.B19': 'pitch + 0.0001 in',
    'Spreadsheet.B2': '<<NPT_M_Thread_Spreadsheet>>.NominalOD',
    'Spreadsheet.B20': 'cone_bottom_small_r + 0.001 in',
    'Spreadsheet.B3': 'tan(1.7899)',
    'Spreadsheet.B4': '<<NPT_M_Thread_Spreadsheet>>.RealOD',
    'Spreadsheet.B5': 'specOD * '
                        '<<NPT_M_Global_Spreadsheet>>.horizontalScale',
    'Spreadsheet.B6': '<<NPT_M_Global_Spreadsheet>>.NPT_M_height',
    'Spreadsheet.B7': '<<NPT_M_Global_Spreadsheet>>.NPT_M_height '
                        '* '
                        '<<NPT_M_Global_Spreadsheet>>.verticalScale',
    'Spreadsheet.B8': 'male_height',
    'Spreadsheet.B9': '<<NPT_M_Global_Spreadsheet>>.HoleDiaExansion',

    the followings are configuration table in Spreadsheet:
    'Spreadsheet001..cells.Bind.B2.I2': 'tuple(.cells; <<B>> + '
                                        'str(hiddenref(nominalOD) '
                                        '+ 3); <<I>> + '
                                        'str(hiddenref(nominalOD) '
                                        '+ 3))',
    'Spreadsheet001..nominalOD.Enum': 'cells[<<A3:|>>]',
    'Spreadsheet001.A2': 'hiddenref(.nominalOD.String)',

    the followings are configuration table value.
    'Spreadsheet001.B2': '.B11',
    'Spreadsheet001.C2': '.C11',
    'Spreadsheet001.D2': '.D11',
    'Spreadsheet001.E2': '.E11',
    'Spreadsheet001.F2': '.F11',
    'Spreadsheet001.G2': '.G11',
    'Spreadsheet001.H2': '.H11',
'''

def get_expInfo_by_objPropKey(doc, objPropKey, useLabel, debug=0):
    # print(f"useLabel={useLabel} get_expInfo_by_objPropKey called.")
    '''
    get expression string by objName.propName
    '''
    exprInfo_by_objProp = get_doc_all_expInfo(doc, useLabel, debug=debug)

    # print(f"exprInfo_by_objProp keys, useLabel={useLabel}: \n{pformat(exprInfo_by_objProp)}")

    if objPropKey in exprInfo_by_objProp:
        return exprInfo_by_objProp[objPropKey]
    return None


def token_to_rawObjProp(token:str, propNameHint:str=None, objHint=None):
    # check whether depends on another object's property.

    # skip FreeCAD internals
    if token in ['in',  # inch
                 'mm',
                ]:
        return None

    # skip numeric literals
    if re.fullmatch(r'[-+]?[0-9]*\.?[0-9]+', token):
        return None

    if (propNameHint and 'cells.Bind' in propNameHint) or (objHint and 'Spreadsheet' in objHint.TypeId):
        '''
        in spreadsheet configuration table, 
        objProp=Spreadsheet001..cells.Bind.B2.I2, expression=
        tuple(.cells; <<B>> + str(hiddenref(nominalOD) + 3); <<I>> + str(hiddenref(nominalOD) + 3))
        we should ignore <<B>> and <<I>>, they are not references.
        '''
        if re.fullmatch(r'<<[A-Z]>>', token):
            print(f"  Ignoring token={token} because objPropHint={propNameHint} or objHint={objHint.Name}")
            return None

    string_by_atom = {}
    # atomize string like <<NPT_M_Global_Spreadsheet>> for easier parsing
    i = 0
    while (match := re.search(r'<<.*?>>', token)):
        atom_str = match.group(0)
        atom_key = f"__dep_atom{i}__"
        string_by_atom[atom_key] = atom_str
        token = token[:match.start()] + atom_key + token[match.end():]
        i += 1

    if '.' in token:
        refObjKey, refPropName, *_ = token.split('.')
        # refObjStr, refPropName, *_ = token.split('.')
        # if refObjStr is None or refObjStr == '':
        #     # if it starts with '.', then it is relative to the same object
        #     # eg  .nominalOD.String or .realOD are both relative to the same object.
        #     if useLabel:
        #         # we need to wrap label with << and >> to distinguish from obj name.
        #         refObjKey = f"<<{objKey}>>"
        #     else:
        #         refObjKey = objKey
        # else:
        #     refObjKey = refObjStr

    else:
        # it is a simple variable, relative to the same object
        # eg 'nominalOD'
        # if useLabel:
        #     # we need to wrap label with << and >> to distinguish from obj name.
        #     refObjKey = f"<<{objKey}>>"
        # else:
        #     refObjKey = objKey
        refObjKey = ""
        refPropName = token

    # restore atom strings
    while match := re.search(r'__dep_atom(\d+)__', refObjKey):
        atom_key = match.group(0)
        atom_str = string_by_atom[atom_key]
        refObjKey = refObjKey.replace(atom_key, atom_str)

    while match := re.search(r'__dep_atom(\d+)__', refPropName):
        atom_key = match.group(0)
        atom_str = string_by_atom[atom_key]
        refPropName = refPropName.replace(atom_key, atom_str)

    return (refObjKey, refPropName)

def get_expression_tokens(expression):
    '''
    extract tokens from an expression string.
    # expression=specOD / 2                 -> tokens = {specOD}
    # expression=cone_height + 0.1 in -> tokens = {cone_height, '0.1 in'}
    # expression=male_height            -> tokens = {male_height}
    # expression=<<NPT_M_Global_Spreadsheet>>.HoleDiaExansion -> tokens = {<<NPT_M_Global_Spreadsheet.HoleDiaExansion>}
    # hiddenref(.nominalOD.String),         -> tokens = {.nominalOD.String}
    # tuple(.cells; <<B>> + str(hiddenref(nominalOD) + 3); <<I>> + str(hiddenref(nominalOD) + 3)) -> tokens = {nominalOD, 3}
    '''
    
    exp_by_atom = {}

    '''
    rename some strings to __atom123__ to avoid confusion with other tokens.
    eg, <<...>>, <<NPT_M_Global_Spreadsheet>>
    eg, cells[...] in Spreadsheet001.cells[<<A3:|>>
    '''
    i = 0
    # mosst specific patterns first
    for pattern in [r'cells\[<<.*?>>\]',   # cells[<<A3:|>>]
                    r'<<.*?>>',  # <<NPT_M_Global_Spreadsheet>>
                    ]:
        while (match := re.search(pattern, expression)):
            atom_str = match.group(0)
            atom_key = f"__get_atom{i}__"
            exp_by_atom[atom_key] = atom_str
            expression = expression[:match.start()] + atom_key + expression[match.end():]
            i += 1

    # print(f"replaced expression={expression}")
    # print(f"exp_by_atom={exp_by_atom}")

    tokens = get_expression_tokens_recursively(expression)

    # restore atom strings
    restored_tokens = set()
    for token in tokens:
        while match := re.search(r'__get_atom(\d+)__', token):
            atom_key = match.group(0)
            atom_str = exp_by_atom[atom_key]
            token = token.replace(atom_key, atom_str)

        restored_tokens.add(token)

    return restored_tokens

def get_expression_tokens_recursively(expression, level=0):
    max_level = 20
    if level > max_level:
        raise RuntimeError(f"Exceeded max recursion level {max_level} when getting expression='{expression}'")
    tokens = set()
    '''
    find other tokens recursively.
    1. extract the innermost '(...)' or '[...]' and reduce the expression as much as possible.
    2.  start from 1st letter. if we see +, -, *, /, space, ; ',', etc, we consider it as separator.
    3. if an item is like -0.1 or '-0.1 in', we ignore it.
    4. what is left are tokens.   
    '''

    pattern_innermost = re.compile(r'[a-zA-Z0-9_.]*[\[\(]([^()\[\]]+)[\)\]]')
    # str(hiddenref(nominalOD) + 3) -> nominalOD + 3

    while (match := pattern_innermost.search(expression)):
        inner_expr = match.group(1)
        tokens.update(get_expression_tokens_recursively(inner_expr, level=level+1))
        # print(f" match={match}")
        expression = expression[:match.start()] + expression[match.end():]
        # print(f" reduced expression={expression}")

    # find other tokens
    # 
    # if other_refs := re.findall(r'([a-zA-Z_._<][a-zA-Z0-9_.<>]*)', expression):
    if other_refs := re.findall(r'([a-zA-Z0-9_.]+)', expression):
        for ref in other_refs:
            tokens.add(ref)

    return tokens



'''
spreadsheet config table needs to be in this order
    $ /bin/grep nominalOD o2p_test_partdesign_spreadsheet_output_label.py
    NPT_M_Thread_Spreadsheet.addProperty("App::PropertyEnumeration", "nominalOD")
    NPT_M_Thread_Spreadsheet.setExpression('.nominalOD.Enum', 'cells[<<A3:|>>]')
    NPT_M_Thread_Spreadsheet.setExpression('.cells.Bind.B2.I2', 'tuple(.cells; <<B>> + str(hiddenref(nominalOD) + 3); <<I>> + str(hiddenref(nominalOD) + 3))')
    NPT_M_Thread_Spreadsheet.nominalOD = '`1 / 16'
    NPT_M_Thread_Spreadsheet.set('A2', '=hiddenref(.nominalOD.String)')

otherwise, you would get error
    NPT_M_Thread_Spreadsheet.nominalOD = '`1 / 16'
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ValueError: {'sclassname': 'class Base::ValueError', 'sErrMsg': "'`1 / 16' is not part of the enumeration 
error from below lines:    
    NPT_M_Thread_Spreadsheet.addProperty("App::PropertyEnumeration", "nominalOD")
    NPT_M_Thread_Spreadsheet.nominalOD = '`1 / 16'

'''

def sort_objs_exp_dependency(doc, useLabel, objList=None, externalReadyList=None, debug=False, printDetail=False) -> list:
    # print(f"useLabel={useLabel} sort_objs_exp_dependency called.")
    if objList is None:
        selections = Gui.Selection.getSelection()
        if not selections:
            objList = doc.Objects
        else:
            objList = selections
    expKeyList = []
    for obj in objList:
        if debug:
            print(f"Selected object Name={obj.Name}, TypeId={obj.TypeId}, Label={obj.Label}, useLabel={useLabel}")

        expInfoDict = get_obj_all_expInfo(doc, obj, useLabel=useLabel)
        expKeyList.extend(expInfoDict.keys())

    ret = sort_objPropKey_by_exp_dependency(doc, expKeyList, useLabel, externalReadyList=externalReadyList, debug=debug)
    if printDetail:
        indent = '    '
        print(f"sort_objs_exp_dependency: final result:")
        for k, v in ret.items():
            print(f"{indent}{k}:")
            if "_list" in k:
                # preserve order for lists
                for e in v:
                    print(f"{indent*2}{e}")
            else:
                for e in sorted(v):
                    print(f"{indent*2}{e}")
    return ret

def sort_objPropKey_by_exp_dependency(doc, objPropKeyList: list, useLabel, externalReadyList=None, debug=False) -> list:
    # print(f"useLabel={useLabel} sort_objPropKey_by_exp_dependency called.")
    '''
    only consider dependency within expr_list.
    mark expressions that depend on others outside expr_list as 'grounded'.
    '''
    
    delayed_set = set(objPropKeyList.copy())
    ready_list = [] # use array to preserve order.
    external_other_set = set()
    external_nonexp_set = set()
    external_grounded_set = set()
    external_ready_set = set()
    
    while delayed_set:
        begin_len = len(delayed_set)
        delayed_set_keys = list(delayed_set)
        for objPropKey in sorted(delayed_set_keys): # sort to have deterministic order, for easier testing.
            info = get_expInfo_by_objPropKey(doc, objPropKey, useLabel, debug=debug)
            if info is None:
                # not an expression
                ready_list.append(objPropKey)
                delayed_set.remove(objPropKey)
                if debug:
                    print(f"sort_objPropKey_by_exp_dependency: objPropKey={objPropKey} is not an expression, moved to ready_list.")
                break
            objKey , propName, *_ = objPropKey.split('.')
            all_upstreams = get_all_upstream_expObjPropKeys(doc, objKey, propName, useLabel, debug=debug, printDetail=False)
            # check whether all upstreams are in ready_list
            upstreams_ready = True
            for us in all_upstreams: # sort to have deterministic order, for easier testing.
                if us in ready_list:
                    continue

                usinfo = get_expInfo_by_objPropKey(doc, us, useLabel, debug=debug)
                if us not in delayed_set:
                    # ds is external, ie, outside objPropKeyList,  because 
                    #   objPropKeyList = ready_list + delayed_list.
                    
                    if externalReadyList is not None and us in externalReadyList:
                        # consider it ready
                        external_ready_set.add(us)
                        if debug:
                            print(f"sort_objPropKey_by_exp_dependency: objPropKey={objPropKey} upstream={us} is an external expression but in externalReadyList, considered ready.")
                        continue # don't break here. we want to check other upstreams.
                    elif usinfo is None:
                        # upstream is not an expression, consider it ready, eg, a well defined spreadsheet cell.
                        external_nonexp_set.add(us)
                        if debug:
                            print(f"sort_objPropKey_by_exp_dependency: objPropKey={objPropKey} upstream={us} is an external non-expression. considered ready.")
                        continue
                    elif usinfo.get('grounded', False):
                        # upstream is grounded expression, consider it ready.
                        external_grounded_set.add(us)
                        if debug:
                            print(f"sort_objPropKey_by_exp_dependency: objPropKey={objPropKey} upstream={us} is an external grounded expression. considered ready.")
                        continue
                    else:
                        # upstream is ungrounded expression, consider it not ready.
                        external_other_set.add(us)
                        upstreams_ready = False
                        if debug:
                            print(f"sort_objPropKey_by_exp_dependency: objPropKey={objPropKey} upstream={us} is an external ungrounded expression. considered not ready.")
                        continue
                else:
                    # ds is still in delayed_set, not ready yet.
                    upstreams_ready = False
                    if debug:
                        print(f"sort_objPropKey_by_exp_dependency: objPropKey={objPropKey} upstream={us} is still in delayed_set, not ready yet.")
                    continue
            if upstreams_ready:
                ready_list.append(objPropKey)
                delayed_set.remove(objPropKey)
                if debug:
                    print(f"sort_objPropKey_by_exp_dependency: objPropKey={objPropKey} upstreams ready, moved to ready_list.")
                continue # don't break here. we want to check other delayed items.
        if len(delayed_set) == begin_len:
            break

    ret = {
        'ready_list': ready_list,
        'delayed_set': delayed_set,
        'external_other_set': external_other_set,
        'external_nonexp_set': external_nonexp_set,
        'external_grounded_set': external_grounded_set,
        'external_ready_set': external_ready_set,
    }
    return ret

def main():
    doc = App.ActiveDocument
    selections = Gui.Selection.getSelection()

    test_expressions = [
        '-1.5',
        '0.04 in',
        '1.33 mm',
        'specOD / 2',
        'cone_height + 0.1 in',
        'cells[<<A2:A3>>]',
        'tan(1.7899)',
        '<<NPT_M_Global_Spreadsheet>>.HoleDiaExansion',
        'str(hiddenref(<<NPT_M_Global_Spreadsheet>>.HoleDiaExansion) + 3)',
        'Spreadsheet001.nominalOD.Enum',
        'tuple(.cells; <<B>> + str(hiddenref(nominalOD) + 3); <<I>> + str(hiddenref(nominalOD) + 3))'
    ]
    for expression in test_expressions:
        tokens = get_expression_tokens(expression)
        print(f"expression={expression}")
        print(f"    tokens={tokens}")
        is_grounded = is_exp_grounded(expression)
        print(f"    is_grounded={is_grounded}")
        print()
    print()

    # if not selections:
    #      print("No selection found.")
    #      return
     
    # selectedObj = selections[0]
    # print(f"extended prop list = {getPropListExt(selectedObj)}")
    # for anyName in [ 
    #     'B5', # cell
    #     'HoleDiaExpansion', # alias
    # ]:
    #     try:
    #         value = getPropByNameExt(selectedObj, anyName)
    #         print(f"selectedObj={selectedObj.Name}, anyName={anyName}, value={value}")
    #     except Exception as e:
    #         print(f"Error getting property '{anyName}' from object '{selectedObj.Name}': {e}")


if __name__ == "__main__":
    main()


                
