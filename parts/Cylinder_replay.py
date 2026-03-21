from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.baseClass import baseClass
from pdfclib.containertools import get_LCS_by_prefix
from pdfclib.objtools import update_obj_prop_jsonDict

class Cylinder(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, cylinder_height_spec='0.5 in', cylinder_radius_spec='0.5 in', horizontalScale=1.1982, verticalScale=1.261,  ):
        self.cylinder_height_spec = cylinder_height_spec
        self.cylinder_radius_spec = cylinder_radius_spec
        self.horizontalScale = horizontalScale
        self.verticalScale = verticalScale
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        
        # add objects and add static value to objects' properties based on object dependencies
        cylinder = doc.addObject('PartDesign::Body', self.addPrefix('Body') )
        cylinder.Label = self.addPrefix('cylinder')
        self.cylinder = cylinder # expose as instance variable using Label varname
        self.post_new_obj(cylinder)
        cylinder_Origin = get_LCS_by_prefix(doc, cylinder, 'Origin') # source objName=Origin
        cylinder_X_Axis = get_LCS_by_prefix(doc, cylinder, 'X_Axis') # source objName=X_Axis
        cylinder_Y_Axis = get_LCS_by_prefix(doc, cylinder, 'Y_Axis') # source objName=Y_Axis
        cylinder_Z_Axis = get_LCS_by_prefix(doc, cylinder, 'Z_Axis') # source objName=Z_Axis
        cylinder_XY_Plane = get_LCS_by_prefix(doc, cylinder, 'XY_Plane') # source objName=XY_Plane
        cylinder_XZ_Plane = get_LCS_by_prefix(doc, cylinder, 'XZ_Plane') # source objName=XZ_Plane
        cylinder_YZ_Plane = get_LCS_by_prefix(doc, cylinder, 'YZ_Plane') # source objName=YZ_Plane
        self.cylinder_Origin = cylinder_Origin # expose as instance variable using Label varname
        self.cylinder_X_Axis = cylinder_X_Axis # expose as instance variable using Label varname
        self.cylinder_Y_Axis = cylinder_Y_Axis # expose as instance variable using Label varname
        self.cylinder_Z_Axis = cylinder_Z_Axis # expose as instance variable using Label varname
        self.cylinder_XY_Plane = cylinder_XY_Plane # expose as instance variable using Label varname
        self.cylinder_XZ_Plane = cylinder_XZ_Plane # expose as instance variable using Label varname
        self.cylinder_YZ_Plane = cylinder_YZ_Plane # expose as instance variable using Label varname
        self.post_new_obj(cylinder_Origin)
        self.post_new_obj(cylinder_X_Axis)
        self.post_new_obj(cylinder_Y_Axis)
        self.post_new_obj(cylinder_Z_Axis)
        self.post_new_obj(cylinder_XY_Plane)
        self.post_new_obj(cylinder_XZ_Plane)
        self.post_new_obj(cylinder_YZ_Plane)
        cylinder.recompute()  # recompute after adding object
        
        cylinder_callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('cylinder_callsheet') )
        cylinder_callsheet.Label = self.addPrefix('cylinder_callsheet')
        self.cylinder_callsheet = cylinder_callsheet # expose as instance variable using Label varname
        self.post_new_obj(cylinder_callsheet)
        cylinder_callsheet.set('A1', 'variableName')
        cylinder_callsheet.set('A2', 'horizontalScale')
        cylinder_callsheet.set('A3', 'verticalScale')
        cylinder_callsheet.set('A4', 'cylinder_radius_spec')
        cylinder_callsheet.set('A5', 'cylinder_radius')
        cylinder_callsheet.set('A6', 'cylinder_height_spec')
        cylinder_callsheet.set('A7', 'cylinder_height')
        cylinder_callsheet.set('B1', 'value')
        cylinder_callsheet.set('B2', '1.1982')
        cylinder_callsheet.setAlias('B2', 'horizontalScale')
        cylinder_callsheet.set('B2', f'{self.horizontalScale}') # call param
        cylinder_callsheet.set('B3', '1.261')
        cylinder_callsheet.setAlias('B3', 'verticalScale')
        cylinder_callsheet.set('B3', f'{self.verticalScale}') # call param
        cylinder_callsheet.set('B4', '=0.5 in')
        cylinder_callsheet.setAlias('B4', 'cylinder_radius_spec')
        cylinder_callsheet.set('B4', f'={self.cylinder_radius_spec}') # call param
        cylinder_callsheet.set('B5', '=0.5991 in')
        cylinder_callsheet.setAlias('B5', 'cylinder_radius')
        cylinder_callsheet.set('B6', '=0.5 in')
        cylinder_callsheet.setAlias('B6', 'cylinder_height_spec')
        cylinder_callsheet.set('B6', f'={self.cylinder_height_spec}') # call param
        cylinder_callsheet.set('B7', '=0.6305 in')
        cylinder_callsheet.setAlias('B7', 'cylinder_height')
        cylinder_callsheet.set('C1', 'isCallParam')
        cylinder_callsheet.set('C2', 'Y')
        cylinder_callsheet.set('C3', 'Y')
        cylinder_callsheet.set('C4', 'Y')
        cylinder_callsheet.set('C5', 'N')
        cylinder_callsheet.set('C6', 'Y')
        cylinder_callsheet.set('C7', 'N')
        cylinder_callsheet.set('D1', 'comment')
        cylinder_callsheet.set('D2', 'BASF 17-4 xy scale 1.1982')
        cylinder_callsheet.set('D3', 'BASF 17-4 z scale 1.2610')
        cylinder_callsheet.set('D4', 'radius of circle circumferencing polygon')
        cylinder_callsheet.set('D6', 'pad height')
        cylinder_callsheet.recompute()  # recompute after adding object
        
        cylinder_sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('Sketch') )
        cylinder_sketch.Label = self.addPrefix('cylinder_sketch')
        self.cylinder_sketch = cylinder_sketch # expose as instance variable using Label varname
        self.post_new_obj(cylinder_sketch)
        self.container_append_object(cylinder, cylinder_sketch)
        geo0 = cylinder_sketch.addGeometry(Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 15.2171))
        cylinder_sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 3, -1, 1))
        cylinder_sketch.addConstraint(Sketcher.Constraint('Radius', geo0, 15.2171))
        cylinder_sketch.AttacherEngine = 'Engine Plane'
        from pdfclib.subelementtools import get_seName_by_posName
        cylinder_sketch.AttachmentSupport = (cylinder_XY_Plane, (''))
        cylinder_XY_Plane.Visibility = False  # hide base object
        cylinder_sketch.MapMode = 'FlatFace'
        cylinder_sketch.Visibility = False
        cylinder_sketch.ViewObject.Visibility = False
        cylinder_sketch.recompute()  # recompute after adding object
        
        cylinder_pad = doc.addObject('PartDesign::Pad', self.addPrefix('Pad') )
        cylinder_pad.Label = self.addPrefix('cylinder_pad')
        self.cylinder_pad = cylinder_pad # expose as instance variable using Label varname
        self.post_new_obj(cylinder_pad)
        self.container_append_object(cylinder, cylinder_pad)
        cylinder_pad.Length = 16.014699999999998
        cylinder_pad.Profile = (cylinder_sketch, [''])
        cylinder_pad.ReferenceAxis = (cylinder_sketch, ['N_Axis'])
        cylinder_pad.recompute()  # recompute after adding object
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        cylinder_callsheet.set("B5", f"=cylinder_radius_spec * horizontalScale") # B5's alias=cylinder_radius
        cylinder_callsheet.set("B7", f"=cylinder_height_spec * verticalScale") # B7's alias=cylinder_height
        cylinder_pad.setExpression("Length", f"<<{self.addPrefix('cylinder_callsheet')}>>.cylinder_height")
        cylinder_sketch.setExpression("Constraints[1]", f"<<{self.addPrefix('cylinder_callsheet')}>>.cylinder_radius")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # set callsheet
        self.callsheet = self.cylinder_callsheet
        self.update_callsheet()


def main():
    # main_part1
    from pdfclib.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of Cylinder
    myInstance = Cylinder("myInstance", doc, objPrefix="", useLabel=True, importer=None, cylinder_height_spec='0.5 in', cylinder_radius_spec='0.5 in', horizontalScale=1.1982, verticalScale=1.261, )
    
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
