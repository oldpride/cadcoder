from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.baseClass import baseClass
from cadcoder.containertools import get_LCS_by_prefix
from cadcoder.objtools import update_obj_prop_jsonDict
from cadcoder.subelementtools import update_objs_seName, update_doc_seName, get_seName_by_posName

class npt_m(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, diaExpansion='0 in', male_height='0.3 in', nominalOD='`1/16',  ):
        self.diaExpansion = diaExpansion
        self.male_height = male_height
        self.nominalOD = nominalOD
        
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
        spec.set('A2', '`1/16')
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
        spec.set('B2', '=.B3')
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
        spec.set('C2', '27')
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
        spec.set('D2', '=.D3')
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
        spec.set('E2', '0.2712')
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
        spec.set('F2', '0.16')
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
        spec.set('G2', '0.2812')
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
        spec.set('H2', '0.2611')
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
        spec.set('I2', '0.2875')
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
        callsheet.set('A10', 'cone_top_small_r')
        callsheet.set('A11', 'TPI')
        callsheet.set('A12', 'pitch')
        callsheet.set('A13', 'helix_angle')
        callsheet.set('A14', 'helix_height')
        callsheet.set('A15', 'helix_r')
        callsheet.set('A16', 'thread_cutter_side')
        callsheet.set('A17', 'thread_start_r')
        callsheet.set('A18', 'thread_cutter_z')
        callsheet.set('A2', 'nominalOD')
        callsheet.set('A3', 'slope_angle')
        callsheet.set('A4', 'slope_const')
        callsheet.set('A5', 'diaExpansion')
        callsheet.set('A6', 'realOD')
        callsheet.set('A7', 'male_height')
        callsheet.set('A8', 'cone_height')
        callsheet.set('A9', 'cone_bottom_big_r')
        callsheet.set('B1', 'value')
        callsheet.set('B10', '=0.14456025451219495 in')
        callsheet.setAlias('B10', 'cone_top_small_r')
        callsheet.set('B11', '27')
        callsheet.setAlias('B11', 'TPI')
        callsheet.set('B12', '=0.037037037037037035 in')
        callsheet.setAlias('B12', 'pitch')
        callsheet.set('B13', '-1.7899')
        callsheet.setAlias('B13', 'helix_angle')
        callsheet.set('B14', '=0.3370370370370371 in')
        callsheet.setAlias('B14', 'helix_height')
        callsheet.set('B15', '=0.15625 in')
        callsheet.setAlias('B15', 'helix_r')
        callsheet.set('B16', '=0.035925925925925924 in')
        callsheet.setAlias('B16', 'thread_cutter_side')
        callsheet.set('B17', '=0.15810185185185185 in')
        callsheet.setAlias('B17', 'thread_start_r')
        callsheet.set('B18', '=0.016069198528782823 in')
        callsheet.setAlias('B18', 'thread_cutter_z')
        callsheet.set('B2', '`1/16')
        callsheet.setAlias('B2', 'nominalOD')
        callsheet.set('B3', '1.7899')
        callsheet.setAlias('B3', 'slope_angle')
        callsheet.set('B4', '0.031249814670369906')
        callsheet.setAlias('B4', 'slope_const')
        callsheet.set('B5', '=0 in')
        callsheet.setAlias('B5', 'diaExpansion')
        callsheet.set('B6', '=0.3125 in')
        callsheet.setAlias('B6', 'realOD')
        callsheet.set('B7', '=0.3 in')
        callsheet.setAlias('B7', 'male_height')
        callsheet.set('B8', '=0.37407407407407406 in')
        callsheet.setAlias('B8', 'cone_height')
        callsheet.set('B9', '=0.15625 in')
        callsheet.setAlias('B9', 'cone_bottom_big_r')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C10', 'N')
        callsheet.set('C11', 'N')
        callsheet.set('C12', 'N')
        callsheet.set('C13', 'N')
        callsheet.set('C14', 'N')
        callsheet.set('C15', 'N')
        callsheet.set('C16', 'N')
        callsheet.set('C17', 'N')
        callsheet.set('C18', 'N')
        callsheet.set('C2', 'Y')
        callsheet.set('C3', 'N')
        callsheet.set('C4', 'N')
        callsheet.set('C5', 'Y')
        callsheet.set('C6', 'N')
        callsheet.set('C7', 'Y')
        callsheet.set('C8', 'N')
        callsheet.set('C9', 'N')
        callsheet.set('D1', 'comment')
        callsheet.set('D2', 'from spec.nominalOD')
        callsheet.set('D3', 'NPT 1.7899')
        callsheet.set('D4', 'tan(1.7899)')
        callsheet.recompute()  # recompute after adding object
        
        sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('sketch') )
        sketch.Label = self.addPrefix('sketch')
        self.sketch = sketch
        self.post_new_obj(sketch)
        self.container_append_object(body, sketch)
        geo0 = sketch.addGeometry(Part.LineSegment(Vector (3.225525053149973, -0.0481016166281754, 0.0), Vector (4.015787037037037, -0.5043608758874346, 0.0)))
        geo1 = sketch.addGeometry(Part.LineSegment(Vector (4.015787037037037, -0.5043608758874347, 0.0), Vector (4.015787037037037, 0.4081576426310837, 0.0)))
        geo2 = sketch.addGeometry(Part.LineSegment(Vector (4.015787037037037, 0.4081576426310837, 0.0), Vector (3.225525053149973, -0.048101616628175414, 0.0)))
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 2, geo1, 1))
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo1, 2, geo2, 1))
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo2, 2, geo0, 1))
        sketch.addConstraint(Sketcher.Constraint('DistanceY', geo1, 1, geo1, 2, 0.9125))
        sketch.addConstraint(Sketcher.Constraint('DistanceX', -1, 1, geo1, 2, 4.0158))
        sketch.addConstraint(Sketcher.Constraint('Vertical', geo1))
        sketch.addConstraint(Sketcher.Constraint('Angle', -1, 2, geo2, 1, 0.5236))
        sketch.addConstraint(Sketcher.Constraint('Angle', geo0, 1, geo2, 2, 1.0472))
        sketch.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, geo1, 2, 0.4082))
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
        additive_cone.Height = 9.50148148148148
        additive_cone.Radius1 = 3.96875
        additive_cone.Radius2 = 3.671830464609752
        additive_cone.Visibility = False
        additive_cone.ViewObject.Visibility = False
        additive_cone.recompute()  # recompute after adding object
        
        additive_cylinder = doc.addObject('PartDesign::AdditiveCylinder', self.addPrefix('additive_cylinder') )
        additive_cylinder.Label = self.addPrefix('additive_cylinder')
        self.additive_cylinder = additive_cylinder
        self.post_new_obj(additive_cylinder)
        self.container_append_object(common_body, additive_cylinder)
        additive_cylinder.Height = 7.619999999999999
        additive_cylinder.Radius = 4.22275
        additive_cylinder.recompute()  # recompute after adding object
        
        subtractive_helix = doc.addObject('PartDesign::SubtractiveHelix', self.addPrefix('subtractive_helix') )
        subtractive_helix.Label = self.addPrefix('subtractive_helix')
        self.subtractive_helix = subtractive_helix
        self.post_new_obj(subtractive_helix)
        self.container_append_object(body, subtractive_helix)
        subtractive_helix.Angle = -1.7899
        subtractive_helix.BaseFeature = additive_cone
        subtractive_helix.HasBeenEdited = True
        subtractive_helix.Height = 8.56074074074074
        subtractive_helix.Pitch = 0.9407407407407407
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
        spec.set(spec.getCellFromAlias("TPI"), f"=.C3")
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
        spec.set("E2", f"=.E3")
        spec.set("F2", f"=.F3")
        spec.set("G2", f"=.G3")
        spec.set("H2", f"=.H3")
        spec.set("I2", f"=.I3")
        spec.setExpression(".nominalOD.Enum", f".cells[<<A3:|>>]")
        spec.recompute() # recompute after setting configuration-table expression; otherwise error: Property ... not found.
        additive_cylinder.setExpression("Height", f"<<{self.addPrefix('callsheet')}>>.male_height")
        callsheet.set(callsheet.getCellFromAlias("TPI"), f"=<<{self.addPrefix('spec')}>>.TPI")
        callsheet.set(callsheet.getCellFromAlias("helix_angle"), f"=-slope_angle")
        callsheet.set(callsheet.getCellFromAlias("slope_const"), f"=tan(slope_angle)")
        spec.set(spec.getCellFromAlias("NominalOD"), f"=hiddenref(.nominalOD.String)")
        spec.set(spec.getCellFromAlias("RealOD"), f"=.B3")
        spec.set(spec.getCellFromAlias("Pitch"), f"=.D3")
        spec.setExpression(".cells.Bind.B2.I2", f"tuple(.cells; <<B>> + str(hiddenref(.nominalOD) + 3); <<I>> + str(hiddenref(.nominalOD) + 3))")
        spec.recompute() # recompute after setting configuration-table expression; otherwise error: Property ... not found.
        subtractive_helix.setExpression("Angle", f"<<{self.addPrefix('callsheet')}>>.helix_angle")
        callsheet.set(callsheet.getCellFromAlias("pitch"), f"=1 in / TPI")
        callsheet.set(callsheet.getCellFromAlias("realOD"), f"=<<{self.addPrefix('spec')}>>.RealOD + diaExpansion")
        subtractive_helix.setExpression("Pitch", f"<<{self.addPrefix('callsheet')}>>.pitch")
        callsheet.set(callsheet.getCellFromAlias("helix_height"), f"=male_height + pitch")
        callsheet.set(callsheet.getCellFromAlias("thread_cutter_side"), f"=pitch * 0.97")
        callsheet.set(callsheet.getCellFromAlias("cone_height"), f"=male_height + 2 * pitch")
        callsheet.set(callsheet.getCellFromAlias("cone_bottom_big_r"), f"=realOD / 2")
        sketch.setExpression("Constraints[3]", f"<<{self.addPrefix('callsheet')}>>.thread_cutter_side")
        subtractive_helix.setExpression("Height", f"<<{self.addPrefix('callsheet')}>>.helix_height")
        additive_cone.setExpression("Height", f"<<{self.addPrefix('callsheet')}>>.cone_height")
        additive_cone.setExpression("Radius1", f"<<{self.addPrefix('callsheet')}>>.cone_bottom_big_r")
        additive_cylinder.setExpression("Radius", f"<<{self.addPrefix('callsheet')}>>.cone_bottom_big_r + 0.01 in")
        callsheet.set(callsheet.getCellFromAlias("cone_top_small_r"), f"=cone_bottom_big_r - slope_const * cone_height")
        callsheet.set(callsheet.getCellFromAlias("helix_r"), f"=cone_bottom_big_r")
        callsheet.set(callsheet.getCellFromAlias("thread_start_r"), f"=cone_bottom_big_r + pitch * 0.05")
        sketch.setExpression("Constraints[4]", f"<<{self.addPrefix('callsheet')}>>.thread_start_r")
        additive_cone.setExpression("Radius2", f"<<{self.addPrefix('callsheet')}>>.cone_top_small_r")
        callsheet.set(callsheet.getCellFromAlias("thread_cutter_z"), f"=(thread_start_r - cone_bottom_big_r) / 1.732 + 0.015 in")
        sketch.setExpression("Constraints[8]", f"<<{self.addPrefix('callsheet')}>>.thread_cutter_z")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        spec.nominalOD = '`1/16'
        
        # now we have rebuilt the original npt_m doc. Now we apply dynmic call parameters
        print("there can be temporary errors when we applying dynamic call parameters that change original npt_m's shape.")
        print("ignore temporary errors, if any, below.")
        callsheet.set(callsheet.getCellFromAlias('nominalOD'), f'{self.nominalOD}')
        callsheet.set(callsheet.getCellFromAlias('diaExpansion'), f'={self.diaExpansion}')
        callsheet.set(callsheet.getCellFromAlias('male_height'), f'={self.male_height}')
        doc.recompute()
        update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.
        print("ignore temporary errors, if any, above.")
        
        self.update_callsheet()


def main():
    # main_part1
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of npt_m
    myInstance = npt_m("myInstance", doc, objPrefix="", useLabel=True, importer=None, diaExpansion='0 in', male_height='0.3 in', nominalOD='`1/16', )
    
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
