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
from pdfclib.callsheettools import is_callParam
from pdfclib.importtools import map_importInfo
from pdfclib.containertools import get_LCS_map, get_LCS_prefixes, get_container_by_objName
from pdfclib.expressiontools import get_expInfo_by_objPropKey, sort_objs_exp_dependency
from pdfclib.logtools import prefix_stack
from pdfclib.matchtools import match_key_startswith
from pdfclib.objtools import expand_objects, get_doc_top_objects, get_group_top_objects, get_obj_by_objKey, sort_objs_by_downstream
from pdfclib.proptools import compare_obj_prop_with_default, float2str, get_prop_info, normalize_label, propValue2python, propIsReadonly, get_obj_varname
from pdfclib.spreadsheettools import is_cell_in_sheet
from pdfclib.subelementtools import get_posName_by_seName
from pdfclib.uitools import TextDialog
import pdb

debug = 0
dialog = None

def main_part1():
    # main_part1
    from pdfclib.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()

def export_doc(topClassName: str):
    # add_script_line('from FreeCAD import Vector, Placement, Rotation')
    # add_script_line('import Sketcher')
    # add_script_line('import Part')
    add_script_line('import FreeCAD as App')
    add_script_line('import FreeCADGui as Gui')
    add_script_line('from pdfclib.baseClass import baseClass')
    # add_script_line('from pdfclib.containertools import get_LCS_by_prefix')
    # add_script_line('from pdfclib.objtools import update_obj_prop_jsonDict')

    # now that we have topClassName, we can define the class interface
    add_script_line('') 
    add_script_line(f'class {topClassName}(baseClass):')
    add_body_line('def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None):')
    add_method_line('')
    add_method_line('super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)')

 
    # create an empty callsheet 
    target_callsheet_vname = 'callsheet'
    add_method_line('')
    add_method_line(f'# create empty callsheet spreadsheet label and varname={target_callsheet_vname}')
    add_method_line(f'{target_callsheet_vname} = doc.addObject("Spreadsheet::Sheet", self.addPrefix("{target_callsheet_vname}"))')
    add_method_line(f'self.{target_callsheet_vname} = {target_callsheet_vname} # expose as instance variable')
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
    add_method_line('# set callsheet')
    # if objs_waiting_for_recompute:
    #     add_method_line('# doc.recompute() # recompute before setting callsheet; otherwisemay get "invalid cell address" error')
    #     objs_waiting_for_recompute.clear()
    add_method_line(f"self.callsheet = self.{target_callsheet_vname}")
    add_method_line(f"self.update_callsheet()")
    add_method_line(f"doc.recompute()")

    
    add_script_line('')
    # from pdfclib.doctools import recreate_tmp_doc
    # doc = recreate_tmp_doc()
    add_script_line(f'doc =App.newDocument("{topClassName}")')
    add_script_line(f'doc.Label = "{topClassName}" # explicitly set document label to {topClassName}; default could be {topClassName}1.')
    add_script_line('')
    add_script_line(f'# create instance of {topClassName}')
    add_script_line(f'myInstance = {topClassName}("myInstance", doc, objPrefix="", useLabel=True, importer=None)')
    
    add_script_line('') # add a final newline


out_line_number = 0
# script_lines = []
script_block = ""
def add_script_line(line, indent=0):
    global out_line_number, script_block

    # remove newlines - make multi-line code into single line
    line = line.replace('\n', ' ')

    out_line_number += 1
    spaces = ' ' * 4 * indent
    prefix_stack(f"{out_line_number}: " + spaces + line, debug=debug)
    if dialog is not None:
        dialog.form.textEdit.append(spaces + line)
    script_block += spaces + line + "\n"

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

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        description='Objects To Python Macro', 
        exit_on_error=False, # default True will call sys.exit(1), which exits FreeCAD entirely. bad!!!
        # this switch doesn't work in FreeCAD 1.0.2. 
        )
    parser.add_argument('topClassName', nargs="?", type=str, default=None,
                        help='specify the top class name to use in the generated script')
    parser.add_argument('-d', '--dialog', action='store_true', 
                        help='pop up a dialog of the python script being generated')
    
    try:
        args = parser.parse_args(sys.argv[1:])
    except SystemExit:
        return None
    
    args = parser.parse_args()
    return args

dialog = None

def main():
    global dialog
    args = parse_args()
    if args is None:
        return
    
    if args.topClassName is None:
        raise RuntimeError("missing topClassName")

    print(f"args={pformat(args)}")

    if args.dialog:
        dialog = TextDialog()

    # doc = App.activeDocument()

    export_doc(topClassName=args.topClassName)

    exec(script_block, globals(), locals())
    
if __name__ == '__main__':
    main()
    
