from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.baseClass import baseClass
from pdfclib.containertools import get_LCS_by_prefix
from pdfclib.objtools import update_obj_prop_jsonDict

class Npt_fxf(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, b_npt_f_height_spec='1 in', b_npt_f_nominalID='`2', b_npt_f_wall_spec='0.08 in', base_plate_thick_spec='0.2 in', holeDiaExpansion_spec='0.03 in', horizontalScale=1.1982, s_npt_f_height_spec='0.8 in', s_npt_f_nominalID='`3/4', s_npt_f_wall_spec='0.08 in', verticalScale=1.261,  ):
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
        from parts.Npt_f import Npt_f
        b_npt_f_instance = Npt_f('b_npt_f_instance', doc, objPrefix=self.objPrefix + 'b_', useLabel=True, importer=self, holeDiaExpansion_spec='0.03 in', nominalID='`2', horizontalScale=1.1982, verticalScale=1.261, femaleOD_wall_spec='0.08 in', female_height_spec='1.0 in', )
        self.b_npt_f_instance = b_npt_f_instance # expose as instance variable
        self.update_imports(b_npt_f_instance) # update import info for the instance
        
        from parts.Npt_f import Npt_f
        s_npt_f_instance = Npt_f('s_npt_f_instance', doc, objPrefix=self.objPrefix + 's_', useLabel=True, importer=self, holeDiaExpansion_spec='0.03 in', nominalID='`3/4', verticalScale=1.261, femaleOD_wall_spec='0.08 in', female_height_spec='0.8 in', )
        self.s_npt_f_instance = s_npt_f_instance # expose as instance variable
        self.update_imports(s_npt_f_instance) # update import info for the instance
        s_npt_f_instance.npt_f.Placement = Placement(Vector(0.0000, 0.0000, 25.6235), Rotation(1.0000, 0.0000, 0.0000, 0.0000))  # adjust imported object
        
        
        # add objects and add static value to objects' properties based on object dependencies
        npt_fxf_base_plate = doc.addObject('PartDesign::Body', self.addPrefix('Body004') )
        npt_fxf_base_plate.Label = self.addPrefix('npt_fxf_base_plate')
        self.npt_fxf_base_plate = npt_fxf_base_plate # expose as instance variable using Label varname
        self.post_new_obj(npt_fxf_base_plate)
        npt_fxf_base_plate_Origin = get_LCS_by_prefix(doc, npt_fxf_base_plate, 'Origin') # source objName=Origin004
        npt_fxf_base_plate_X_Axis = get_LCS_by_prefix(doc, npt_fxf_base_plate, 'X_Axis') # source objName=X_Axis004
        npt_fxf_base_plate_Y_Axis = get_LCS_by_prefix(doc, npt_fxf_base_plate, 'Y_Axis') # source objName=Y_Axis004
        npt_fxf_base_plate_Z_Axis = get_LCS_by_prefix(doc, npt_fxf_base_plate, 'Z_Axis') # source objName=Z_Axis004
        npt_fxf_base_plate_XY_Plane = get_LCS_by_prefix(doc, npt_fxf_base_plate, 'XY_Plane') # source objName=XY_Plane004
        npt_fxf_base_plate_XZ_Plane = get_LCS_by_prefix(doc, npt_fxf_base_plate, 'XZ_Plane') # source objName=XZ_Plane004
        npt_fxf_base_plate_YZ_Plane = get_LCS_by_prefix(doc, npt_fxf_base_plate, 'YZ_Plane') # source objName=YZ_Plane004
        self.npt_fxf_base_plate_Origin = npt_fxf_base_plate_Origin # expose as instance variable using Label varname
        self.npt_fxf_base_plate_X_Axis = npt_fxf_base_plate_X_Axis # expose as instance variable using Label varname
        self.npt_fxf_base_plate_Y_Axis = npt_fxf_base_plate_Y_Axis # expose as instance variable using Label varname
        self.npt_fxf_base_plate_Z_Axis = npt_fxf_base_plate_Z_Axis # expose as instance variable using Label varname
        self.npt_fxf_base_plate_XY_Plane = npt_fxf_base_plate_XY_Plane # expose as instance variable using Label varname
        self.npt_fxf_base_plate_XZ_Plane = npt_fxf_base_plate_XZ_Plane # expose as instance variable using Label varname
        self.npt_fxf_base_plate_YZ_Plane = npt_fxf_base_plate_YZ_Plane # expose as instance variable using Label varname
        self.post_new_obj(npt_fxf_base_plate_Origin)
        self.post_new_obj(npt_fxf_base_plate_X_Axis)
        self.post_new_obj(npt_fxf_base_plate_Y_Axis)
        self.post_new_obj(npt_fxf_base_plate_Z_Axis)
        self.post_new_obj(npt_fxf_base_plate_XY_Plane)
        self.post_new_obj(npt_fxf_base_plate_XZ_Plane)
        self.post_new_obj(npt_fxf_base_plate_YZ_Plane)
        npt_fxf_base_plate.recompute()  # recompute after adding object
        
        npt_fxf_callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('npt_fxf_callsheet') )
        npt_fxf_callsheet.Label = self.addPrefix('npt_fxf_callsheet')
        self.npt_fxf_callsheet = npt_fxf_callsheet # expose as instance variable using Label varname
        self.post_new_obj(npt_fxf_callsheet)
        npt_fxf_callsheet.set('A1', 'variableName')
        npt_fxf_callsheet.set('A10', 'base_plate_thick')
        npt_fxf_callsheet.set('A11', 'horizontalScale')
        npt_fxf_callsheet.set('A12', 'verticalScale')
        npt_fxf_callsheet.set('A13', 'holeDiaExpansion_spec')
        npt_fxf_callsheet.set('A2', 's_npt_f_nominalID')
        npt_fxf_callsheet.set('A3', 'b_npt_f_nominalID')
        npt_fxf_callsheet.set('A4', 's_npt_f_wall_spec')
        npt_fxf_callsheet.set('A5', 'b_npt_f_wall_spec')
        npt_fxf_callsheet.set('A6', 's_npt_f_height_spec')
        npt_fxf_callsheet.set('A7', 'b_npt_f_height_spec')
        npt_fxf_callsheet.set('A8', 's_npt_f_height')
        npt_fxf_callsheet.set('A9', 'base_plate_thick_spec')
        npt_fxf_callsheet.set('B1', 'value')
        npt_fxf_callsheet.set('B10', '=0.2522 in')
        npt_fxf_callsheet.setAlias('B10', 'base_plate_thick')
        npt_fxf_callsheet.set('B11', '1.1982')
        npt_fxf_callsheet.setAlias('B11', 'horizontalScale')
        npt_fxf_callsheet.set('B11', f'{self.horizontalScale}') # call param
        npt_fxf_callsheet.set('B12', '1.261')
        npt_fxf_callsheet.setAlias('B12', 'verticalScale')
        npt_fxf_callsheet.set('B12', f'{self.verticalScale}') # call param
        npt_fxf_callsheet.set('B13', '=0.03 in')
        npt_fxf_callsheet.setAlias('B13', 'holeDiaExpansion_spec')
        npt_fxf_callsheet.set('B13', f'={self.holeDiaExpansion_spec}') # call param
        npt_fxf_callsheet.set('B2', '`3/4')
        npt_fxf_callsheet.setAlias('B2', 's_npt_f_nominalID')
        npt_fxf_callsheet.set('B2', f'{self.s_npt_f_nominalID}') # call param
        npt_fxf_callsheet.set('B3', '`2')
        npt_fxf_callsheet.setAlias('B3', 'b_npt_f_nominalID')
        npt_fxf_callsheet.set('B3', f'{self.b_npt_f_nominalID}') # call param
        npt_fxf_callsheet.set('B4', '=0.08 in')
        npt_fxf_callsheet.setAlias('B4', 's_npt_f_wall_spec')
        npt_fxf_callsheet.set('B4', f'={self.s_npt_f_wall_spec}') # call param
        npt_fxf_callsheet.set('B5', '=0.08 in')
        npt_fxf_callsheet.setAlias('B5', 'b_npt_f_wall_spec')
        npt_fxf_callsheet.set('B5', f'={self.b_npt_f_wall_spec}') # call param
        npt_fxf_callsheet.set('B6', '=0.8 in')
        npt_fxf_callsheet.setAlias('B6', 's_npt_f_height_spec')
        npt_fxf_callsheet.set('B6', f'={self.s_npt_f_height_spec}') # call param
        npt_fxf_callsheet.set('B7', '=1 in')
        npt_fxf_callsheet.setAlias('B7', 'b_npt_f_height_spec')
        npt_fxf_callsheet.set('B7', f'={self.b_npt_f_height_spec}') # call param
        npt_fxf_callsheet.set('B8', '=1.0088 in')
        npt_fxf_callsheet.setAlias('B8', 's_npt_f_height')
        npt_fxf_callsheet.set('B9', '=0.2 in')
        npt_fxf_callsheet.setAlias('B9', 'base_plate_thick_spec')
        npt_fxf_callsheet.set('B9', f'={self.base_plate_thick_spec}') # call param
        npt_fxf_callsheet.set('C1', 'isCallParam')
        npt_fxf_callsheet.set('C10', 'N')
        npt_fxf_callsheet.set('C11', 'Y')
        npt_fxf_callsheet.set('C12', 'Y')
        npt_fxf_callsheet.set('C13', 'Y')
        npt_fxf_callsheet.set('C2', 'Y')
        npt_fxf_callsheet.set('C3', 'Y')
        npt_fxf_callsheet.set('C4', 'Y')
        npt_fxf_callsheet.set('C5', 'Y')
        npt_fxf_callsheet.set('C6', 'Y')
        npt_fxf_callsheet.set('C7', 'Y')
        npt_fxf_callsheet.set('C8', 'N')
        npt_fxf_callsheet.set('C9', 'Y')
        npt_fxf_callsheet.set('D1', 'hint')
        npt_fxf_callsheet.set('E1', 'comment')
        npt_fxf_callsheet.set('E10', 'base_plate_thick_spec * verticalScale')
        npt_fxf_callsheet.set('E11', 'BASF 17-4 xy scale 1.1982')
        npt_fxf_callsheet.set('E12', 'BASF 17-4 z scale 1.2610')
        npt_fxf_callsheet.set('E8', 's_npt_f_height_spec * verticalScale')
        npt_fxf_callsheet.recompute()  # recompute after adding object
        
        npt_fxf_sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('Sketch004') )
        npt_fxf_sketch.Label = self.addPrefix('npt_fxf_sketch')
        self.npt_fxf_sketch = npt_fxf_sketch # expose as instance variable using Label varname
        self.post_new_obj(npt_fxf_sketch)
        self.container_append_object(npt_fxf_base_plate, npt_fxf_sketch)
        geo0 = npt_fxf_sketch.addGeometry(Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 39.0320))
        geo1 = npt_fxf_sketch.addGeometry(Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 18.8693))
        npt_fxf_sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 3, -1, 1))
        npt_fxf_sketch.addConstraint(Sketcher.Constraint('Coincident', geo1, 3, geo0, 3))
        npt_fxf_sketch.addConstraint(Sketcher.Constraint('Diameter', geo0, 78.0639))
        npt_fxf_sketch.addConstraint(Sketcher.Constraint('Diameter', geo1, 37.7385))
        npt_fxf_sketch.AttacherEngine = 'Engine Plane'
        from pdfclib.subelementtools import get_seName_by_posName
        npt_fxf_sketch.AttachmentSupport = (npt_fxf_base_plate_XY_Plane, (''))
        npt_fxf_base_plate_XY_Plane.Visibility = False  # hide base object
        npt_fxf_sketch.MapMode = 'FlatFace'
        npt_fxf_sketch.Visibility = False
        npt_fxf_sketch.ViewObject.Visibility = False
        npt_fxf_sketch.recompute()  # recompute after adding object
        
        npt_fxf_pad = doc.addObject('PartDesign::Pad', self.addPrefix('Pad002') )
        npt_fxf_pad.Label = self.addPrefix('npt_fxf_pad')
        self.npt_fxf_pad = npt_fxf_pad # expose as instance variable using Label varname
        self.post_new_obj(npt_fxf_pad)
        self.container_append_object(npt_fxf_base_plate, npt_fxf_pad)
        npt_fxf_pad.Length = 6.40588
        npt_fxf_pad.Profile = (npt_fxf_sketch, [''])
        npt_fxf_pad.ReferenceAxis = (npt_fxf_sketch, ['N_Axis'])
        npt_fxf_pad.Visibility = False
        npt_fxf_pad.ViewObject.Visibility = False
        npt_fxf_pad.recompute()  # recompute after adding object
        
        npt_fxf_boolean = doc.addObject('PartDesign::Boolean', self.addPrefix('Boolean') )
        npt_fxf_boolean.Label = self.addPrefix('npt_fxf_boolean')
        self.npt_fxf_boolean = npt_fxf_boolean # expose as instance variable using Label varname
        self.post_new_obj(npt_fxf_boolean)
        self.container_append_object(npt_fxf_base_plate, npt_fxf_boolean)
        npt_fxf_boolean.BaseFeature = npt_fxf_pad
        npt_fxf_boolean.Group = [b_npt_f_instance.npt_f, s_npt_f_instance.npt_f]
        npt_fxf_boolean.UsePlacement = True
        doc.recompute() # recompute whole document for {obj.TypeId}
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        s_npt_f_instance.npt_f_callsheet.set('B10', f"=<<{self.addPrefix('npt_fxf_callsheet')}>>.holeDiaExpansion_spec") # call param, B10's alias=holeDiaExpansion_spec
        s_npt_f_instance.npt_f_callsheet.set('B2', f"=<<{self.addPrefix('npt_fxf_callsheet')}>>.s_npt_f_nominalID") # call param, B2's alias=nominalID
        s_npt_f_instance.npt_f_callsheet.set('B4', f"=<<{self.addPrefix('npt_fxf_callsheet')}>>.verticalScale") # call param, B4's alias=verticalScale
        s_npt_f_instance.npt_f_callsheet.set('B5', f"=<<{self.addPrefix('npt_fxf_callsheet')}>>.s_npt_f_wall_spec") # call param, B5's alias=femaleOD_wall_spec
        s_npt_f_instance.npt_f_callsheet.set('B8', f"=<<{self.addPrefix('npt_fxf_callsheet')}>>.s_npt_f_height_spec") # call param, B8's alias=female_height_spec
        b_npt_f_instance.npt_f_callsheet.set('B10', f"=<<{self.addPrefix('npt_fxf_callsheet')}>>.holeDiaExpansion_spec") # call param, B10's alias=holeDiaExpansion_spec
        b_npt_f_instance.npt_f_callsheet.set('B2', f"=<<{self.addPrefix('npt_fxf_callsheet')}>>.b_npt_f_nominalID") # call param, B2's alias=nominalID
        b_npt_f_instance.npt_f_callsheet.set('B3', f"=<<{self.addPrefix('npt_fxf_callsheet')}>>.horizontalScale") # call param, B3's alias=horizontalScale
        b_npt_f_instance.npt_f_callsheet.set('B4', f"=<<{self.addPrefix('npt_fxf_callsheet')}>>.verticalScale") # call param, B4's alias=verticalScale
        b_npt_f_instance.npt_f_callsheet.set('B5', f"=<<{self.addPrefix('npt_fxf_callsheet')}>>.b_npt_f_wall_spec") # call param, B5's alias=femaleOD_wall_spec
        b_npt_f_instance.npt_f_callsheet.set('B8', f"=<<{self.addPrefix('npt_fxf_callsheet')}>>.b_npt_f_height_spec") # call param, B8's alias=female_height_spec
        npt_fxf_callsheet.set("B10", f"=base_plate_thick_spec * verticalScale") # B10's alias=base_plate_thick
        npt_fxf_callsheet.set("B8", f"=s_npt_f_height_spec * verticalScale") # B8's alias=s_npt_f_height
        npt_fxf_pad.setExpression("Length", f"<<{self.addPrefix('npt_fxf_callsheet')}>>.base_plate_thick")
        npt_fxf_sketch.setExpression("Constraints[2]", f"<<{self.addPrefix('b_npt_f_callsheet')}>>.femaleOD")
        npt_fxf_sketch.setExpression("Constraints[3]", f"<<{self.addPrefix('s_npt_f_callsheet')}>>.femaleOD")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # set callsheet
        self.callsheet = self.npt_fxf_callsheet
        self.update_callsheet()


def main():
    # main_part1
    from pdfclib.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of Npt_fxf
    myInstance = Npt_fxf("myInstance", doc, objPrefix="", useLabel=True, importer=None, b_npt_f_height_spec='1 in', b_npt_f_nominalID='`2', b_npt_f_wall_spec='0.08 in', base_plate_thick_spec='0.2 in', holeDiaExpansion_spec='0.03 in', horizontalScale=1.1982, s_npt_f_height_spec='0.8 in', s_npt_f_nominalID='`3/4', s_npt_f_wall_spec='0.08 in', verticalScale=1.261, )
    
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
