from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.baseClass import baseClass
from pdfclib.containertools import get_LCS_by_prefix
from pdfclib.objtools import update_obj_prop_jsonDict
from pdfclib.subelementtools import update_objs_seName, update_doc_seName, get_seName_by_posName

class Npt_ext(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, bottom_npt_f_femaleOD_wall_spec='2.032 mm', bottom_npt_f_holeDiaExpansion_spec='0.762 mm', horizontalScale=1.1982, middle_cone_height_spec='1 in', middle_cone_wall_spec='0.12 in', top_npt_m_hole_holeDiaExpansion_spec='0.762 mm', top_npt_m_hole_male_height_spec='15.24 mm', top_npt_m_hole_nominalOD='`2', verticalScale=1.261,  ):
        self.bottom_npt_f_femaleOD_wall_spec = bottom_npt_f_femaleOD_wall_spec
        self.bottom_npt_f_holeDiaExpansion_spec = bottom_npt_f_holeDiaExpansion_spec
        self.horizontalScale = horizontalScale
        self.middle_cone_height_spec = middle_cone_height_spec
        self.middle_cone_wall_spec = middle_cone_wall_spec
        self.top_npt_m_hole_holeDiaExpansion_spec = top_npt_m_hole_holeDiaExpansion_spec
        self.top_npt_m_hole_male_height_spec = top_npt_m_hole_male_height_spec
        self.top_npt_m_hole_nominalOD = top_npt_m_hole_nominalOD
        self.verticalScale = verticalScale
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        from parts.Npt_f import Npt_f
        bottom_npt_f_instance = Npt_f('bottom_npt_f_instance', doc, objPrefix=self.objPrefix + 'bottom_npt_f_', useLabel=True, importer=self, femaleOD_wall_spec='0.08 in', female_height_spec='0.6000000000000001 in', holeDiaExpansion_spec='0.030000000000000002 in', horizontalScale=1.1982, nominalID='`2', verticalScale=1.261, )
        self.bottom_npt_f_instance = bottom_npt_f_instance # expose as instance variable
        self.update_imports(bottom_npt_f_instance) # update import info for the instance
        bottom_npt_f_instance.boolean.Visibility = False  # adjust imported object
        from parts.Npt_m_hole import Npt_m_hole
        top_npt_m_hole_instance = Npt_m_hole('top_npt_m_hole_instance', doc, objPrefix=self.objPrefix + 'top_npt_m_hole_', useLabel=True, importer=self, bottomHoleDepth_spec='0.1 in', bottomHoleDia_spec='2.0706521739130435 in', holeDiaExpansion_spec='0.030000000000000002 in', horizontalScale=1.1982, male_height_spec='0.6000000000000001 in', nominalOD='`2', topHoleDepth_spec='0.5 in', topHoleDia_spec='2.0706521739130435 in', verticalScale=1.261, )
        self.top_npt_m_hole_instance = top_npt_m_hole_instance # expose as instance variable
        self.update_imports(top_npt_m_hole_instance) # update import info for the instance
        top_npt_m_hole_instance.npt_m_instance.body.Placement = Placement(Vector(0.0000, 0.0000, 51.2470), Rotation(0.0000, 0.0000, 0.0000, 1.0000))  # adjust imported object
        
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
        middle_outside_body.Placement = Placement(Vector(0.0000, 0.0000, 19.2176), Rotation(0.0000, 0.0000, 0.0000, 1.0000))
        middle_outside_body.recompute()  # recompute after adding object
        
        callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('callsheet') )
        callsheet.Label = self.addPrefix('callsheet')
        self.callsheet = callsheet
        self.post_new_obj(callsheet)
        callsheet.set('A1', 'variableName')
        callsheet.set('A10', 'top_npt_m_hole_bottomHoleDia_spec')
        callsheet.set('A11', 'top_npt_m_hole_holeDiaExpansion_spec')
        callsheet.set('A12', 'top_npt_m_hole_male_height_spec')
        callsheet.set('A13', 'top_npt_m_hole_nominalOD')
        callsheet.set('A14', 'top_npt_m_hole_topHoleDepth_spec')
        callsheet.set('A15', 'top_npt_m_hole_topHoleDia_spec')
        callsheet.set('A16', 'middle_cone_height_spec')
        callsheet.set('A17', 'middle_cone_height')
        callsheet.set('A18', 'middle_cone_wall_spec')
        callsheet.set('A19', 'middle_cone_wall')
        callsheet.set('A2', 'bottom_npt_f_femaleOD_wall_spec')
        callsheet.set('A20', 'middle_cone_outside_bottom_r')
        callsheet.set('A21', 'middle_cone_outside_top_r')
        callsheet.set('A22', 'middle_cone_inside_bottom_r')
        callsheet.set('A23', 'middle_cone_inside_top_r')
        callsheet.set('A3', 'bottom_npt_f_female_height_spec')
        callsheet.set('A4', 'bottom_npt_f_female_height')
        callsheet.set('A5', 'bottom_npt_f_holeDiaExpansion_spec')
        callsheet.set('A6', 'horizontalScale')
        callsheet.set('A7', 'bottom_npt_f_nominalID')
        callsheet.set('A8', 'verticalScale')
        callsheet.set('A9', 'top_npt_m_hole_bottomHoleDepth_spec')
        callsheet.set('B1', 'value')
        callsheet.set('B10', '=2.0706521739130435 in')
        callsheet.setAlias('B10', 'top_npt_m_hole_bottomHoleDia_spec')
        callsheet.set('B11', '=0.762 mm')
        callsheet.setAlias('B11', 'top_npt_m_hole_holeDiaExpansion_spec')
        callsheet.set('B12', '=15.24 mm')
        callsheet.setAlias('B12', 'top_npt_m_hole_male_height_spec')
        callsheet.set('B13', '`2')
        callsheet.setAlias('B13', 'top_npt_m_hole_nominalOD')
        callsheet.set('B14', '=0.5 in')
        callsheet.setAlias('B14', 'top_npt_m_hole_topHoleDepth_spec')
        callsheet.set('B15', '=2.0706521739130435 in')
        callsheet.setAlias('B15', 'top_npt_m_hole_topHoleDia_spec')
        callsheet.set('B16', '=1 in')
        callsheet.setAlias('B16', 'middle_cone_height_spec')
        callsheet.set('B17', '=1.261 in')
        callsheet.setAlias('B17', 'middle_cone_height')
        callsheet.set('B18', '=0.12 in')
        callsheet.setAlias('B18', 'middle_cone_wall_spec')
        callsheet.set('B19', '=0.143784 in')
        callsheet.setAlias('B19', 'middle_cone_wall')
        callsheet.set('B2', '=2.032 mm')
        callsheet.setAlias('B2', 'bottom_npt_f_femaleOD_wall_spec')
        callsheet.set('B20', '=1.5366914999999999 in')
        callsheet.setAlias('B20', 'middle_cone_outside_bottom_r')
        callsheet.set('B21', '=1.4228625 in')
        callsheet.setAlias('B21', 'middle_cone_outside_top_r')
        callsheet.set('B22', '=1.3929075 in')
        callsheet.setAlias('B22', 'middle_cone_inside_bottom_r')
        callsheet.set('B23', '=1.2790785 in')
        callsheet.setAlias('B23', 'middle_cone_inside_top_r')
        callsheet.set('B3', '=0.6000000000000001 in')
        callsheet.setAlias('B3', 'bottom_npt_f_female_height_spec')
        callsheet.set('B4', '=0.7566 in')
        callsheet.setAlias('B4', 'bottom_npt_f_female_height')
        callsheet.set('B5', '=0.762 mm')
        callsheet.setAlias('B5', 'bottom_npt_f_holeDiaExpansion_spec')
        callsheet.set('B6', '1.1982')
        callsheet.setAlias('B6', 'horizontalScale')
        callsheet.set('B7', '`2')
        callsheet.setAlias('B7', 'bottom_npt_f_nominalID')
        callsheet.set('B8', '1.261')
        callsheet.setAlias('B8', 'verticalScale')
        callsheet.set('B9', '=0.1 in')
        callsheet.setAlias('B9', 'top_npt_m_hole_bottomHoleDepth_spec')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C10', 'N')
        callsheet.set('C11', 'Y')
        callsheet.set('C12', 'Y')
        callsheet.set('C13', 'Y')
        callsheet.set('C14', 'N')
        callsheet.set('C15', 'N')
        callsheet.set('C16', 'Y')
        callsheet.set('C17', 'N')
        callsheet.set('C18', 'Y')
        callsheet.set('C19', 'N')
        callsheet.set('C2', 'Y')
        callsheet.set('C20', 'N')
        callsheet.set('C21', 'N')
        callsheet.set('C22', 'N')
        callsheet.set('C23', 'N')
        callsheet.set('C3', 'N')
        callsheet.set('C4', 'N')
        callsheet.set('C5', 'Y')
        callsheet.set('C6', 'Y')
        callsheet.set('C7', 'N')
        callsheet.set('C8', 'Y')
        callsheet.set('C9', 'N')
        callsheet.set('D1', 'comment')
        callsheet.set('D11', '0.03 in for 3D print')
        callsheet.set('D13', 'from npt_m_spec.nominalOD')
        callsheet.set('D6', 'BASF 17-4 xy scale 1.1982')
        callsheet.set('D8', 'BASF 17-4 z scale 1.2610')
        callsheet.Visibility = False
        callsheet.ViewObject.Visibility = False
        callsheet.recompute()  # recompute after adding object
        
        middle_inside_cone = doc.addObject('PartDesign::AdditiveCone', self.addPrefix('middle_inside_cone') )
        middle_inside_cone.Label = self.addPrefix('middle_inside_cone')
        self.middle_inside_cone = middle_inside_cone
        self.post_new_obj(middle_inside_cone)
        self.container_append_object(middle_inside_body, middle_inside_cone)
        middle_inside_cone.AttachmentSupport = (callsheet, (''))
        callsheet.Visibility = False  # hide base object
        middle_inside_cone.Height = 32.029399999999995
        middle_inside_cone.Radius1 = 35.379850499999996
        middle_inside_cone.Radius2 = 32.4885939
        middle_inside_cone.recompute()  # recompute after adding object
        
        middle_outside_cone = doc.addObject('PartDesign::AdditiveCone', self.addPrefix('middle_outside_cone') )
        middle_outside_cone.Label = self.addPrefix('middle_outside_cone')
        self.middle_outside_cone = middle_outside_cone
        self.post_new_obj(middle_outside_cone)
        self.container_append_object(middle_outside_body, middle_outside_cone)
        middle_outside_cone.Height = 32.029399999999995
        middle_outside_cone.Radius1 = 39.031964099999996
        middle_outside_cone.Radius2 = 36.1407075
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
        callsheet.set(callsheet.getCellFromAlias("top_npt_m_hole_bottomHoleDepth_spec"), f"=0.1 in")
        top_npt_m_hole_instance.callsheet.set(top_npt_m_hole_instance.callsheet.getCellFromAlias('bottomHoleDepth_spec'), f"=<<{self.addPrefix('callsheet')}>>.top_npt_m_hole_bottomHoleDepth_spec")
        top_npt_m_hole_instance.callsheet.set(top_npt_m_hole_instance.callsheet.getCellFromAlias('nominalOD'), f"=<<{self.addPrefix('callsheet')}>>.top_npt_m_hole_nominalOD")
        top_npt_m_hole_instance.callsheet.set(top_npt_m_hole_instance.callsheet.getCellFromAlias('horizontalScale'), f"=<<{self.addPrefix('callsheet')}>>.horizontalScale")
        top_npt_m_hole_instance.callsheet.set(top_npt_m_hole_instance.callsheet.getCellFromAlias('verticalScale'), f"=<<{self.addPrefix('callsheet')}>>.verticalScale")
        top_npt_m_hole_instance.callsheet.set(top_npt_m_hole_instance.callsheet.getCellFromAlias('holeDiaExpansion_spec'), f"=<<{self.addPrefix('callsheet')}>>.top_npt_m_hole_holeDiaExpansion_spec")
        top_npt_m_hole_instance.callsheet.set(top_npt_m_hole_instance.callsheet.getCellFromAlias('male_height_spec'), f"=<<{self.addPrefix('callsheet')}>>.top_npt_m_hole_male_height_spec")
        bottom_npt_f_instance.callsheet.set(bottom_npt_f_instance.callsheet.getCellFromAlias('holeDiaExpansion_spec'), f"=<<{self.addPrefix('callsheet')}>>.bottom_npt_f_holeDiaExpansion_spec")
        bottom_npt_f_instance.callsheet.set(bottom_npt_f_instance.callsheet.getCellFromAlias('horizontalScale'), f"=<<{self.addPrefix('callsheet')}>>.horizontalScale")
        bottom_npt_f_instance.callsheet.set(bottom_npt_f_instance.callsheet.getCellFromAlias('verticalScale'), f"=<<{self.addPrefix('callsheet')}>>.verticalScale")
        bottom_npt_f_instance.callsheet.set(bottom_npt_f_instance.callsheet.getCellFromAlias('femaleOD_wall_spec'), f"=<<{self.addPrefix('callsheet')}>>.bottom_npt_f_femaleOD_wall_spec")
        callsheet.set(callsheet.getCellFromAlias("top_npt_m_hole_topHoleDepth_spec"), f"=top_npt_m_hole_male_height_spec - top_npt_m_hole_bottomHoleDepth_spec")
        callsheet.set(callsheet.getCellFromAlias("middle_cone_height"), f"=middle_cone_height_spec * verticalScale")
        callsheet.set(callsheet.getCellFromAlias("middle_cone_wall"), f"=middle_cone_wall_spec * horizontalScale")
        callsheet.set(callsheet.getCellFromAlias("bottom_npt_f_female_height_spec"), f"=top_npt_m_hole_male_height_spec")
        callsheet.set(callsheet.getCellFromAlias("bottom_npt_f_nominalID"), f"=top_npt_m_hole_nominalOD")
        middle_inside_cone.setExpression("Height", f"<<{self.addPrefix('callsheet')}>>.middle_cone_height")
        middle_outside_cone.setExpression("Height", f"<<{self.addPrefix('callsheet')}>>.middle_cone_height")
        top_npt_m_hole_instance.callsheet.set(top_npt_m_hole_instance.callsheet.getCellFromAlias('topHoleDepth_spec'), f"=<<{self.addPrefix('callsheet')}>>.top_npt_m_hole_topHoleDepth_spec")
        bottom_npt_f_instance.callsheet.set(bottom_npt_f_instance.callsheet.getCellFromAlias('nominalID'), f"=<<{self.addPrefix('callsheet')}>>.bottom_npt_f_nominalID")
        bottom_npt_f_instance.callsheet.set(bottom_npt_f_instance.callsheet.getCellFromAlias('female_height_spec'), f"=<<{self.addPrefix('callsheet')}>>.bottom_npt_f_female_height_spec")
        callsheet.set(callsheet.getCellFromAlias("bottom_npt_f_female_height"), f"=bottom_npt_f_female_height_spec * verticalScale")
        middle_outside_body.setExpression(".Placement.Base.z", f"<<{self.addPrefix('callsheet')}>>.bottom_npt_f_female_height")
        callsheet.set(callsheet.getCellFromAlias("top_npt_m_hole_bottomHoleDia_spec"), f"=hiddenref(<<{self.addPrefix('top_npt_m_hole_npt_m_callsheet')}>>.realOD_expanded_spec - <<{self.addPrefix('top_npt_m_hole_npt_m_callsheet')}>>.pitch_spec * 3.5)")
        callsheet.set(callsheet.getCellFromAlias("middle_cone_outside_bottom_r"), f"=hiddenref(<<{self.addPrefix('bottom_npt_f_callsheet')}>>.femaleOD / 2)")
        callsheet.set(callsheet.getCellFromAlias("middle_cone_outside_top_r"), f"=hiddenref(<<{self.addPrefix('top_npt_m_hole_npt_m_callsheet')}>>.realOD / 2)")
        middle_outside_cone.setExpression("Radius1", f"<<{self.addPrefix('callsheet')}>>.middle_cone_outside_bottom_r")
        middle_outside_cone.setExpression("Radius2", f"<<{self.addPrefix('callsheet')}>>.middle_cone_outside_top_r")
        top_npt_m_hole_instance.callsheet_hole.set(top_npt_m_hole_instance.callsheet_hole.getCellFromAlias('bottomHoleDia_spec'), f"=<<{self.addPrefix('callsheet')}>>.top_npt_m_hole_bottomHoleDia_spec")
        callsheet.set(callsheet.getCellFromAlias("top_npt_m_hole_topHoleDia_spec"), f"=top_npt_m_hole_bottomHoleDia_spec")
        callsheet.set(callsheet.getCellFromAlias("middle_cone_inside_bottom_r"), f"=middle_cone_outside_bottom_r - middle_cone_wall")
        callsheet.set(callsheet.getCellFromAlias("middle_cone_inside_top_r"), f"=middle_cone_outside_top_r - middle_cone_wall")
        middle_inside_cone.setExpression("Radius1", f"<<{self.addPrefix('callsheet')}>>.middle_cone_inside_bottom_r")
        middle_inside_cone.setExpression("Radius2", f"<<{self.addPrefix('callsheet')}>>.middle_cone_inside_top_r")
        top_npt_m_hole_instance.callsheet_hole.set(top_npt_m_hole_instance.callsheet_hole.getCellFromAlias('topHoleDia_spec'), f"=<<{self.addPrefix('callsheet')}>>.top_npt_m_hole_topHoleDia_spec")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # now we have rebuilt the original Npt_ext doc. Now we apply dynmic call parameters
        print("there can be temporary errors when we applying dynamic call parameters that change original Npt_ext's shape.")
        print("ignore temporary errors, if any, below.")
        callsheet.set(callsheet.getCellFromAlias('top_npt_m_hole_holeDiaExpansion_spec'), f'={self.top_npt_m_hole_holeDiaExpansion_spec}')
        callsheet.set(callsheet.getCellFromAlias('top_npt_m_hole_male_height_spec'), f'={self.top_npt_m_hole_male_height_spec}')
        callsheet.set(callsheet.getCellFromAlias('top_npt_m_hole_nominalOD'), f'{self.top_npt_m_hole_nominalOD}')
        callsheet.set(callsheet.getCellFromAlias('middle_cone_height_spec'), f'={self.middle_cone_height_spec}')
        callsheet.set(callsheet.getCellFromAlias('middle_cone_wall_spec'), f'={self.middle_cone_wall_spec}')
        callsheet.set(callsheet.getCellFromAlias('bottom_npt_f_femaleOD_wall_spec'), f'={self.bottom_npt_f_femaleOD_wall_spec}')
        callsheet.set(callsheet.getCellFromAlias('bottom_npt_f_holeDiaExpansion_spec'), f'={self.bottom_npt_f_holeDiaExpansion_spec}')
        callsheet.set(callsheet.getCellFromAlias('horizontalScale'), f'{self.horizontalScale}')
        callsheet.set(callsheet.getCellFromAlias('verticalScale'), f'{self.verticalScale}')
        doc.recompute()
        update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.
        print("ignore temporary errors, if any, above.")
        
        self.update_callsheet()


def main():
    # main_part1
    from pdfclib.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of Npt_ext
    myInstance = Npt_ext("myInstance", doc, objPrefix="", useLabel=True, importer=None, bottom_npt_f_femaleOD_wall_spec='2.032 mm', bottom_npt_f_holeDiaExpansion_spec='0.762 mm', horizontalScale=1.1982, middle_cone_height_spec='1 in', middle_cone_wall_spec='0.12 in', top_npt_m_hole_holeDiaExpansion_spec='0.762 mm', top_npt_m_hole_male_height_spec='15.24 mm', top_npt_m_hole_nominalOD='`2', verticalScale=1.261, )
    
    # main_part2
    from pprint import pformat
    print(f"myInstance.exportObj_by_objName= {pformat(myInstance.exportObj_by_objName)}")
    
    top_objects = myInstance.get_top_objects()
    print(f"myInstance.top_objects=")
    for obj in top_objects:
        print(f"    name={obj.Name}, label={obj.Label}")
    
    from pdfclib.doctools import reorganize_doc
    reorganize_doc(doc) 


if __name__ == '__main__':
    main()
