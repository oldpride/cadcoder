from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.baseClass import baseClass
from cadcoder.containertools import get_LCS_by_prefix
from cadcoder.objtools import update_obj_prop_jsonDict

class Cylinder(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, height_spec='0.5 in', radius_spec='0.5 in', horizontalScale=1.1982, verticalScale=1.261,  ):
        self.height_spec = height_spec
        self.radius_spec = radius_spec
        self.horizontalScale = horizontalScale
        self.verticalScale = verticalScale
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        
        # add objects and add static value to objects' properties based on object dependencies
        body = doc.addObject('PartDesign::Body', self.addPrefix('body') )
        body.Label = self.addPrefix('body')
        self.cylinder = body # expose as instance variable using Label varname
        self.post_new_obj(body)
        body_Origin = get_LCS_by_prefix(doc, body, 'Origin') # source objName=Origin
        body_X_Axis = get_LCS_by_prefix(doc, body, 'X_Axis') # source objName=X_Axis
        body_Y_Axis = get_LCS_by_prefix(doc, body, 'Y_Axis') # source objName=Y_Axis
        body_Z_Axis = get_LCS_by_prefix(doc, body, 'Z_Axis') # source objName=Z_Axis
        body_XY_Plane = get_LCS_by_prefix(doc, body, 'XY_Plane') # source objName=XY_Plane
        body_XZ_Plane = get_LCS_by_prefix(doc, body, 'XZ_Plane') # source objName=XZ_Plane
        body_YZ_Plane = get_LCS_by_prefix(doc, body, 'YZ_Plane') # source objName=YZ_Plane
        self.body_Origin = body_Origin # expose as instance variable using Label varname
        self.body_X_Axis = body_X_Axis # expose as instance variable using Label varname
        self.body_Y_Axis = body_Y_Axis # expose as instance variable using Label varname
        self.body_Z_Axis = body_Z_Axis # expose as instance variable using Label varname
        self.body_XY_Plane = body_XY_Plane # expose as instance variable using Label varname
        self.body_XZ_Plane = body_XZ_Plane # expose as instance variable using Label varname
        self.body_YZ_Plane = body_YZ_Plane # expose as instance variable using Label varname
        self.post_new_obj(body_Origin)
        self.post_new_obj(body_X_Axis)
        self.post_new_obj(body_Y_Axis)
        self.post_new_obj(body_Z_Axis)
        self.post_new_obj(body_XY_Plane)
        self.post_new_obj(body_XZ_Plane)
        self.post_new_obj(body_YZ_Plane)
        body.recompute()  # recompute after adding object
        
        callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('callsheet') )
        callsheet.Label = self.addPrefix('callsheet')
        self.callsheet = callsheet # expose as instance variable using Label varname
        self.post_new_obj(callsheet)
        callsheet.set('A1', 'variableName')
        callsheet.set('A2', 'horizontalScale')
        callsheet.set('A3', 'verticalScale')
        callsheet.set('A4', 'radius_spec')
        callsheet.set('A5', 'radius')
        callsheet.set('A6', 'height_spec')
        callsheet.set('A7', 'height')
        callsheet.set('B1', 'value')
        callsheet.set('B2', '1.1982')
        callsheet.setAlias('B2', 'horizontalScale')
        callsheet.set('B2', f'{self.horizontalScale}') # call param
        callsheet.set('B3', '1.261')
        callsheet.setAlias('B3', 'verticalScale')
        callsheet.set('B3', f'{self.verticalScale}') # call param
        callsheet.set('B4', '=0.5 in')
        callsheet.setAlias('B4', 'radius_spec')
        callsheet.set('B4', f'={self.radius_spec}') # call param
        callsheet.set('B5', '=0.5991 in')
        callsheet.setAlias('B5', 'radius')
        callsheet.set('B6', '=0.5 in')
        callsheet.setAlias('B6', 'height_spec')
        callsheet.set('B6', f'={self.height_spec}') # call param
        callsheet.set('B7', '=0.6305 in')
        callsheet.setAlias('B7', 'height')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C2', 'Y')
        callsheet.set('C3', 'Y')
        callsheet.set('C4', 'Y')
        callsheet.set('C5', 'N')
        callsheet.set('C6', 'Y')
        callsheet.set('C7', 'N')
        callsheet.set('D1', 'comment')
        callsheet.set('D2', 'BASF 17-4 xy scale 1.1982')
        callsheet.set('D3', 'BASF 17-4 z scale 1.2610')
        callsheet.set('D4', 'radius of circle circumferencing polygon')
        callsheet.set('D6', 'pad height')
        callsheet.recompute()  # recompute after adding object
        
        sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('sketch') )
        sketch.Label = self.addPrefix('sketch')
        self.sketch = sketch # expose as instance variable using Label varname
        self.post_new_obj(sketch)
        self.container_append_object(body, sketch)
        geo0 = sketch.addGeometry(Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 15.2171))
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 3, -1, 1))
        sketch.addConstraint(Sketcher.Constraint('Radius', geo0, 15.2171))
        sketch.AttacherEngine = 'Engine Plane'
        from cadcoder.subelementtools import get_seName_by_posName
        sketch.AttachmentSupport = (body_XY_Plane, (''))
        body_XY_Plane.Visibility = False  # hide base object
        sketch.MapMode = 'FlatFace'
        sketch.Visibility = False
        sketch.ViewObject.Visibility = False
        sketch.recompute()  # recompute after adding object
        
        pad = doc.addObject('PartDesign::Pad', self.addPrefix('pad') )
        pad.Label = self.addPrefix('pad')
        self.pad = pad # expose as instance variable using Label varname
        self.post_new_obj(pad)
        self.container_append_object(body, pad)
        pad.Length = 16.014699999999998
        pad.Profile = (sketch, [''])
        pad.ReferenceAxis = (sketch, ['N_Axis'])
        pad.recompute()  # recompute after adding object
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        callsheet.set(callsheet.getCellFromAlias("radius"), f"=radius_spec * horizontalScale") # B5's alias=radius
        callsheet.set(callsheet.getCellFromAlias("height"), f"=height_spec * verticalScale") # B7's alias=height
        pad.setExpression("Length", f"<<{self.addPrefix('callsheet')}>>.height")
        sketch.setExpression("Constraints[1]", f"<<{self.addPrefix('callsheet')}>>.radius")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        self.update_callsheet()


def main():
    # main_part1
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of Cylinder
    myInstance = Cylinder("myInstance", doc, objPrefix="", useLabel=True, importer=None, height_spec='0.5 in', radius_spec='0.5 in', horizontalScale=1.1982, verticalScale=1.261, )
    
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
