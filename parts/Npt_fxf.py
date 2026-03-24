from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.baseClass import baseClass
from cadcoder.containertools import get_LCS_by_prefix
from cadcoder.objtools import update_obj_prop_jsonDict
from cadcoder.subelementtools import update_objs_seName, update_doc_seName, get_seName_by_posName

class npt_fxf(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, b_npt_f_height_spec='0.5 in', b_npt_f_nominalID='`2', b_npt_f_wall_spec='0.08 in', base_plate_thick_spec='0.13 in', holeDiaExpansion_spec='0.03 in', horizontalScale=1.1982, s_npt_f_height_spec='0.5 in', s_npt_f_nominalID='`3/4', s_npt_f_wall_spec='0.08 in', verticalScale=1.261,  ):
        self.b_npt_f_height_spec = b_npt_f_height_spec
        self.b_npt_f_nominalID = b_npt_f_nominalID
        self.b_npt_f_wall_spec = b_npt_f_wall_spec
        self.base_plate_thick_spec = base_plate_thick_spec
        self.holeDiaExpansion_spec = holeDiaExpansion_spec
        self.horizontalScale = horizontalScale
        self.s_npt_f_height_spec = s_npt_f_height_spec
        self.s_npt_f_nominalID = s_npt_f_nominalID
        self.s_npt_f_wall_spec = s_npt_f_wall_spec
        self.verticalScale = verticalScale
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        from parts.npt_f import npt_f
        b_npt_f_instance = npt_f('b_npt_f_instance', doc, objPrefix=self.objPrefix + 'b_npt_f_', useLabel=True, importer=self, femaleOD_wall_spec='0.08 in', female_height_spec='0.5 in', holeDiaExpansion_spec='0.03 in', horizontalScale=1.1982, nominalID='`2', verticalScale=1.261, )
        self.b_npt_f_instance = b_npt_f_instance # expose as instance variable
        self.update_imports(b_npt_f_instance) # update import info for the instance
        b_npt_f_instance.body.Placement = Placement(Vector(0.0000, -0.0000, 20.1785), Rotation(1.0000, 0.0000, 0.0000, 0.0000))  # adjust imported object
        from parts.npt_f import npt_f
        s_npt_f_instance = npt_f('s_npt_f_instance', doc, objPrefix=self.objPrefix + 's_npt_f_', useLabel=True, importer=self, femaleOD_wall_spec='0.08 in', female_height_spec='0.5 in', holeDiaExpansion_spec='0.03 in', nominalID='`3/4', verticalScale=1.261, )
        self.s_npt_f_instance = s_npt_f_instance # expose as instance variable
        self.update_imports(s_npt_f_instance) # update import info for the instance
        
        # add objects and add static value to objects' properties based on object dependencies
        base_plate = doc.addObject('PartDesign::Body', self.addPrefix('base_plate') )
        base_plate.Label = self.addPrefix('base_plate')
        self.base_plate = base_plate
        self.post_new_obj(base_plate)
        base_plate_Origin = get_LCS_by_prefix(doc, base_plate, 'Origin')
        base_plate_X_Axis = get_LCS_by_prefix(doc, base_plate, 'X_Axis')
        base_plate_Y_Axis = get_LCS_by_prefix(doc, base_plate, 'Y_Axis')
        base_plate_Z_Axis = get_LCS_by_prefix(doc, base_plate, 'Z_Axis')
        base_plate_XY_Plane = get_LCS_by_prefix(doc, base_plate, 'XY_Plane')
        base_plate_XZ_Plane = get_LCS_by_prefix(doc, base_plate, 'XZ_Plane')
        base_plate_YZ_Plane = get_LCS_by_prefix(doc, base_plate, 'YZ_Plane')
        self.base_plate_Origin = base_plate_Origin
        self.base_plate_X_Axis = base_plate_X_Axis
        self.base_plate_Y_Axis = base_plate_Y_Axis
        self.base_plate_Z_Axis = base_plate_Z_Axis
        self.base_plate_XY_Plane = base_plate_XY_Plane
        self.base_plate_XZ_Plane = base_plate_XZ_Plane
        self.base_plate_YZ_Plane = base_plate_YZ_Plane
        self.post_new_obj(base_plate_Origin)
        self.post_new_obj(base_plate_X_Axis)
        self.post_new_obj(base_plate_Y_Axis)
        self.post_new_obj(base_plate_Z_Axis)
        self.post_new_obj(base_plate_XY_Plane)
        self.post_new_obj(base_plate_XZ_Plane)
        self.post_new_obj(base_plate_YZ_Plane)
        base_plate.recompute()  # recompute after adding object
        
        callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('callsheet') )
        callsheet.Label = self.addPrefix('callsheet')
        self.callsheet = callsheet
        self.post_new_obj(callsheet)
        callsheet.set('A1', 'variableName')
        callsheet.set('A10', 'base_plate_thick_spec')
        callsheet.set('A11', 'base_plate_thick')
        callsheet.set('A12', 'horizontalScale')
        callsheet.set('A13', 'verticalScale')
        callsheet.set('A14', 'holeDiaExpansion_spec')
        callsheet.set('A2', 's_npt_f_nominalID')
        callsheet.set('A3', 'b_npt_f_nominalID')
        callsheet.set('A4', 's_npt_f_wall_spec')
        callsheet.set('A5', 'b_npt_f_wall_spec')
        callsheet.set('A6', 's_npt_f_height_spec')
        callsheet.set('A7', 'b_npt_f_height_spec')
        callsheet.set('A8', 's_npt_f_height')
        callsheet.set('A9', 'b_npt_f_height')
        callsheet.set('B1', 'value')
        callsheet.set('B10', '=0.13 in')
        callsheet.setAlias('B10', 'base_plate_thick_spec')
        callsheet.set('B11', '=0.16393 in')
        callsheet.setAlias('B11', 'base_plate_thick')
        callsheet.set('B12', '1.1982')
        callsheet.setAlias('B12', 'horizontalScale')
        callsheet.set('B13', '1.261')
        callsheet.setAlias('B13', 'verticalScale')
        callsheet.set('B14', '=0.03 in')
        callsheet.setAlias('B14', 'holeDiaExpansion_spec')
        callsheet.set('B2', '`3/4')
        callsheet.setAlias('B2', 's_npt_f_nominalID')
        callsheet.set('B3', '`2')
        callsheet.setAlias('B3', 'b_npt_f_nominalID')
        callsheet.set('B4', '=0.08 in')
        callsheet.setAlias('B4', 's_npt_f_wall_spec')
        callsheet.set('B5', '=0.08 in')
        callsheet.setAlias('B5', 'b_npt_f_wall_spec')
        callsheet.set('B6', '=0.5 in')
        callsheet.setAlias('B6', 's_npt_f_height_spec')
        callsheet.set('B7', '=0.5 in')
        callsheet.setAlias('B7', 'b_npt_f_height_spec')
        callsheet.set('B8', '=0.6305 in')
        callsheet.setAlias('B8', 's_npt_f_height')
        callsheet.set('B9', '=0.6305 in')
        callsheet.setAlias('B9', 'b_npt_f_height')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C10', 'Y')
        callsheet.set('C11', 'N')
        callsheet.set('C12', 'Y')
        callsheet.set('C13', 'Y')
        callsheet.set('C14', 'Y')
        callsheet.set('C2', 'Y')
        callsheet.set('C3', 'Y')
        callsheet.set('C4', 'Y')
        callsheet.set('C5', 'Y')
        callsheet.set('C6', 'Y')
        callsheet.set('C7', 'Y')
        callsheet.set('C8', 'N')
        callsheet.set('C9', 'N')
        callsheet.set('D1', 'comment')
        callsheet.set('D11', 'base_plate_thick_spec * verticalScale')
        callsheet.set('D12', 'BASF 17-4 xy scale 1.1982')
        callsheet.set('D13', 'BASF 17-4 z scale 1.2610')
        callsheet.set('D8', 's_npt_f_height_spec * verticalScale')
        callsheet.recompute()  # recompute after adding object
        
        ketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('ketch') )
        ketch.Label = self.addPrefix('ketch')
        self.ketch = ketch
        self.post_new_obj(ketch)
        self.container_append_object(base_plate, ketch)
        geo0 = ketch.addGeometry(Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 39.0320))
        geo1 = ketch.addGeometry(Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 18.8693))
        ketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 3, -1, 1))
        ketch.addConstraint(Sketcher.Constraint('Coincident', geo1, 3, geo0, 3))
        ketch.addConstraint(Sketcher.Constraint('Diameter', geo0, 78.0639))
        ketch.addConstraint(Sketcher.Constraint('Diameter', geo1, 37.7385))
        ketch.AttacherEngine = 'Engine Plane'
        ketch.AttachmentSupport = (base_plate_XY_Plane, (''))
        base_plate_XY_Plane.Visibility = False  # hide base object
        ketch.MapMode = 'FlatFace'
        ketch.Visibility = False
        ketch.ViewObject.Visibility = False
        ketch.recompute()  # recompute after adding object
        
        pad = doc.addObject('PartDesign::Pad', self.addPrefix('pad') )
        pad.Label = self.addPrefix('pad')
        self.pad = pad
        self.post_new_obj(pad)
        self.container_append_object(base_plate, pad)
        pad.Length = 4.163822
        pad.Profile = (ketch, [''])
        pad.ReferenceAxis = (ketch, ['N_Axis'])
        pad.Visibility = False
        pad.ViewObject.Visibility = False
        pad.recompute()  # recompute after adding object
        
        boolean = doc.addObject('PartDesign::Boolean', self.addPrefix('boolean') )
        boolean.Label = self.addPrefix('boolean')
        self.boolean = boolean
        self.post_new_obj(boolean)
        self.container_append_object(base_plate, boolean)
        boolean.BaseFeature = pad
        boolean.Group = [b_npt_f_instance.body, s_npt_f_instance.body]
        boolean.UsePlacement = True
        doc.recompute() # recompute whole document for PartDesign::Boolean
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        s_npt_f_instance.callsheet.set(s_npt_f_instance.callsheet.getCellFromAlias('holeDiaExpansion_spec'), f"=<<{self.addPrefix('callsheet')}>>.holeDiaExpansion_spec")
        s_npt_f_instance.callsheet.set(s_npt_f_instance.callsheet.getCellFromAlias('nominalID'), f"=<<{self.addPrefix('callsheet')}>>.s_npt_f_nominalID")
        s_npt_f_instance.callsheet.set(s_npt_f_instance.callsheet.getCellFromAlias('verticalScale'), f"=<<{self.addPrefix('callsheet')}>>.verticalScale")
        s_npt_f_instance.callsheet.set(s_npt_f_instance.callsheet.getCellFromAlias('femaleOD_wall_spec'), f"=<<{self.addPrefix('callsheet')}>>.s_npt_f_wall_spec")
        s_npt_f_instance.callsheet.set(s_npt_f_instance.callsheet.getCellFromAlias('female_height_spec'), f"=<<{self.addPrefix('callsheet')}>>.s_npt_f_height_spec")
        b_npt_f_instance.callsheet.set(b_npt_f_instance.callsheet.getCellFromAlias('holeDiaExpansion_spec'), f"=<<{self.addPrefix('callsheet')}>>.holeDiaExpansion_spec")
        b_npt_f_instance.callsheet.set(b_npt_f_instance.callsheet.getCellFromAlias('nominalID'), f"=<<{self.addPrefix('callsheet')}>>.b_npt_f_nominalID")
        b_npt_f_instance.callsheet.set(b_npt_f_instance.callsheet.getCellFromAlias('horizontalScale'), f"=<<{self.addPrefix('callsheet')}>>.horizontalScale")
        b_npt_f_instance.callsheet.set(b_npt_f_instance.callsheet.getCellFromAlias('verticalScale'), f"=<<{self.addPrefix('callsheet')}>>.verticalScale")
        b_npt_f_instance.callsheet.set(b_npt_f_instance.callsheet.getCellFromAlias('femaleOD_wall_spec'), f"=<<{self.addPrefix('callsheet')}>>.b_npt_f_wall_spec")
        b_npt_f_instance.callsheet.set(b_npt_f_instance.callsheet.getCellFromAlias('female_height_spec'), f"=<<{self.addPrefix('callsheet')}>>.b_npt_f_height_spec")
        callsheet.set(callsheet.getCellFromAlias("base_plate_thick"), f"=base_plate_thick_spec * verticalScale")
        callsheet.set(callsheet.getCellFromAlias("s_npt_f_height"), f"=s_npt_f_height_spec * verticalScale")
        callsheet.set(callsheet.getCellFromAlias("b_npt_f_height"), f"=b_npt_f_height_spec * verticalScale")
        pad.setExpression("Length", f"<<{self.addPrefix('callsheet')}>>.base_plate_thick")
        b_npt_f_instance.body.setExpression('.Placement.Base.z', f"<<{self.addPrefix('callsheet')}>>.base_plate_thick + <<{self.addPrefix('callsheet')}>>.b_npt_f_height")
        ketch.setExpression("Constraints[2]", f"<<{self.addPrefix('b_npt_f_callsheet')}>>.femaleOD")
        ketch.setExpression("Constraints[3]", f"<<{self.addPrefix('s_npt_f_callsheet')}>>.femaleOD")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # now we have rebuilt the original npt_fxf doc. Now we apply dynmic call parameters
        print("there can be temporary errors when we applying dynamic call parameters that change original npt_fxf's shape.")
        print("ignore temporary errors, if any, below.")
        callsheet.set(callsheet.getCellFromAlias('base_plate_thick_spec'), f'={self.base_plate_thick_spec}')
        callsheet.set(callsheet.getCellFromAlias('horizontalScale'), f'{self.horizontalScale}')
        callsheet.set(callsheet.getCellFromAlias('verticalScale'), f'{self.verticalScale}')
        callsheet.set(callsheet.getCellFromAlias('holeDiaExpansion_spec'), f'={self.holeDiaExpansion_spec}')
        callsheet.set(callsheet.getCellFromAlias('s_npt_f_nominalID'), f'{self.s_npt_f_nominalID}')
        callsheet.set(callsheet.getCellFromAlias('b_npt_f_nominalID'), f'{self.b_npt_f_nominalID}')
        callsheet.set(callsheet.getCellFromAlias('s_npt_f_wall_spec'), f'={self.s_npt_f_wall_spec}')
        callsheet.set(callsheet.getCellFromAlias('b_npt_f_wall_spec'), f'={self.b_npt_f_wall_spec}')
        callsheet.set(callsheet.getCellFromAlias('s_npt_f_height_spec'), f'={self.s_npt_f_height_spec}')
        callsheet.set(callsheet.getCellFromAlias('b_npt_f_height_spec'), f'={self.b_npt_f_height_spec}')
        doc.recompute()
        update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.
        print("ignore temporary errors, if any, above.")
        
        self.update_callsheet()


def main():
    # main_part1
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of npt_fxf
    myInstance = npt_fxf("myInstance", doc, objPrefix="", useLabel=True, importer=None, b_npt_f_height_spec='0.5 in', b_npt_f_nominalID='`2', b_npt_f_wall_spec='0.08 in', base_plate_thick_spec='0.13 in', holeDiaExpansion_spec='0.03 in', horizontalScale=1.1982, s_npt_f_height_spec='0.5 in', s_npt_f_nominalID='`3/4', s_npt_f_wall_spec='0.08 in', verticalScale=1.261, )
    
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
