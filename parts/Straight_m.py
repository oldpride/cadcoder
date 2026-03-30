from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.baseClass import baseClass
from cadcoder.containertools import get_LCS_by_prefix
from cadcoder.objtools import update_obj_prop_jsonDict
from cadcoder.subelementtools import update_objs_seName, update_doc_seName, get_seName_by_posName

class straight_m(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, diaExpansion='0 mm', height='1 in', pitch='1 mm', radius='0.2 in',  ):
        self.diaExpansion = diaExpansion
        self.height = height
        self.pitch = pitch
        self.radius = radius
        
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
        callsheet.set('A2', 'radius')
        callsheet.set('A3', 'radius_expanded')
        callsheet.set('A4', 'height')
        callsheet.set('A5', 'pitch')
        callsheet.set('A6', 'thread_height')
        callsheet.set('A7', 'cutter_side')
        callsheet.set('A8', 'cutter_radius')
        callsheet.set('A9', 'diaExpansion')
        callsheet.set('B1', 'value')
        callsheet.set('B2', '=0.2 in')
        callsheet.setAlias('B2', 'radius')
        callsheet.set('B3', '=0.2 in')
        callsheet.setAlias('B3', 'radius_expanded')
        callsheet.set('B4', '=1 in')
        callsheet.setAlias('B4', 'height')
        callsheet.set('B5', '=1 mm')
        callsheet.setAlias('B5', 'pitch')
        callsheet.set('B6', '=1.0999999999999999 in')
        callsheet.setAlias('B6', 'thread_height')
        callsheet.set('B7', '=0.03933070866141732 in')
        callsheet.setAlias('B7', 'cutter_side')
        callsheet.set('B8', '=0.202 in')
        callsheet.setAlias('B8', 'cutter_radius')
        callsheet.set('B9', '=0 mm')
        callsheet.setAlias('B9', 'diaExpansion')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C2', 'Y')
        callsheet.set('C3', 'N')
        callsheet.set('C4', 'Y')
        callsheet.set('C5', 'Y')
        callsheet.set('C6', 'N')
        callsheet.set('C7', 'N')
        callsheet.set('C8', 'N')
        callsheet.set('C9', 'Y')
        callsheet.set('D1', 'comment')
        callsheet.set('D9', 'b_ 0.03 in for 3D print')
        callsheet.recompute()  # recompute after adding object
        
        straight_m_circle_sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('straight_m_circle_sketch') )
        straight_m_circle_sketch.Label = self.addPrefix('straight_m_circle_sketch')
        self.straight_m_circle_sketch = straight_m_circle_sketch
        self.post_new_obj(straight_m_circle_sketch)
        self.container_append_object(body, straight_m_circle_sketch)
        geo0 = straight_m_circle_sketch.addGeometry(Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 5.0800))
        straight_m_circle_sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 3, -1, 1))
        straight_m_circle_sketch.addConstraint(Sketcher.Constraint('Radius', geo0, 5.0800))
        straight_m_circle_sketch.AttacherEngine = 'Engine Plane'
        straight_m_circle_sketch.AttachmentSupport = (body_XY_Plane, (''))
        body_XY_Plane.Visibility = False  # hide base object
        straight_m_circle_sketch.MapMode = 'FlatFace'
        straight_m_circle_sketch.Visibility = False
        straight_m_circle_sketch.ViewObject.Visibility = False
        straight_m_circle_sketch.recompute()  # recompute after adding object
        
        straight_m_cutter_sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('straight_m_cutter_sketch') )
        straight_m_cutter_sketch.Label = self.addPrefix('straight_m_cutter_sketch')
        self.straight_m_cutter_sketch = straight_m_cutter_sketch
        self.post_new_obj(straight_m_cutter_sketch)
        self.container_append_object(body, straight_m_cutter_sketch)
        geo0 = straight_m_cutter_sketch.addGeometry(Part.LineSegment(Vector (4.265643068020128, -0.4994957627799554, 0.0), Vector (5.1308, 0.0, 0.0)))
        geo1 = straight_m_cutter_sketch.addGeometry(Part.LineSegment(Vector (5.1308, 0.0, 0.0), Vector (5.1308, -0.999, 0.0)))
        geo2 = straight_m_cutter_sketch.addGeometry(Part.LineSegment(Vector (5.1308, -0.999, 0.0), Vector (4.265643068020128, -0.4994957627799554, 0.0)))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('Coincident', geo1, 1, geo0, 2))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('Vertical', geo1))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('Coincident', geo2, 1, geo1, 2))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('DistanceY', geo1, 2, geo1, 1, 0.9990))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('DistanceX', -1, 1, geo0, 2, 5.1308))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 1, geo2, 2))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('PointOnObject', geo0, 2, -1))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('Angle', geo0, 2, geo1, 1, 1.0472))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('Angle', geo2, 2, geo0, 1, 1.0472))
        straight_m_cutter_sketch.AttacherEngine = 'Engine Plane'
        straight_m_cutter_sketch.AttachmentSupport = (body_XZ_Plane, (''))
        body_XZ_Plane.Visibility = False  # hide base object
        straight_m_cutter_sketch.MapMode = 'FlatFace'
        straight_m_cutter_sketch.Visibility = False
        straight_m_cutter_sketch.ViewObject.Visibility = False
        straight_m_cutter_sketch.recompute()  # recompute after adding object
        
        straight_m_helix = doc.addObject('Part::Helix', self.addPrefix('straight_m_helix') )
        straight_m_helix.Label = self.addPrefix('straight_m_helix')
        self.straight_m_helix = straight_m_helix
        self.post_new_obj(straight_m_helix)
        straight_m_helix.Height = 27.939999999999998
        straight_m_helix.Radius = 5.08
        straight_m_helix.SegmentLength = 1.0
        straight_m_helix.Style = 'New style'
        straight_m_helix.Visibility = False
        straight_m_helix.ViewObject.Visibility = False
        straight_m_helix.recompute()  # recompute after adding object
        
        helix_binder = doc.addObject('PartDesign::SubShapeBinder', self.addPrefix('helix_binder') )
        helix_binder.Label = self.addPrefix('helix_binder')
        self.helix_binder = helix_binder
        self.post_new_obj(helix_binder)
        self.container_append_object(body, helix_binder)
        helix_binder.addProperty("App::PropertyMatrix", "Cache_straight_m_helix")
        helix_binder.Cache_straight_m_helix = App.Matrix(1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0)
        helix_binder.Context = (body, 'Binder.')
        helix_binder.Support = [(straight_m_helix, (''))]
        helix_binder.Visibility = False
        helix_binder.ViewObject.Visibility = False
        helix_binder.recompute()  # recompute after adding object
        
        pad = doc.addObject('PartDesign::Pad', self.addPrefix('pad') )
        pad.Label = self.addPrefix('pad')
        self.pad = pad
        self.post_new_obj(pad)
        self.container_append_object(body, pad)
        pad.Length = 25.4
        pad.Profile = (straight_m_circle_sketch, [''])
        pad.ReferenceAxis = (straight_m_circle_sketch, ['N_Axis'])
        pad.Visibility = False
        pad.ViewObject.Visibility = False
        pad.recompute()  # recompute after adding object
        
        subtractivepipe = doc.addObject('PartDesign::SubtractivePipe', self.addPrefix('subtractivepipe') )
        subtractivepipe.Label = self.addPrefix('subtractivepipe')
        self.subtractivepipe = subtractivepipe
        self.post_new_obj(subtractivepipe)
        self.container_append_object(body, subtractivepipe)
        subtractivepipe.BaseFeature = pad
        subtractivepipe.Mode = 'Frenet'
        subtractivepipe.Profile = (straight_m_cutter_sketch, [])
        subtractivepipe.Spine = (helix_binder, [])
        subtractivepipe.recompute()  # recompute after adding object
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        pad.setExpression("Length", f"<<{self.addPrefix('callsheet')}>>.height")
        straight_m_helix.setExpression("Pitch", f"<<{self.addPrefix('callsheet')}>>.pitch")
        callsheet.set(callsheet.getCellFromAlias("radius_expanded"), f"=radius + diaExpansion / 2")
        callsheet.set(callsheet.getCellFromAlias("thread_height"), f"=height + 0.1 in")
        callsheet.set(callsheet.getCellFromAlias("cutter_side"), f"=pitch * 0.999")
        straight_m_circle_sketch.setExpression("Constraints[1]", f"<<{self.addPrefix('callsheet')}>>.radius_expanded")
        straight_m_cutter_sketch.setExpression("Constraints[3]", f"<<{self.addPrefix('callsheet')}>>.cutter_side")
        straight_m_helix.setExpression("Height", f"<<{self.addPrefix('callsheet')}>>.thread_height")
        straight_m_helix.setExpression("Radius", f"<<{self.addPrefix('callsheet')}>>.radius_expanded")
        callsheet.set(callsheet.getCellFromAlias("cutter_radius"), f"=radius_expanded * 1.01")
        straight_m_cutter_sketch.setExpression("Constraints[4]", f"<<{self.addPrefix('callsheet')}>>.cutter_radius")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # now we have rebuilt the original straight_m doc. Now we apply dynmic call parameters
        print("there can be temporary errors when we applying dynamic call parameters that change original straight_m's shape.")
        print("ignore temporary errors, if any, below.")
        callsheet.set(callsheet.getCellFromAlias('radius'), f'={self.radius}')
        callsheet.set(callsheet.getCellFromAlias('height'), f'={self.height}')
        callsheet.set(callsheet.getCellFromAlias('pitch'), f'={self.pitch}')
        callsheet.set(callsheet.getCellFromAlias('diaExpansion'), f'={self.diaExpansion}')
        doc.recompute()
        update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.
        print("ignore temporary errors, if any, above.")
        
        self.update_callsheet()


def main():
    # main_part1
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of straight_m
    myInstance = straight_m("myInstance", doc, objPrefix="", useLabel=True, importer=None, diaExpansion='0 mm', height='1 in', pitch='1 mm', radius='0.2 in', )
    
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
