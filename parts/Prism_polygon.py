from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.baseClass import baseClass
from cadcoder.containertools import get_LCS_by_prefix
from cadcoder.objtools import update_obj_prop_jsonDict
from cadcoder.subelementtools import update_objs_seName, update_doc_seName, get_seName_by_posName
from math import cos, sin, pi


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

        draw_polygon_sketch(sketch, sides=sides)
        
        sketch.AttacherEngine = 'Engine Plane'
        sketch.AttachmentSupport = (body_XY_Plane, (''))
        body_XY_Plane.Visibility = False  # hide base object
        sketch.MapMode = 'FlatFace'
        sketch.Visibility = False
        sketch.ViewObject.Visibility = False
        # sketch.recompute()  # recompute after adding object
        
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
        
        # add trigger objects' expressions
        from cadcoder.triggertools import link_watch_to_target
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

    def redraw_sketch(self, sides:int):
        # redraw if sides changed.
        if sides == self.sides:
            return
        self.sides = sides
        sketch = self.sketch

        draw_polygon_sketch(sketch, sides=sides)
        self.doc.recompute()

def draw_polygon_sketch(sketchObj, sides:int, old_sides:str=None, **opt):   
    # remove existing geometry and constraints
    constraint_count = len(sketchObj.Constraints)
    for i in range(constraint_count):
        sketchObj.delConstraint(constraint_count-1-i) # delete constraints in reverse order to avoid messing up constraint indices
    geo_count = len(sketchObj.Geometry)        
    for i in range(geo_count):
        sketchObj.delGeometries([geo_count-1-i])
    
    geos = []
    for i in range(sides):
        # cos(), sin() in math module use radians!!!
        # cos(), sin() in freecad expression use degrees!!!
        theta0 = 2*pi * i / sides
        theta1 = 2*pi * (i+1) / sides
        geos.append(sketchObj.addGeometry(
            Part.LineSegment(Vector(cos(theta0)*10, sin(theta0)*10, 0), 
                                Vector(cos(theta1)*10, sin(theta1)*10, 0))))
    geos.append(sketchObj.addGeometry(
        Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 10))) # radius
    sketchObj.toggleConstruction(geos[sides])
    constraint_i = 0
    for i in range(sides):
        j = (i+1) % sides
        sketchObj.addConstraint(Sketcher.Constraint('Coincident', geos[i], 2, geos[j], 1))
        constraint_i += 1
    for i in range(sides-1):
        sketchObj.addConstraint(Sketcher.Constraint('Equal', geos[0], geos[i+1]))
        constraint_i += 1
    for i in range(sides):
        j = (i+1) % sides
        sketchObj.addConstraint(Sketcher.Constraint('PointOnObject', geos[i], 2, geos[sides]))
        constraint_i += 1
    sketchObj.addConstraint(Sketcher.Constraint('Coincident', geos[sides], 3, -1, 1))
    constraint_i += 1
    sketchObj.addConstraint(Sketcher.Constraint('PointOnObject', geos[0], 2, -2))
    constraint_i += 1
    sketchObj.addConstraint(Sketcher.Constraint('Radius', geos[sides], 10.0000))
    radius_constraint_i = constraint_i
    constraint_i += 1
    sketchObj.recompute()

    instancePrefix = sketchObj.Label.replace('sketch', '')
    callsheet_Label = f"{instancePrefix}callsheet"
    sketchObj.setExpression(f"Constraints[{radius_constraint_i}]", f"<<{callsheet_Label}>>.radius")   

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

    # myInstance.redraw_sketch(sides=4) # redraw sketch with 4 sides


if __name__ == '__main__':
    main()
