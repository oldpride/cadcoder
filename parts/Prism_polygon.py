from FreeCAD import Vector, Placement, Rotation
from math import cos, sin, pi
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.baseClass import baseClass
from cadcoder.containertools import get_LCS_by_prefix

class prism_polygon(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, prism_polygon_height_spec='0.5 in', horizontalScale=1.1982, prism_polygon_radius_spec='1 in', prism_polygon_sides=8, verticalScale=1.261,  ):
        self.horizontalScale = horizontalScale
        self.prism_polygon_height_spec = prism_polygon_height_spec
        self.prism_polygon_radius_spec = prism_polygon_radius_spec
        self.prism_polygon_sides = prism_polygon_sides
        self.verticalScale = verticalScale
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        
        # adjust placement of top-level directly imported objects if needed. static values only.
        
        # add objects and add static value to objects' properties based on object dependencies
        body = doc.addObject('PartDesign::Body', self.addPrefix('body') )
        body.Label = self.addPrefix('body')
        self.body = body # expose as instance variable using Label varname
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
        body.recompute()  # recompute after adding object
        callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('callsheet') )
        callsheet.Label = self.addPrefix('callsheet')
        self.callsheet = callsheet # expose as instance variable using Label varname
        self.post_new_obj(callsheet)
        callsheet.set('A1', 'variableName')
        callsheet.set('A2', 'prism_polygon_sides')
        callsheet.set('A3', 'horizontalScale')
        callsheet.set('A4', 'verticalScale')
        callsheet.set('A5', 'prism_polygon_radius_spec')
        callsheet.set('A6', 'prism_polygon_radius')
        callsheet.set('A7', 'prism_polygon_height_spec')
        callsheet.set('A8', 'prism_polygon_height')
        callsheet.set('B1', 'value')
        callsheet.set('B2', '8')
        callsheet.setAlias('B2', 'prism_polygon_sides')
        callsheet.set('B2', f'{self.prism_polygon_sides}') # call param
        callsheet.set('B3', '1.1982')
        callsheet.setAlias('B3', 'horizontalScale')
        callsheet.set('B3', f'{self.horizontalScale}') # call param
        callsheet.set('B4', '1.261')
        callsheet.setAlias('B4', 'verticalScale')
        callsheet.set('B4', f'{self.verticalScale}') # call param
        callsheet.set('B5', '=1 in')
        callsheet.setAlias('B5', 'prism_polygon_radius_spec')
        callsheet.set('B5', f'={self.prism_polygon_radius_spec}') # call param
        callsheet.set('B6', '=1.1982 in')
        callsheet.setAlias('B6', 'prism_polygon_radius')
        callsheet.set('B7', '=0.5 in')
        callsheet.setAlias('B7', 'prism_polygon_height_spec')
        callsheet.set('B7', f'={self.prism_polygon_height_spec}') # call param
        callsheet.set('B8', '=0.6305 in')
        callsheet.setAlias('B8', 'prism_polygon_height')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C2', 'Y')
        callsheet.set('C3', 'Y')
        callsheet.set('C4', 'Y')
        callsheet.set('C5', 'Y')
        callsheet.set('C6', 'N')
        callsheet.set('C7', 'Y')
        callsheet.set('C8', 'N')
        callsheet.set('D1', 'comment')
        callsheet.set('D2', 'number of sides of a polygon')
        callsheet.set('D3', 'BASF 17-4 xy scale 1.1982')
        callsheet.set('D4', 'BASF 17-4 z scale 1.2610')
        callsheet.set('D5', 'radius of circle circumferencing polygon')
        callsheet.set('D7', 'pad height')
        callsheet.recompute()  # recompute after adding object
        sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('sketch') )
        sketch.Label = self.addPrefix('sketch')
        self.sketch = sketch # expose as instance variable using Label varname
        self.post_new_obj(sketch)
        self.container_append_object(body, sketch)
        # geo0 = prism_polygon_sketch.addGeometry(Part.LineSegment(Vector (9.99998, 0.0, 0.0), Vector (0.0, 9.99998, 0.0)))
        # geo1 = prism_polygon_sketch.addGeometry(Part.LineSegment(Vector (0.0, 9.99998, 0.0), Vector (-9.99998, 0.0, 0.0)))
        # geo2 = prism_polygon_sketch.addGeometry(Part.LineSegment(Vector (-9.99998, -7.020610351606955e-16, 0.0), Vector (0.0, -9.99998, 0.0)))
        # geo3 = prism_polygon_sketch.addGeometry(Part.LineSegment(Vector (-3.194361284757029e-21, -9.99998, 0.0), Vector (9.99998, 0.0, 0.0)))
        # geo4 = prism_polygon_sketch.addGeometry(Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 10.0000))
        # prism_polygon_sketch.toggleConstruction(geo4)
        # prism_polygon_sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 2, geo1, 1))
        # prism_polygon_sketch.addConstraint(Sketcher.Constraint('Coincident', geo1, 2, geo2, 1))
        # prism_polygon_sketch.addConstraint(Sketcher.Constraint('Coincident', geo2, 2, geo3, 1))
        # prism_polygon_sketch.addConstraint(Sketcher.Constraint('Coincident', geo3, 2, geo0, 1))
        # prism_polygon_sketch.addConstraint(Sketcher.Constraint('Equal', geo0, geo1))
        # prism_polygon_sketch.addConstraint(Sketcher.Constraint('Equal', geo0, geo2))
        # prism_polygon_sketch.addConstraint(Sketcher.Constraint('Equal', geo0, geo3))
        # prism_polygon_sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo0, 2, geo4))
        # prism_polygon_sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo1, 2, geo4))
        # prism_polygon_sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo2, 2, geo4))
        # prism_polygon_sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo3, 2, geo4))
        # prism_polygon_sketch.addConstraint(Sketcher.Constraint('Coincident', geo4, 3, -1, 1))
        # prism_polygon_sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo0, 2, -2))
        
        geo = []
        for i in range(self.prism_polygon_sides):
            # cos(), sin() in math module use radians!!!
            # cos(), sin() in freecad expression use degrees!!!
            theta0 = 2*pi * i / self.prism_polygon_sides
            theta1 = 2*pi * (i+1) / self.prism_polygon_sides
            geo.append(sketch.addGeometry(
                Part.LineSegment(Vector(cos(theta0)*10, sin(theta0)*10, 0), 
                                 Vector(cos(theta1)*10, sin(theta1)*10, 0))))
    
        geo.append(sketch.addGeometry(
            Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 10))) # radius
        
        sketch.toggleConstruction(geo[prism_polygon_sides])

        constraint_i = 0
        for i in range(self.prism_polygon_sides):
            j = (i+1) % self.prism_polygon_sides
            sketch.addConstraint(Sketcher.Constraint('Coincident', geo[i], 2, geo[j], 1))
            constraint_i += 1

        for i in range(self.prism_polygon_sides-1):
            sketch.addConstraint(Sketcher.Constraint('Equal', geo[0], geo[i+1]))
            constraint_i += 1

        for i in range(self.prism_polygon_sides):
            j = (i+1) % self.prism_polygon_sides
            sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo[i], 2, geo[prism_polygon_sides]))
            constraint_i += 1

        sketch.addConstraint(Sketcher.Constraint('Coincident', geo[prism_polygon_sides], 3, -1, 1))
        constraint_i += 1
        sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo[0], 2, -2))
        constraint_i += 1
        sketch.addConstraint(Sketcher.Constraint('Radius', geo[prism_polygon_sides], 10.0000))
        radius_constraint_i = constraint_i
        constraint_i += 1
        # prism_polygon_sketch.addConstraint(Sketcher.Constraint('Radius', geo[prism_polygon_sides], radius))
        sketch.AttacherEngine = 'Engine Plane'
        from cadcoder.subelementtools import get_seName_by_posName
        sketch.AttachmentSupport = (body_XY_Plane, (''))
        body_XY_Plane.Visibility = False  # hide base object
        sketch.MapMode = 'FlatFace'
        sketch.Visibility = False
        sketch.recompute()  # recompute after adding object
        pad = doc.addObject('PartDesign::Pad', self.addPrefix('pad') )
        pad.Label = self.addPrefix('pad')
        self.pad = pad # expose as instance variable using Label varname
        self.post_new_obj(pad)
        self.container_append_object(body, pad)
        pad.AllowMultiFace = False
        pad.Length = 16.014699999999998
        pad.Profile = (sketch, [])
        pad.ReferenceAxis = (sketch, ['N_Axis'])
        pad.recompute()  # recompute after adding object
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        callsheet.set(callsheet.getCellFromAlias("prism_polygon_radius"), f"=prism_polygon_radius_spec * horizontalScale")
        callsheet.set(callsheet.getCellFromAlias("prism_polygon_height"), f"=prism_polygon_height_spec * verticalScale")
        pad.setExpression("Length", f"<<{self.addPrefix('callsheet')}>>.prism_polygon_height")
        sketch.setExpression(f"Constraints[{radius_constraint_i}]", f"<<{self.addPrefix('callsheet')}>>.prism_polygon_radius")
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # set callsheet
        self.callsheet = self.callsheet
        self.update_callsheet()


def main():
    # main_part1
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of Prism_polygon
    myInstance = prism_polygon("myInstance", doc, objPrefix="", useLabel=True, importer=None, prism_polygon_height_spec='0.5 in', horizontalScale=1.1982, prism_polygon_radius_spec='1 in', prism_polygon_sides=8, verticalScale=1.261, )
    
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
