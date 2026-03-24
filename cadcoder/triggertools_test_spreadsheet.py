from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.baseClass import baseClass


class triggertools_test_spreadsheet(baseClass):
    def __init__(self, doc,  objPrefix="", useLabel=True):
        
        super().__init__(doc, objPrefix=objPrefix, useLabel=useLabel)
        
        # add objects and add static value to objects' properties based on object dependencies
        cfgTableSheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('cfgTableSheet') )
        self.cfgTableSheet = cfgTableSheet # expose as instance variable
        self.post_new_obj(cfgTableSheet)
        cfgTableSheet.set('A1', 'a')
        cfgTableSheet.set('A2', 'a')
        cfgTableSheet.set('A3', 'b')
        cfgTableSheet.set('A4', 'c')
        cfgTableSheet.set('B1', '1')
        cfgTableSheet.set('B2', '1')
        cfgTableSheet.set('B3', '2')
        cfgTableSheet.set('B4', '3')
        cfgTableSheet.addProperty("App::PropertyEnumeration", "myModel")

        cfgTableSheet.set('D6', 'xyz')
        cfgTableSheet.setAlias('D6', 'myModel2')
        
        triggertools_test_spreadsheet_callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('triggertools_test_spreadsheet_callsheet') )
        self.triggertools_test_spreadsheet_callsheet = triggertools_test_spreadsheet_callsheet # expose as instance variable
        self.post_new_obj(triggertools_test_spreadsheet_callsheet)
        triggertools_test_spreadsheet_callsheet.set('A1', 'b')
        triggertools_test_spreadsheet_callsheet.setAlias('A1', 'myModelTrigger')
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        cfgTableSheet.set("B1", f"=.B2")
        cfgTableSheet.setExpression(".myModel.Enum", f"cells[<<A2:|>>]")
        # recompute after setting configuration-table expression; otherwise error: Property ... not found.
        doc.recompute()
        cfgTableSheet.set("A1", f"=hiddenref(.myModel.String)")
        cfgTableSheet.setExpression(".cells.Bind.B1.B1", f"tuple(.cells; <<B>> + str(hiddenref(myModel) + 2); <<B>> + str(hiddenref(myModel) + 2))")
        # recompute after setting configuration-table expression; otherwise error: Property ... not found.
        doc.recompute()


        # add delayed expression property values - values, not expressions, eg, enum value
        doc.recompute()
        cfgTableSheet.myModel = 'a'
        triggertools_test_spreadsheet_callsheet.set('myModelTrigger', 'b')

        # add triggers
        from examples.triggertools import link_watch_to_target
        # def set_myModel(info, oldValue):
        #     cfgTableSheet.myModel = info['value']
        # set_trigger(doc, triggertools_test_spreadsheet_callsheet, 'myModelTrigger', set_myModel, useLabel=True)
        link_watch_to_target(doc, triggertools_test_spreadsheet_callsheet, 'myModelTrigger', cfgTableSheet, 'myModel', self.useLabel)
        link_watch_to_target(doc, triggertools_test_spreadsheet_callsheet, 'myModelTrigger', cfgTableSheet, 'myModel2', self.useLabel)



 


def main():
    # main_part1
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of triggertools_test_spreadsheet
    instance = triggertools_test_spreadsheet(doc, objPrefix="", useLabel=True)
    
    # main_part2
    from pprint import pformat
    print(f"instance.exportObj_by_objKey= {pformat(instance.exportObj_by_objKey)}")
    
    top_objects = instance.get_top_objects()
    print(f"instance.top_objects= {pformat(top_objects)}")
    
    from cadcoder.doctools import reorganize_doc
    reorganize_doc(doc) 


if __name__ == '__main__':
    main()
