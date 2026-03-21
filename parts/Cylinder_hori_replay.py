from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.baseClass import baseClass
from pdfclib.containertools import get_LCS_by_prefix
from pdfclib.objtools import update_obj_prop_jsonDict

class Cylinder_hori(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, cylinder_pad_length_spec='0.5 in', cylinder_radius_y_spec='0.5 in', cylinder_radius_z_spec='0.5 in', horizontalScale=1.1982, verticalScale=1.261,  ):
        self.cylinder_pad_length_spec = cylinder_pad_length_spec
        self.cylinder_radius_y_spec = cylinder_radius_y_spec
        self.cylinder_radius_z_spec = cylinder_radius_z_spec
        self.horizontalScale = horizontalScale
        self.verticalScale = verticalScale
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        
        # adjust placement and visibility of top-level directly imported objects; static values only
        
        # add objects and add static value to objects' properties based on object dependencies
        cylinder_hori = doc.addObject('PartDesign::Body', self.addPrefix('Body') )
        cylinder_hori.Label = self.addPrefix('cylinder_hori')
        self.cylinder_hori = cylinder_hori # expose as instance variable using Label varname
        self.post_new_obj(cylinder_hori)
        cylinder_hori_Origin = get_LCS_by_prefix(doc, cylinder_hori, 'Origin') # source objName=Origin
        cylinder_hori_X_Axis = get_LCS_by_prefix(doc, cylinder_hori, 'X_Axis') # source objName=X_Axis
        cylinder_hori_Y_Axis = get_LCS_by_prefix(doc, cylinder_hori, 'Y_Axis') # source objName=Y_Axis
        cylinder_hori_Z_Axis = get_LCS_by_prefix(doc, cylinder_hori, 'Z_Axis') # source objName=Z_Axis
        cylinder_hori_XY_Plane = get_LCS_by_prefix(doc, cylinder_hori, 'XY_Plane') # source objName=XY_Plane
        cylinder_hori_XZ_Plane = get_LCS_by_prefix(doc, cylinder_hori, 'XZ_Plane') # source objName=XZ_Plane
        cylinder_hori_YZ_Plane = get_LCS_by_prefix(doc, cylinder_hori, 'YZ_Plane') # source objName=YZ_Plane
        self.cylinder_hori_Origin = cylinder_hori_Origin # expose as instance variable using Label varname
        self.cylinder_hori_X_Axis = cylinder_hori_X_Axis # expose as instance variable using Label varname
        self.cylinder_hori_Y_Axis = cylinder_hori_Y_Axis # expose as instance variable using Label varname
        self.cylinder_hori_Z_Axis = cylinder_hori_Z_Axis # expose as instance variable using Label varname
        self.cylinder_hori_XY_Plane = cylinder_hori_XY_Plane # expose as instance variable using Label varname
        self.cylinder_hori_XZ_Plane = cylinder_hori_XZ_Plane # expose as instance variable using Label varname
        self.cylinder_hori_YZ_Plane = cylinder_hori_YZ_Plane # expose as instance variable using Label varname
        self.post_new_obj(cylinder_hori_Origin)
        self.post_new_obj(cylinder_hori_X_Axis)
        self.post_new_obj(cylinder_hori_Y_Axis)
        self.post_new_obj(cylinder_hori_Z_Axis)
        self.post_new_obj(cylinder_hori_XY_Plane)
        self.post_new_obj(cylinder_hori_XZ_Plane)
        self.post_new_obj(cylinder_hori_YZ_Plane)
        cylinder_hori.recompute()  # recompute after adding object

        cylinder_hori_callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('cylinder_hori_callsheet') )
        cylinder_hori_callsheet.Label = self.addPrefix('cylinder_hori_callsheet')
        self.cylinder_hori_callsheet = cylinder_hori_callsheet # expose as instance variable using Label varname
        self.post_new_obj(cylinder_hori_callsheet)
        cylinder_hori_callsheet.set('A1', 'variableName')
        cylinder_hori_callsheet.set('A2', 'horizontalScale')
        cylinder_hori_callsheet.set('A3', 'verticalScale')
        cylinder_hori_callsheet.set('A4', 'cylinder_radius_y_spec')
        cylinder_hori_callsheet.set('A5', 'cylinder_radius_y')
        cylinder_hori_callsheet.set('A6', 'cylinder_radius_z_spec')
        cylinder_hori_callsheet.set('A7', 'cylinder_radius_z')
        cylinder_hori_callsheet.set('A8', 'cylinder_pad_length_spec')
        cylinder_hori_callsheet.set('A9', 'cylinder_pad_length')
        cylinder_hori_callsheet.set('B1', 'value')
        cylinder_hori_callsheet.set('B2', '1.1982')
        cylinder_hori_callsheet.setAlias('B2', 'horizontalScale')
        cylinder_hori_callsheet.set('B2', f'{self.horizontalScale}') # call param
        cylinder_hori_callsheet.set('B3', '1.261')
        cylinder_hori_callsheet.setAlias('B3', 'verticalScale')
        cylinder_hori_callsheet.set('B3', f'{self.verticalScale}') # call param
        cylinder_hori_callsheet.set('B4', '=0.5 in')
        cylinder_hori_callsheet.setAlias('B4', 'cylinder_radius_y_spec')
        cylinder_hori_callsheet.set('B4', f'={self.cylinder_radius_y_spec}') # call param
        cylinder_hori_callsheet.set('B5', '=0.5991 in')
        cylinder_hori_callsheet.setAlias('B5', 'cylinder_radius_y')
        cylinder_hori_callsheet.set('B6', '=0.5 in')
        cylinder_hori_callsheet.setAlias('B6', 'cylinder_radius_z_spec')
        cylinder_hori_callsheet.set('B6', f'={self.cylinder_radius_z_spec}') # call param
        cylinder_hori_callsheet.set('B7', '=0.6305 in')
        cylinder_hori_callsheet.setAlias('B7', 'cylinder_radius_z')
        cylinder_hori_callsheet.set('B8', '=0.5 in')
        cylinder_hori_callsheet.setAlias('B8', 'cylinder_pad_length_spec')
        cylinder_hori_callsheet.set('B8', f'={self.cylinder_pad_length_spec}') # call param
        cylinder_hori_callsheet.set('B9', '=0.5991 in')
        cylinder_hori_callsheet.setAlias('B9', 'cylinder_pad_length')
        cylinder_hori_callsheet.set('C1', 'isCallParam')
        cylinder_hori_callsheet.set('C2', 'Y')
        cylinder_hori_callsheet.set('C3', 'Y')
        cylinder_hori_callsheet.set('C4', 'Y')
        cylinder_hori_callsheet.set('C5', 'N')
        cylinder_hori_callsheet.set('C6', 'Y')
        cylinder_hori_callsheet.set('C7', 'N')
        cylinder_hori_callsheet.set('C8', 'Y')
        cylinder_hori_callsheet.set('C9', 'N')
        cylinder_hori_callsheet.set('D1', 'comment')
        cylinder_hori_callsheet.set('D2', 'BASF 17-4 xy scale 1.1982')
        cylinder_hori_callsheet.set('D3', 'BASF 17-4 z scale 1.2610')
        cylinder_hori_callsheet.set('D4', 'y radius')
        cylinder_hori_callsheet.set('D6', 'z radius')
        cylinder_hori_callsheet.set('D8', 'pad length')
        cylinder_hori_callsheet.recompute()  # recompute after adding object
        
        cylinder_hori_sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('Sketch') )
        cylinder_hori_sketch.Label = self.addPrefix('cylinder_hori_sketch')
        self.cylinder_hori_sketch = cylinder_hori_sketch # expose as instance variable using Label varname
        self.post_new_obj(cylinder_hori_sketch)
        self.container_append_object(cylinder_hori, cylinder_hori_sketch)

        # # Create ellipse: major along Z (3), minor along Y (2)
        # ellipse = Part.Ellipse(
        #     App.Vector(0, 0, 0),                # center
        #     App.Vector(0, 2, 0),                # point on minor (Y)
        #     App.Vector(0, 0, 3)                 # point on major (Z)
        # )

        # geo_ellipse = cylinder_hori_sketch.addGeometry(ellipse)
        # print(f"geo_ellipse={geo_ellipse}")
        # cylinder_hori_sketch.addConstraint(Sketcher.Constraint('Coincident', geo_ellipse, 1, -1, 1))      # center → origin
        # cylinder_hori_sketch.addConstraint(Sketcher.Constraint('Vertical', geo_ellipse))                   # major axis vertical
        # cylinder_hori_sketch.addConstraint(Sketcher.Constraint('Distance', geo_ellipse, 3, App.Units.Quantity('3 mm')))  # major semi = 3
        # cylinder_hori_sketch.addConstraint(Sketcher.Constraint('Distance', geo_ellipse, 2, App.Units.Quantity('2 mm')))  # minor semi = 2

        # cylinder_hori_sketch.solve()
        # doc.recompute()
        # geo0 = cylinder_hori_sketch.addGeometry(Part.Ellipse(Vector(0.0000, 0.0000, 0.0000), 7.620000000029982, 5.080000000000037))
        # geo1 = cylinder_hori_sketch.addGeometry(Part.LineSegment(Vector (0.0, 7.62, 0.0), Vector (-1.3535889121665592e-22, -7.62, 0.0)))
        # cylinder_hori_sketch.toggleConstruction(geo1)
        # geo2 = cylinder_hori_sketch.addGeometry(Part.LineSegment(Vector (-5.0800000000000995, 2.5181671619805657e-12, 0.0), Vector (5.0800000000000995, -2.5181671602864998e-12, 0.0)))
        # cylinder_hori_sketch.toggleConstruction(geo2)
        # geo3 = cylinder_hori_sketch.addGeometry(Part.Point(Vector(-0.0000, 5.6796, 0.0000)))
        # cylinder_hori_sketch.toggleConstruction(geo3)
        # geo4 = cylinder_hori_sketch.addGeometry(Part.Point(Vector(0.0000, -5.6796, 0.0000)))
        # cylinder_hori_sketch.toggleConstruction(geo4)
        # cylinder_hori_sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 3, -1, 1))
        # cylinder_hori_sketch.addConstraint(Sketcher.Constraint('Distance', geo2, 2, geo0, 3, 5.0800))
        # cylinder_hori_sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo1, 1, -2))
        # cylinder_hori_sketch.addConstraint(Sketcher.Constraint('DistanceY', geo0, 3, geo1, 1, 7.6200))

        # constraints = []
        # # sketch = App.ActiveDocument.ActiveObject  # or your sketch name
        # constraints.append(Sketcher.Constraint('InternalAlignment', 1, 0, 0, 0, -2000, 0, 0.0)) # constraint1
        # constraints.append(Sketcher.Constraint('InternalAlignment', 2, 0, 0, 0, -2000, 0, 0.0)) # constraint2
        # constraints.append(Sketcher.Constraint('InternalAlignment', 3, 1, 0, 0, -2000, 0, 0.0)) # constraint3
        # constraints.append(Sketcher.Constraint('InternalAlignment', 4, 1, 0, 0, -2000, 0, 0.0)) # constraint4
        # constraints.append(Sketcher.Constraint('Coincident', 0, 3, 1, -2000, 0, 0.0)) # constraint5
        # constraints.append(Sketcher.Constraint('Distance', 2, 2, 0, 3, -2000, 0, App.Units.Quantity('5.08 mm'))) # constraint6
        # constraints.append(Sketcher.Constraint('PointOnObject', 1, 1, -2, 0, -2000, 0, 0.0)) # constraint7
        # constraints.append(Sketcher.Constraint('DistanceY', 0, 3, 1, 1, -2000, 0, App.Units.Quantity('7.62 mm'))) # constraint8
        # cylinder_hori_sketch.addConstraint(constraints)
        # cylinder_hori_sketch.solve()

        '''
        09:32:11      modified: MainObject-Constraints
        09:32:11        Object value:
        09:32:11          propType: Sketcher::PropertyConstraintList
        09:32:11          propValue: [<Constraint 'InternalAlignment:EllipseMajorDiameter'>, 
        <Constraint 'InternalAlignment:EllipseMinorDiameter'>, <Constraint 'InternalAlignment:EllipseFocus1'>, 
        <Constraint 'InternalAlignment:EllipseFocus2'>, <Constraint 'Coincident'>, 
        <Constraint 'Distance'>, <Constraint 'PointOnObject' (1,-2)>, <Constraint 'DistanceY'>]
        09:32:11          readonly: False
        09:32:11          valueClass: list
        09:32:11          valueClassTree: {'list/Constraint'}
        09:32:11          valueObjName: None
        09:32:11          valuePython: [<Constraint 'InternalAlignment:EllipseMajorDiameter'>, 
        <Constraint 'InternalAlignment:EllipseMinorDiameter'>, <Constraint 'InternalAlignment:EllipseFocus1'>, 
        <Constraint 'InternalAlignment:EllipseFocus2'>, <Constraint 'Coincident'>, 
        <Constraint 'Distance'>, <Constraint 'PointOnObject' (1,-2)>, <Constraint 'DistanceY'>]
        09:32:11          valueTypeId: None
        09:32:11          prefixPython: [<Constraint 'InternalAlignment:EllipseMajorDiameter'>, 
        <Constraint 'InternalAlignment:EllipseMinorDiameter'>, <Constraint 'InternalAlignment:EllipseFocus1'>, 
        <Constraint 'InternalAlignment:EllipseFocus2'>, <Constraint 'Coincident'>, 
        <Constraint 'Distance'>, <Constraint 'PointOnObject' (1,-2)>, <Constraint 'DistanceY'>]
        09:32:11          propName: Constraints
        09:32:11        Default value:
        09:32:11          propType: Sketcher::PropertyConstraintList
        09:32:11          propValue: []
        09:32:11          readonly: False
        09:32:11          valueClass: list
        09:32:11          valueClassTree: {'list'}
        09:32:11          valueObjName: None
        09:32:11          valuePython: []
        09:32:11          valueTypeId: None
        09:32:11          prefixPython: []
        09:32:11          propName: Constraints
        '''
        from pdfclib.subelementtools import get_seName_by_posName
        cylinder_hori_sketch.AttachmentSupport = (cylinder_hori_YZ_Plane, (''))
        cylinder_hori_YZ_Plane.Visibility = False  # hide base object
        cylinder_hori_sketch.MapMode = 'FlatFace'

        # Create ellipse: major along Z (3), minor along Y (2)
        # ellipse = Part.Ellipse(
        #     App.Vector(0, 0, 0),                # center
        #     App.Vector(0, 2, 0),                # point on minor (Y)
        #     App.Vector(0, 0, 3)                 # point on major (Z)
        # )
        ellipse = Part.Ellipse(App.Vector(0.000000, 30.103247, 0.000000), App.Vector(-11.649301, 0.000000, 0.000000), App.Vector(0.000000, 0.000000, 0.000000))

        geo_ellipse = cylinder_hori_sketch.addGeometry(ellipse)
        print(f"geo_ellipse={geo_ellipse}")
        cylinder_hori_sketch.exposeInternalGeometry(0)
        # cylinder_hori_sketch.addConstraint(Sketcher.Constraint('Coincident', geo_ellipse, 3, -1, 1))      # center → origin
        # cylinder_hori_sketch.addConstraint(Sketcher.Constraint('PointOnObject',1,1,-2))                   # major axis vertical
        # cylinder_hori_sketch.addConstraint(Sketcher.Constraint('DistanceY',geo_ellipse,3,1,1,30.103247))  # major semi = 3
        # cylinder_hori_sketch.setDatum(6,App.Units.Quantity('7.620000 mm')) # 0.3 in
        # cylinder_hori_sketch.addConstraint(Sketcher.Constraint('DistanceX',geo_ellipse,3,2,2,0.652827))  # minor semi = 2
        # cylinder_hori_sketch.setDatum(7,App.Units.Quantity('5.080000 mm')) # 0.2 in

        constraints = []
        # the first 4 are internal from Part.Ellipse
        # constraints.append(Sketcher.Constraint('InternalAlignment:EllipseMajorDiameter', 1, 0)) # constraint1
        # constraints.append(Sketcher.Constraint('InternalAlignment:EllipseMinorDiameter', 2, 0)) # constraint2
        # constraints.append(Sketcher.Constraint('InternalAlignment:EllipseFocus1', 3, 1, 0)) # constraint3
        # constraints.append(Sketcher.Constraint('InternalAlignment:EllipseFocus2', 4, 1, 0)) # constraint4
        constraints.append(Sketcher.Constraint('Coincident', 0, 3, -1, 1)) # constraint5
        constraints.append(Sketcher.Constraint('PointOnObject', 1, 1, -2)) # constraint6
        constraints.append(Sketcher.Constraint('DistanceY', 0, 3, 1, 1, App.Units.Quantity('15.24 mm'))) # constraint7
        constraints.append(Sketcher.Constraint('DistanceX', 0, 3, 2, 2, App.Units.Quantity('10.16 mm'))) # constraint8
        cylinder_hori_sketch.addConstraint(constraints)
        cylinder_hori_sketch.solve()

        cylinder_hori_sketch.Visibility = False
        cylinder_hori_sketch.ViewObject.Visibility = False
        cylinder_hori_sketch.recompute()  # recompute after adding object
        
        cylinder_hori_pad = doc.addObject('PartDesign::Pad', self.addPrefix('Pad') )
        cylinder_hori_pad.Label = self.addPrefix('cylinder_hori_pad')
        self.cylinder_hori_pad = cylinder_hori_pad # expose as instance variable using Label varname
        self.post_new_obj(cylinder_hori_pad)
        self.container_append_object(cylinder_hori, cylinder_hori_pad)
        cylinder_hori_pad.Length = 10.16
        cylinder_hori_pad.Profile = (cylinder_hori_sketch, [''])
        cylinder_hori_pad.ReferenceAxis = (cylinder_hori_sketch, ['N_Axis'])
        cylinder_hori_pad.recompute()  # recompute after adding object
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        cylinder_hori_callsheet.set("B5", f"=cylinder_radius_y_spec * horizontalScale") # B5's alias=cylinder_radius_y
        cylinder_hori_callsheet.set("B7", f"=cylinder_radius_z_spec * verticalScale") # B7's alias=cylinder_radius_z
        cylinder_hori_callsheet.set("B9", f"=cylinder_pad_length_spec * horizontalScale") # B9's alias=cylinder_pad_length
        cylinder_hori_pad.setExpression("Length", f"<<{self.addPrefix('cylinder_hori_callsheet')}>>.cylinder_pad_length")
        cylinder_hori_sketch.setExpression("Constraints[6]", f"<<{self.addPrefix('cylinder_hori_callsheet')}>>.cylinder_radius_z")
        cylinder_hori_sketch.setExpression("Constraints[7]", f"<<{self.addPrefix('cylinder_hori_callsheet')}>>.cylinder_radius_y")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # create empty callsheet spreadsheet label and varname=cylinder_hori_callsheet
        cylinder_hori_callsheet.recompute() # recompute sheet to make new cells available
        
        # set callsheet
        self.callsheet = self.cylinder_hori_callsheet
        self.update_callsheet()


def main():
    # main_part1
    from pdfclib.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of Cylinder_hori
    myInstance = Cylinder_hori("myInstance", doc, objPrefix="", useLabel=True, importer=None, )
    
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
