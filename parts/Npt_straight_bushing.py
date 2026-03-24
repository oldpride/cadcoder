from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.baseClass import baseClass
from cadcoder.containertools import get_LCS_by_prefix
from cadcoder.objtools import update_obj_prop_jsonDict
from cadcoder.subelementtools import update_objs_seName, update_doc_seName, get_seName_by_posName

class npt_straight_bushing(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, b_OD_shrink_spec='0.02 in', b_male_height_spec='0.5 in', b_nominalOD='`3/4', horizontalScale=1, prism_polygon_height_spec='0.2 in', prism_polygon_sides=6, s_effective_height_spec='0.45 in', s_holeDiaExpansion_spec='0.03 in', s_pitch_spec='0.05 in', s_radius_spec='0.25 in', verticalScale=1,  ):
        self.b_OD_shrink_spec = b_OD_shrink_spec
        self.b_male_height_spec = b_male_height_spec
        self.b_nominalOD = b_nominalOD
        self.horizontalScale = horizontalScale
        self.prism_polygon_height_spec = prism_polygon_height_spec
        self.prism_polygon_sides = prism_polygon_sides
        self.s_effective_height_spec = s_effective_height_spec
        self.s_holeDiaExpansion_spec = s_holeDiaExpansion_spec
        self.s_pitch_spec = s_pitch_spec
        self.s_radius_spec = s_radius_spec
        self.verticalScale = verticalScale
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        from parts.npt_m import npt_m
        b_npt_m_instance = npt_m('b_npt_m_instance', doc, objPrefix=self.objPrefix + 'b_npt_m_', useLabel=True, importer=self, OD_shrink_spec='0.02 in', horizontalScale=1, male_height_spec='0.5 in', nominalOD='`3/4', verticalScale=1, )
        self.b_npt_m_instance = b_npt_m_instance # expose as instance variable
        self.update_imports(b_npt_m_instance) # update import info for the instance
        b_npt_m_instance.body.Placement = Placement(Vector(0.0000, 0.0000, 0.0000), Rotation(1.0000, 0.0000, 0.0000, 0.0000))  # adjust imported object
        b_npt_m_instance.common_boolean.Visibility = False  # adjust imported object
        from parts.prism_polygon import prism_polygon
        prism_polygon_instance = prism_polygon('prism_polygon_instance', doc, objPrefix=self.objPrefix + 'prism_polygon_', useLabel=True, importer=self, horizontalScale=1, prism_polygon_height_spec='0.2 in', prism_polygon_radius_spec='0.6408587988004846 in', prism_polygon_sides=6, verticalScale=1, )
        self.prism_polygon_instance = prism_polygon_instance # expose as instance variable
        self.update_imports(prism_polygon_instance) # update import info for the instance
        prism_polygon_instance.body.Placement = Placement(Vector(0.0000, 0.0000, -5.0800), Rotation(0.0000, 0.0000, 0.0000, 1.0000))  # adjust imported object
        from parts.straight_m import straight_m
        s_straight_m_instance = straight_m('s_straight_m_instance', doc, objPrefix=self.objPrefix + 's_straight_m_', useLabel=True, importer=self, height_spec='0.8 in', holeDiaExpansion_spec='0.03 in', horizontalScale=1, pitch_spec='0.05 in', radius_spec='0.25 in', verticalScale=1, )
        self.s_straight_m_instance = s_straight_m_instance # expose as instance variable
        self.update_imports(s_straight_m_instance) # update import info for the instance
        s_straight_m_instance.body.Placement = Placement(Vector(0.0000, 0.0000, -5.0800), Rotation(0.0000, 0.0000, 0.0000, 1.0000))  # adjust imported object
        
        # add objects and add static value to objects' properties based on object dependencies
        bottom_cutter = doc.addObject('PartDesign::Body', self.addPrefix('bottom_cutter') )
        bottom_cutter.Label = self.addPrefix('bottom_cutter')
        self.bottom_cutter = bottom_cutter
        self.post_new_obj(bottom_cutter)
        bottom_cutter_Origin = get_LCS_by_prefix(doc, bottom_cutter, 'Origin')
        bottom_cutter_X_Axis = get_LCS_by_prefix(doc, bottom_cutter, 'X_Axis')
        bottom_cutter_Y_Axis = get_LCS_by_prefix(doc, bottom_cutter, 'Y_Axis')
        bottom_cutter_Z_Axis = get_LCS_by_prefix(doc, bottom_cutter, 'Z_Axis')
        bottom_cutter_XY_Plane = get_LCS_by_prefix(doc, bottom_cutter, 'XY_Plane')
        bottom_cutter_XZ_Plane = get_LCS_by_prefix(doc, bottom_cutter, 'XZ_Plane')
        bottom_cutter_YZ_Plane = get_LCS_by_prefix(doc, bottom_cutter, 'YZ_Plane')
        self.bottom_cutter_Origin = bottom_cutter_Origin
        self.bottom_cutter_X_Axis = bottom_cutter_X_Axis
        self.bottom_cutter_Y_Axis = bottom_cutter_Y_Axis
        self.bottom_cutter_Z_Axis = bottom_cutter_Z_Axis
        self.bottom_cutter_XY_Plane = bottom_cutter_XY_Plane
        self.bottom_cutter_XZ_Plane = bottom_cutter_XZ_Plane
        self.bottom_cutter_YZ_Plane = bottom_cutter_YZ_Plane
        self.post_new_obj(bottom_cutter_Origin)
        self.post_new_obj(bottom_cutter_X_Axis)
        self.post_new_obj(bottom_cutter_Y_Axis)
        self.post_new_obj(bottom_cutter_Z_Axis)
        self.post_new_obj(bottom_cutter_XY_Plane)
        self.post_new_obj(bottom_cutter_XZ_Plane)
        self.post_new_obj(bottom_cutter_YZ_Plane)
        bottom_cutter.Placement = Placement(Vector(0.0000, 0.0000, 6.3500), Rotation(0.0000, 0.0000, 0.0000, 1.0000))
        bottom_cutter.recompute()  # recompute after adding object
        
        callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('callsheet') )
        callsheet.Label = self.addPrefix('callsheet')
        self.callsheet = callsheet
        self.post_new_obj(callsheet)
        callsheet.set('A1', 'variableName')
        callsheet.set('A10', 'verticalScale')
        callsheet.set('A11', 's_cutter_height_spec')
        callsheet.set('A12', 's_effective_height_spec')
        callsheet.set('A13', 's_pitch_spec')
        callsheet.set('A14', 's_radius_spec')
        callsheet.set('A15', 's_holeDiaExpansion_spec')
        callsheet.set('A16', 'bottom_cone_cutter_s_radus_spec')
        callsheet.set('A17', 'bottom_cone_cutter_s_radus')
        callsheet.set('A18', 'bottom_cone_cutter_b_radus_spec')
        callsheet.set('A19', 'bottom_cone_cutter_b_radus')
        callsheet.set('A2', 'b_OD_shrink_spec')
        callsheet.set('A20', 'bottom_cone_cutter_height_spec')
        callsheet.set('A21', 'bottom_cone_cutter_height')
        callsheet.set('A3', 'b_male_height_spec')
        callsheet.set('A4', 'b_male_height')
        callsheet.set('A5', 'b_nominalOD')
        callsheet.set('A6', 'horizontalScale')
        callsheet.set('A7', 'prism_polygon_height_spec')
        callsheet.set('A8', 'prism_polygon_height')
        callsheet.set('A9', 'prism_polygon_sides')
        callsheet.set('B1', 'value')
        callsheet.set('B10', '1')
        callsheet.setAlias('B10', 'verticalScale')
        callsheet.set('B11', '=0.8 in')
        callsheet.setAlias('B11', 's_cutter_height_spec')
        callsheet.set('B12', '=0.45 in')
        callsheet.setAlias('B12', 's_effective_height_spec')
        callsheet.set('B13', '=0.05 in')
        callsheet.setAlias('B13', 's_pitch_spec')
        callsheet.set('B14', '=0.25 in')
        callsheet.setAlias('B14', 's_radius_spec')
        callsheet.set('B15', '=0.03 in')
        callsheet.setAlias('B15', 's_holeDiaExpansion_spec')
        callsheet.set('B16', '=0.27 in')
        callsheet.setAlias('B16', 'bottom_cone_cutter_s_radus_spec')
        callsheet.set('B17', '=0.27 in')
        callsheet.setAlias('B17', 'bottom_cone_cutter_s_radus')
        callsheet.set('B18', '=0.35100000000000003 in')
        callsheet.setAlias('B18', 'bottom_cone_cutter_b_radus_spec')
        callsheet.set('B19', '=0.35100000000000003 in')
        callsheet.setAlias('B19', 'bottom_cone_cutter_b_radus')
        callsheet.set('B2', '=0.02 in')
        callsheet.setAlias('B2', 'b_OD_shrink_spec')
        callsheet.set('B20', '=0.25000000000000006 in')
        callsheet.setAlias('B20', 'bottom_cone_cutter_height_spec')
        callsheet.set('B21', '=0.25000000000000006 in')
        callsheet.setAlias('B21', 'bottom_cone_cutter_height')
        callsheet.set('B3', '=0.5 in')
        callsheet.setAlias('B3', 'b_male_height_spec')
        callsheet.set('B4', '=0.5 in')
        callsheet.setAlias('B4', 'b_male_height')
        callsheet.set('B5', '`3/4')
        callsheet.setAlias('B5', 'b_nominalOD')
        callsheet.set('B6', '1')
        callsheet.setAlias('B6', 'horizontalScale')
        callsheet.set('B7', '=0.2 in')
        callsheet.setAlias('B7', 'prism_polygon_height_spec')
        callsheet.set('B8', '=0.2 in')
        callsheet.setAlias('B8', 'prism_polygon_height')
        callsheet.set('B9', '6')
        callsheet.setAlias('B9', 'prism_polygon_sides')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C10', 'Y')
        callsheet.set('C11', 'N')
        callsheet.set('C12', 'Y')
        callsheet.set('C13', 'Y')
        callsheet.set('C14', 'Y')
        callsheet.set('C15', 'Y')
        callsheet.set('C16', 'N')
        callsheet.set('C17', 'N')
        callsheet.set('C18', 'N')
        callsheet.set('C19', 'N')
        callsheet.set('C2', 'Y')
        callsheet.set('C20', 'N')
        callsheet.set('C21', 'N')
        callsheet.set('C3', 'Y')
        callsheet.set('C4', 'N')
        callsheet.set('C5', 'Y')
        callsheet.set('C6', 'Y')
        callsheet.set('C7', 'Y')
        callsheet.set('C8', 'N')
        callsheet.set('C9', 'Y')
        callsheet.set('D1', 'comment')
        callsheet.set('D10', ' BASF 17-4 z scale 1.2610')
        callsheet.set('D11', 'thread cutter length')
        callsheet.set('D12', 'thread in-use length')
        callsheet.set('D2', 'shrink OD to easy fitting')
        callsheet.set('D3', '0')
        callsheet.set('D5', 'from npt_m_spec.nominalOD')
        callsheet.set('D6', ' BASF 17-4 xy scale 1.1982')
        callsheet.set('D7', ' pad height')
        callsheet.set('D9', ' number of sides of a polygon')
        callsheet.Visibility = False
        callsheet.ViewObject.Visibility = False
        callsheet.recompute()  # recompute after adding object
        
        bottom_cone = doc.addObject('PartDesign::AdditiveCone', self.addPrefix('bottom_cone') )
        bottom_cone.Label = self.addPrefix('bottom_cone')
        self.bottom_cone = bottom_cone
        self.post_new_obj(bottom_cone)
        self.container_append_object(bottom_cutter, bottom_cone)
        bottom_cone.AttachmentSupport = (callsheet, (''))
        callsheet.Visibility = False  # hide base object
        bottom_cone.Height = 6.350000000000001
        bottom_cone.Radius1 = 6.858
        bottom_cone.Radius2 = 8.9154
        bottom_cone.recompute()  # recompute after adding object
        
        callsheet2 = doc.addObject('Spreadsheet::Sheet', self.addPrefix('callsheet2') )
        callsheet2.Label = self.addPrefix('callsheet2')
        self.callsheet2 = callsheet2
        self.post_new_obj(callsheet2)
        callsheet2.set('A1', 'variableName')
        callsheet2.set('A2', 'prism_polygon_radius_spec')
        callsheet2.set('B1', 'value')
        callsheet2.set('B2', '=0.6408587988004846 in')
        callsheet2.setAlias('B2', 'prism_polygon_radius_spec')
        callsheet2.set('C1', 'isCallParam')
        callsheet2.set('C2', 'N')
        callsheet2.set('D1', 'comment')
        callsheet2.recompute()  # recompute after adding object
        
        boolean_add_prism_polygon = doc.addObject('PartDesign::Boolean', self.addPrefix('boolean_add_prism_polygon') )
        boolean_add_prism_polygon.Label = self.addPrefix('boolean_add_prism_polygon')
        self.boolean_add_prism_polygon = boolean_add_prism_polygon
        self.post_new_obj(boolean_add_prism_polygon)
        self.container_append_object(b_npt_m_instance.body, boolean_add_prism_polygon)
        boolean_add_prism_polygon.BaseFeature = b_npt_m_instance.common_boolean
        boolean_add_prism_polygon.Group = [prism_polygon_instance.body]
        boolean_add_prism_polygon.UsePlacement = True
        boolean_add_prism_polygon.Visibility = False
        boolean_add_prism_polygon.ViewObject.Visibility = False
        doc.recompute() # recompute whole document for PartDesign::Boolean
        
        boolean_cut_s_straight_m = doc.addObject('PartDesign::Boolean', self.addPrefix('boolean_cut_s_straight_m') )
        boolean_cut_s_straight_m.Label = self.addPrefix('boolean_cut_s_straight_m')
        self.boolean_cut_s_straight_m = boolean_cut_s_straight_m
        self.post_new_obj(boolean_cut_s_straight_m)
        self.container_append_object(b_npt_m_instance.body, boolean_cut_s_straight_m)
        boolean_cut_s_straight_m.BaseFeature = boolean_add_prism_polygon
        boolean_cut_s_straight_m.Group = [s_straight_m_instance.body]
        boolean_cut_s_straight_m.Type = 'Cut'
        boolean_cut_s_straight_m.UsePlacement = True
        boolean_cut_s_straight_m.Visibility = False
        boolean_cut_s_straight_m.ViewObject.Visibility = False
        doc.recompute() # recompute whole document for PartDesign::Boolean
        
        bottom_boolean = doc.addObject('PartDesign::Boolean', self.addPrefix('bottom_boolean') )
        bottom_boolean.Label = self.addPrefix('bottom_boolean')
        self.bottom_boolean = bottom_boolean
        self.post_new_obj(bottom_boolean)
        self.container_append_object(b_npt_m_instance.body, bottom_boolean)
        bottom_boolean.BaseFeature = boolean_cut_s_straight_m
        bottom_boolean.Group = [bottom_cutter]
        bottom_boolean.Type = 'Cut'
        bottom_boolean.UsePlacement = True
        doc.recompute() # recompute whole document for PartDesign::Boolean
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        prism_polygon_instance.callsheet.set(prism_polygon_instance.callsheet.getCellFromAlias('prism_polygon_sides'), f"=<<{self.addPrefix('callsheet')}>>.prism_polygon_sides")
        prism_polygon_instance.callsheet.set(prism_polygon_instance.callsheet.getCellFromAlias('horizontalScale'), f"=<<{self.addPrefix('callsheet')}>>.horizontalScale")
        prism_polygon_instance.callsheet.set(prism_polygon_instance.callsheet.getCellFromAlias('verticalScale'), f"=<<{self.addPrefix('callsheet')}>>.verticalScale")
        prism_polygon_instance.callsheet.set(prism_polygon_instance.callsheet.getCellFromAlias('prism_polygon_height_spec'), f"=<<{self.addPrefix('callsheet')}>>.prism_polygon_height_spec")
        s_straight_m_instance.body.setExpression('.Placement.Base.z', f"-<<{self.addPrefix('callsheet')}>>.prism_polygon_height_spec * <<{self.addPrefix('callsheet')}>>.verticalScale")
        s_straight_m_instance.callsheet.set(s_straight_m_instance.callsheet.getCellFromAlias('holeDiaExpansion_spec'), f"=<<{self.addPrefix('callsheet')}>>.s_holeDiaExpansion_spec")
        s_straight_m_instance.callsheet.set(s_straight_m_instance.callsheet.getCellFromAlias('horizontalScale'), f"=<<{self.addPrefix('callsheet')}>>.horizontalScale")
        s_straight_m_instance.callsheet.set(s_straight_m_instance.callsheet.getCellFromAlias('verticalScale'), f"=<<{self.addPrefix('callsheet')}>>.verticalScale")
        s_straight_m_instance.callsheet.set(s_straight_m_instance.callsheet.getCellFromAlias('radius_spec'), f"=<<{self.addPrefix('callsheet')}>>.s_radius_spec")
        s_straight_m_instance.callsheet.set(s_straight_m_instance.callsheet.getCellFromAlias('pitch_spec'), f"=<<{self.addPrefix('callsheet')}>>.s_pitch_spec")
        b_npt_m_instance.callsheet.set(b_npt_m_instance.callsheet.getCellFromAlias('OD_shrink_spec'), f"=<<{self.addPrefix('callsheet')}>>.b_OD_shrink_spec")
        b_npt_m_instance.callsheet.set(b_npt_m_instance.callsheet.getCellFromAlias('male_height_spec'), f"=<<{self.addPrefix('callsheet')}>>.b_male_height_spec")
        b_npt_m_instance.callsheet.set(b_npt_m_instance.callsheet.getCellFromAlias('nominalOD'), f"=<<{self.addPrefix('callsheet')}>>.b_nominalOD")
        b_npt_m_instance.callsheet.set(b_npt_m_instance.callsheet.getCellFromAlias('horizontalScale'), f"=<<{self.addPrefix('callsheet')}>>.horizontalScale")
        b_npt_m_instance.callsheet.set(b_npt_m_instance.callsheet.getCellFromAlias('verticalScale'), f"=<<{self.addPrefix('callsheet')}>>.verticalScale")
        callsheet.set(callsheet.getCellFromAlias("s_cutter_height_spec"), f"=b_male_height_spec + prism_polygon_height_spec + 0.1 in")
        callsheet.set(callsheet.getCellFromAlias("bottom_cone_cutter_s_radus_spec"), f"=s_radius_spec + 0.02 in")
        callsheet.set(callsheet.getCellFromAlias("bottom_cone_cutter_height_spec"), f"=b_male_height_spec + prism_polygon_height_spec - s_effective_height_spec")
        callsheet.set(callsheet.getCellFromAlias("b_male_height"), f"=b_male_height_spec * verticalScale")
        callsheet.set(callsheet.getCellFromAlias("prism_polygon_height"), f"=prism_polygon_height_spec * verticalScale")
        prism_polygon_instance.body.setExpression('.Placement.Base.z', f"-<<{self.addPrefix('callsheet')}>>.prism_polygon_height")
        s_straight_m_instance.callsheet.set(s_straight_m_instance.callsheet.getCellFromAlias('height_spec'), f"=<<{self.addPrefix('callsheet')}>>.s_cutter_height_spec")
        bottom_cone.setExpression("Height", f"<<{self.addPrefix('callsheet')}>>.bottom_cone_cutter_height_spec")
        callsheet.set(callsheet.getCellFromAlias("bottom_cone_cutter_s_radus"), f"=bottom_cone_cutter_s_radus_spec * horizontalScale")
        callsheet.set(callsheet.getCellFromAlias("bottom_cone_cutter_b_radus_spec"), f"=bottom_cone_cutter_s_radus_spec * 1.3")
        callsheet.set(callsheet.getCellFromAlias("bottom_cone_cutter_height"), f"=bottom_cone_cutter_height_spec * verticalScale")
        bottom_cone.setExpression("Radius1", f"<<{self.addPrefix('callsheet')}>>.bottom_cone_cutter_s_radus")
        bottom_cutter.setExpression(".Placement.Base.z", f"<<{self.addPrefix('callsheet')}>>.b_male_height - <<{self.addPrefix('callsheet')}>>.bottom_cone_cutter_height")
        callsheet.set(callsheet.getCellFromAlias("bottom_cone_cutter_b_radus"), f"=bottom_cone_cutter_b_radus_spec * horizontalScale")
        callsheet2.set(callsheet2.getCellFromAlias("prism_polygon_radius_spec"), f"=(<<{self.addPrefix('b_npt_m_callsheet')}>>.realOD / 2 + 0.04 in) / cos(360 / 2 / <<{self.addPrefix('callsheet')}>>.prism_polygon_sides)")
        prism_polygon_instance.callsheet.set(prism_polygon_instance.callsheet.getCellFromAlias('prism_polygon_radius_spec'), f"=<<{self.addPrefix('callsheet2')}>>.prism_polygon_radius_spec")
        bottom_cone.setExpression("Radius2", f"<<{self.addPrefix('callsheet')}>>.bottom_cone_cutter_b_radus")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # now we have rebuilt the original npt_straight_bushing doc. Now we apply dynmic call parameters
        print("there can be temporary errors when we applying dynamic call parameters that change original npt_straight_bushing's shape.")
        print("ignore temporary errors, if any, below.")
        callsheet.set(callsheet.getCellFromAlias('verticalScale'), f'{self.verticalScale}')
        callsheet.set(callsheet.getCellFromAlias('s_effective_height_spec'), f'={self.s_effective_height_spec}')
        callsheet.set(callsheet.getCellFromAlias('s_pitch_spec'), f'={self.s_pitch_spec}')
        callsheet.set(callsheet.getCellFromAlias('s_radius_spec'), f'={self.s_radius_spec}')
        callsheet.set(callsheet.getCellFromAlias('s_holeDiaExpansion_spec'), f'={self.s_holeDiaExpansion_spec}')
        callsheet.set(callsheet.getCellFromAlias('b_OD_shrink_spec'), f'={self.b_OD_shrink_spec}')
        callsheet.set(callsheet.getCellFromAlias('b_male_height_spec'), f'={self.b_male_height_spec}')
        callsheet.set(callsheet.getCellFromAlias('b_nominalOD'), f'{self.b_nominalOD}')
        callsheet.set(callsheet.getCellFromAlias('horizontalScale'), f'{self.horizontalScale}')
        callsheet.set(callsheet.getCellFromAlias('prism_polygon_height_spec'), f'={self.prism_polygon_height_spec}')
        callsheet.set(callsheet.getCellFromAlias('prism_polygon_sides'), f'{self.prism_polygon_sides}')
        doc.recompute()
        update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.
        print("ignore temporary errors, if any, above.")
        
        self.update_callsheet()


def main():
    # main_part1
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of npt_straight_bushing
    myInstance = npt_straight_bushing("myInstance", doc, objPrefix="", useLabel=True, importer=None, b_OD_shrink_spec='0.02 in', b_male_height_spec='0.5 in', b_nominalOD='`3/4', horizontalScale=1, prism_polygon_height_spec='0.2 in', prism_polygon_sides=6, s_effective_height_spec='0.45 in', s_holeDiaExpansion_spec='0.03 in', s_pitch_spec='0.05 in', s_radius_spec='0.25 in', verticalScale=1, )
    
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
