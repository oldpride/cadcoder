import FreeCAD
import csv
import re

'''
 propName: cells
 dir: ['Content', 'MemSize', 'Module', 'TypeId', '__class__', 
 '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', 
 '__ge__', '__getattribute__', '__getitem__', '__getstate__', 
 '__gt__', '__hash__', '__init__', '__init_subclass__', 
 '__le__', '__lt__', '__ne__', '__new__', '__reduce__', 
 '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', 
 '__str__', '__subclasshook__', 'dumpContent', 
 'getAllDerivedFrom', 'isDerivedFrom', 'restoreContent']

default cells (different address):
   propType: Spreadsheet::PropertySheet
   propValue: <PropertySheet object>
   valueTypeId: Spreadsheet::PropertySheet
   valueClass: PropertySheet
   valueClassTree: {'PropertySheet'}
   valueObjName: None
   readonly: False
   valuePython: <PropertySheet object>
   propName: cells
   Expression: None
   Content: <Cells Count="2" xlink="1">
    <XLinks count="0">
    </XLinks>
    <Cell address="A1" content="1" alias="aliasA1" />
    <Cell address="B1" content="=aliasA1 + 1" />
</Cells>
'''

content_by_docKey__sheetName_cellAddr = {}

def map_content_by_cellAddr(sheet, refreshCache=False)->dict:
    '''
    parse spreadsheet, map content by cellAddr
    '''
    doc = sheet.Document
    docKey = f"{doc.Name},{id(doc)}"
    sheetName = sheet.Name

    if docKey not in content_by_docKey__sheetName_cellAddr:
        content_by_docKey__sheetName_cellAddr[docKey] = {}
        
    if sheetName in content_by_docKey__sheetName_cellAddr[docKey] and not refreshCache:
        return content_by_docKey__sheetName_cellAddr[docKey][sheetName]
    
    content_by_docKey__sheetName_cellAddr[docKey][sheetName] = {}

    content_by_cellAddr = {}

    contentXml = sheet.getPropertyByName("cells").Content
    '''
    content example:
    <Cells Count="2" xlink="1">
        <XLinks count="0">
        </XLinks>
        <Cell address="A1" content="1" alias="aliasA1" />
        <Cell address="B1" content="=aliasA1 + 1" />
    </Cells>
    '''
    import xml.etree.ElementTree as ET
    root = ET.fromstring(contentXml)
    for cell in root.findall("Cell"):
        cellAddr = cell.get("address")
        cellContent = cell.get("content")
        content_by_cellAddr[cellAddr] = cellContent

    content_by_docKey__sheetName_cellAddr[docKey][sheetName] = content_by_cellAddr
    return content_by_cellAddr

def get_content_by_cellAddr(sheet, cellAddr, refreshCache=False):
    content_by_cellAddr = map_content_by_cellAddr(sheet, refreshCache=refreshCache)
    return content_by_cellAddr.get(cellAddr, None)

def get_cell_list(sheet, refreshCache=False)->list:
    sheetName = sheet.Name
    content_by_sheetName_cellAddr = map_content_by_cellAddr(sheet, refreshCache=refreshCache)
    return list(content_by_sheetName_cellAddr.keys())

def is_cell_in_sheet(cellAddr:str, sheet, refreshCache=False) -> bool:
    '''
    check if a cell_name (e.g., 'A1') is in the given sheet.

    'sel.getContents(cell) is not None' always return True, thus we implement our own version.
    '''
    content_by_cellAddr = map_content_by_cellAddr(sheet, refreshCache=refreshCache)
    return cellAddr in content_by_cellAddr

def col_index_to_letter(col_idx:int) -> str:
    """Convert a 1-based column index to a letter (e.g., 1 -> 'A', 27 -> 'AA')."""
    letter = ""
    while col_idx > 0:
        col_idx, remainder = divmod(col_idx - 1, 26)
        letter = chr(65 + remainder) + letter
    return letter

def csv_to_spreadsheet(csv_file, sheet, cfgTablePropName=None, max_rows=1000, max_cols=50):
    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row_idx, row in enumerate(reader):
            for col_idx, value in enumerate(row):
                cell_name = f"{chr(65 + col_idx)}{row_idx + 1}"  # A1, B1, etc.
                sheet.set(cell_name, value)
    sheet.recompute()
    FreeCAD.ActiveDocument.recompute()

    if cfgTablePropName:
        # add property to spreadsheet
        sheet.addProperty("App::PropertyEnumeration", cfgTablePropName)
        sheet.recompute()

        sheet.insertRows('2', 1)  # insert a row at index 2, this is for config table.
        sheet.recompute()
        FreeCAD.ActiveDocument.recompute()

        '''
        recorded step to set up config table into Macro recorder:
            App.getDocument('Unnamed1').getObject('nptSpecSheet').setExpression('myPropName.Enum', 'Unnamed1#nptSpecSheet.cells[<<A3:|>>]')
            App.getDocument('Unnamed1').getObject('nptSpecSheet').recompute()
            App.getDocument('Unnamed1').getObject('nptSpecSheet').set('A2', '=hiddenref(Unnamed1#nptSpecSheet.myPropName.String)')
            App.getDocument('Unnamed1').getObject('nptSpecSheet').setExpression('.cells.Bind.B2.I2', 'tuple(.cells, <<B>> + str(hiddenref(Unnamed1#nptSpecSheet.myPropName)+3), <<I>> + str(hiddenref(Unnamed1#nptSpecSheet.myPropName)+3))')
            App.ActiveDocument.recompute()
        '''

        # config table should be 
        # from A2 
        # to   row=the row before 1st empty row or last row, 
        #      column=last column of header row

        docName = FreeCAD.ActiveDocument.Name

        # find the last non-empty row in column A, starting from row 3
        last_cfg_row = None
        for r in range(3, max_rows + 1):
            try:
                cell_value = sheet.get(f'A{r}')
            except Exception:
                cell_value = None
            if not cell_value:
                last_cfg_row = r - 1
                break
        if last_cfg_row is None:
            raise RuntimeError(f"more than max_rows={max_rows} rows in the csv file, please increase max_rows parameter.")

        print(f'{cfgTablePropName}.Enum', f'{docName}#{sheet.Name}.cells[<<A3:A{last_cfg_row}>>]')
        sheet.setExpression(f'{cfgTablePropName}.Enum', f'{docName}#{sheet.Name}.cells[<<A3:A{last_cfg_row}>>]')
        sheet.recompute()
        # A1_value = sheet.get('A1')
        sheet.set('A2', f'=hiddenref({docName}#{sheet.Name}.{cfgTablePropName}.String)')

        # get the last index of the header column
        last_header_col = None
        for c in range(1, max_cols + 1):
            col_letter = col_index_to_letter(c)
            try:
                header_val = sheet.get(f'{col_letter}1')
            except Exception:
                header_val = None
            if not header_val:
                last_header_col = c - 1
                break
        if last_header_col is None:
            raise RuntimeError(f"more than max_cols={max_cols} columns in the csv file, please increase max_cols parameter.")
        
        # convert it to column letter, eg` A=1, B=2, ...`
        last_header_col_letter = col_index_to_letter(last_header_col)

        sheet.setExpression(f'.cells.Bind.B2.{last_header_col_letter}2', f'tuple(.cells, <<B>> + str(hiddenref({docName}#{sheet.Name}.{cfgTablePropName})+3), <<{last_header_col_letter}>> + str(hiddenref({docName}#{sheet.Name}.{cfgTablePropName})+3))')

        # recompute whole doc at the end.
        FreeCAD.ActiveDocument.recompute()
        
def dump_spreadsheet(doc, sheetObj):
    '''
    dump the content of the spreadsheet to console
    '''
    print(f"Dumping spreadsheet: {sheetObj.Name}")
    content = sheetObj.getPropertyByName("cells").Content
    print(content)

    # dump the python code to recreate the spreadsheet
    # print out code in 1 flush for easier copy-paste. otherwise, each line will have a time stamp in the console.
    lines = []  
    sheetLabel = sheetObj.Label
    print(f"Python code to recreate spreadsheet: {sheetObj.Name}, label: {sheetObj.Label}")
    lines.append(f'{sheetLabel} = doc.addObject("Spreadsheet::Sheet", "{sheetObj.Name}")')

    import xml.etree.ElementTree as ET
    root = ET.fromstring(content)
    cells = root.findall("Cell")
    
    cell_by_address = {}
    for cell in cells:
        address = cell.get("address")
        cell_by_address[address] = cell

    
    for address in sorted(cell_by_address.keys()):
        cell = cell_by_address[address]
        cell_content = cell.get("content")
        lines.append(f'{sheetLabel}.set("{address}", "{cell_content}")')

        # also dump alias if exists
        alias = cell.get("alias")
        if alias:
            lines.append(f'{sheetLabel}.setAlias("{address}", "{alias}")')

    print("\n" + "\n".join(lines))

next_row = None
def find_next_row(sheet, 
                  refreshCache=False, 
                  consume=True, # if we consume the next row, increment the global next_row counter
                  keyColumn='A', # the column to check for the next available row
                  )->int:
    global next_row
    if next_row is not None:
        if consume:
            next_row += 1
            return next_row - 1
        else:
            return next_row
        
    cell_list = get_cell_list(sheet, refreshCache=refreshCache)
    keyColumn_cells = [cell for cell in cell_list if re.match(r'^' + re.escape(keyColumn) + r'\d+$', cell)]
    keyColumn_indices = [ int(cell[1:]) for cell in keyColumn_cells]
    max_index = max(keyColumn_indices) if keyColumn_indices else 0
    next_row = max_index + 1
    if consume:
        next_row += 1
        return next_row - 1
    else:
        return next_row

def get_cellValue_from_propInfo(propInfo):
    '''
    set cell value using propValue, which is from getPropInfo().
    '''
    valueClass = propInfo['valueClass']

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
        raise RuntimeError(msg)
    return equal_sign + str(propInfo['propValue'])

def set_cellValue_by_propInfo(sheet, cellAddr, propInfo):
    cellValue = get_cellValue_from_propInfo(propInfo)
    sheet.set(cellAddr, cellValue)

def main():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        raise RuntimeError("No active document found")

    # get the selected object in the GUI
    selections = FreeCAD.Gui.Selection.getSelection()
    if not selections:
        raise RuntimeError("No object selected")

    for sel in selections:
        # test get_cell_list
        cell_list = get_cell_list(sel)
        print(f"Cell list for {sel.Name}: {cell_list}")
        # test is_cell_in_sheet
        test_cells = ['A1', 'B1', 'C10']
        for cell in test_cells:
            in_sheet_by_customized = is_cell_in_sheet(cell, sel)
            in_sheet_by_getContents = sel.getContents(cell) is not None
            print(f"Is cell {cell} in sheet {sel.Name}? in_sheet_by_customized={in_sheet_by_customized} in_sheet_by_getContents={in_sheet_by_getContents}")

if __name__ == "__main__":
    main()
