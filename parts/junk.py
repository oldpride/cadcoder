from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.baseClass import baseClass
from cadcoder.containertools import get_LCS_by_prefix
from cadcoder.objtools import update_obj_prop_jsonDict
from cadcoder.subelementtools import update_objs_seName, update_doc_seName, get_seName_by_posName

class prism_polygon(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, height='0.5 in', radius='1 in', sides=8,  ):
        self.height = height
        self.radius = radius
        self.sides = sides
        
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
        callsheet.set('A2', 'sides')
        callsheet.set('A3', 'radius')
        callsheet.set('A4', 'height')
        callsheet.set('B1', 'value')
        callsheet.set('B2', '8')
        callsheet.setAlias('B2', 'sides')
        callsheet.set('B3', '=1 in')
        callsheet.setAlias('B3', 'radius')
        callsheet.set('B4', '=0.5 in')
        callsheet.setAlias('B4', 'height')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C2', 'Y')
        callsheet.set('C3', 'Y')
        callsheet.set('C4', 'Y')
        callsheet.set('D1', 'comment')
        callsheet.set('D3', 'circumcircle circle')
        callsheet.recompute()  # recompute after adding object
        
        sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('sketch') )
        sketch.Label = self.addPrefix('sketch')
        self.sketch = sketch
        self.post_new_obj(sketch)
        self.container_append_object(body, sketch)
        geo0 = sketch.addGeometry(Part.LineSegment(Vector (17.960512242138304, 17.960512242138304, 0.0), Vector (0.0, 25.4, 0.0)))
        geo1 = sketch.addGeometry(Part.LineSegment(Vector (-0.0, 25.4, 0.0), Vector (-17.960512242138307, 17.960512242138304, 0.0)))
        geo2 = sketch.addGeometry(Part.LineSegment(Vector (-17.960512242138307, 17.960512242138304, 0.0), Vector (-25.4, 0.0, 0.0)))
        geo3 = sketch.addGeometry(Part.LineSegment(Vector (-25.4, 1.5e-15, 0.0), Vector (-17.960512242138304, -17.960512242138304, 0.0)))
        geo4 = sketch.addGeometry(Part.LineSegment(Vector (-17.960512242138304, -17.960512242138304, 0.0), Vector (-3.552713678800501e-15, -25.4, 0.0)))
        geo5 = sketch.addGeometry(Part.LineSegment(Vector (-2.1e-15, -25.4, 0.0), Vector (17.960512242138304, -17.960512242138304, 0.0)))
        geo6 = sketch.addGeometry(Part.LineSegment(Vector (17.960512242138304, -17.960512242138304, 0.0), Vector (25.4, 0.0, 0.0)))
        geo7 = sketch.addGeometry(Part.LineSegment(Vector (25.4, 2e-16, 0.0), Vector (17.960512242138304, 17.960512242138304, 0.0)))
        geo8 = sketch.addGeometry(Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 25.4000))
        sketch.toggleConstruction(geo8)
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 2, geo1, 1))
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo1, 2, geo2, 1))
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo2, 2, geo3, 1))
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo3, 2, geo4, 1))
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo4, 2, geo5, 1))
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo5, 2, geo6, 1))
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo6, 2, geo7, 1))
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo7, 2, geo0, 1))
        sketch.addConstraint(Sketcher.Constraint('Equal', geo0, geo1))
        sketch.addConstraint(Sketcher.Constraint('Equal', geo0, geo2))
        sketch.addConstraint(Sketcher.Constraint('Equal', geo0, geo3))
        sketch.addConstraint(Sketcher.Constraint('Equal', geo0, geo4))
        sketch.addConstraint(Sketcher.Constraint('Equal', geo0, geo5))
        sketch.addConstraint(Sketcher.Constraint('Equal', geo0, geo6))
        sketch.addConstraint(Sketcher.Constraint('Equal', geo0, geo7))
        sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo0, 2, geo8))
        sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo1, 2, geo8))
        sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo2, 2, geo8))
        sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo3, 2, geo8))
        sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo4, 2, geo8))
        sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo5, 2, geo8))
        sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo6, 2, geo8))
        sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo7, 2, geo8))
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo8, 3, -1, 1))
        sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo0, 2, -2))
        sketch.addConstraint(Sketcher.Constraint('Radius', geo8, 25.4000))
        sketch.AttacherEngine = 'Engine Plane'
        sketch.AttachmentSupport = (body_XY_Plane, (''))
        body_XY_Plane.Visibility = False  # hide base object
        sketch.MapMode = 'FlatFace'
        sketch.Visibility = False
        sketch.ViewObject.Visibility = False
        sketch.recompute()  # recompute after adding object
        
        pad = doc.addObject('PartDesign::Pad', self.addPrefix('pad') )
        pad.Label = self.addPrefix('pad')
        self.pad = pad
        self.post_new_obj(pad)
        self.container_append_object(body, pad)
        pad.AllowMultiFace = False
        pad.Length = 12.7
        pad.Profile = (sketch, [])
        pad.ReferenceAxis = (sketch, ['N_Axis'])
        pad.recompute()  # recompute after adding object
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        pad.setExpression("Length", f"<<{self.addPrefix('callsheet')}>>.height")
        sketch.setExpression("Constraints[25]", f"<<{self.addPrefix('callsheet')}>>.radius")
        
        # add trigger objects' expressions
        from cadcoder.triggertools import link_watch_to_target_func
        link_watch_to_target_func(doc, callsheet, 'sides', sketch, 'parts.prism_polygon', 'draw_polygon_sketch', '{}', useLabel)
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # now we have rebuilt the original prism_polygon doc. Now we apply dynmic call parameters
        print("there can be temporary errors when we applying dynamic call parameters that change original prism_polygon's shape.")
        print("ignore temporary errors, if any, below.")
        callsheet.set(callsheet.getCellFromAlias('sides'), f'{self.sides}')
        callsheet.set(callsheet.getCellFromAlias('radius'), f'={self.radius}')
        callsheet.set(callsheet.getCellFromAlias('height'), f'={self.height}')
        doc.recompute()
        update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.
        print("ignore temporary errors, if any, above.")
        
        self.update_callsheet()


def main():
    # main_part1
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of prism_polygon
    myInstance = prism_polygon("myInstance", doc, objPrefix="", useLabel=True, importer=None, height='0.5 in', radius='1 in', sides=8, )
    
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
