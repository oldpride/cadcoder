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
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, height_spec='1 in', holeDiaExpansion_spec='0 mm', horizontalScale=1.1982, pitch_spec='1 mm', radius_spec='0.2 in', verticalScale=1.261,  ):
        self.height_spec = height_spec
        self.holeDiaExpansion_spec = holeDiaExpansion_spec
        self.horizontalScale = horizontalScale
        self.pitch_spec = pitch_spec
        self.radius_spec = radius_spec
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
        callsheet.set('A10', 'thread_height')
        callsheet.set('A11', 'cutter_side')
        callsheet.set('A12', 'cutter_radius')
        callsheet.set('A13', 'holeDiaExpansion_spec')
        callsheet.set('A2', 'horizontalScale')
        callsheet.set('A3', 'verticalScale')
        callsheet.set('A4', 'radius_spec')
        callsheet.set('A5', 'radius')
        callsheet.set('A6', 'height_spec')
        callsheet.set('A7', 'height')
        callsheet.set('A8', 'pitch_spec')
        callsheet.set('A9', 'pitch')
        callsheet.set('B1', 'value')
        callsheet.set('B10', '=1.3609999999999998 in')
        callsheet.setAlias('B10', 'thread_height')
        callsheet.set('B11', '=0.04959602362204724 in')
        callsheet.setAlias('B11', 'cutter_side')
        callsheet.set('B12', '=0.24203640000000004 in')
        callsheet.setAlias('B12', 'cutter_radius')
        callsheet.set('B13', '=0 mm')
        callsheet.setAlias('B13', 'holeDiaExpansion_spec')
        callsheet.set('B2', '1.1982')
        callsheet.setAlias('B2', 'horizontalScale')
        callsheet.set('B3', '1.261')
        callsheet.setAlias('B3', 'verticalScale')
        callsheet.set('B4', '=0.2 in')
        callsheet.setAlias('B4', 'radius_spec')
        callsheet.set('B5', '=0.23964000000000002 in')
        callsheet.setAlias('B5', 'radius')
        callsheet.set('B6', '=1 in')
        callsheet.setAlias('B6', 'height_spec')
        callsheet.set('B7', '=1.261 in')
        callsheet.setAlias('B7', 'height')
        callsheet.set('B8', '=1 mm')
        callsheet.setAlias('B8', 'pitch_spec')
        callsheet.set('B9', '=0.04964566929133858 in')
        callsheet.setAlias('B9', 'pitch')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C10', 'N')
        callsheet.set('C11', 'N')
        callsheet.set('C12', 'N')
        callsheet.set('C13', 'Y')
        callsheet.set('C2', 'Y')
        callsheet.set('C3', 'Y')
        callsheet.set('C4', 'Y')
        callsheet.set('C5', 'N')
        callsheet.set('C6', 'Y')
        callsheet.set('C7', 'N')
        callsheet.set('C8', 'Y')
        callsheet.set('C9', 'N')
        callsheet.set('D1', 'comment')
        callsheet.set('D13', 'b_ 0.03 in for 3D print')
        callsheet.set('D2', 'BASF 17-4 xy scale 1.1982')
        callsheet.set('D3', 'BASF 17-4 z scale 1.2610')
        callsheet.recompute()  # recompute after adding object
        
        circle_sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('circle_sketch') )
        circle_sketch.Label = self.addPrefix('straight_m_circle_sketch')
        self.circle_sketch = circle_sketch # expose as instance variable using Label varname
        self.post_new_obj(circle_sketch)
        self.container_append_object(body, circle_sketch)
        geo0 = circle_sketch.addGeometry(Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 6.0869))
        circle_sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 3, -1, 1))
        circle_sketch.addConstraint(Sketcher.Constraint('Radius', geo0, 6.0869))
        circle_sketch.AttacherEngine = 'Engine Plane'
        circle_sketch.AttachmentSupport = (body_XY_Plane, (''))
        body_XY_Plane.Visibility = False  # hide base object
        circle_sketch.MapMode = 'FlatFace'
        circle_sketch.Visibility = False
        circle_sketch.ViewObject.Visibility = False
        circle_sketch.recompute()  # recompute after adding object
        
        cutter_sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('cutter_sketch') )
        cutter_sketch.Label = self.addPrefix('straight_m_cutter_sketch')
        self.cutter_sketch = cutter_sketch # expose as instance variable using Label varname
        self.post_new_obj(cutter_sketch)
        self.container_append_object(body, cutter_sketch)
        geo0 = cutter_sketch.addGeometry(Part.LineSegment(Vector (5.05676166872823, -0.6298641568851653, 0.0), Vector (6.14772456, 0.0, 0.0)))
        geo1 = cutter_sketch.addGeometry(Part.LineSegment(Vector (6.14772456, 0.0, 0.0), Vector (6.14772456, -1.259739, 0.0)))
        geo2 = cutter_sketch.addGeometry(Part.LineSegment(Vector (6.14772456, -1.259739, 0.0), Vector (5.05676166872823, -0.6298641568851653, 0.0)))
        cutter_sketch.addConstraint(Sketcher.Constraint('Coincident', geo1, 1, geo0, 2))
        cutter_sketch.addConstraint(Sketcher.Constraint('Vertical', geo1))
        cutter_sketch.addConstraint(Sketcher.Constraint('Coincident', geo2, 1, geo1, 2))
        cutter_sketch.addConstraint(Sketcher.Constraint('DistanceY', geo1, 2, geo1, 1, 1.2597))
        cutter_sketch.addConstraint(Sketcher.Constraint('DistanceX', -1, 1, geo0, 2, 6.1477))
        cutter_sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 1, geo2, 2))
        cutter_sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo0, 2, -1))
        cutter_sketch.addConstraint(Sketcher.Constraint('Angle', geo0, 2, geo1, 1, 1.0472))
        cutter_sketch.addConstraint(Sketcher.Constraint('Angle', geo2, 2, geo0, 1, 1.0472))
        cutter_sketch.AttacherEngine = 'Engine Plane'
        cutter_sketch.AttachmentSupport = (body_XZ_Plane, (''))
        body_XZ_Plane.Visibility = False  # hide base object
        cutter_sketch.MapMode = 'FlatFace'
        cutter_sketch.Visibility = False
        cutter_sketch.ViewObject.Visibility = False
        cutter_sketch.recompute()  # recompute after adding object
        
        helix = doc.addObject('Part::Helix', self.addPrefix('helix') )
        helix.Label = self.addPrefix('straight_m_helix')
        self.helix = helix # expose as instance variable using Label varname
        self.post_new_obj(helix)
        helix.Height = 34.569399999999995
        helix.Pitch = 1.261
        helix.Radius = 6.086856
        helix.SegmentLength = 1.0
        helix.Style = 'New style'
        helix.Visibility = False
        helix.ViewObject.Visibility = False
        helix.recompute()  # recompute after adding object
        
        helix_binder = doc.addObject('PartDesign::SubShapeBinder', self.addPrefix('helix_binder') )
        helix_binder.Label = self.addPrefix('helix_binder')
        self.helix_binder = helix_binder # expose as instance variable using Label varname
        self.post_new_obj(helix_binder)
        self.container_append_object(body, helix_binder)
        helix_binder.addProperty("App::PropertyMatrix", "Cache_Helix")
        helix_binder.Cache_Helix = App.Matrix(1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0)
        helix_binder.Context = (body, 'Binder.')
        helix_binder.Support = [(helix, (''))]
        helix_binder.Visibility = False
        helix_binder.ViewObject.Visibility = False
        helix_binder.recompute()  # recompute after adding object
        
        pad = doc.addObject('PartDesign::Pad', self.addPrefix('pad') )
        pad.Label = self.addPrefix('pad')
        self.pad = pad # expose as instance variable using Label varname
        self.post_new_obj(pad)
        self.container_append_object(body, pad)
        pad.Length = 32.029399999999995
        pad.Profile = (circle_sketch, [''])
        pad.ReferenceAxis = (circle_sketch, ['N_Axis'])
        pad.Visibility = False
        pad.ViewObject.Visibility = False
        pad.recompute()  # recompute after adding object
        
        subtractivepipe = doc.addObject('PartDesign::SubtractivePipe', self.addPrefix('subtractivepipe') )
        subtractivepipe.Label = self.addPrefix('subtractivepipe')
        self.subtractivepipe = subtractivepipe # expose as instance variable using Label varname
        self.post_new_obj(subtractivepipe)
        self.container_append_object(body, subtractivepipe)
        subtractivepipe.BaseFeature = pad
        subtractivepipe.Mode = 'Frenet'
        subtractivepipe.Profile = (cutter_sketch, [])
        subtractivepipe.Spine = (helix_binder, [])
        subtractivepipe.recompute()  # recompute after adding object
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        callsheet.set(callsheet.getCellFromAlias("radius"), f"=(radius_spec + holeDiaExpansion_spec/2) * horizontalScale")
        callsheet.set(callsheet.getCellFromAlias("height"), f"=height_spec * verticalScale")
        callsheet.set(callsheet.getCellFromAlias("pitch"), f"=pitch_spec * verticalScale")
        circle_sketch.setExpression("Constraints[1]", f"<<{self.addPrefix('callsheet')}>>.radius")
        helix.setExpression("Pitch", f"<<{self.addPrefix('callsheet')}>>.pitch")
        helix.setExpression("Radius", f"<<{self.addPrefix('callsheet')}>>.radius")
        pad.setExpression("Length", f"<<{self.addPrefix('callsheet')}>>.height")
        callsheet.set(callsheet.getCellFromAlias("thread_height"), f"=height + 0.1 in")
        callsheet.set(callsheet.getCellFromAlias("cutter_side"), f"=pitch * 0.999")
        callsheet.set(callsheet.getCellFromAlias("cutter_radius"), f"=radius * 1.01")
        cutter_sketch.setExpression("Constraints[3]", f"<<{self.addPrefix('callsheet')}>>.cutter_side")
        cutter_sketch.setExpression("Constraints[4]", f"<<{self.addPrefix('callsheet')}>>.cutter_radius")
        helix.setExpression("Height", f"<<{self.addPrefix('callsheet')}>>.thread_height")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # now we have rebuilt the original Straight_m doc. Now we apply dynmic call parameters
        print("there can be temporary errors when we applying dynamic call parameters that change original Straight_m's shape.")
        print("ignore temporary errors, if any, below.")
        callsheet.set('B13', f'={self.holeDiaExpansion_spec}')
        callsheet.set('B2', f'{self.horizontalScale}')
        callsheet.set('B3', f'{self.verticalScale}')
        callsheet.set('B4', f'={self.radius_spec}')
        callsheet.set('B6', f'={self.height_spec}')
        callsheet.set('B8', f'={self.pitch_spec}')
        doc.recompute()
        update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.
        print("ignore temporary errors, if any, above.")
        
        # set callsheet
        self.update_callsheet()


def main():
    # main_part1
    from pdfclib.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of Straight_m
    myInstance = Straight_m("myInstance", doc, objPrefix="", useLabel=True, importer=None, height_spec='1 in', holeDiaExpansion_spec='0 mm', horizontalScale=1.1982, pitch_spec='1 mm', radius_spec='0.2 in', verticalScale=1.261, )
    
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
