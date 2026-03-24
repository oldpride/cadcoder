from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.baseClass import baseClass
from cadcoder.containertools import get_LCS_by_prefix
from cadcoder.objtools import update_obj_prop_jsonDict
from cadcoder.subelementtools import update_objs_seName, update_doc_seName, get_seName_by_posName

class Cylinder_hori(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, pad_length_spec='0.5 in', radius_y_spec='0.5 in', horizontalScale=1, verticalScale=1,  ):
        self.pad_length_spec = pad_length_spec
        self.radius_y_spec = radius_y_spec
        self.horizontalScale = horizontalScale
        self.verticalScale = verticalScale
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        
        # add objects and add static value to objects' properties based on object dependencies
        body = doc.addObject('PartDesign::Body', self.addPrefix('body') )
        body.Label = self.addPrefix('body')
        self.body = body # expose as instance variable using Label varname
        self.post_new_obj(body)
        body_Origin = get_LCS_by_prefix(doc, body, 'Origin')
        body_X_Axis = get_LCS_by_prefix(doc, body, 'X_Axis')
        body_Y_Axis = get_LCS_by_prefix(doc, body, 'Y_Axis')
        body_Z_Axis = get_LCS_by_prefix(doc, body, 'Z_Axis')
        body_XY_Plane = get_LCS_by_prefix(doc, body, 'XY_Plane')
        body_XZ_Plane = get_LCS_by_prefix(doc, body, 'XZ_Plane')
        body_YZ_Plane = get_LCS_by_prefix(doc, body, 'YZ_Plane')
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
        callsheet.set('A4', 'radius_y_spec')
        callsheet.set('A5', 'radius_y')
        callsheet.set('A6', 'radius_z_spec')
        callsheet.set('A7', 'radius_z')
        callsheet.set('A8', 'pad_length_spec')
        callsheet.set('A9', 'pad_length')
        callsheet.set('B1', 'value')
        callsheet.set('B2', '1')
        callsheet.setAlias('B2', 'horizontalScale')
        callsheet.set('B2', f'{self.horizontalScale}') # call param
        callsheet.set('B3', '1')
        callsheet.setAlias('B3', 'verticalScale')
        callsheet.set('B3', f'{self.verticalScale}') # call param
        callsheet.set('B4', '=0.5 in')
        callsheet.setAlias('B4', 'radius_y_spec')
        callsheet.set('B4', f'={self.radius_y_spec}') # call param
        callsheet.set('B5', '=0.5 in')
        callsheet.setAlias('B5', 'radius_y')
        callsheet.set('B6', '=0.501 in')
        callsheet.setAlias('B6', 'radius_z_spec')
        callsheet.set('B7', '=0.501 in')
        callsheet.setAlias('B7', 'radius_z')
        callsheet.set('B8', '=0.5 in')
        callsheet.setAlias('B8', 'pad_length_spec')
        callsheet.set('B8', f'={self.pad_length_spec}') # call param
        callsheet.set('B9', '=0.5 in')
        callsheet.setAlias('B9', 'pad_length')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C2', 'Y')
        callsheet.set('C3', 'Y')
        callsheet.set('C4', 'Y')
        callsheet.set('C5', 'N')
        callsheet.set('C6', 'N')
        callsheet.set('C7', 'N')
        callsheet.set('C8', 'Y')
        callsheet.set('C9', 'N')
        callsheet.set('D1', 'comment')
        callsheet.set('D2', 'BASF 17-4 xy scale 1.1982')
        callsheet.set('D3', 'BASF 17-4 z scale 1.2610')
        callsheet.set('D4', 'y radius')
        callsheet.set('D6', 'z radius > y radius')
        callsheet.set('D8', 'pad length')
        callsheet.recompute()  # recompute after adding object
        
        sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('sketch') )
        sketch.Label = self.addPrefix('sketch')
        self.sketch = sketch # expose as instance variable using Label varname
        self.post_new_obj(sketch)
        self.container_append_object(body, sketch)
        geo0 = sketch.addGeometry(Part.Ellipse(Vector(0.0000, 12.7254, 0.0000), Vector(-12.7000, 0.0000, 0.0000), Vector(0.0000, 0.0000, 0.0000)))
        sketch.exposeInternalGeometry(0)
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 3, -1, 1))
        sketch.addConstraint(Sketcher.Constraint('PointOnObject', 1, 1, -2))
        sketch.addConstraint(Sketcher.Constraint('DistanceY', geo0, 3, 1, 1, 12.7254))
        sketch.addConstraint(Sketcher.Constraint('DistanceX', geo0, 3, 2, 2, 12.7000))
        sketch.AttacherEngine = 'Engine Plane'
        sketch.AttachmentSupport = (body_YZ_Plane, (''))
        body_YZ_Plane.Visibility = False  # hide base object
        sketch.MapMode = 'FlatFace'
        sketch.Visibility = False
        sketch.ViewObject.Visibility = False
        sketch.recompute()  # recompute after adding object
        
        pad = doc.addObject('PartDesign::Pad', self.addPrefix('pad') )
        pad.Label = self.addPrefix('pad')
        self.pad = pad # expose as instance variable using Label varname
        self.post_new_obj(pad)
        self.container_append_object(body, pad)
        pad.Length = 12.7
        pad.Profile = (sketch, [''])
        pad.ReferenceAxis = (sketch, ['N_Axis'])
        pad.recompute()  # recompute after adding object
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        callsheet.set(callsheet.getCellFromAlias("radius_y"), f"=radius_y_spec * horizontalScale")
        callsheet.set(callsheet.getCellFromAlias("radius_z_spec"), f"=radius_y_spec * 1.002")
        callsheet.set(callsheet.getCellFromAlias("pad_length"), f"=pad_length_spec * horizontalScale")
        pad.setExpression("Length", f"<<{self.addPrefix('callsheet')}>>.pad_length")
        sketch.setExpression("Constraints[7]", f"<<{self.addPrefix('callsheet')}>>.radius_y")
        callsheet.set(callsheet.getCellFromAlias("radius_z"), f"=radius_z_spec * verticalScale")
        sketch.setExpression("Constraints[6]", f"<<{self.addPrefix('callsheet')}>>.radius_z")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        self.update_callsheet()


def main():
    # main_part1
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    myInstance = Cylinder_hori("myInstance", doc, objPrefix="", useLabel=True, importer=None, pad_length_spec='0.5 in', radius_y_spec='0.5 in', horizontalScale=1, verticalScale=1, )
    
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
