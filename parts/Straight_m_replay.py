from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.baseClass import baseClass
from pdfclib.containertools import get_LCS_by_prefix
from pdfclib.objtools import update_obj_prop_jsonDict
from pdfclib.subelementtools import update_objs_seName, update_doc_seName, get_seName_by_posName

class Straight_m(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, b_holeDiaExpansion_spec='0 mm', height_spec='1 in', horizontalScale=1.1982, pitch_spec='1 mm', radius_spec='0.2 in', verticalScale=1.261,  ):
        self.b_holeDiaExpansion_spec = b_holeDiaExpansion_spec
        self.height_spec = height_spec
        self.horizontalScale = horizontalScale
        self.pitch_spec = pitch_spec
        self.radius_spec = radius_spec
        self.verticalScale = verticalScale
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        
        # add objects and add static value to objects' properties based on object dependencies
        straight_m = doc.addObject('PartDesign::Body', self.addPrefix('Body') )
        straight_m.Label = self.addPrefix('straight_m')
        self.straight_m = straight_m # expose as instance variable using Label varname
        self.post_new_obj(straight_m)
        straight_m_Origin = get_LCS_by_prefix(doc, straight_m, 'Origin')
        straight_m_X_Axis = get_LCS_by_prefix(doc, straight_m, 'X_Axis')
        straight_m_Y_Axis = get_LCS_by_prefix(doc, straight_m, 'Y_Axis')
        straight_m_Z_Axis = get_LCS_by_prefix(doc, straight_m, 'Z_Axis')
        straight_m_XY_Plane = get_LCS_by_prefix(doc, straight_m, 'XY_Plane')
        straight_m_XZ_Plane = get_LCS_by_prefix(doc, straight_m, 'XZ_Plane')
        straight_m_YZ_Plane = get_LCS_by_prefix(doc, straight_m, 'YZ_Plane')
        self.straight_m_Origin = straight_m_Origin # expose as instance variable using Label varname
        self.straight_m_X_Axis = straight_m_X_Axis # expose as instance variable using Label varname
        self.straight_m_Y_Axis = straight_m_Y_Axis # expose as instance variable using Label varname
        self.straight_m_Z_Axis = straight_m_Z_Axis # expose as instance variable using Label varname
        self.straight_m_XY_Plane = straight_m_XY_Plane # expose as instance variable using Label varname
        self.straight_m_XZ_Plane = straight_m_XZ_Plane # expose as instance variable using Label varname
        self.straight_m_YZ_Plane = straight_m_YZ_Plane # expose as instance variable using Label varname
        self.post_new_obj(straight_m_Origin)
        self.post_new_obj(straight_m_X_Axis)
        self.post_new_obj(straight_m_Y_Axis)
        self.post_new_obj(straight_m_Z_Axis)
        self.post_new_obj(straight_m_XY_Plane)
        self.post_new_obj(straight_m_XZ_Plane)
        self.post_new_obj(straight_m_YZ_Plane)
        straight_m.recompute()  # recompute after adding object
        
        straight_m_callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('Spreadsheet') )
        straight_m_callsheet.Label = self.addPrefix('straight_m_callsheet')
        self.straight_m_callsheet = straight_m_callsheet # expose as instance variable using Label varname
        self.post_new_obj(straight_m_callsheet)
        straight_m_callsheet.set('A1', 'variableName')
        straight_m_callsheet.set('A10', 'thread_height')
        straight_m_callsheet.set('A11', 'cutter_side')
        straight_m_callsheet.set('A12', 'cutter_radius')
        straight_m_callsheet.set('A13', 'b_holeDiaExpansion_spec')
        straight_m_callsheet.set('A2', 'horizontalScale')
        straight_m_callsheet.set('A3', 'verticalScale')
        straight_m_callsheet.set('A4', 'radius_spec')
        straight_m_callsheet.set('A5', 'radius')
        straight_m_callsheet.set('A6', 'height_spec')
        straight_m_callsheet.set('A7', 'height')
        straight_m_callsheet.set('A8', 'pitch_spec')
        straight_m_callsheet.set('A9', 'pitch')
        straight_m_callsheet.set('B1', 'value')
        straight_m_callsheet.set('B10', '=1.3609999999999998 in')
        straight_m_callsheet.setAlias('B10', 'thread_height')
        straight_m_callsheet.set('B11', '=0.04959602362204724 in')
        straight_m_callsheet.setAlias('B11', 'cutter_side')
        straight_m_callsheet.set('B12', '=0.24203640000000004 in')
        straight_m_callsheet.setAlias('B12', 'cutter_radius')
        straight_m_callsheet.set('B13', '=0 mm')
        straight_m_callsheet.setAlias('B13', 'b_holeDiaExpansion_spec')
        straight_m_callsheet.set('B13', f'={self.b_holeDiaExpansion_spec}') # call param
        straight_m_callsheet.set('B2', '1.1982')
        straight_m_callsheet.setAlias('B2', 'horizontalScale')
        straight_m_callsheet.set('B2', f'{self.horizontalScale}') # call param
        straight_m_callsheet.set('B3', '1.261')
        straight_m_callsheet.setAlias('B3', 'verticalScale')
        straight_m_callsheet.set('B3', f'{self.verticalScale}') # call param
        straight_m_callsheet.set('B4', '=0.2 in')
        straight_m_callsheet.setAlias('B4', 'radius_spec')
        straight_m_callsheet.set('B4', f'={self.radius_spec}') # call param
        straight_m_callsheet.set('B5', '=0.23964000000000002 in')
        straight_m_callsheet.setAlias('B5', 'radius')
        straight_m_callsheet.set('B6', '=1 in')
        straight_m_callsheet.setAlias('B6', 'height_spec')
        straight_m_callsheet.set('B6', f'={self.height_spec}') # call param
        straight_m_callsheet.set('B7', '=1.261 in')
        straight_m_callsheet.setAlias('B7', 'height')
        straight_m_callsheet.set('B8', '=1 mm')
        straight_m_callsheet.setAlias('B8', 'pitch_spec')
        straight_m_callsheet.set('B8', f'={self.pitch_spec}') # call param
        straight_m_callsheet.set('B9', '=0.04964566929133858 in')
        straight_m_callsheet.setAlias('B9', 'pitch')
        straight_m_callsheet.set('C1', 'isCallParam')
        straight_m_callsheet.set('C10', 'N')
        straight_m_callsheet.set('C11', 'N')
        straight_m_callsheet.set('C12', 'N')
        straight_m_callsheet.set('C13', 'Y')
        straight_m_callsheet.set('C2', 'Y')
        straight_m_callsheet.set('C3', 'Y')
        straight_m_callsheet.set('C4', 'Y')
        straight_m_callsheet.set('C5', 'N')
        straight_m_callsheet.set('C6', 'Y')
        straight_m_callsheet.set('C7', 'N')
        straight_m_callsheet.set('C8', 'Y')
        straight_m_callsheet.set('C9', 'N')
        straight_m_callsheet.set('D1', 'comment')
        straight_m_callsheet.set('D13', 'b_ 0.03 in for 3D print')
        straight_m_callsheet.set('D2', 'BASF 17-4 xy scale 1.1982')
        straight_m_callsheet.set('D3', 'BASF 17-4 z scale 1.2610')
        straight_m_callsheet.recompute()  # recompute after adding object
        
        straight_m_circle_sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('Sketch') )
        straight_m_circle_sketch.Label = self.addPrefix('straight_m_circle_sketch')
        self.straight_m_circle_sketch = straight_m_circle_sketch # expose as instance variable using Label varname
        self.post_new_obj(straight_m_circle_sketch)
        self.container_append_object(straight_m, straight_m_circle_sketch)
        geo0 = straight_m_circle_sketch.addGeometry(Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 6.0869))
        straight_m_circle_sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 3, -1, 1))
        straight_m_circle_sketch.addConstraint(Sketcher.Constraint('Radius', geo0, 6.0869))
        straight_m_circle_sketch.AttacherEngine = 'Engine Plane'
        straight_m_circle_sketch.AttachmentSupport = (straight_m_XY_Plane, (''))
        straight_m_XY_Plane.Visibility = False  # hide base object
        straight_m_circle_sketch.MapMode = 'FlatFace'
        straight_m_circle_sketch.Visibility = False
        straight_m_circle_sketch.ViewObject.Visibility = False
        straight_m_circle_sketch.recompute()  # recompute after adding object
        
        straight_m_cutter_sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('Sketch001') )
        straight_m_cutter_sketch.Label = self.addPrefix('straight_m_cutter_sketch')
        self.straight_m_cutter_sketch = straight_m_cutter_sketch # expose as instance variable using Label varname
        self.post_new_obj(straight_m_cutter_sketch)
        self.container_append_object(straight_m, straight_m_cutter_sketch)
        geo0 = straight_m_cutter_sketch.addGeometry(Part.LineSegment(Vector (5.05676166872823, -0.6298641568851656, 0.0), Vector (6.14772456, 0.0, 0.0)))
        geo1 = straight_m_cutter_sketch.addGeometry(Part.LineSegment(Vector (6.14772456, 0.0, 0.0), Vector (6.14772456, -1.259739, 0.0)))
        geo2 = straight_m_cutter_sketch.addGeometry(Part.LineSegment(Vector (6.14772456, -1.259739, 0.0), Vector (5.05676166872823, -0.6298641568851657, 0.0)))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('Coincident', geo1, 1, geo0, 2))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('Vertical', geo1))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('Coincident', geo2, 1, geo1, 2))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('DistanceY', geo1, 2, geo1, 1, 1.2597))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('DistanceX', -1, 1, geo0, 2, 6.1477))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 1, geo2, 2))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo0, 2, -1))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('Angle', geo0, 2, geo1, 1, 1.0472))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('Angle', geo2, 2, geo0, 1, 1.0472))
        straight_m_cutter_sketch.AttacherEngine = 'Engine Plane'
        straight_m_cutter_sketch.AttachmentSupport = (straight_m_XZ_Plane, (''))
        straight_m_XZ_Plane.Visibility = False  # hide base object
        straight_m_cutter_sketch.MapMode = 'FlatFace'
        straight_m_cutter_sketch.Visibility = False
        straight_m_cutter_sketch.ViewObject.Visibility = False
        straight_m_cutter_sketch.recompute()  # recompute after adding object
        
        straight_m_helix = doc.addObject('Part::Helix', self.addPrefix('Helix') )
        straight_m_helix.Label = self.addPrefix('straight_m_helix')
        self.straight_m_helix = straight_m_helix # expose as instance variable using Label varname
        self.post_new_obj(straight_m_helix)
        straight_m_helix.Height = 34.569399999999995
        straight_m_helix.Pitch = 1.261
        straight_m_helix.Radius = 6.086856
        straight_m_helix.SegmentLength = 1.0
        straight_m_helix.Style = 'New style'
        straight_m_helix.Visibility = False
        straight_m_helix.ViewObject.Visibility = False
        straight_m_helix.recompute()  # recompute after adding object
        
        straight_m_helix_binder = doc.addObject('PartDesign::SubShapeBinder', self.addPrefix('Binder') )
        straight_m_helix_binder.Label = self.addPrefix('straight_m_helix_binder')
        self.straight_m_helix_binder = straight_m_helix_binder # expose as instance variable using Label varname
        self.post_new_obj(straight_m_helix_binder)
        self.container_append_object(straight_m, straight_m_helix_binder)
        straight_m_helix_binder.addProperty("App::PropertyMatrix", "Cache_Helix")
        straight_m_helix_binder.Cache_Helix = App.Matrix(1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0)
        straight_m_helix_binder.Context = (straight_m, 'Binder.')
        straight_m_helix_binder.Support = [(straight_m_helix, (''))]
        straight_m_helix_binder.Visibility = False
        straight_m_helix_binder.ViewObject.Visibility = False
        straight_m_helix_binder.recompute()  # recompute after adding object
        
        straight_m_pad = doc.addObject('PartDesign::Pad', self.addPrefix('Pad') )
        straight_m_pad.Label = self.addPrefix('straight_m_pad')
        self.straight_m_pad = straight_m_pad # expose as instance variable using Label varname
        self.post_new_obj(straight_m_pad)
        self.container_append_object(straight_m, straight_m_pad)
        straight_m_pad.Length = 32.029399999999995
        straight_m_pad.Profile = (straight_m_circle_sketch, [''])
        straight_m_pad.ReferenceAxis = (straight_m_circle_sketch, ['N_Axis'])
        straight_m_pad.Visibility = False
        straight_m_pad.ViewObject.Visibility = False
        straight_m_pad.recompute()  # recompute after adding object
        
        straight_m_subtractivepipe = doc.addObject('PartDesign::SubtractivePipe', self.addPrefix('SubtractivePipe') )
        straight_m_subtractivepipe.Label = self.addPrefix('straight_m_subtractivepipe')
        self.straight_m_subtractivepipe = straight_m_subtractivepipe # expose as instance variable using Label varname
        self.post_new_obj(straight_m_subtractivepipe)
        self.container_append_object(straight_m, straight_m_subtractivepipe)
        straight_m_subtractivepipe.BaseFeature = straight_m_pad
        straight_m_subtractivepipe.Mode = 'Frenet'
        straight_m_subtractivepipe.Profile = (straight_m_cutter_sketch, [])
        straight_m_subtractivepipe.Spine = (straight_m_helix_binder, [])
        straight_m_subtractivepipe.recompute()  # recompute after adding object
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        straight_m_callsheet.set(straight_m_callsheet.getCellFromAlias("radius"), f"=(radius_spec + b_holeDiaExpansion_spec) * horizontalScale") # B5's alias=radius
        straight_m_callsheet.set(straight_m_callsheet.getCellFromAlias("height"), f"=height_spec * verticalScale") # B7's alias=height
        straight_m_callsheet.set(straight_m_callsheet.getCellFromAlias("pitch"), f"=pitch_spec * verticalScale") # B9's alias=pitch
        straight_m_circle_sketch.setExpression("Constraints[1]", f"<<{self.addPrefix('straight_m_callsheet')}>>.radius")
        straight_m_helix.setExpression("Pitch", f"<<{self.addPrefix('straight_m_callsheet')}>>.pitch")
        straight_m_helix.setExpression("Radius", f"<<{self.addPrefix('straight_m_callsheet')}>>.radius")
        straight_m_pad.setExpression("Length", f"<<{self.addPrefix('straight_m_callsheet')}>>.height")
        straight_m_callsheet.set(straight_m_callsheet.getCellFromAlias("thread_height"), f"=height + 0.1 in") # B10's alias=thread_height
        straight_m_callsheet.set(straight_m_callsheet.getCellFromAlias("cutter_side"), f"=pitch * 0.999") # B11's alias=cutter_side
        straight_m_callsheet.set(straight_m_callsheet.getCellFromAlias("cutter_radius"), f"=radius * 1.01") # B12's alias=cutter_radius
        straight_m_cutter_sketch.setExpression("Constraints[3]", f"<<{self.addPrefix('straight_m_callsheet')}>>.cutter_side")
        straight_m_cutter_sketch.setExpression("Constraints[4]", f"<<{self.addPrefix('straight_m_callsheet')}>>.cutter_radius")
        straight_m_helix.setExpression("Height", f"<<{self.addPrefix('straight_m_callsheet')}>>.thread_height")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # set callsheet
        self.callsheet = self.straight_m_callsheet
        self.update_callsheet()


def main():
    # main_part1
    from pdfclib.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of Straight_m
    myInstance = Straight_m("myInstance", doc, objPrefix="", useLabel=True, importer=None, b_holeDiaExpansion_spec='0 mm', height_spec='1 in', horizontalScale=1.1982, pitch_spec='1 mm', radius_spec='0.2 in', verticalScale=1.261, )
    
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
