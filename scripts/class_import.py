# dump properties

import json
import os
from pdb import main
import sys

import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.callsheettools import get_top_callsheets_using_exp
from cadcoder.objtools import print_obj
from cadcoder.subelementtools import update_doc_seName

prog = os.path.basename(sys.argv[0])
    
example_usage = f"""
Examples:

    {prog} Prism_polygon
    {prog} Prism_polygon -op 'big_'
    {prog} Prism_polygon -param 'prism_polygon_sides=6, prism_polygon_radius_spec="0.5 in"'

    # import the class that is used by object s_npt_m_callsheet
    {prog} Npt_fxf.FCStd -doc -ob 's_npt_m'
"""
   


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="import class to doc",
        epilog="Example: class.py"
    )

    parser.add_argument(
        "classNames",
        nargs="+",
        default=None,
        help="import class names, eg, Npt_m Prism_polygon Cylinder"
    )

    parser.add_argument(
        '-m', '--moduleName',
        type=str,
        default=None,
        help='module name, eg, parts.Npt_m'
    )
    
    parser.add_argument(
        "-op",
        '--objPrefix',
        action = 'store',
        type=str,
        default='',
        help="import classes, eg, Npt_m Prism_polygon Cylinder"
    )

    parser.add_argument(
        "-param",
        '--param',
        action = 'store',
        type=str,
        default='',
        help="""import param, eg, 'prism_polygon_sides=6, prism_polygon_radius_spec="0.5 in"')"""
    )

    try:
        args = parser.parse_args()
    except Exception as e:
        print(f"Error parsing arguments: {e}")
        return None

    return args

def main():
    args = parse_args()

    if not args:
        return
    
    if args.classNames is None:
        print(f"missing classes")
        return

    doc = App.ActiveDocument
    if doc is None:
        raise RuntimeError("No active document found")

    # get top callsheet by label
    top_callsheet = None
    for obj in doc.Objects:
        if obj.TypeId == 'Spreadsheet::Sheet' and obj.Label == 'callsheet':
            top_callsheet = obj
            break
    if top_callsheet is None:
        raise RuntimeError("No top callsheet found in the document. Please ensure there is a callsheet spreadsheet named 'callsheet'.")

    top_callsheet_name = top_callsheet.Name
    top_callsheet_pythonSource_dict = json.loads(top_callsheet.pythonSource)
    top_callsheet_pythonSource_str = f"{top_callsheet_pythonSource_dict}".replace('\n', '')
    print(f"Top callsheet PythonSource: {top_callsheet_pythonSource_str}")
    
    # the following uses exec() 
    # code_block=""
    # for className in args.classNames:
    #     code_block += f"from parts.{className} import {className}\n"
    #     instanceName = f"{args.objPrefix}{className.lower()}_instance"
    #     code_block += f"{instanceName} = {className}('{instanceName}', doc, objPrefix='{args.objPrefix}', useLabel=True, importer={top_callsheet_pythonSource_str}, {args.param})\n"
    #     code_block += f"doc.recompute()\n"
    #     code_block += f"from cadcoder.objtools import map_obj_name_label\n"
    #     code_block += f"map_obj_name_label(doc, refreshCache=True) # update object name to label mapping\n"
    #     code_block += f""
    #     code_block += f"from cadcoder.callsheettools import link_parent_child_callsheets\n"
    #     code_block += f"link_parent_child_callsheets(doc.getObject('{top_callsheet_name}'), {instanceName}.callsheet)\n"
    #     code_block += f"doc.recompute()\n"
    #     code_block += f""
    # print(f"\nExecuting code block:\n{code_block}\n")
    # exec(code_block, globals(), locals())

    # the following without using exec()
    import importlib
    for className in args.classNames:

        if args.moduleName is None:
            moduleName = f"parts.{className}"
        else:
            moduleName = args.moduleName
        try:
            module = importlib.import_module(moduleName)
            cls = getattr(module, className)
        except Exception as e:
            print(f"Error importing class {className}: {e}")
            continue

        instanceName = f"{args.objPrefix}instance"
        try:
            instance = cls(instanceName, doc, objPrefix=args.objPrefix, useLabel=True, importer=top_callsheet_pythonSource_dict, **eval(f"dict({args.param})"))
        except Exception as e:
            print(f"Error creating instance of class {className}: {e}")
            continue

        doc.recompute()
        from cadcoder.objtools import map_obj_name_label
        map_obj_name_label(doc, refreshCache=True)  # update object name to label mapping
        from cadcoder.callsheettools import link_parent_child_callsheets
        link_parent_child_callsheets(doc.getObject(top_callsheet_name), instance.callsheet)
        doc.recompute()

    from cadcoder.doctools import reorganize_doc
    reorganize_doc(doc) 


if __name__ == "__main__":
    main()
