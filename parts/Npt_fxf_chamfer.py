from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.baseClass import baseClass
from cadcoder.containertools import get_LCS_by_prefix
from cadcoder.objtools import update_obj_prop_jsonDict
from cadcoder.subelementtools import update_objs_seName, update_doc_seName, get_seName_by_posName

class Npt_fxf_chamfer(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, b_npt_f_height_spec='0.5 in', b_npt_f_nominalID='`2', b_npt_f_wall_spec='0.08 in', base_plate_thick_spec='0.12 in', holeDiaExpansion_spec='0.03 in', horizontalScale=1.1982, npt_fxf_chamfer_bottom_size_spec='0.04 in', npt_fxf_chamfer_top_size_spec='0.04 in', s_npt_f_height_spec='0.5 in', s_npt_f_nominalID='`3/4', s_npt_f_wall_spec='0.08 in', verticalScale=1.261,  ):
        self.b_npt_f_height_spec = b_npt_f_height_spec
        self.b_npt_f_nominalID = b_npt_f_nominalID
        self.b_npt_f_wall_spec = b_npt_f_wall_spec
        self.base_plate_thick_spec = base_plate_thick_spec
        self.holeDiaExpansion_spec = holeDiaExpansion_spec
        self.horizontalScale = horizontalScale
        self.npt_fxf_chamfer_bottom_size_spec = npt_fxf_chamfer_bottom_size_spec
        self.npt_fxf_chamfer_top_size_spec = npt_fxf_chamfer_top_size_spec
        self.s_npt_f_height_spec = s_npt_f_height_spec
        self.s_npt_f_nominalID = s_npt_f_nominalID
        self.s_npt_f_wall_spec = s_npt_f_wall_spec
        self.verticalScale = verticalScale
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        from examples.Npt_fxf import Npt_fxf
        npt_fxf_instance = Npt_fxf('npt_fxf_instance', doc, objPrefix=self.objPrefix + 'npt_fxf_', useLabel=True, importer=self, b_npt_f_height_spec='0.5 in', b_npt_f_nominalID='`2', b_npt_f_wall_spec='0.08 in', base_plate_thick_spec='0.12 in', holeDiaExpansion_spec='0.03 in', horizontalScale=1.1982, s_npt_f_height_spec='0.5 in', s_npt_f_nominalID='`3/4', s_npt_f_wall_spec='0.08 in', verticalScale=1.261, )
        self.npt_fxf_instance = npt_fxf_instance # expose as instance variable
        self.update_imports(npt_fxf_instance) # update import info for the instance
        npt_fxf_instance.b_npt_f_instance.body.Placement = Placement(Vector(0.0000, -0.0000, 19.8582), Rotation(1.0000, 0.0000, 0.0000, 0.0000))  # adjust imported object
        npt_fxf_instance.boolean.Visibility = False  # adjust imported object
        
        # add objects and add static value to objects' properties based on object dependencies
        callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('callsheet') )
        callsheet.Label = self.addPrefix('callsheet')
        self.callsheet = callsheet
        self.post_new_obj(callsheet)
        callsheet.set('A1', 'variableName')
        callsheet.set('A10', 's_npt_f_height_spec')
        callsheet.set('A11', 'b_npt_f_height_spec')
        callsheet.set('A12', 'base_plate_thick_spec')
        callsheet.set('A13', 'horizontalScale')
        callsheet.set('A14', 'verticalScale')
        callsheet.set('A15', 'holeDiaExpansion_spec')
        callsheet.set('A2', 'npt_fxf_chamfer_top_size_spec')
        callsheet.set('A3', 'npt_fxf_chamfer_top_size')
        callsheet.set('A4', 'npt_fxf_chamfer_bottom_size_spec')
        callsheet.set('A5', 'npt_fxf_chamfer_bottom_size')
        callsheet.set('A6', 's_npt_f_nominalID')
        callsheet.set('A7', 'b_npt_f_nominalID')
        callsheet.set('A8', 's_npt_f_wall_spec')
        callsheet.set('A9', 'b_npt_f_wall_spec')
        callsheet.set('B1', 'value')
        callsheet.set('B10', '=0.5 in')
        callsheet.setAlias('B10', 's_npt_f_height_spec')
        callsheet.set('B11', '=0.5 in')
        callsheet.setAlias('B11', 'b_npt_f_height_spec')
        callsheet.set('B12', '=0.12 in')
        callsheet.setAlias('B12', 'base_plate_thick_spec')
        callsheet.set('B13', '1.1982')
        callsheet.setAlias('B13', 'horizontalScale')
        callsheet.set('B14', '1.261')
        callsheet.setAlias('B14', 'verticalScale')
        callsheet.set('B15', '=0.03 in')
        callsheet.setAlias('B15', 'holeDiaExpansion_spec')
        callsheet.set('B2', '=0.04 in')
        callsheet.setAlias('B2', 'npt_fxf_chamfer_top_size_spec')
        callsheet.set('B3', '=0.047928 in')
        callsheet.setAlias('B3', 'npt_fxf_chamfer_top_size')
        callsheet.set('B4', '=0.04 in')
        callsheet.setAlias('B4', 'npt_fxf_chamfer_bottom_size_spec')
        callsheet.set('B5', '=0.047928 in')
        callsheet.setAlias('B5', 'npt_fxf_chamfer_bottom_size')
        callsheet.set('B6', '`3/4')
        callsheet.setAlias('B6', 's_npt_f_nominalID')
        callsheet.set('B7', '`2')
        callsheet.setAlias('B7', 'b_npt_f_nominalID')
        callsheet.set('B8', '=0.08 in')
        callsheet.setAlias('B8', 's_npt_f_wall_spec')
        callsheet.set('B9', '=0.08 in')
        callsheet.setAlias('B9', 'b_npt_f_wall_spec')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C10', 'Y')
        callsheet.set('C11', 'Y')
        callsheet.set('C12', 'Y')
        callsheet.set('C13', 'Y')
        callsheet.set('C14', 'Y')
        callsheet.set('C15', 'Y')
        callsheet.set('C2', 'Y')
        callsheet.set('C3', 'N')
        callsheet.set('C4', 'Y')
        callsheet.set('C5', 'N')
        callsheet.set('C6', 'Y')
        callsheet.set('C7', 'Y')
        callsheet.set('C8', 'Y')
        callsheet.set('C9', 'Y')
        callsheet.set('D1', 'comment')
        callsheet.set('D13', 'BASF 17-4 xy scale 1.1982')
        callsheet.set('D14', 'BASF 17-4 z scale 1.2610')
        callsheet.recompute()  # recompute after adding object
        
        doc.recompute() # recompute before adding PartDesign::Chamfer to avoid error
        bottom = doc.addObject('PartDesign::Chamfer', self.addPrefix('bottom') )
        bottom.Label = self.addPrefix('bottom')
        self.bottom = bottom
        self.post_new_obj(bottom)
        self.container_append_object(npt_fxf_instance.base_plate, bottom)
        bottom.Base = (npt_fxf_instance.boolean, [get_seName_by_posName(npt_fxf_instance.boolean, 'Edge', 'bottom1')])
        npt_fxf_instance.boolean.Visibility = False  # hide chamfer base object
        update_obj_prop_jsonDict(bottom, "pythonFeature",{"Base": [{"seType": "Edge", "posName": "bottom1"}]})
        bottom.Size = 1.2173711999999999
        bottom.Visibility = False
        bottom.ViewObject.Visibility = False
        bottom.recompute()  # recompute after adding object
        
        doc.recompute() # recompute before adding PartDesign::Chamfer to avoid error
        top = doc.addObject('PartDesign::Chamfer', self.addPrefix('top') )
        top.Label = self.addPrefix('top')
        self.top = top
        self.post_new_obj(top)
        self.container_append_object(npt_fxf_instance.base_plate, top)
        top.Base = (bottom, [get_seName_by_posName(bottom, 'Edge', 'top1')])
        bottom.Visibility = False  # hide chamfer base object
        update_obj_prop_jsonDict(top, "pythonFeature",{"Base": [{"seType": "Edge", "posName": "top1"}]})
        top.Size = 1.2173711999999999
        top.recompute()  # recompute after adding object
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        npt_fxf_instance.callsheet.set(npt_fxf_instance.callsheet.getCellFromAlias('base_plate_thick_spec'), f"=<<{self.addPrefix('callsheet')}>>.base_plate_thick_spec")
        npt_fxf_instance.callsheet.set(npt_fxf_instance.callsheet.getCellFromAlias('horizontalScale'), f"=<<{self.addPrefix('callsheet')}>>.horizontalScale")
        npt_fxf_instance.callsheet.set(npt_fxf_instance.callsheet.getCellFromAlias('verticalScale'), f"=<<{self.addPrefix('callsheet')}>>.verticalScale")
        npt_fxf_instance.callsheet.set(npt_fxf_instance.callsheet.getCellFromAlias('holeDiaExpansion_spec'), f"=<<{self.addPrefix('callsheet')}>>.holeDiaExpansion_spec")
        npt_fxf_instance.callsheet.set(npt_fxf_instance.callsheet.getCellFromAlias('s_npt_f_nominalID'), f"=<<{self.addPrefix('callsheet')}>>.s_npt_f_nominalID")
        npt_fxf_instance.callsheet.set(npt_fxf_instance.callsheet.getCellFromAlias('b_npt_f_nominalID'), f"=<<{self.addPrefix('callsheet')}>>.b_npt_f_nominalID")
        npt_fxf_instance.callsheet.set(npt_fxf_instance.callsheet.getCellFromAlias('s_npt_f_wall_spec'), f"=<<{self.addPrefix('callsheet')}>>.s_npt_f_wall_spec")
        npt_fxf_instance.callsheet.set(npt_fxf_instance.callsheet.getCellFromAlias('b_npt_f_wall_spec'), f"=<<{self.addPrefix('callsheet')}>>.b_npt_f_wall_spec")
        npt_fxf_instance.callsheet.set(npt_fxf_instance.callsheet.getCellFromAlias('s_npt_f_height_spec'), f"=<<{self.addPrefix('callsheet')}>>.s_npt_f_height_spec")
        npt_fxf_instance.callsheet.set(npt_fxf_instance.callsheet.getCellFromAlias('b_npt_f_height_spec'), f"=<<{self.addPrefix('callsheet')}>>.b_npt_f_height_spec")
        callsheet.set(callsheet.getCellFromAlias("npt_fxf_chamfer_top_size"), f"=npt_fxf_chamfer_top_size_spec * horizontalScale")
        callsheet.set(callsheet.getCellFromAlias("npt_fxf_chamfer_bottom_size"), f"=npt_fxf_chamfer_bottom_size_spec * horizontalScale")
        top.setExpression("Size", f"<<{self.addPrefix('callsheet')}>>.npt_fxf_chamfer_top_size")
        bottom.setExpression("Size", f"<<{self.addPrefix('callsheet')}>>.npt_fxf_chamfer_bottom_size")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # now we have rebuilt the original Npt_fxf_chamfer doc. Now we apply dynmic call parameters
        print("there can be temporary errors when we applying dynamic call parameters that change original Npt_fxf_chamfer's shape.")
        print("ignore temporary errors, if any, below.")
        callsheet.set(callsheet.getCellFromAlias('s_npt_f_height_spec'), f'={self.s_npt_f_height_spec}')
        callsheet.set(callsheet.getCellFromAlias('b_npt_f_height_spec'), f'={self.b_npt_f_height_spec}')
        callsheet.set(callsheet.getCellFromAlias('base_plate_thick_spec'), f'={self.base_plate_thick_spec}')
        callsheet.set(callsheet.getCellFromAlias('horizontalScale'), f'{self.horizontalScale}')
        callsheet.set(callsheet.getCellFromAlias('verticalScale'), f'{self.verticalScale}')
        callsheet.set(callsheet.getCellFromAlias('holeDiaExpansion_spec'), f'={self.holeDiaExpansion_spec}')
        callsheet.set(callsheet.getCellFromAlias('npt_fxf_chamfer_top_size_spec'), f'={self.npt_fxf_chamfer_top_size_spec}')
        callsheet.set(callsheet.getCellFromAlias('npt_fxf_chamfer_bottom_size_spec'), f'={self.npt_fxf_chamfer_bottom_size_spec}')
        callsheet.set(callsheet.getCellFromAlias('s_npt_f_nominalID'), f'{self.s_npt_f_nominalID}')
        callsheet.set(callsheet.getCellFromAlias('b_npt_f_nominalID'), f'{self.b_npt_f_nominalID}')
        callsheet.set(callsheet.getCellFromAlias('s_npt_f_wall_spec'), f'={self.s_npt_f_wall_spec}')
        callsheet.set(callsheet.getCellFromAlias('b_npt_f_wall_spec'), f'={self.b_npt_f_wall_spec}')
        doc.recompute()
        update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.
        print("ignore temporary errors, if any, above.")
        
        self.update_callsheet()


def main():
    # main_part1
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of Npt_fxf_chamfer
    myInstance = Npt_fxf_chamfer("myInstance", doc, objPrefix="", useLabel=True, importer=None, b_npt_f_height_spec='0.5 in', b_npt_f_nominalID='`2', b_npt_f_wall_spec='0.08 in', base_plate_thick_spec='0.12 in', holeDiaExpansion_spec='0.03 in', horizontalScale=1.1982, npt_fxf_chamfer_bottom_size_spec='0.04 in', npt_fxf_chamfer_top_size_spec='0.04 in', s_npt_f_height_spec='0.5 in', s_npt_f_nominalID='`3/4', s_npt_f_wall_spec='0.08 in', verticalScale=1.261, )
    
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
