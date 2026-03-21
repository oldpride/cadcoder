from FreeCAD import Vector, Placement, Rotation
from math import cos, sin, pi
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.baseClass import baseClass
from pdfclib.containertools import get_LCS_by_prefix

class Prism_polygon(baseClass):
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
        prism_polygon = doc.addObject('PartDesign::Body', self.addPrefix('Body') )
        prism_polygon.Label = self.addPrefix('prism_polygon')
        self.prism_polygon = prism_polygon # expose as instance variable using Label varname
        self.post_new_obj(prism_polygon)
        prism_polygon_Origin = get_LCS_by_prefix(doc, prism_polygon, 'Origin') # source objName=Origin
        prism_polygon_X_Axis = get_LCS_by_prefix(doc, prism_polygon, 'X_Axis') # source objName=X_Axis
        prism_polygon_Y_Axis = get_LCS_by_prefix(doc, prism_polygon, 'Y_Axis') # source objName=Y_Axis
        prism_polygon_Z_Axis = get_LCS_by_prefix(doc, prism_polygon, 'Z_Axis') # source objName=Z_Axis
        prism_polygon_XY_Plane = get_LCS_by_prefix(doc, prism_polygon, 'XY_Plane') # source objName=XY_Plane
        prism_polygon_XZ_Plane = get_LCS_by_prefix(doc, prism_polygon, 'XZ_Plane') # source objName=XZ_Plane
        prism_polygon_YZ_Plane = get_LCS_by_prefix(doc, prism_polygon, 'YZ_Plane') # source objName=YZ_Plane
        self.prism_polygon_Origin = prism_polygon_Origin # expose as instance variable using Label varname
        self.prism_polygon_X_Axis = prism_polygon_X_Axis # expose as instance variable using Label varname
        self.prism_polygon_Y_Axis = prism_polygon_Y_Axis # expose as instance variable using Label varname
        self.prism_polygon_Z_Axis = prism_polygon_Z_Axis # expose as instance variable using Label varname
        self.prism_polygon_XY_Plane = prism_polygon_XY_Plane # expose as instance variable using Label varname
        self.prism_polygon_XZ_Plane = prism_polygon_XZ_Plane # expose as instance variable using Label varname
        self.prism_polygon_YZ_Plane = prism_polygon_YZ_Plane # expose as instance variable using Label varname
        prism_polygon.recompute()  # recompute after adding object
        prism_polygon_callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('prism_polygon_callsheet') )
        prism_polygon_callsheet.Label = self.addPrefix('prism_polygon_callsheet')
        self.prism_polygon_callsheet = prism_polygon_callsheet # expose as instance variable using Label varname
        self.post_new_obj(prism_polygon_callsheet)
        prism_polygon_callsheet.set('A1', 'variableName')
        prism_polygon_callsheet.set('A2', 'prism_polygon_sides')
        prism_polygon_callsheet.set('A3', 'horizontalScale')
        prism_polygon_callsheet.set('A4', 'verticalScale')
        prism_polygon_callsheet.set('A5', 'prism_polygon_radius_spec')
        prism_polygon_callsheet.set('A6', 'prism_polygon_radius')
        prism_polygon_callsheet.set('A7', 'prism_polygon_height_spec')
        prism_polygon_callsheet.set('A8', 'prism_polygon_height')
        prism_polygon_callsheet.set('B1', 'value')
        prism_polygon_callsheet.set('B2', '8')
        prism_polygon_callsheet.setAlias('B2', 'prism_polygon_sides')
        prism_polygon_callsheet.set('B2', f'{self.prism_polygon_sides}') # call param
        prism_polygon_callsheet.set('B3', '1.1982')
        prism_polygon_callsheet.setAlias('B3', 'horizontalScale')
        prism_polygon_callsheet.set('B3', f'{self.horizontalScale}') # call param
        prism_polygon_callsheet.set('B4', '1.261')
        prism_polygon_callsheet.setAlias('B4', 'verticalScale')
        prism_polygon_callsheet.set('B4', f'{self.verticalScale}') # call param
        prism_polygon_callsheet.set('B5', '=1 in')
        prism_polygon_callsheet.setAlias('B5', 'prism_polygon_radius_spec')
        prism_polygon_callsheet.set('B5', f'={self.prism_polygon_radius_spec}') # call param
        prism_polygon_callsheet.set('B6', '=1.1982 in')
        prism_polygon_callsheet.setAlias('B6', 'prism_polygon_radius')
        prism_polygon_callsheet.set('B7', '=0.5 in')
        prism_polygon_callsheet.setAlias('B7', 'prism_polygon_height_spec')
        prism_polygon_callsheet.set('B7', f'={self.prism_polygon_height_spec}') # call param
        prism_polygon_callsheet.set('B8', '=0.6305 in')
        prism_polygon_callsheet.setAlias('B8', 'prism_polygon_height')
        prism_polygon_callsheet.set('C1', 'isCallParam')
        prism_polygon_callsheet.set('C2', 'Y')
        prism_polygon_callsheet.set('C3', 'Y')
        prism_polygon_callsheet.set('C4', 'Y')
        prism_polygon_callsheet.set('C5', 'Y')
        prism_polygon_callsheet.set('C6', 'N')
        prism_polygon_callsheet.set('C7', 'Y')
        prism_polygon_callsheet.set('C8', 'N')
        prism_polygon_callsheet.set('D1', 'comment')
        prism_polygon_callsheet.set('D2', 'number of sides of a polygon')
        prism_polygon_callsheet.set('D3', 'BASF 17-4 xy scale 1.1982')
        prism_polygon_callsheet.set('D4', 'BASF 17-4 z scale 1.2610')
        prism_polygon_callsheet.set('D5', 'radius of circle circumferencing polygon')
        prism_polygon_callsheet.set('D7', 'pad height')
        prism_polygon_callsheet.recompute()  # recompute after adding object
        prism_polygon_sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('Sketch') )
        prism_polygon_sketch.Label = self.addPrefix('prism_polygon_sketch')
        self.prism_polygon_sketch = prism_polygon_sketch # expose as instance variable using Label varname
        self.post_new_obj(prism_polygon_sketch)
        self.container_append_object(prism_polygon, prism_polygon_sketch)
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
            geo.append(prism_polygon_sketch.addGeometry(
                Part.LineSegment(Vector(cos(theta0)*10, sin(theta0)*10, 0), 
                                 Vector(cos(theta1)*10, sin(theta1)*10, 0))))
    
        geo.append(prism_polygon_sketch.addGeometry(
            Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 10))) # radius
        
        prism_polygon_sketch.toggleConstruction(geo[prism_polygon_sides])

        constraint_i = 0
        for i in range(self.prism_polygon_sides):
            j = (i+1) % self.prism_polygon_sides
            prism_polygon_sketch.addConstraint(Sketcher.Constraint('Coincident', geo[i], 2, geo[j], 1))
            constraint_i += 1

        for i in range(self.prism_polygon_sides-1):
            prism_polygon_sketch.addConstraint(Sketcher.Constraint('Equal', geo[0], geo[i+1]))
            constraint_i += 1

        for i in range(self.prism_polygon_sides):
            j = (i+1) % self.prism_polygon_sides
            prism_polygon_sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo[i], 2, geo[prism_polygon_sides]))
            constraint_i += 1

        prism_polygon_sketch.addConstraint(Sketcher.Constraint('Coincident', geo[prism_polygon_sides], 3, -1, 1))
        constraint_i += 1
        prism_polygon_sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo[0], 2, -2))
        constraint_i += 1
        prism_polygon_sketch.addConstraint(Sketcher.Constraint('Radius', geo[prism_polygon_sides], 10.0000))
        radius_constraint_i = constraint_i
        constraint_i += 1
        # prism_polygon_sketch.addConstraint(Sketcher.Constraint('Radius', geo[prism_polygon_sides], radius))
        prism_polygon_sketch.AttacherEngine = 'Engine Plane'
        from pdfclib.subelementtools import get_seName_by_posName
        prism_polygon_sketch.AttachmentSupport = (prism_polygon_XY_Plane, (''))
        prism_polygon_XY_Plane.Visibility = False  # hide base object
        prism_polygon_sketch.MapMode = 'FlatFace'
        prism_polygon_sketch.Visibility = False
        prism_polygon_sketch.recompute()  # recompute after adding object
        prism_polygon_pad = doc.addObject('PartDesign::Pad', self.addPrefix('Pad') )
        prism_polygon_pad.Label = self.addPrefix('prism_polygon_pad')
        self.prism_polygon_pad = prism_polygon_pad # expose as instance variable using Label varname
        self.post_new_obj(prism_polygon_pad)
        self.container_append_object(prism_polygon, prism_polygon_pad)
        prism_polygon_pad.AllowMultiFace = False
        prism_polygon_pad.Length = 16.014699999999998
        prism_polygon_pad.Profile = (prism_polygon_sketch, [])
        prism_polygon_pad.ReferenceAxis = (prism_polygon_sketch, ['N_Axis'])
        prism_polygon_pad.recompute()  # recompute after adding object
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        prism_polygon_callsheet.set(prism_polygon_callsheet.getCellFromAlias("prism_polygon_radius"), f"=prism_polygon_radius_spec * horizontalScale")
        prism_polygon_callsheet.set(prism_polygon_callsheet.getCellFromAlias("prism_polygon_height"), f"=prism_polygon_height_spec * verticalScale")
        prism_polygon_pad.setExpression("Length", f"<<{self.addPrefix('prism_polygon_callsheet')}>>.prism_polygon_height")
        prism_polygon_sketch.setExpression(f"Constraints[{radius_constraint_i}]", f"<<{self.addPrefix('prism_polygon_callsheet')}>>.prism_polygon_radius")
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # set callsheet
        self.callsheet = self.prism_polygon_callsheet
        self.update_callsheet()


def main():
    # main_part1
    from pdfclib.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of Prism_polygon
    myInstance = Prism_polygon("myInstance", doc, objPrefix="", useLabel=True, importer=None, prism_polygon_height_spec='0.5 in', horizontalScale=1.1982, prism_polygon_radius_spec='1 in', prism_polygon_sides=8, verticalScale=1.261, )
    
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
