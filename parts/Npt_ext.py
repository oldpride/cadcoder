from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.baseClass import baseClass
from cadcoder.containertools import get_LCS_by_prefix
from cadcoder.objtools import update_obj_prop_jsonDict
from cadcoder.subelementtools import update_objs_seName, update_doc_seName, get_seName_by_posName

class npt_ext(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, bottom_npt_f_femaleOD_wall='2.032 mm', bottom_npt_f_holeDiaExpansion='0.762 mm', middle_cone_height='1 in', middle_cone_wall='0.12 in', top_npt_m_hole_holeDiaExpansion='0.762 mm', top_npt_m_hole_male_height='15.24 mm', top_npt_m_hole_nominalOD='`1',  ):
        self.bottom_npt_f_femaleOD_wall = bottom_npt_f_femaleOD_wall
        self.bottom_npt_f_holeDiaExpansion = bottom_npt_f_holeDiaExpansion
        self.middle_cone_height = middle_cone_height
        self.middle_cone_wall = middle_cone_wall
        self.top_npt_m_hole_holeDiaExpansion = top_npt_m_hole_holeDiaExpansion
        self.top_npt_m_hole_male_height = top_npt_m_hole_male_height
        self.top_npt_m_hole_nominalOD = top_npt_m_hole_nominalOD
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        from parts.npt_f import npt_f
        bottom_npt_f_instance = npt_f('bottom_npt_f_instance', doc, objPrefix=self.objPrefix + 'bottom_npt_f_', useLabel=True, importer=self, diaExpansion='0.030000000000000002 in', femaleOD_wall='0.08 in', female_height='0.6000000000000001 in', nominalID='`1', )
        self.bottom_npt_f_instance = bottom_npt_f_instance # expose as instance variable
        self.update_imports(bottom_npt_f_instance) # update import info for the instance
        bottom_npt_f_instance.boolean.Visibility = False  # adjust imported object
        from parts.npt_m_hole import npt_m_hole
        top_npt_m_hole_instance = npt_m_hole('top_npt_m_hole_instance', doc, objPrefix=self.objPrefix + 'top_npt_m_hole_', useLabel=True, importer=self, bottomHoleDepth='0.1 in', bottomHoleDia0='1.0106521739130434 in', holeDiaExpansion='0.030000000000000002 in', male_height='0.6000000000000001 in', nominalOD='`1', topHoleDepth='0.5 in', topHoleDia0='1.0106521739130434 in', )
        self.top_npt_m_hole_instance = top_npt_m_hole_instance # expose as instance variable
        self.update_imports(top_npt_m_hole_instance) # update import info for the instance
        top_npt_m_hole_instance.npt_m_instance.body.Placement = Placement(Vector(0.0000, 0.0000, 40.6400), Rotation(0.0000, 0.0000, 0.0000, 1.0000))  # adjust imported object
        
        # add objects and add static value to objects' properties based on object dependencies
        middle_inside_body = doc.addObject('PartDesign::Body', self.addPrefix('middle_inside_body') )
        middle_inside_body.Label = self.addPrefix('middle_inside_body')
        self.middle_inside_body = middle_inside_body
        self.post_new_obj(middle_inside_body)
        middle_inside_body_Origin = get_LCS_by_prefix(doc, middle_inside_body, 'Origin')
        middle_inside_body_X_Axis = get_LCS_by_prefix(doc, middle_inside_body, 'X_Axis')
        middle_inside_body_Y_Axis = get_LCS_by_prefix(doc, middle_inside_body, 'Y_Axis')
        middle_inside_body_Z_Axis = get_LCS_by_prefix(doc, middle_inside_body, 'Z_Axis')
        middle_inside_body_XY_Plane = get_LCS_by_prefix(doc, middle_inside_body, 'XY_Plane')
        middle_inside_body_XZ_Plane = get_LCS_by_prefix(doc, middle_inside_body, 'XZ_Plane')
        middle_inside_body_YZ_Plane = get_LCS_by_prefix(doc, middle_inside_body, 'YZ_Plane')
        self.middle_inside_body_Origin = middle_inside_body_Origin
        self.middle_inside_body_X_Axis = middle_inside_body_X_Axis
        self.middle_inside_body_Y_Axis = middle_inside_body_Y_Axis
        self.middle_inside_body_Z_Axis = middle_inside_body_Z_Axis
        self.middle_inside_body_XY_Plane = middle_inside_body_XY_Plane
        self.middle_inside_body_XZ_Plane = middle_inside_body_XZ_Plane
        self.middle_inside_body_YZ_Plane = middle_inside_body_YZ_Plane
        self.post_new_obj(middle_inside_body_Origin)
        self.post_new_obj(middle_inside_body_X_Axis)
        self.post_new_obj(middle_inside_body_Y_Axis)
        self.post_new_obj(middle_inside_body_Z_Axis)
        self.post_new_obj(middle_inside_body_XY_Plane)
        self.post_new_obj(middle_inside_body_XZ_Plane)
        self.post_new_obj(middle_inside_body_YZ_Plane)
        middle_inside_body.recompute()  # recompute after adding object
        
        middle_outside_body = doc.addObject('PartDesign::Body', self.addPrefix('middle_outside_body') )
        middle_outside_body.Label = self.addPrefix('middle_outside_body')
        self.middle_outside_body = middle_outside_body
        self.post_new_obj(middle_outside_body)
        middle_outside_body_Origin = get_LCS_by_prefix(doc, middle_outside_body, 'Origin')
        middle_outside_body_X_Axis = get_LCS_by_prefix(doc, middle_outside_body, 'X_Axis')
        middle_outside_body_Y_Axis = get_LCS_by_prefix(doc, middle_outside_body, 'Y_Axis')
        middle_outside_body_Z_Axis = get_LCS_by_prefix(doc, middle_outside_body, 'Z_Axis')
        middle_outside_body_XY_Plane = get_LCS_by_prefix(doc, middle_outside_body, 'XY_Plane')
        middle_outside_body_XZ_Plane = get_LCS_by_prefix(doc, middle_outside_body, 'XZ_Plane')
        middle_outside_body_YZ_Plane = get_LCS_by_prefix(doc, middle_outside_body, 'YZ_Plane')
        self.middle_outside_body_Origin = middle_outside_body_Origin
        self.middle_outside_body_X_Axis = middle_outside_body_X_Axis
        self.middle_outside_body_Y_Axis = middle_outside_body_Y_Axis
        self.middle_outside_body_Z_Axis = middle_outside_body_Z_Axis
        self.middle_outside_body_XY_Plane = middle_outside_body_XY_Plane
        self.middle_outside_body_XZ_Plane = middle_outside_body_XZ_Plane
        self.middle_outside_body_YZ_Plane = middle_outside_body_YZ_Plane
        self.post_new_obj(middle_outside_body_Origin)
        self.post_new_obj(middle_outside_body_X_Axis)
        self.post_new_obj(middle_outside_body_Y_Axis)
        self.post_new_obj(middle_outside_body_Z_Axis)
        self.post_new_obj(middle_outside_body_XY_Plane)
        self.post_new_obj(middle_outside_body_XZ_Plane)
        self.post_new_obj(middle_outside_body_YZ_Plane)
        middle_outside_body.Placement = Placement(Vector(0.0000, 0.0000, 15.2400), Rotation(0.0000, 0.0000, 0.0000, 1.0000))
        middle_outside_body.recompute()  # recompute after adding object
        
        callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('callsheet') )
        callsheet.Label = self.addPrefix('callsheet')
        self.callsheet = callsheet
        self.post_new_obj(callsheet)
        callsheet.set('A1', 'variableName')
        callsheet.set('A10', 'top_npt_m_hole_topHoleDepth')
        callsheet.set('A11', 'top_npt_m_hole_placement_z')
        callsheet.set('A12', 'middle_cone_height')
        callsheet.set('A13', 'middle_cone_wall')
        callsheet.set('A2', 'bottom_npt_f_femaleOD_wall')
        callsheet.set('A3', 'bottom_npt_f_female_height')
        callsheet.set('A4', 'bottom_npt_f_holeDiaExpansion')
        callsheet.set('A5', 'bottom_npt_f_nominalID')
        callsheet.set('A6', 'top_npt_m_hole_bottomHoleDepth')
        callsheet.set('A7', 'top_npt_m_hole_holeDiaExpansion')
        callsheet.set('A8', 'top_npt_m_hole_male_height')
        callsheet.set('A9', 'top_npt_m_hole_nominalOD')
        callsheet.set('B1', 'value')
        callsheet.set('B10', '=0.5 in')
        callsheet.setAlias('B10', 'top_npt_m_hole_topHoleDepth')
        callsheet.set('B11', '=1.6 in')
        callsheet.setAlias('B11', 'top_npt_m_hole_placement_z')
        callsheet.set('B12', '=1 in')
        callsheet.setAlias('B12', 'middle_cone_height')
        callsheet.set('B13', '=0.12 in')
        callsheet.setAlias('B13', 'middle_cone_wall')
        callsheet.set('B2', '=2.032 mm')
        callsheet.setAlias('B2', 'bottom_npt_f_femaleOD_wall')
        callsheet.set('B3', '=0.6000000000000001 in')
        callsheet.setAlias('B3', 'bottom_npt_f_female_height')
        callsheet.set('B4', '=0.762 mm')
        callsheet.setAlias('B4', 'bottom_npt_f_holeDiaExpansion')
        callsheet.set('B5', '`1')
        callsheet.setAlias('B5', 'bottom_npt_f_nominalID')
        callsheet.set('B6', '=0.1 in')
        callsheet.setAlias('B6', 'top_npt_m_hole_bottomHoleDepth')
        callsheet.set('B7', '=0.762 mm')
        callsheet.setAlias('B7', 'top_npt_m_hole_holeDiaExpansion')
        callsheet.set('B8', '=15.24 mm')
        callsheet.setAlias('B8', 'top_npt_m_hole_male_height')
        callsheet.set('B9', '`1')
        callsheet.setAlias('B9', 'top_npt_m_hole_nominalOD')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C10', 'N')
        callsheet.set('C11', 'N')
        callsheet.set('C12', 'Y')
        callsheet.set('C13', 'Y')
        callsheet.set('C2', 'Y')
        callsheet.set('C3', 'N')
        callsheet.set('C4', 'Y')
        callsheet.set('C5', 'N')
        callsheet.set('C6', 'N')
        callsheet.set('C7', 'Y')
        callsheet.set('C8', 'Y')
        callsheet.set('C9', 'Y')
        callsheet.set('D1', 'comment')
        callsheet.set('D7', '0.03 in for 3D print')
        callsheet.set('D9', 'from npt_m_spec.nominalOD')
        callsheet.Visibility = False
        callsheet.ViewObject.Visibility = False
        callsheet.recompute()  # recompute after adding object
        
        callsheet2 = doc.addObject('Spreadsheet::Sheet', self.addPrefix('callsheet2') )
        callsheet2.Label = self.addPrefix('callsheet2')
        self.callsheet2 = callsheet2
        self.post_new_obj(callsheet2)
        callsheet2.set('A1', 'variableName')
        callsheet2.set('A2', 'top_npt_m_hole_bottomHoleDia')
        callsheet2.set('A3', 'top_npt_m_hole_topHoleDia')
        callsheet2.set('A4', 'middle_cone_outside_bottom_r')
        callsheet2.set('A5', 'middle_cone_outside_top_r')
        callsheet2.set('A6', 'middle_cone_inside_bottom_r')
        callsheet2.set('A7', 'middle_cone_inside_top_r')
        callsheet2.set('B1', 'value')
        callsheet2.set('B2', '=1.0106521739130434 in')
        callsheet2.setAlias('B2', 'top_npt_m_hole_bottomHoleDia')
        callsheet2.set('B3', '=1.0106521739130434 in')
        callsheet2.setAlias('B3', 'top_npt_m_hole_topHoleDia')
        callsheet2.set('B4', '=0.7525 in')
        callsheet2.setAlias('B4', 'middle_cone_outside_bottom_r')
        callsheet2.set('B5', '=0.6575 in')
        callsheet2.setAlias('B5', 'middle_cone_outside_top_r')
        callsheet2.set('B6', '=0.6325000000000001 in')
        callsheet2.setAlias('B6', 'middle_cone_inside_bottom_r')
        callsheet2.set('B7', '=0.5375 in')
        callsheet2.setAlias('B7', 'middle_cone_inside_top_r')
        callsheet2.set('C1', 'isCallParam')
        callsheet2.set('C2', 'N')
        callsheet2.set('C3', 'N')
        callsheet2.set('C4', 'N')
        callsheet2.set('C5', 'N')
        callsheet2.set('C6', 'N')
        callsheet2.set('C7', 'N')
        callsheet2.set('D1', 'comment')
        callsheet2.recompute()  # recompute after adding object
        
        middle_inside_cone = doc.addObject('PartDesign::AdditiveCone', self.addPrefix('middle_inside_cone') )
        middle_inside_cone.Label = self.addPrefix('middle_inside_cone')
        self.middle_inside_cone = middle_inside_cone
        self.post_new_obj(middle_inside_cone)
        self.container_append_object(middle_inside_body, middle_inside_cone)
        middle_inside_cone.AttachmentSupport = (callsheet, (''))
        callsheet.Visibility = False  # hide base object
        middle_inside_cone.Height = 25.4
        middle_inside_cone.Radius1 = 16.0655
        middle_inside_cone.Radius2 = 13.652499999999998
        middle_inside_cone.recompute()  # recompute after adding object
        
        middle_outside_cone = doc.addObject('PartDesign::AdditiveCone', self.addPrefix('middle_outside_cone') )
        middle_outside_cone.Label = self.addPrefix('middle_outside_cone')
        self.middle_outside_cone = middle_outside_cone
        self.post_new_obj(middle_outside_cone)
        self.container_append_object(middle_outside_body, middle_outside_cone)
        middle_outside_cone.Height = 25.4
        middle_outside_cone.Radius1 = 19.1135
        middle_outside_cone.Radius2 = 16.700499999999998
        middle_outside_cone.Visibility = False
        middle_outside_cone.ViewObject.Visibility = False
        middle_outside_cone.recompute()  # recompute after adding object
        
        middle_boolean_cut = doc.addObject('PartDesign::Boolean', self.addPrefix('middle_boolean_cut') )
        middle_boolean_cut.Label = self.addPrefix('middle_boolean_cut')
        self.middle_boolean_cut = middle_boolean_cut
        self.post_new_obj(middle_boolean_cut)
        self.container_append_object(middle_outside_body, middle_boolean_cut)
        middle_boolean_cut.BaseFeature = middle_outside_cone
        middle_boolean_cut.Group = [middle_inside_body]
        middle_boolean_cut.Type = 'Cut'
        middle_boolean_cut.UsePlacement = True
        doc.recompute() # recompute whole document for PartDesign::Boolean
        
        boolean_add_middle_cone = doc.addObject('PartDesign::Boolean', self.addPrefix('boolean_add_middle_cone') )
        boolean_add_middle_cone.Label = self.addPrefix('boolean_add_middle_cone')
        self.boolean_add_middle_cone = boolean_add_middle_cone
        self.post_new_obj(boolean_add_middle_cone)
        self.container_append_object(bottom_npt_f_instance.body, boolean_add_middle_cone)
        boolean_add_middle_cone.BaseFeature = bottom_npt_f_instance.boolean
        boolean_add_middle_cone.Group = [middle_outside_body]
        boolean_add_middle_cone.UsePlacement = True
        boolean_add_middle_cone.Visibility = False
        boolean_add_middle_cone.ViewObject.Visibility = False
        doc.recompute() # recompute whole document for PartDesign::Boolean
        
        boolean_add_top_npt_m = doc.addObject('PartDesign::Boolean', self.addPrefix('boolean_add_top_npt_m') )
        boolean_add_top_npt_m.Label = self.addPrefix('boolean_add_top_npt_m')
        self.boolean_add_top_npt_m = boolean_add_top_npt_m
        self.post_new_obj(boolean_add_top_npt_m)
        self.container_append_object(bottom_npt_f_instance.body, boolean_add_top_npt_m)
        boolean_add_top_npt_m.BaseFeature = boolean_add_middle_cone
        boolean_add_top_npt_m.Group = [top_npt_m_hole_instance.npt_m_instance.body]
        boolean_add_top_npt_m.UsePlacement = True
        doc.recompute() # recompute whole document for PartDesign::Boolean
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        callsheet.set(callsheet.getCellFromAlias("top_npt_m_hole_bottomHoleDepth"), f"=0.1 in")
        middle_inside_cone.setExpression("Height", f"<<{self.addPrefix('callsheet')}>>.middle_cone_height")
        middle_outside_cone.setExpression("Height", f"<<{self.addPrefix('callsheet')}>>.middle_cone_height")
        top_npt_m_hole_instance.callsheet.set(top_npt_m_hole_instance.callsheet.getCellFromAlias('nominalOD'), f"=<<{self.addPrefix('callsheet')}>>.top_npt_m_hole_nominalOD")
        top_npt_m_hole_instance.callsheet.set(top_npt_m_hole_instance.callsheet.getCellFromAlias('holeDiaExpansion'), f"=<<{self.addPrefix('callsheet')}>>.top_npt_m_hole_holeDiaExpansion")
        top_npt_m_hole_instance.callsheet.set(top_npt_m_hole_instance.callsheet.getCellFromAlias('male_height'), f"=<<{self.addPrefix('callsheet')}>>.top_npt_m_hole_male_height")
        top_npt_m_hole_instance.callsheet.set(top_npt_m_hole_instance.callsheet.getCellFromAlias('bottomHoleDepth'), f"=<<{self.addPrefix('callsheet')}>>.top_npt_m_hole_bottomHoleDepth")
        bottom_npt_f_instance.callsheet.set(bottom_npt_f_instance.callsheet.getCellFromAlias('femaleOD_wall'), f"=<<{self.addPrefix('callsheet')}>>.bottom_npt_f_femaleOD_wall")
        bottom_npt_f_instance.callsheet.set(bottom_npt_f_instance.callsheet.getCellFromAlias('diaExpansion'), f"=<<{self.addPrefix('callsheet')}>>.bottom_npt_f_holeDiaExpansion")
        callsheet.set(callsheet.getCellFromAlias("top_npt_m_hole_topHoleDepth"), f"=top_npt_m_hole_male_height - top_npt_m_hole_bottomHoleDepth")
        callsheet.set(callsheet.getCellFromAlias("bottom_npt_f_female_height"), f"=top_npt_m_hole_male_height")
        callsheet.set(callsheet.getCellFromAlias("bottom_npt_f_nominalID"), f"=top_npt_m_hole_nominalOD")
        middle_outside_body.setExpression(".Placement.Base.z", f"<<{self.addPrefix('callsheet')}>>.bottom_npt_f_female_height")
        top_npt_m_hole_instance.callsheet.set(top_npt_m_hole_instance.callsheet.getCellFromAlias('topHoleDepth'), f"=<<{self.addPrefix('callsheet')}>>.top_npt_m_hole_topHoleDepth")
        bottom_npt_f_instance.callsheet.set(bottom_npt_f_instance.callsheet.getCellFromAlias('nominalID'), f"=<<{self.addPrefix('callsheet')}>>.bottom_npt_f_nominalID")
        bottom_npt_f_instance.callsheet.set(bottom_npt_f_instance.callsheet.getCellFromAlias('female_height'), f"=<<{self.addPrefix('callsheet')}>>.bottom_npt_f_female_height")
        callsheet.set(callsheet.getCellFromAlias("top_npt_m_hole_placement_z"), f"=middle_cone_height + bottom_npt_f_female_height")
        callsheet2.set(callsheet2.getCellFromAlias("middle_cone_outside_bottom_r"), f"=<<{self.addPrefix('bottom_npt_f_callsheet')}>>.femaleOD / 2")
        middle_outside_cone.setExpression("Radius1", f"<<{self.addPrefix('callsheet2')}>>.middle_cone_outside_bottom_r")
        callsheet2.set(callsheet2.getCellFromAlias("top_npt_m_hole_bottomHoleDia"), f"=<<{self.addPrefix('top_npt_m_hole_npt_m_callsheet')}>>.realOD - <<{self.addPrefix('top_npt_m_hole_npt_m_callsheet')}>>.pitch * 3.5")
        callsheet2.set(callsheet2.getCellFromAlias("middle_cone_outside_top_r"), f"=<<{self.addPrefix('top_npt_m_hole_npt_m_callsheet')}>>.realOD / 2")
        callsheet2.set(callsheet2.getCellFromAlias("middle_cone_inside_bottom_r"), f"=middle_cone_outside_bottom_r - <<{self.addPrefix('callsheet')}>>.middle_cone_wall")
        middle_inside_cone.setExpression("Radius1", f"<<{self.addPrefix('callsheet2')}>>.middle_cone_inside_bottom_r")
        middle_outside_cone.setExpression("Radius2", f"<<{self.addPrefix('callsheet2')}>>.middle_cone_outside_top_r")
        top_npt_m_hole_instance.callsheet_hole.set(top_npt_m_hole_instance.callsheet_hole.getCellFromAlias('bottomHoleDia0'), f"=<<{self.addPrefix('callsheet2')}>>.top_npt_m_hole_bottomHoleDia")
        callsheet2.set(callsheet2.getCellFromAlias("top_npt_m_hole_topHoleDia"), f"=top_npt_m_hole_bottomHoleDia")
        callsheet2.set(callsheet2.getCellFromAlias("middle_cone_inside_top_r"), f"=middle_cone_outside_top_r - <<{self.addPrefix('callsheet')}>>.middle_cone_wall")
        middle_inside_cone.setExpression("Radius2", f"<<{self.addPrefix('callsheet2')}>>.middle_cone_inside_top_r")
        top_npt_m_hole_instance.callsheet_hole.set(top_npt_m_hole_instance.callsheet_hole.getCellFromAlias('topHoleDia0'), f"=<<{self.addPrefix('callsheet2')}>>.top_npt_m_hole_topHoleDia")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # now we have rebuilt the original npt_ext doc. Now we apply dynmic call parameters
        print("there can be temporary errors when we applying dynamic call parameters that change original npt_ext's shape.")
        print("ignore temporary errors, if any, below.")
        callsheet.set(callsheet.getCellFromAlias('middle_cone_height'), f'={self.middle_cone_height}')
        callsheet.set(callsheet.getCellFromAlias('middle_cone_wall'), f'={self.middle_cone_wall}')
        callsheet.set(callsheet.getCellFromAlias('bottom_npt_f_femaleOD_wall'), f'={self.bottom_npt_f_femaleOD_wall}')
        callsheet.set(callsheet.getCellFromAlias('bottom_npt_f_holeDiaExpansion'), f'={self.bottom_npt_f_holeDiaExpansion}')
        callsheet.set(callsheet.getCellFromAlias('top_npt_m_hole_holeDiaExpansion'), f'={self.top_npt_m_hole_holeDiaExpansion}')
        callsheet.set(callsheet.getCellFromAlias('top_npt_m_hole_male_height'), f'={self.top_npt_m_hole_male_height}')
        callsheet.set(callsheet.getCellFromAlias('top_npt_m_hole_nominalOD'), f'{self.top_npt_m_hole_nominalOD}')
        doc.recompute()
        update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.
        print("ignore temporary errors, if any, above.")
        
        self.update_callsheet()


def main():
    # main_part1
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of npt_ext
    myInstance = npt_ext("myInstance", doc, objPrefix="", useLabel=True, importer=None, bottom_npt_f_femaleOD_wall='2.032 mm', bottom_npt_f_holeDiaExpansion='0.762 mm', middle_cone_height='1 in', middle_cone_wall='0.12 in', top_npt_m_hole_holeDiaExpansion='0.762 mm', top_npt_m_hole_male_height='15.24 mm', top_npt_m_hole_nominalOD='`1', )
    
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
