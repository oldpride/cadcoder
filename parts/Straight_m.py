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
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, diaExpansion='0 in', height='1 in', pitch='0.0357 in', radius='0.2 in',  ):
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
        
        common_cutter = doc.addObject('PartDesign::Body', self.addPrefix('common_cutter') )
        common_cutter.Label = self.addPrefix('common_cutter')
        self.common_cutter = common_cutter
        self.post_new_obj(common_cutter)
        common_cutter_Origin = get_LCS_by_prefix(doc, common_cutter, 'Origin')
        common_cutter_X_Axis = get_LCS_by_prefix(doc, common_cutter, 'X_Axis')
        common_cutter_Y_Axis = get_LCS_by_prefix(doc, common_cutter, 'Y_Axis')
        common_cutter_Z_Axis = get_LCS_by_prefix(doc, common_cutter, 'Z_Axis')
        common_cutter_XY_Plane = get_LCS_by_prefix(doc, common_cutter, 'XY_Plane')
        common_cutter_XZ_Plane = get_LCS_by_prefix(doc, common_cutter, 'XZ_Plane')
        common_cutter_YZ_Plane = get_LCS_by_prefix(doc, common_cutter, 'YZ_Plane')
        self.common_cutter_Origin = common_cutter_Origin
        self.common_cutter_X_Axis = common_cutter_X_Axis
        self.common_cutter_Y_Axis = common_cutter_Y_Axis
        self.common_cutter_Z_Axis = common_cutter_Z_Axis
        self.common_cutter_XY_Plane = common_cutter_XY_Plane
        self.common_cutter_XZ_Plane = common_cutter_XZ_Plane
        self.common_cutter_YZ_Plane = common_cutter_YZ_Plane
        self.post_new_obj(common_cutter_Origin)
        self.post_new_obj(common_cutter_X_Axis)
        self.post_new_obj(common_cutter_Y_Axis)
        self.post_new_obj(common_cutter_Z_Axis)
        self.post_new_obj(common_cutter_XY_Plane)
        self.post_new_obj(common_cutter_XZ_Plane)
        self.post_new_obj(common_cutter_YZ_Plane)
        common_cutter.recompute()  # recompute after adding object
        
        callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('callsheet') )
        callsheet.Label = self.addPrefix('callsheet')
        self.callsheet = callsheet
        self.post_new_obj(callsheet)
        callsheet.set('A1', 'variableName')
        callsheet.set('A2', 'radius')
        callsheet.set('A3', 'height')
        callsheet.set('A4', 'pad_height')
        callsheet.set('A5', 'pitch')
        callsheet.set('A6', 'helix_height')
        callsheet.set('A7', 'cutter_side')
        callsheet.set('A8', 'cutter_radius')
        callsheet.set('A9', 'diaExpansion')
        callsheet.set('B1', 'value')
        callsheet.set('B2', '=0.2 in')
        callsheet.setAlias('B2', 'radius')
        callsheet.set('B3', '=1 in')
        callsheet.setAlias('B3', 'height')
        callsheet.set('B4', '=1.1071 in')
        callsheet.setAlias('B4', 'pad_height')
        callsheet.set('B5', '=0.0357 in')
        callsheet.setAlias('B5', 'pitch')
        callsheet.set('B6', '=1.0714 in')
        callsheet.setAlias('B6', 'helix_height')
        callsheet.set('B7', '=0.034986 in')
        callsheet.setAlias('B7', 'cutter_side')
        callsheet.set('B8', '=0.202 in')
        callsheet.setAlias('B8', 'cutter_radius')
        callsheet.set('B9', '=0 in')
        callsheet.setAlias('B9', 'diaExpansion')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C2', 'Y')
        callsheet.set('C3', 'Y')
        callsheet.set('C4', 'N')
        callsheet.set('C5', 'Y')
        callsheet.set('C6', 'N')
        callsheet.set('C7', 'N')
        callsheet.set('C8', 'N')
        callsheet.set('C9', 'Y')
        callsheet.set('D1', 'comment')
        callsheet.set('D9', 'b_ 0.03 in for 3D print')
        callsheet.recompute()  # recompute after adding object
        
        common_cutter_sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('common_cutter_sketch') )
        common_cutter_sketch.Label = self.addPrefix('common_cutter_sketch')
        self.common_cutter_sketch = common_cutter_sketch
        self.post_new_obj(common_cutter_sketch)
        self.container_append_object(common_cutter, common_cutter_sketch)
        geo0 = common_cutter_sketch.addGeometry(Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 5.0800))
        common_cutter_sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 3, -1, 1))
        common_cutter_sketch.addConstraint(Sketcher.Constraint('Radius', geo0, 5.0800))
        common_cutter_sketch.AttacherEngine = 'Engine Plane'
        common_cutter_sketch.AttachmentSupport = (common_cutter_XY_Plane, (''))
        common_cutter_XY_Plane.Visibility = False  # hide base object
        common_cutter_sketch.MapMode = 'FlatFace'
        common_cutter_sketch.Visibility = False
        common_cutter_sketch.ViewObject.Visibility = False
        common_cutter_sketch.recompute()  # recompute after adding object
        
        sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('sketch') )
        sketch.Label = self.addPrefix('sketch')
        self.sketch = sketch
        self.post_new_obj(sketch)
        self.container_append_object(body, sketch)
        geo0 = sketch.addGeometry(Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 5.0800))
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 3, -1, 1))
        sketch.addConstraint(Sketcher.Constraint('Radius', geo0, 5.0800))
        sketch.AttacherEngine = 'Engine Plane'
        sketch.AttachmentSupport = (body_XY_Plane, (''))
        body_XY_Plane.Visibility = False  # hide base object
        sketch.MapMode = 'FlatFace'
        sketch.Visibility = False
        sketch.ViewObject.Visibility = False
        sketch.recompute()  # recompute after adding object
        
        straight_m_cutter_sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('straight_m_cutter_sketch') )
        straight_m_cutter_sketch.Label = self.addPrefix('straight_m_cutter_sketch')
        self.straight_m_cutter_sketch = straight_m_cutter_sketch
        self.post_new_obj(straight_m_cutter_sketch)
        self.container_append_object(body, straight_m_cutter_sketch)
        geo0 = straight_m_cutter_sketch.addGeometry(Part.LineSegment(Vector (4.361213550816896, -0.44431843086378514, 0.0), Vector (5.1308, 0.0, 0.0)))
        geo1 = straight_m_cutter_sketch.addGeometry(Part.LineSegment(Vector (5.1308, 0.0, 0.0), Vector (5.1308, -0.8886444, 0.0)))
        geo2 = straight_m_cutter_sketch.addGeometry(Part.LineSegment(Vector (5.1308, -0.8886444, 0.0), Vector (4.361213550816896, -0.4443184308637851, 0.0)))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('Coincident', geo1, 1, geo0, 2))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('Vertical', geo1))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('Coincident', geo2, 1, geo1, 2))
        straight_m_cutter_sketch.addConstraint(Sketcher.Constraint('DistanceY', geo1, 2, geo1, 1, 0.8886))
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
        
        common_cutter_pad = doc.addObject('PartDesign::Pad', self.addPrefix('common_cutter_pad') )
        common_cutter_pad.Label = self.addPrefix('common_cutter_pad')
        self.common_cutter_pad = common_cutter_pad
        self.post_new_obj(common_cutter_pad)
        self.container_append_object(common_cutter, common_cutter_pad)
        common_cutter_pad.Length = 25.4
        common_cutter_pad.Profile = (common_cutter_sketch, [''])
        common_cutter_pad.ReferenceAxis = (common_cutter_sketch, ['N_Axis'])
        common_cutter_pad.recompute()  # recompute after adding object
        
        pad = doc.addObject('PartDesign::Pad', self.addPrefix('pad') )
        pad.Label = self.addPrefix('pad')
        self.pad = pad
        self.post_new_obj(pad)
        self.container_append_object(body, pad)
        pad.Length = 28.12034
        pad.Profile = (sketch, [''])
        pad.ReferenceAxis = (sketch, ['N_Axis'])
        pad.Visibility = False
        pad.ViewObject.Visibility = False
        pad.recompute()  # recompute after adding object
        
        SubtractiveHelix = doc.addObject('PartDesign::SubtractiveHelix', self.addPrefix('SubtractiveHelix') )
        SubtractiveHelix.Label = self.addPrefix('SubtractiveHelix')
        self.SubtractiveHelix = SubtractiveHelix
        self.post_new_obj(SubtractiveHelix)
        self.container_append_object(body, SubtractiveHelix)
        SubtractiveHelix.BaseFeature = pad
        SubtractiveHelix.HasBeenEdited = True
        SubtractiveHelix.Height = 27.213559999999998
        SubtractiveHelix.Pitch = 0.90678
        SubtractiveHelix.Profile = (straight_m_cutter_sketch, [''])
        SubtractiveHelix.ReferenceAxis = (straight_m_cutter_sketch, ['V_Axis'])
        SubtractiveHelix.Visibility = False
        SubtractiveHelix.ViewObject.Visibility = False
        SubtractiveHelix.recompute()  # recompute after adding object
        
        boolean_common = doc.addObject('PartDesign::Boolean', self.addPrefix('boolean_common') )
        boolean_common.Label = self.addPrefix('boolean_common')
        self.boolean_common = boolean_common
        self.post_new_obj(boolean_common)
        self.container_append_object(body, boolean_common)
        boolean_common.BaseFeature = SubtractiveHelix
        boolean_common.Group = [common_cutter]
        boolean_common.Type = 'Common'
        boolean_common.UsePlacement = True
        doc.recompute() # recompute whole document for PartDesign::Boolean
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        SubtractiveHelix.setExpression('Angle', f"0")
        common_cutter_pad.setExpression('Length', f"<<{self.addPrefix('callsheet')}>>.height")
        common_cutter_sketch.setExpression('Constraints[1]', f"<<{self.addPrefix('callsheet')}>>.radius")
        sketch.setExpression('Constraints[1]', f"<<{self.addPrefix('callsheet')}>>.radius")
        SubtractiveHelix.setExpression('Pitch', f"<<{self.addPrefix('callsheet')}>>.pitch")
        callsheet.set(callsheet.getCellFromAlias('pad_height'), f"=height + 3 * pitch")
        callsheet.set(callsheet.getCellFromAlias('helix_height'), f"=height + 2 * pitch")
        callsheet.set(callsheet.getCellFromAlias('cutter_side'), f"=pitch * 0.98")
        callsheet.set(callsheet.getCellFromAlias('cutter_radius'), f"=radius * 1.01")
        pad.setExpression('Length', f"<<{self.addPrefix('callsheet')}>>.pad_height")
        straight_m_cutter_sketch.setExpression('Constraints[3]', f"<<{self.addPrefix('callsheet')}>>.cutter_side")
        straight_m_cutter_sketch.setExpression('Constraints[4]', f"<<{self.addPrefix('callsheet')}>>.cutter_radius")
        SubtractiveHelix.setExpression('Height', f"<<{self.addPrefix('callsheet')}>>.helix_height")
        
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
    myInstance = straight_m("myInstance", doc, objPrefix="", useLabel=True, importer=None, diaExpansion='0 in', height='1 in', pitch='0.0357 in', radius='0.2 in', )
    
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
