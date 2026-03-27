from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.baseClass import baseClass
from cadcoder.containertools import get_LCS_by_prefix
from cadcoder.objtools import update_obj_prop_jsonDict
from cadcoder.subelementtools import update_objs_seName, update_doc_seName, get_seName_by_posName

class cylinder_hori(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, pad_length='0.5 in', radius_y='0.5 in',  ):
        self.pad_length = pad_length
        self.radius_y = radius_y
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        
        # add objects and add static value to objects' properties based on object dependencies
        body = doc.addObject('PartDesign::Body', self.addPrefix('body') )
        body.Label = self.addPrefix('body')
        self.body = body
        self.post_new_obj(body)
        body_Origin = get_LCS_by_prefix(doc, body, 'Origin')
        body_X_Axis = get_LCS_by_prefix(doc, body, 'X_Axis')
        body_Y_Axis = get_LCS_by_prefix(doc, body, 'Y_Axis')
        body_Z_Axis = get_LCS_by_prefix(doc, body, 'Z_Axis')
        body_XY_Plane = get_LCS_by_prefix(doc, body, 'XY_Plane')
        body_XZ_Plane = get_LCS_by_prefix(doc, body, 'XZ_Plane')
        body_YZ_Plane = get_LCS_by_prefix(doc, body, 'YZ_Plane')
        self.body_Origin = body_Origin
        self.body_X_Axis = body_X_Axis
        self.body_Y_Axis = body_Y_Axis
        self.body_Z_Axis = body_Z_Axis
        self.body_XY_Plane = body_XY_Plane
        self.body_XZ_Plane = body_XZ_Plane
        self.body_YZ_Plane = body_YZ_Plane
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
        self.callsheet = callsheet
        self.post_new_obj(callsheet)
        callsheet.set('A1', 'variableName')
        callsheet.set('A2', 'radius_y')
        callsheet.set('A3', 'radius_z')
        callsheet.set('A4', 'pad_length')
        callsheet.set('B1', 'value')
        callsheet.set('B2', '=0.5 in')
        callsheet.setAlias('B2', 'radius_y')
        callsheet.set('B3', '=0.501 in')
        callsheet.setAlias('B3', 'radius_z')
        callsheet.set('B4', '=0.5 in')
        callsheet.setAlias('B4', 'pad_length')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C2', 'Y')
        callsheet.set('C3', 'N')
        callsheet.set('C4', 'Y')
        callsheet.set('D1', 'comment')
        callsheet.recompute()  # recompute after adding object
        
        sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('sketch') )
        sketch.Label = self.addPrefix('sketch')
        self.sketch = sketch
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
        self.pad = pad
        self.post_new_obj(pad)
        self.container_append_object(body, pad)
        pad.Length = 12.7
        pad.Profile = (sketch, [''])
        pad.ReferenceAxis = (sketch, ['N_Axis'])
        pad.recompute()  # recompute after adding object
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        pad.setExpression("Length", f"<<{self.addPrefix('callsheet')}>>.pad_length")
        sketch.setExpression("Constraints[7]", f"<<{self.addPrefix('callsheet')}>>.radius_y")
        callsheet.set(callsheet.getCellFromAlias("radius_z"), f"=radius_y * 1.002")
        sketch.setExpression("Constraints[6]", f"<<{self.addPrefix('callsheet')}>>.radius_z")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # now we have rebuilt the original cylinder_hori doc. Now we apply dynmic call parameters
        print("there can be temporary errors when we applying dynamic call parameters that change original cylinder_hori's shape.")
        print("ignore temporary errors, if any, below.")
        callsheet.set(callsheet.getCellFromAlias('radius_y'), f'={self.radius_y}')
        callsheet.set(callsheet.getCellFromAlias('pad_length'), f'={self.pad_length}')
        doc.recompute()
        update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.
        print("ignore temporary errors, if any, above.")
        
        self.update_callsheet()


def main():
    # main_part1
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of cylinder_hori
    myInstance = cylinder_hori("myInstance", doc, objPrefix="", useLabel=True, importer=None, pad_length='0.5 in', radius_y='0.5 in', )
    
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
