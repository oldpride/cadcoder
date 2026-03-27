from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.baseClass import baseClass
from cadcoder.containertools import get_LCS_by_prefix
from cadcoder.objtools import update_obj_prop_jsonDict
from cadcoder.subelementtools import update_objs_seName, update_doc_seName, get_seName_by_posName

class npt_fxf_chamfer(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, b_npt_f_height='0.5 in', b_npt_f_nominalID='`1-1/4', b_npt_f_wall='0.08 in', base_plate_thick='0.12 in', holeDiaExpansion='0.03 in', npt_fxf_chamfer_bottom_size='0.04 in', npt_fxf_chamfer_top_size='0.04 in', s_npt_f_height='0.5 in', s_npt_f_nominalID='`3/4', s_npt_f_wall='0.08 in',  ):
        self.b_npt_f_height = b_npt_f_height
        self.b_npt_f_nominalID = b_npt_f_nominalID
        self.b_npt_f_wall = b_npt_f_wall
        self.base_plate_thick = base_plate_thick
        self.holeDiaExpansion = holeDiaExpansion
        self.npt_fxf_chamfer_bottom_size = npt_fxf_chamfer_bottom_size
        self.npt_fxf_chamfer_top_size = npt_fxf_chamfer_top_size
        self.s_npt_f_height = s_npt_f_height
        self.s_npt_f_nominalID = s_npt_f_nominalID
        self.s_npt_f_wall = s_npt_f_wall
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        from parts.npt_fxf import npt_fxf
        npt_fxf_instance = npt_fxf('npt_fxf_instance', doc, objPrefix=self.objPrefix + 'npt_fxf_', useLabel=True, importer=self, b_npt_f_height='0.5 in', b_npt_f_nominalID='`1-1/4', b_npt_f_wall='0.08 in', base_plate_thick='0.12 in', holeDiaExpansion='0.03 in', s_npt_f_height='0.5 in', s_npt_f_nominalID='`3/4', s_npt_f_wall='0.08 in', )
        self.npt_fxf_instance = npt_fxf_instance # expose as instance variable
        self.update_imports(npt_fxf_instance) # update import info for the instance
        npt_fxf_instance.b_npt_f_instance.body.Placement = Placement(Vector(0.0000, -0.0000, 15.7480), Rotation(1.0000, 0.0000, 0.0000, 0.0000))  # adjust imported object
        npt_fxf_instance.boolean.Visibility = False  # adjust imported object
        
        # add objects and add static value to objects' properties based on object dependencies
        callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('callsheet') )
        callsheet.Label = self.addPrefix('callsheet')
        self.callsheet = callsheet
        self.post_new_obj(callsheet)
        callsheet.set('A1', 'variableName')
        callsheet.set('A10', 'base_plate_thick')
        callsheet.set('A11', 'holeDiaExpansion')
        callsheet.set('A2', 'npt_fxf_chamfer_top_size')
        callsheet.set('A3', 'npt_fxf_chamfer_bottom_size')
        callsheet.set('A4', 's_npt_f_nominalID')
        callsheet.set('A5', 'b_npt_f_nominalID')
        callsheet.set('A6', 's_npt_f_wall')
        callsheet.set('A7', 'b_npt_f_wall')
        callsheet.set('A8', 's_npt_f_height')
        callsheet.set('A9', 'b_npt_f_height')
        callsheet.set('B1', 'value')
        callsheet.set('B10', '=0.12 in')
        callsheet.setAlias('B10', 'base_plate_thick')
        callsheet.set('B11', '=0.03 in')
        callsheet.setAlias('B11', 'holeDiaExpansion')
        callsheet.set('B2', '=0.04 in')
        callsheet.setAlias('B2', 'npt_fxf_chamfer_top_size')
        callsheet.set('B3', '=0.04 in')
        callsheet.setAlias('B3', 'npt_fxf_chamfer_bottom_size')
        callsheet.set('B4', '`3/4')
        callsheet.setAlias('B4', 's_npt_f_nominalID')
        callsheet.set('B5', '`1-1/4')
        callsheet.setAlias('B5', 'b_npt_f_nominalID')
        callsheet.set('B6', '=0.08 in')
        callsheet.setAlias('B6', 's_npt_f_wall')
        callsheet.set('B7', '=0.08 in')
        callsheet.setAlias('B7', 'b_npt_f_wall')
        callsheet.set('B8', '=0.5 in')
        callsheet.setAlias('B8', 's_npt_f_height')
        callsheet.set('B9', '=0.5 in')
        callsheet.setAlias('B9', 'b_npt_f_height')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C10', 'Y')
        callsheet.set('C11', 'Y')
        callsheet.set('C2', 'Y')
        callsheet.set('C3', 'Y')
        callsheet.set('C4', 'Y')
        callsheet.set('C5', 'Y')
        callsheet.set('C6', 'Y')
        callsheet.set('C7', 'Y')
        callsheet.set('C8', 'Y')
        callsheet.set('C9', 'Y')
        callsheet.set('D1', 'comment')
        callsheet.recompute()  # recompute after adding object
        
        doc.recompute() # recompute before adding PartDesign::Chamfer to avoid error
        chamfer_bottom = doc.addObject('PartDesign::Chamfer', self.addPrefix('chamfer_bottom') )
        chamfer_bottom.Label = self.addPrefix('chamfer_bottom')
        self.chamfer_bottom = chamfer_bottom
        self.post_new_obj(chamfer_bottom)
        self.container_append_object(npt_fxf_instance.base_plate, chamfer_bottom)
        chamfer_bottom.Base = (npt_fxf_instance.boolean, [get_seName_by_posName(npt_fxf_instance.boolean, 'Edge', 'bottom1')])
        npt_fxf_instance.boolean.Visibility = False  # hide chamfer base object
        update_obj_prop_jsonDict(chamfer_bottom, "pythonFeature",{"Base": [{"seType": "Edge", "posName": "bottom1"}]})
        chamfer_bottom.Size = 1.016
        chamfer_bottom.Visibility = False
        chamfer_bottom.ViewObject.Visibility = False
        chamfer_bottom.recompute()  # recompute after adding object
        
        doc.recompute() # recompute before adding PartDesign::Chamfer to avoid error
        chamfer_top = doc.addObject('PartDesign::Chamfer', self.addPrefix('chamfer_top') )
        chamfer_top.Label = self.addPrefix('chamfer_top')
        self.chamfer_top = chamfer_top
        self.post_new_obj(chamfer_top)
        self.container_append_object(npt_fxf_instance.base_plate, chamfer_top)
        chamfer_top.Base = (chamfer_bottom, [get_seName_by_posName(chamfer_bottom, 'Edge', 'top1')])
        chamfer_bottom.Visibility = False  # hide chamfer base object
        update_obj_prop_jsonDict(chamfer_top, "pythonFeature",{"Base": [{"seType": "Edge", "posName": "top1"}]})
        chamfer_top.Size = 1.016
        chamfer_top.recompute()  # recompute after adding object
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        chamfer_bottom.setExpression("Size", f"<<{self.addPrefix('callsheet')}>>.npt_fxf_chamfer_bottom_size")
        chamfer_top.setExpression("Size", f"<<{self.addPrefix('callsheet')}>>.npt_fxf_chamfer_top_size")
        npt_fxf_instance.callsheet.set(npt_fxf_instance.callsheet.getCellFromAlias('s_npt_f_nominalID'), f"=<<{self.addPrefix('callsheet')}>>.s_npt_f_nominalID")
        npt_fxf_instance.callsheet.set(npt_fxf_instance.callsheet.getCellFromAlias('b_npt_f_nominalID'), f"=<<{self.addPrefix('callsheet')}>>.b_npt_f_nominalID")
        npt_fxf_instance.callsheet.set(npt_fxf_instance.callsheet.getCellFromAlias('s_npt_f_wall'), f"=<<{self.addPrefix('callsheet')}>>.s_npt_f_wall")
        npt_fxf_instance.callsheet.set(npt_fxf_instance.callsheet.getCellFromAlias('b_npt_f_wall'), f"=<<{self.addPrefix('callsheet')}>>.b_npt_f_wall")
        npt_fxf_instance.callsheet.set(npt_fxf_instance.callsheet.getCellFromAlias('s_npt_f_height'), f"=<<{self.addPrefix('callsheet')}>>.s_npt_f_height")
        npt_fxf_instance.callsheet.set(npt_fxf_instance.callsheet.getCellFromAlias('b_npt_f_height'), f"=<<{self.addPrefix('callsheet')}>>.b_npt_f_height")
        npt_fxf_instance.callsheet.set(npt_fxf_instance.callsheet.getCellFromAlias('base_plate_thick'), f"=<<{self.addPrefix('callsheet')}>>.base_plate_thick")
        npt_fxf_instance.callsheet.set(npt_fxf_instance.callsheet.getCellFromAlias('holeDiaExpansion'), f"=<<{self.addPrefix('callsheet')}>>.holeDiaExpansion")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # now we have rebuilt the original npt_fxf_chamfer doc. Now we apply dynmic call parameters
        print("there can be temporary errors when we applying dynamic call parameters that change original npt_fxf_chamfer's shape.")
        print("ignore temporary errors, if any, below.")
        callsheet.set(callsheet.getCellFromAlias('base_plate_thick'), f'={self.base_plate_thick}')
        callsheet.set(callsheet.getCellFromAlias('holeDiaExpansion'), f'={self.holeDiaExpansion}')
        callsheet.set(callsheet.getCellFromAlias('npt_fxf_chamfer_top_size'), f'={self.npt_fxf_chamfer_top_size}')
        callsheet.set(callsheet.getCellFromAlias('npt_fxf_chamfer_bottom_size'), f'={self.npt_fxf_chamfer_bottom_size}')
        callsheet.set(callsheet.getCellFromAlias('s_npt_f_nominalID'), f'{self.s_npt_f_nominalID}')
        callsheet.set(callsheet.getCellFromAlias('b_npt_f_nominalID'), f'{self.b_npt_f_nominalID}')
        callsheet.set(callsheet.getCellFromAlias('s_npt_f_wall'), f'={self.s_npt_f_wall}')
        callsheet.set(callsheet.getCellFromAlias('b_npt_f_wall'), f'={self.b_npt_f_wall}')
        callsheet.set(callsheet.getCellFromAlias('s_npt_f_height'), f'={self.s_npt_f_height}')
        callsheet.set(callsheet.getCellFromAlias('b_npt_f_height'), f'={self.b_npt_f_height}')
        doc.recompute()
        update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.
        print("ignore temporary errors, if any, above.")
        
        self.update_callsheet()


def main():
    # main_part1
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of npt_fxf_chamfer
    myInstance = npt_fxf_chamfer("myInstance", doc, objPrefix="", useLabel=True, importer=None, b_npt_f_height='0.5 in', b_npt_f_nominalID='`1-1/4', b_npt_f_wall='0.08 in', base_plate_thick='0.12 in', holeDiaExpansion='0.03 in', npt_fxf_chamfer_bottom_size='0.04 in', npt_fxf_chamfer_top_size='0.04 in', s_npt_f_height='0.5 in', s_npt_f_nominalID='`3/4', s_npt_f_wall='0.08 in', )
    
    # main_part2
    from pprint import pformat
    print(f"myInstance.exportObj_by_objName= {pformat(myInstance.exportObj_by_objName)}")
    
    top_objects = myInstance.get_top_objects()
    print(f"myInstance.top_objects=")
    for obj in top_objects:
        print(f"    name={obj.Name}, label={obj.Label}")
    
    from cadcoder.doctools import reorganize_doc
    reorganize_doc(doc) 


if __name__ == '__main__':
    main()
