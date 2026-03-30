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
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, b_diaExpansion='-0.02 in', b_male_height='0.5 in', b_nominalOD='`3/4', horizontalScale=1, prism_polygon_height='0.2 in', prism_polygon_sides=6, s_effective_height='0.45 in', s_holeDiaExpansion='0.03 in', s_pitch='0.05 in', s_radius='0.25 in', verticalScale=1,  ):
        self.b_diaExpansion = b_diaExpansion
        self.b_male_height = b_male_height
        self.b_nominalOD = b_nominalOD
        self.horizontalScale = horizontalScale
        self.prism_polygon_height = prism_polygon_height
        self.prism_polygon_sides = prism_polygon_sides
        self.s_effective_height = s_effective_height
        self.s_holeDiaExpansion = s_holeDiaExpansion
        self.s_pitch = s_pitch
        self.s_radius = s_radius
        self.verticalScale = verticalScale
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        from parts.npt_m import npt_m
        b_npt_m_instance = npt_m('b_npt_m_instance', doc, objPrefix=self.objPrefix + 'b_npt_m_', useLabel=True, importer=self, diaExpansion='-0.02 in', male_height='0.5 in', nominalOD='`3/4', )
        self.b_npt_m_instance = b_npt_m_instance # expose as instance variable
        self.update_imports(b_npt_m_instance) # update import info for the instance
        b_npt_m_instance.common_boolean.Visibility = False  # adjust imported object
        from parts.prism_polygon import prism_polygon
        prism_polygon_instance = prism_polygon('prism_polygon_instance', doc, objPrefix=self.objPrefix + 'prism_polygon_', useLabel=True, importer=self, height='0.2 in', radius='0.6146707772653145 in', sides=6, )
        self.prism_polygon_instance = prism_polygon_instance # expose as instance variable
        self.update_imports(prism_polygon_instance) # update import info for the instance
        prism_polygon_instance.body.Placement = Placement(Vector(0.0000, 0.0000, -5.0800), Rotation(0.0000, 0.0000, 0.0000, 1.0000))  # adjust imported object
        from parts.straight_m import straight_m
        s_straight_m_instance = straight_m('s_straight_m_instance', doc, objPrefix=self.objPrefix + 's_straight_m_', useLabel=True, importer=self, diaExpansion='0.03 in', height='0.7000000000000001 in', pitch='0.05 in', radius='0.25 in', )
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
        callsheet.set('A10', 's_effective_height')
        callsheet.set('A11', 's_cutter_placement_z')
        callsheet.set('A12', 's_pitch')
        callsheet.set('A13', 's_radius')
        callsheet.set('A14', 's_holeDiaExpansion')
        callsheet.set('A15', 'bottom_cone_cutter_s_radius')
        callsheet.set('A16', 'bottom_cone_cutter_height')
        callsheet.set('A2', 'b_diaExpansion')
        callsheet.set('A3', 'b_male_height')
        callsheet.set('A4', 'b_nominalOD')
        callsheet.set('A5', 'horizontalScale')
        callsheet.set('A6', 'prism_polygon_height')
        callsheet.set('A7', 'prism_polygon_sides')
        callsheet.set('A8', 'verticalScale')
        callsheet.set('A9', 's_cutter_height')
        callsheet.set('B1', 'value')
        callsheet.set('B10', '=0.45 in')
        callsheet.setAlias('B10', 's_effective_height')
        callsheet.set('B11', '=-0.2 in')
        callsheet.setAlias('B11', 's_cutter_placement_z')
        callsheet.set('B12', '=0.05 in')
        callsheet.setAlias('B12', 's_pitch')
        callsheet.set('B13', '=0.25 in')
        callsheet.setAlias('B13', 's_radius')
        callsheet.set('B14', '=0.03 in')
        callsheet.setAlias('B14', 's_holeDiaExpansion')
        callsheet.set('B15', '=0.27 in')
        callsheet.setAlias('B15', 'bottom_cone_cutter_s_radius')
        callsheet.set('B16', '=0.25000000000000006 in')
        callsheet.setAlias('B16', 'bottom_cone_cutter_height')
        callsheet.set('B2', '=-0.02 in')
        callsheet.setAlias('B2', 'b_diaExpansion')
        callsheet.set('B3', '=0.5 in')
        callsheet.setAlias('B3', 'b_male_height')
        callsheet.set('B4', '`3/4')
        callsheet.setAlias('B4', 'b_nominalOD')
        callsheet.set('B5', '1')
        callsheet.setAlias('B5', 'horizontalScale')
        callsheet.set('B6', '=0.2 in')
        callsheet.setAlias('B6', 'prism_polygon_height')
        callsheet.set('B7', '6')
        callsheet.setAlias('B7', 'prism_polygon_sides')
        callsheet.set('B8', '1')
        callsheet.setAlias('B8', 'verticalScale')
        callsheet.set('B9', '=0.7000000000000001 in')
        callsheet.setAlias('B9', 's_cutter_height')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C10', 'Y')
        callsheet.set('C11', 'N')
        callsheet.set('C12', 'Y')
        callsheet.set('C13', 'Y')
        callsheet.set('C14', 'Y')
        callsheet.set('C15', 'N')
        callsheet.set('C16', 'N')
        callsheet.set('C2', 'Y')
        callsheet.set('C3', 'Y')
        callsheet.set('C4', 'Y')
        callsheet.set('C5', 'Y')
        callsheet.set('C6', 'Y')
        callsheet.set('C7', 'Y')
        callsheet.set('C8', 'Y')
        callsheet.set('C9', 'N')
        callsheet.set('D1', 'comment')
        callsheet.set('D10', 'thread in-use length')
        callsheet.set('D2', 'shrink OD to easy fitting')
        callsheet.set('D4', 'from npt_m_spec.nominalOD')
        callsheet.set('D5', 'del')
        callsheet.set('D7', ' number of sides of a polygon')
        callsheet.set('D8', ' BASF 17-4 z scale 1.2610')
        callsheet.set('D9', 'thread cutter length')
        callsheet.Visibility = False
        callsheet.ViewObject.Visibility = False
        callsheet.recompute()  # recompute after adding object
        
        callsheet2 = doc.addObject('Spreadsheet::Sheet', self.addPrefix('callsheet2') )
        callsheet2.Label = self.addPrefix('callsheet2')
        self.callsheet2 = callsheet2
        self.post_new_obj(callsheet2)
        callsheet2.set('A1', 'variableName')
        callsheet2.set('A2', 'prism_polygon_radius')
        callsheet2.set('A3', 'bottom_cone_cutter_b_radius')
        callsheet2.set('B1', 'value')
        callsheet2.set('B2', '=0.6146707772653145 in')
        callsheet2.setAlias('B2', 'prism_polygon_radius')
        callsheet2.set('B3', '=0.3449999999999999 in')
        callsheet2.setAlias('B3', 'bottom_cone_cutter_b_radius')
        callsheet2.set('C1', 'isCallParam')
        callsheet2.set('C2', 'N')
        callsheet2.set('C3', 'N')
        callsheet2.set('D1', 'comment')
        callsheet2.recompute()  # recompute after adding object
        
        bottom_cone = doc.addObject('PartDesign::AdditiveCone', self.addPrefix('bottom_cone') )
        bottom_cone.Label = self.addPrefix('bottom_cone')
        self.bottom_cone = bottom_cone
        self.post_new_obj(bottom_cone)
        self.container_append_object(bottom_cutter, bottom_cone)
        bottom_cone.AttachmentSupport = (callsheet, (''))
        callsheet.Visibility = False  # hide base object
        bottom_cone.Height = 6.350000000000001
        bottom_cone.Radius1 = 6.858
        bottom_cone.Radius2 = 8.762999999999998
        bottom_cone.recompute()  # recompute after adding object
        
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
        prism_polygon_instance.callsheet.set(prism_polygon_instance.callsheet.getCellFromAlias('sides'), f"=<<{self.addPrefix('callsheet')}>>.prism_polygon_sides")
        prism_polygon_instance.callsheet.set(prism_polygon_instance.callsheet.getCellFromAlias('height'), f"=<<{self.addPrefix('callsheet')}>>.prism_polygon_height")
        s_straight_m_instance.callsheet.set(s_straight_m_instance.callsheet.getCellFromAlias('radius'), f"=<<{self.addPrefix('callsheet')}>>.s_radius")
        s_straight_m_instance.callsheet.set(s_straight_m_instance.callsheet.getCellFromAlias('pitch'), f"=<<{self.addPrefix('callsheet')}>>.s_pitch")
        s_straight_m_instance.callsheet.set(s_straight_m_instance.callsheet.getCellFromAlias('diaExpansion'), f"=<<{self.addPrefix('callsheet')}>>.s_holeDiaExpansion")
        b_npt_m_instance.callsheet.set(b_npt_m_instance.callsheet.getCellFromAlias('nominalOD'), f"=<<{self.addPrefix('callsheet')}>>.b_nominalOD")
        b_npt_m_instance.callsheet.set(b_npt_m_instance.callsheet.getCellFromAlias('diaExpansion'), f"=<<{self.addPrefix('callsheet')}>>.b_diaExpansion")
        b_npt_m_instance.callsheet.set(b_npt_m_instance.callsheet.getCellFromAlias('male_height'), f"=<<{self.addPrefix('callsheet')}>>.b_male_height")
        callsheet.set(callsheet.getCellFromAlias("s_cutter_placement_z"), f"=-prism_polygon_height")
        callsheet.set(callsheet.getCellFromAlias("bottom_cone_cutter_s_radius"), f"=s_radius + 0.02 in")
        callsheet.set(callsheet.getCellFromAlias("s_cutter_height"), f"=b_male_height + prism_polygon_height")
        s_straight_m_instance.body.setExpression('.Placement.Base.z', f"<<{self.addPrefix('callsheet')}>>.s_cutter_placement_z")
        s_straight_m_instance.callsheet.set(s_straight_m_instance.callsheet.getCellFromAlias('height'), f"=<<{self.addPrefix('callsheet')}>>.s_cutter_height")
        bottom_cone.setExpression("Radius1", f"<<{self.addPrefix('callsheet')}>>.bottom_cone_cutter_s_radius")
        callsheet.set(callsheet.getCellFromAlias("bottom_cone_cutter_height"), f"=s_cutter_height - s_effective_height")
        callsheet2.set(callsheet2.getCellFromAlias("prism_polygon_radius"), f"=<<{self.addPrefix('b_npt_m_callsheet')}>>.realOD / 2 / cos(360 / <<{self.addPrefix('callsheet')}>>.prism_polygon_sides / 2) + 0.02 in")
        callsheet2.set(callsheet2.getCellFromAlias("bottom_cone_cutter_b_radius"), f"=<<{self.addPrefix('b_npt_m_callsheet')}>>.realOD / 2 - 0.17 in")
        prism_polygon_instance.callsheet.set(prism_polygon_instance.callsheet.getCellFromAlias('radius'), f"=<<{self.addPrefix('callsheet2')}>>.prism_polygon_radius")
        bottom_cone.setExpression("Height", f"<<{self.addPrefix('callsheet')}>>.bottom_cone_cutter_height")
        bottom_cone.setExpression("Radius2", f"<<{self.addPrefix('callsheet2')}>>.bottom_cone_cutter_b_radius")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # now we have rebuilt the original npt_straight_bushing doc. Now we apply dynmic call parameters
        print("there can be temporary errors when we applying dynamic call parameters that change original npt_straight_bushing's shape.")
        print("ignore temporary errors, if any, below.")
        callsheet.set(callsheet.getCellFromAlias('s_effective_height'), f'={self.s_effective_height}')
        callsheet.set(callsheet.getCellFromAlias('s_pitch'), f'={self.s_pitch}')
        callsheet.set(callsheet.getCellFromAlias('s_radius'), f'={self.s_radius}')
        callsheet.set(callsheet.getCellFromAlias('s_holeDiaExpansion'), f'={self.s_holeDiaExpansion}')
        callsheet.set(callsheet.getCellFromAlias('b_diaExpansion'), f'={self.b_diaExpansion}')
        callsheet.set(callsheet.getCellFromAlias('b_male_height'), f'={self.b_male_height}')
        callsheet.set(callsheet.getCellFromAlias('b_nominalOD'), f'{self.b_nominalOD}')
        callsheet.set(callsheet.getCellFromAlias('horizontalScale'), f'{self.horizontalScale}')
        callsheet.set(callsheet.getCellFromAlias('prism_polygon_height'), f'={self.prism_polygon_height}')
        callsheet.set(callsheet.getCellFromAlias('prism_polygon_sides'), f'{self.prism_polygon_sides}')
        callsheet.set(callsheet.getCellFromAlias('verticalScale'), f'{self.verticalScale}')
        doc.recompute()
        update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.
        print("ignore temporary errors, if any, above.")
        
        self.update_callsheet()


def main():
    # main_part1
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of npt_straight_bushing
    myInstance = npt_straight_bushing("myInstance", doc, objPrefix="", useLabel=True, importer=None, b_diaExpansion='-0.02 in', b_male_height='0.5 in', b_nominalOD='`3/4', horizontalScale=1, prism_polygon_height='0.2 in', prism_polygon_sides=6, s_effective_height='0.45 in', s_holeDiaExpansion='0.03 in', s_pitch='0.05 in', s_radius='0.25 in', verticalScale=1, )
    
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
