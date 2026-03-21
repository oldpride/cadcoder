from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.baseClass import baseClass
from pdfclib.containertools import get_LCS_by_prefix
from pdfclib.objtools import update_obj_prop_jsonDict
from pdfclib.subelementtools import update_objs_seName, update_doc_seName, get_seName_by_posName

class Npt_m(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, OD_shrink_spec='0 in', holeDiaExpansion_spec='0 in', horizontalScale=1.1982, male_height_spec='0.3 in', nominalOD='`1', verticalScale=1.261,  ):
        self.OD_shrink_spec = OD_shrink_spec
        self.holeDiaExpansion_spec = holeDiaExpansion_spec
        self.horizontalScale = horizontalScale
        self.male_height_spec = male_height_spec
        self.nominalOD = nominalOD
        self.verticalScale = verticalScale
        
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
        
        common_body = doc.addObject('PartDesign::Body', self.addPrefix('common_body') )
        common_body.Label = self.addPrefix('common_body')
        self.common_body = common_body
        self.post_new_obj(common_body)
        common_body_Origin = get_LCS_by_prefix(doc, common_body, 'Origin')
        common_body_X_Axis = get_LCS_by_prefix(doc, common_body, 'X_Axis')
        common_body_Y_Axis = get_LCS_by_prefix(doc, common_body, 'Y_Axis')
        common_body_Z_Axis = get_LCS_by_prefix(doc, common_body, 'Z_Axis')
        common_body_XY_Plane = get_LCS_by_prefix(doc, common_body, 'XY_Plane')
        common_body_XZ_Plane = get_LCS_by_prefix(doc, common_body, 'XZ_Plane')
        common_body_YZ_Plane = get_LCS_by_prefix(doc, common_body, 'YZ_Plane')
        self.common_body_Origin = common_body_Origin
        self.common_body_X_Axis = common_body_X_Axis
        self.common_body_Y_Axis = common_body_Y_Axis
        self.common_body_Z_Axis = common_body_Z_Axis
        self.common_body_XY_Plane = common_body_XY_Plane
        self.common_body_XZ_Plane = common_body_XZ_Plane
        self.common_body_YZ_Plane = common_body_YZ_Plane
        self.post_new_obj(common_body_Origin)
        self.post_new_obj(common_body_X_Axis)
        self.post_new_obj(common_body_Y_Axis)
        self.post_new_obj(common_body_Z_Axis)
        self.post_new_obj(common_body_XY_Plane)
        self.post_new_obj(common_body_XZ_Plane)
        self.post_new_obj(common_body_YZ_Plane)
        common_body.recompute()  # recompute after adding object
        
        spec = doc.addObject('Spreadsheet::Sheet', self.addPrefix('spec') )
        spec.Label = self.addPrefix('spec')
        self.spec = spec
        self.post_new_obj(spec)
        spec.set('A1', 'NominalOD')
        spec.set('A10', '`1-1/4')
        spec.set('A11', '`1-1/2')
        spec.set('A12', '`2')
        spec.set('A13', '`2-1/2')
        spec.set('A14', '`3')
        spec.set('A15', '`4')
        spec.set('A2', '`1')
        spec.setAlias('A2', 'NominalOD')
        spec.set('A3', '`1/16')
        spec.set('A4', '`1/8')
        spec.set('A5', '`1/4')
        spec.set('A6', '`3/8')
        spec.set('A7', '`1/2')
        spec.set('A8', '`3/4')
        spec.set('A9', '`1')
        spec.set('B1', '`RealOD')
        spec.set('B10', '=1.66 in')
        spec.set('B11', '=1.9 in')
        spec.set('B12', '=2.375 in')
        spec.set('B13', '=2.875 in')
        spec.set('B14', '=3.5 in')
        spec.set('B15', '=4.5 in')
        spec.set('B2', '=.B9')
        spec.setAlias('B2', 'RealOD')
        spec.set('B3', '=0.3125 in')
        spec.set('B4', '=0.405 in')
        spec.set('B5', '=0.54 in')
        spec.set('B6', '=0.675 in')
        spec.set('B7', '=0.84 in')
        spec.set('B8', '=1.05 in')
        spec.set('B9', '=1.315 in')
        spec.set('C1', 'TPI')
        spec.set('C10', '11.5')
        spec.set('C11', '11.5')
        spec.set('C12', '11.5')
        spec.set('C13', '8')
        spec.set('C14', '8')
        spec.set('C15', '8')
        spec.set('C2', '11.5')
        spec.setAlias('C2', 'TPI')
        spec.set('C3', '27')
        spec.set('C4', '27')
        spec.set('C5', '18')
        spec.set('C6', '18')
        spec.set('C7', '14')
        spec.set('C8', '14')
        spec.set('C9', '11.5')
        spec.set('D1', 'Pitch')
        spec.set('D10', '=0.08696 in')
        spec.set('D11', '=0.08696 in')
        spec.set('D12', '=0.08696 in')
        spec.set('D13', '=0.125 in')
        spec.set('D14', '=0.125 in')
        spec.set('D15', '=0.125 in')
        spec.set('D2', '=.D9')
        spec.setAlias('D2', 'Pitch')
        spec.set('D3', '=0.03704 in')
        spec.set('D4', '=0.03704 in')
        spec.set('D5', '=0.05556 in')
        spec.set('D6', '=0.05556 in')
        spec.set('D7', '=0.07143 in')
        spec.set('D8', '=0.07143 in')
        spec.set('D9', '=0.08696 in')
        spec.set('E1', 'Pitch Diameter at External Thread Start (E0)')
        spec.set('E10', '1.5571')
        spec.set('E11', '1.7961')
        spec.set('E12', '2.269')
        spec.set('E13', '2.7195')
        spec.set('E14', '3.3406')
        spec.set('E15', '4.3344')
        spec.set('E2', '1.2136')
        spec.set('E3', '0.2712')
        spec.set('E4', '0.3635')
        spec.set('E5', '0.4774')
        spec.set('E6', '0.612')
        spec.set('E7', '0.7584')
        spec.set('E8', '0.9677')
        spec.set('E9', '1.2136')
        spec.set('F1', 'Hand Tight Engagement (Length L1)')
        spec.set('F10', '0.42')
        spec.set('F11', '0.42')
        spec.set('F12', '0.436')
        spec.set('F13', '0.682')
        spec.set('F14', '0.766')
        spec.set('F15', '0.844')
        spec.set('F2', '0.4')
        spec.set('F3', '0.16')
        spec.set('F4', '0.1615')
        spec.set('F5', '0.2278')
        spec.set('F6', '0.24')
        spec.set('F7', '0.32')
        spec.set('F8', '0.339')
        spec.set('F9', '0.4')
        spec.set('G1', 'Hand Tight Engagement (Diameter E1)')
        spec.set('G10', '1.5834')
        spec.set('G11', '1.8223')
        spec.set('G12', '2.2963')
        spec.set('G13', '2.7622')
        spec.set('G14', '3.3885')
        spec.set('G15', '4.3871')
        spec.set('G2', '1.2386')
        spec.set('G3', '0.2812')
        spec.set('G4', '0.3736')
        spec.set('G5', '0.4916')
        spec.set('G6', '0.627')
        spec.set('G7', '0.7784')
        spec.set('G8', '0.9889')
        spec.set('G9', '1.2386')
        spec.set('H1', 'Effective Thread External (Length L2)')
        spec.set('H10', '0.7068')
        spec.set('H11', '0.7235')
        spec.set('H12', '0.7565')
        spec.set('H13', '1.1375')
        spec.set('H14', '1.2')
        spec.set('H15', '1.3')
        spec.set('H2', '0.6828')
        spec.set('H3', '0.2611')
        spec.set('H4', '0.2639')
        spec.set('H5', '0.4018')
        spec.set('H6', '0.4078')
        spec.set('H7', '0.5337')
        spec.set('H8', '0.5457')
        spec.set('H9', '0.6828')
        spec.set('I1', 'Effective Thread External (Diameter E2)')
        spec.set('I10', '1.6013')
        spec.set('I11', '1.8413')
        spec.set('I12', '2.3163')
        spec.set('I13', '2.7906')
        spec.set('I14', '3.4156')
        spec.set('I15', '4.4156')
        spec.set('I2', '1.2563')
        spec.set('I3', '0.2875')
        spec.set('I4', '0.38')
        spec.set('I5', '0.5025')
        spec.set('I6', '0.6375')
        spec.set('I7', '0.7918')
        spec.set('I8', '1.0018')
        spec.set('I9', '1.2563')
        spec.Visibility = False
        spec.addProperty("App::PropertyEnumeration", "nominalOD")
        spec.ViewObject.Visibility = False
        spec.recompute()  # recompute after adding object
        
        callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('callsheet') )
        callsheet.Label = self.addPrefix('callsheet')
        self.callsheet = callsheet
        self.post_new_obj(callsheet)
        callsheet.set('A1', 'variableName')
        callsheet.set('A10', 'OD_shrink_spec')
        callsheet.set('A11', 'realOD_expanded_spec')
        callsheet.set('A12', 'realOD')
        callsheet.set('A13', 'male_height_spec')
        callsheet.set('A14', 'male_height')
        callsheet.set('A15', 'cone_height_spec')
        callsheet.set('A16', 'cone_height')
        callsheet.set('A17', 'cone_bottom_big_r_spec')
        callsheet.set('A18', 'cone_bottom_big_r')
        callsheet.set('A19', 'cone_top_small_r_spec')
        callsheet.set('A2', 'nominalOD')
        callsheet.set('A20', 'cone_top_small_r')
        callsheet.set('A21', 'TPI')
        callsheet.set('A22', 'pitch_spec')
        callsheet.set('A23', 'pitch')
        callsheet.set('A24', 'helix_angle')
        callsheet.set('A25', 'helix_height')
        callsheet.set('A26', 'helix_r')
        callsheet.set('A27', 'thread_cutter_side')
        callsheet.set('A28', 'thread_start_r')
        callsheet.set('A29', 'thread_cutter_z')
        callsheet.set('A3', 'horizontalScale')
        callsheet.set('A4', 'verticalScale')
        callsheet.set('A5', 'slope_angle')
        callsheet.set('A6', 'slope_const')
        callsheet.set('A7', 'holeDiaExpansion_spec')
        callsheet.set('A8', 'holeDiaExpansion')
        callsheet.set('A9', 'realOD_spec')
        callsheet.set('B1', 'value')
        callsheet.set('B10', '=0 in')
        callsheet.setAlias('B10', 'OD_shrink_spec')
        callsheet.set('B11', '=1.315 in')
        callsheet.setAlias('B11', 'realOD_expanded_spec')
        callsheet.set('B12', '=1.5756329999999998 in')
        callsheet.setAlias('B12', 'realOD')
        callsheet.set('B13', '=0.3 in')
        callsheet.setAlias('B13', 'male_height_spec')
        callsheet.set('B14', '=0.3782999999999999 in')
        callsheet.setAlias('B14', 'male_height')
        callsheet.set('B15', '=0.47391304347826085 in')
        callsheet.setAlias('B15', 'cone_height_spec')
        callsheet.set('B16', '=0.5976043478260868 in')
        callsheet.setAlias('B16', 'cone_height')
        callsheet.set('B17', '=0.6575 in')
        callsheet.setAlias('B17', 'cone_bottom_big_r_spec')
        callsheet.set('B18', '=0.7878164999999999 in')
        callsheet.setAlias('B18', 'cone_bottom_big_r')
        callsheet.set('B19', '=0.6426903052214333 in')
        callsheet.setAlias('B19', 'cone_top_small_r_spec')
        callsheet.set('B2', '`1')
        callsheet.setAlias('B2', 'nominalOD')
        callsheet.set('B20', '=0.7700715237163213 in')
        callsheet.setAlias('B20', 'cone_top_small_r')
        callsheet.set('B21', '11.5')
        callsheet.setAlias('B21', 'TPI')
        callsheet.set('B22', '=0.08695652173913043 in')
        callsheet.setAlias('B22', 'pitch_spec')
        callsheet.set('B23', '=0.10965217391304347 in')
        callsheet.setAlias('B23', 'pitch')
        callsheet.set('B24', '=-1.7008135848336787 deg')
        callsheet.setAlias('B24', 'helix_angle')
        callsheet.set('B25', '=0.4879521739130434 in')
        callsheet.setAlias('B25', 'helix_height')
        callsheet.set('B26', '=0.7878164999999999 in')
        callsheet.setAlias('B26', 'helix_r')
        callsheet.set('B27', '=0.10636260869565216 in')
        callsheet.setAlias('B27', 'thread_cutter_side')
        callsheet.set('B28', '=0.793299108695652 in')
        callsheet.setAlias('B28', 'thread_start_r')
        callsheet.set('B29', '=0.018165478461692912 in')
        callsheet.setAlias('B29', 'thread_cutter_z')
        callsheet.set('B3', '1.1982')
        callsheet.setAlias('B3', 'horizontalScale')
        callsheet.set('B4', '1.261')
        callsheet.setAlias('B4', 'verticalScale')
        callsheet.set('B5', '1.7899')
        callsheet.setAlias('B5', 'slope_angle')
        callsheet.set('B6', '0.031249814670369906')
        callsheet.setAlias('B6', 'slope_const')
        callsheet.set('B7', '=0 in')
        callsheet.setAlias('B7', 'holeDiaExpansion_spec')
        callsheet.set('B8', '=0.0 in')
        callsheet.setAlias('B8', 'holeDiaExpansion')
        callsheet.set('B9', '=1.315 in')
        callsheet.setAlias('B9', 'realOD_spec')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C10', 'Y')
        callsheet.set('C11', 'N')
        callsheet.set('C12', 'N')
        callsheet.set('C13', 'Y')
        callsheet.set('C14', 'N')
        callsheet.set('C15', 'N')
        callsheet.set('C16', 'N')
        callsheet.set('C17', 'N')
        callsheet.set('C18', 'N')
        callsheet.set('C19', 'N')
        callsheet.set('C2', 'Y')
        callsheet.set('C20', 'N')
        callsheet.set('C21', 'N')
        callsheet.set('C22', 'N')
        callsheet.set('C23', 'N')
        callsheet.set('C24', 'N')
        callsheet.set('C25', 'N')
        callsheet.set('C26', 'N')
        callsheet.set('C27', 'N')
        callsheet.set('C28', 'N')
        callsheet.set('C29', 'N')
        callsheet.set('C3', 'Y')
        callsheet.set('C4', 'Y')
        callsheet.set('C5', 'N')
        callsheet.set('C6', 'N')
        callsheet.set('C7', 'Y')
        callsheet.set('C8', 'N')
        callsheet.set('C9', 'N')
        callsheet.set('D1', 'comment')
        callsheet.set('D10', 'shrink OD to easy fitting')
        callsheet.set('D11', 'spec.RealOD + holeDiaExpansion_spec')
        callsheet.set('D12', 'scaled')
        callsheet.set('D14', 'scaled')
        callsheet.set('D16', 'male_height')
        callsheet.set('D17', 'realOD_expanded_spec / 2')
        callsheet.set('D18', 'cone_top_big_r_spec * horizontalScale')
        callsheet.set('D19', 'cone_top_big_r_spec - slope * male_height_spec')
        callsheet.set('D2', 'from spec.nominalOD')
        callsheet.set('D20', 'scaled')
        callsheet.set('D21', 'NPT_Spreadsheet.TPI')
        callsheet.set('D22', '1 in/TPI')
        callsheet.set('D23', 'scaled')
        callsheet.set('D24', 'atan((cone_top_big_r - cone_bottom_small_r) / cone_height)')
        callsheet.set('D25', 'cone_height + 0.1 in')
        callsheet.set('D26', 'cone_bottom_small_r')
        callsheet.set('D27', 'pitch * 1.001')
        callsheet.set('D28', 'cone_bottom_small_r * 1.001')
        callsheet.set('D29', 'make sure profile cut into cone')
        callsheet.set('D3', 'BASF 17-4 xy scale 1.1982')
        callsheet.set('D4', 'BASF 17-4 z scale 1.2610')
        callsheet.set('D5', 'NPT 1.7899')
        callsheet.set('D6', 'tan(1.7899)')
        callsheet.set('D7', '0.03 in for 3D print')
        callsheet.set('D8', 'holeDiaExpansion_spec * horizontalScale')
        callsheet.set('D9', 'spec.RealOD')
        callsheet.recompute()  # recompute after adding object
        
        sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('sketch') )
        sketch.Label = self.addPrefix('sketch')
        self.sketch = sketch
        self.post_new_obj(sketch)
        self.container_append_object(body, sketch)
        geo0 = sketch.addGeometry(Part.LineSegment(Vector (17.81014085953018, -0.8894019775077824, 0.0), Vector (20.14979736086956, -2.240207107942565, 0.0)))
        geo1 = sketch.addGeometry(Part.LineSegment(Vector (20.14979736086956, -2.240207107942565, 0.0), Vector (20.14979736086956, 0.46140315292699974, 0.0)))
        geo2 = sketch.addGeometry(Part.LineSegment(Vector (20.14979736086956, 0.461403152927, 0.0), Vector (17.81014085953018, -0.8894019775077824, 0.0)))
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 2, geo1, 1))
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo1, 2, geo2, 1))
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo2, 2, geo0, 1))
        sketch.addConstraint(Sketcher.Constraint('DistanceY', geo1, 1, geo1, 2, 2.7016))
        sketch.addConstraint(Sketcher.Constraint('DistanceX', -1, 1, geo1, 2, 20.1498))
        sketch.addConstraint(Sketcher.Constraint('Vertical', geo1))
        sketch.addConstraint(Sketcher.Constraint('Angle', -1, 2, geo2, 1, 0.5236))
        sketch.addConstraint(Sketcher.Constraint('Angle', geo0, 1, geo2, 2, 1.0472))
        sketch.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, geo1, 2, 0.4614))
        sketch.AttacherEngine = 'Engine Plane'
        sketch.AttachmentSupport = (body_XZ_Plane, (''))
        body_XZ_Plane.Visibility = False  # hide base object
        sketch.MapMode = 'FlatFace'
        sketch.Visibility = False
        sketch.ViewObject.GridSize = 9.999979999999999
        sketch.ViewObject.Visibility = False
        sketch.recompute()  # recompute after adding object
        
        additive_cone = doc.addObject('PartDesign::AdditiveCone', self.addPrefix('additive_cone') )
        additive_cone.Label = self.addPrefix('additive_cone')
        self.additive_cone = additive_cone
        self.post_new_obj(additive_cone)
        self.container_append_object(body, additive_cone)
        additive_cone.Height = 15.179150434782606
        additive_cone.Radius1 = 20.010539099999995
        additive_cone.Radius2 = 19.55981670239456
        additive_cone.Visibility = False
        additive_cone.ViewObject.Visibility = False
        additive_cone.recompute()  # recompute after adding object
        
        additive_cylinder = doc.addObject('PartDesign::AdditiveCylinder', self.addPrefix('additive_cylinder') )
        additive_cylinder.Label = self.addPrefix('additive_cylinder')
        self.additive_cylinder = additive_cylinder
        self.post_new_obj(additive_cylinder)
        self.container_append_object(common_body, additive_cylinder)
        additive_cylinder.Height = 9.608819999999998
        additive_cylinder.Radius = 20.264539099999997
        additive_cylinder.recompute()  # recompute after adding object
        
        subtractive_helix = doc.addObject('PartDesign::SubtractiveHelix', self.addPrefix('subtractive_helix') )
        subtractive_helix.Label = self.addPrefix('subtractive_helix')
        self.subtractive_helix = subtractive_helix
        self.post_new_obj(subtractive_helix)
        self.container_append_object(body, subtractive_helix)
        subtractive_helix.Angle = -1.7008135848336787
        subtractive_helix.BaseFeature = additive_cone
        subtractive_helix.HasBeenEdited = True
        subtractive_helix.Height = 12.393985217391302
        subtractive_helix.Pitch = 2.7851652173913037
        subtractive_helix.Profile = (sketch, [''])
        subtractive_helix.ReferenceAxis = (sketch, ['V_Axis'])
        subtractive_helix.Visibility = False
        subtractive_helix.ViewObject.Visibility = False
        subtractive_helix.recompute()  # recompute after adding object
        
        common_boolean = doc.addObject('PartDesign::Boolean', self.addPrefix('common_boolean') )
        common_boolean.Label = self.addPrefix('common_boolean')
        self.common_boolean = common_boolean
        self.post_new_obj(common_boolean)
        self.container_append_object(body, common_boolean)
        common_boolean.BaseFeature = subtractive_helix
        common_boolean.Group = [common_body]
        common_boolean.Type = 'Common'
        common_boolean.UsePlacement = True
        doc.recompute() # recompute whole document for PartDesign::Boolean
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        spec.set("B10", f"=1.66 in")
        spec.set("B11", f"=1.9 in")
        spec.set("B12", f"=2.375 in")
        spec.set("B13", f"=2.875 in")
        spec.set("B14", f"=3.5 in")
        spec.set("B15", f"=4.5 in")
        spec.set("B3", f"=0.3125 in")
        spec.set("B4", f"=0.405 in")
        spec.set("B5", f"=0.54 in")
        spec.set("B6", f"=0.675 in")
        spec.set("B7", f"=0.84 in")
        spec.set("B8", f"=1.05 in")
        spec.set("B9", f"=1.315 in")
        spec.set(spec.getCellFromAlias("TPI"), f"=.C9")
        spec.set("D10", f"=0.08696 in")
        spec.set("D11", f"=0.08696 in")
        spec.set("D12", f"=0.08696 in")
        spec.set("D13", f"=0.125 in")
        spec.set("D14", f"=0.125 in")
        spec.set("D15", f"=0.125 in")
        spec.set("D3", f"=0.03704 in")
        spec.set("D4", f"=0.03704 in")
        spec.set("D5", f"=0.05556 in")
        spec.set("D6", f"=0.05556 in")
        spec.set("D7", f"=0.07143 in")
        spec.set("D8", f"=0.07143 in")
        spec.set("D9", f"=0.08696 in")
        spec.set("E2", f"=.E9")
        spec.set("F2", f"=.F9")
        spec.set("G2", f"=.G9")
        spec.set("H2", f"=.H9")
        spec.set("I2", f"=.I9")
        spec.setExpression(".nominalOD.Enum", f".cells[<<A3:|>>]")
        spec.recompute() # recompute after setting configuration-table expression; otherwise error: Property ... not found.
        callsheet.set(callsheet.getCellFromAlias("male_height"), f"=male_height_spec * verticalScale")
        callsheet.set(callsheet.getCellFromAlias("TPI"), f"=<<{self.addPrefix('spec')}>>.TPI")
        callsheet.set(callsheet.getCellFromAlias("slope_const"), f"=tan(slope_angle)")
        callsheet.set(callsheet.getCellFromAlias("holeDiaExpansion"), f"=holeDiaExpansion_spec * horizontalScale")
        spec.set(spec.getCellFromAlias("NominalOD"), f"=hiddenref(.nominalOD.String)")
        spec.set(spec.getCellFromAlias("RealOD"), f"=.B9")
        spec.set(spec.getCellFromAlias("Pitch"), f"=.D9")
        spec.setExpression(".cells.Bind.B2.I2", f"tuple(.cells; <<B>> + str(hiddenref(.nominalOD) + 3); <<I>> + str(hiddenref(.nominalOD) + 3))")
        spec.recompute() # recompute after setting configuration-table expression; otherwise error: Property ... not found.
        additive_cylinder.setExpression("Height", f"<<{self.addPrefix('callsheet')}>>.male_height")
        callsheet.set(callsheet.getCellFromAlias("realOD_expanded_spec"), f"=<<{self.addPrefix('spec')}>>.RealOD + holeDiaExpansion_spec - OD_shrink_spec")
        callsheet.set(callsheet.getCellFromAlias("pitch_spec"), f"=1 in / TPI")
        callsheet.set(callsheet.getCellFromAlias("realOD_spec"), f"=<<{self.addPrefix('spec')}>>.RealOD")
        callsheet.set(callsheet.getCellFromAlias("realOD"), f"=realOD_expanded_spec * horizontalScale")
        callsheet.set(callsheet.getCellFromAlias("cone_height_spec"), f"=male_height_spec + 2 * pitch_spec")
        callsheet.set(callsheet.getCellFromAlias("cone_bottom_big_r_spec"), f"=realOD_expanded_spec / 2")
        callsheet.set(callsheet.getCellFromAlias("pitch"), f"=pitch_spec * verticalScale")
        subtractive_helix.setExpression("Pitch", f"<<{self.addPrefix('callsheet')}>>.pitch")
        callsheet.set(callsheet.getCellFromAlias("cone_height"), f"=cone_height_spec * verticalScale")
        callsheet.set(callsheet.getCellFromAlias("cone_bottom_big_r"), f"=cone_bottom_big_r_spec * horizontalScale")
        callsheet.set(callsheet.getCellFromAlias("cone_top_small_r_spec"), f"=cone_bottom_big_r_spec - slope_const * cone_height_spec")
        callsheet.set(callsheet.getCellFromAlias("helix_height"), f"=male_height + pitch")
        callsheet.set(callsheet.getCellFromAlias("thread_cutter_side"), f"=pitch * 0.97")
        sketch.setExpression("Constraints[3]", f"<<{self.addPrefix('callsheet')}>>.thread_cutter_side")
        subtractive_helix.setExpression("Height", f"<<{self.addPrefix('callsheet')}>>.helix_height")
        additive_cone.setExpression("Height", f"<<{self.addPrefix('callsheet')}>>.cone_height")
        additive_cone.setExpression("Radius1", f"<<{self.addPrefix('callsheet')}>>.cone_bottom_big_r")
        additive_cylinder.setExpression("Radius", f"<<{self.addPrefix('callsheet')}>>.cone_bottom_big_r + 0.01 in")
        callsheet.set(callsheet.getCellFromAlias("cone_top_small_r"), f"=cone_top_small_r_spec * horizontalScale")
        callsheet.set(callsheet.getCellFromAlias("helix_r"), f"=cone_bottom_big_r")
        callsheet.set(callsheet.getCellFromAlias("thread_start_r"), f"=cone_bottom_big_r + pitch * 0.05")
        sketch.setExpression("Constraints[4]", f"<<{self.addPrefix('callsheet')}>>.thread_start_r")
        additive_cone.setExpression("Radius2", f"<<{self.addPrefix('callsheet')}>>.cone_top_small_r")
        callsheet.set(callsheet.getCellFromAlias("helix_angle"), f"=atan((cone_top_small_r - cone_bottom_big_r) / cone_height)")
        callsheet.set(callsheet.getCellFromAlias("thread_cutter_z"), f"=(thread_start_r - cone_bottom_big_r) / 1.732 + 0.015 in")
        sketch.setExpression("Constraints[8]", f"<<{self.addPrefix('callsheet')}>>.thread_cutter_z")
        subtractive_helix.setExpression("Angle", f"<<{self.addPrefix('callsheet')}>>.helix_angle")
        
        # add trigger objects' expressions
        from pdfclib.triggertools import link_watch_to_target
        link_watch_to_target(doc, callsheet, 'nominalOD', spec, 'nominalOD', useLabel)
        
        # add delayed expression property values - values, not expressions, eg, enum value
        spec.nominalOD = '`1'
        
        # now we have rebuilt the original Npt_m doc. Now we apply dynmic call parameters
        print("there can be temporary errors when we applying dynamic call parameters that change original Npt_m's shape.")
        print("ignore temporary errors, if any, below.")
        callsheet.set(callsheet.getCellFromAlias('OD_shrink_spec'), f'={self.OD_shrink_spec}')
        callsheet.set(callsheet.getCellFromAlias('male_height_spec'), f'={self.male_height_spec}')
        callsheet.set(callsheet.getCellFromAlias('nominalOD'), f'{self.nominalOD}')
        callsheet.set(callsheet.getCellFromAlias('horizontalScale'), f'{self.horizontalScale}')
        callsheet.set(callsheet.getCellFromAlias('verticalScale'), f'{self.verticalScale}')
        callsheet.set(callsheet.getCellFromAlias('holeDiaExpansion_spec'), f'={self.holeDiaExpansion_spec}')
        doc.recompute()
        update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.
        print("ignore temporary errors, if any, above.")
        
        self.update_callsheet()


def main():
    # main_part1
    from pdfclib.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of Npt_m
    myInstance = Npt_m("myInstance", doc, objPrefix="", useLabel=True, importer=None, OD_shrink_spec='0 in', holeDiaExpansion_spec='0 in', horizontalScale=1.1982, male_height_spec='0.3 in', nominalOD='`1', verticalScale=1.261, )
    
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
