from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.baseClass import baseClass
from cadcoder.containertools import get_LCS_by_prefix
from cadcoder.objtools import update_obj_prop_jsonDict
from cadcoder.subelementtools import update_objs_seName, update_doc_seName, get_seName_by_posName

class npt_m_handle_split_connect(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, bottom_b_pocket_height='1.016 mm', bottom_b_pocket_radius='0.375 in', bottom_s_pocket_radius='0.355 in', cylinder_height='0.5 in', cylinder_radius='19.05 mm', holeDiaExpansion='0.03 in', narrow_id_lenghth='0.72 in', npt_m_male_height='0.72 in', npt_m_nominalOD='`1-1/4', pin_height='0.08 in', pin_radius='0.05 in', prism_polygon_height='0.5 in', prism_polygon_sides=8, top_pocket_radius='9.525 mm',  ):
        self.bottom_b_pocket_height = bottom_b_pocket_height
        self.bottom_b_pocket_radius = bottom_b_pocket_radius
        self.bottom_s_pocket_radius = bottom_s_pocket_radius
        self.cylinder_height = cylinder_height
        self.cylinder_radius = cylinder_radius
        self.holeDiaExpansion = holeDiaExpansion
        self.narrow_id_lenghth = narrow_id_lenghth
        self.npt_m_male_height = npt_m_male_height
        self.npt_m_nominalOD = npt_m_nominalOD
        self.pin_height = pin_height
        self.pin_radius = pin_radius
        self.prism_polygon_height = prism_polygon_height
        self.prism_polygon_sides = prism_polygon_sides
        self.top_pocket_radius = top_pocket_radius
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        from parts.npt_m_handle_split import npt_m_handle_split
        npt_m_handle_split_instance = npt_m_handle_split('npt_m_handle_split_instance', doc, objPrefix=self.objPrefix + 'npt_m_handle_split_', useLabel=True, importer=self, bottom_b_pocket_height='0.04 in', bottom_b_pocket_radius='0.37499999999999994 in', bottom_s_pocket_radius='0.355 in', cylinder_height='0.5 in', cylinder_radius='0.7500000000000001 in', holeDiaExpansion='0.03 in', npt_m_male_height='0.7199999999999999 in', npt_m_nominalOD='`1-1/4', prism_polygon_height='0.5 in', prism_polygon_sides=8, top_pocket_height='1.0 in', top_pocket_radius='0.37500000000000006 in', )
        self.npt_m_handle_split_instance = npt_m_handle_split_instance # expose as instance variable
        self.update_imports(npt_m_handle_split_instance) # update import info for the instance
        npt_m_handle_split_instance.npt_m_handle_instance.bottom_b_sketch.Placement = Placement(Vector(0.0000, 0.0000, -18.2880), Rotation(1.0000, 0.0000, 0.0000, 0.0000))  # adjust imported object
        npt_m_handle_split_instance.npt_m_handle_instance.bottom_s_sketch.Placement = Placement(Vector(0.0000, 0.0000, -18.2880), Rotation(1.0000, 0.0000, 0.0000, 0.0000))  # adjust imported object
        npt_m_handle_split_instance.npt_m_handle_instance.cylinder_instance.body.Placement = Placement(Vector(0.0000, 0.0000, 12.7000), Rotation(0.0000, 0.0000, 0.0000, 1.0000))  # adjust imported object
        npt_m_handle_split_instance.npt_m_handle_instance.top_sketch.Placement = Placement(Vector(0.0000, 0.0000, 25.4000), Rotation(0.0000, 0.0000, 0.0000, 1.0000))  # adjust imported object
        npt_m_handle_split_instance.slice_0.Visibility = False  # adjust imported object
        npt_m_handle_split_instance.slice_1.Visibility = False  # adjust imported object
        from parts.cylinder import cylinder
        l_pin_cylinder_instance = cylinder('l_pin_cylinder_instance', doc, objPrefix=self.objPrefix + 'l_pin_', useLabel=True, importer=self, height='0.08 in', radius='0.05 in', )
        self.l_pin_cylinder_instance = l_pin_cylinder_instance # expose as instance variable
        self.update_imports(l_pin_cylinder_instance) # update import info for the instance
        l_pin_cylinder_instance.body.Placement = Placement(Vector(0.0000, 17.1450, 6.3500), Rotation(0.0000, 0.7071, 0.0000, 0.7071))  # adjust imported object
        from parts.cylinder import cylinder
        r_pin_cylinder_instance = cylinder('r_pin_cylinder_instance', doc, objPrefix=self.objPrefix + 'r_pin_', useLabel=True, importer=self, height='0.08 in', radius='0.05 in', )
        self.r_pin_cylinder_instance = r_pin_cylinder_instance # expose as instance variable
        self.update_imports(r_pin_cylinder_instance) # update import info for the instance
        r_pin_cylinder_instance.body.Placement = Placement(Vector(0.0000, -17.1450, 6.3500), Rotation(0.0000, 0.7071, 0.0000, 0.7071))  # adjust imported object
        from parts.cylinder import cylinder
        r_hole_cylinder_instance = cylinder('r_hole_cylinder_instance', doc, objPrefix=self.objPrefix + 'r_hole_', useLabel=True, importer=self, height='0.12000000000000001 in', radius='0.060000000000000005 in', )
        self.r_hole_cylinder_instance = r_hole_cylinder_instance # expose as instance variable
        self.update_imports(r_hole_cylinder_instance) # update import info for the instance
        r_hole_cylinder_instance.body.Placement = Placement(Vector(0.0000, 17.1450, 6.3500), Rotation(0.0000, 0.7071, 0.0000, 0.7071))  # adjust imported object
        from parts.cylinder import cylinder
        l_hole_cylinder_instance = cylinder('l_hole_cylinder_instance', doc, objPrefix=self.objPrefix + 'l_hole_', useLabel=True, importer=self, height='0.12000000000000001 in', radius='0.060000000000000005 in', )
        self.l_hole_cylinder_instance = l_hole_cylinder_instance # expose as instance variable
        self.update_imports(l_hole_cylinder_instance) # update import info for the instance
        l_hole_cylinder_instance.body.Placement = Placement(Vector(0.0000, -17.1450, 6.3500), Rotation(0.0000, 0.7071, 0.0000, 0.7071))  # adjust imported object
        
        # add objects and add static value to objects' properties based on object dependencies
        hole_side = doc.addObject('PartDesign::Body', self.addPrefix('hole_side') )
        hole_side.Label = self.addPrefix('hole_side')
        self.hole_side = hole_side
        self.post_new_obj(hole_side)
        hole_side_Origin = get_LCS_by_prefix(doc, hole_side, 'Origin')
        hole_side_X_Axis = get_LCS_by_prefix(doc, hole_side, 'X_Axis')
        hole_side_Y_Axis = get_LCS_by_prefix(doc, hole_side, 'Y_Axis')
        hole_side_Z_Axis = get_LCS_by_prefix(doc, hole_side, 'Z_Axis')
        hole_side_XY_Plane = get_LCS_by_prefix(doc, hole_side, 'XY_Plane')
        hole_side_XZ_Plane = get_LCS_by_prefix(doc, hole_side, 'XZ_Plane')
        hole_side_YZ_Plane = get_LCS_by_prefix(doc, hole_side, 'YZ_Plane')
        self.hole_side_Origin = hole_side_Origin
        self.hole_side_X_Axis = hole_side_X_Axis
        self.hole_side_Y_Axis = hole_side_Y_Axis
        self.hole_side_Z_Axis = hole_side_Z_Axis
        self.hole_side_XY_Plane = hole_side_XY_Plane
        self.hole_side_XZ_Plane = hole_side_XZ_Plane
        self.hole_side_YZ_Plane = hole_side_YZ_Plane
        self.post_new_obj(hole_side_Origin)
        self.post_new_obj(hole_side_X_Axis)
        self.post_new_obj(hole_side_Y_Axis)
        self.post_new_obj(hole_side_Z_Axis)
        self.post_new_obj(hole_side_XY_Plane)
        self.post_new_obj(hole_side_XZ_Plane)
        self.post_new_obj(hole_side_YZ_Plane)
        hole_side.recompute()  # recompute after adding object
        
        pin_side = doc.addObject('PartDesign::Body', self.addPrefix('pin_side') )
        pin_side.Label = self.addPrefix('pin_side')
        self.pin_side = pin_side
        self.post_new_obj(pin_side)
        pin_side_Origin = get_LCS_by_prefix(doc, pin_side, 'Origin')
        pin_side_X_Axis = get_LCS_by_prefix(doc, pin_side, 'X_Axis')
        pin_side_Y_Axis = get_LCS_by_prefix(doc, pin_side, 'Y_Axis')
        pin_side_Z_Axis = get_LCS_by_prefix(doc, pin_side, 'Z_Axis')
        pin_side_XY_Plane = get_LCS_by_prefix(doc, pin_side, 'XY_Plane')
        pin_side_XZ_Plane = get_LCS_by_prefix(doc, pin_side, 'XZ_Plane')
        pin_side_YZ_Plane = get_LCS_by_prefix(doc, pin_side, 'YZ_Plane')
        self.pin_side_Origin = pin_side_Origin
        self.pin_side_X_Axis = pin_side_X_Axis
        self.pin_side_Y_Axis = pin_side_Y_Axis
        self.pin_side_Z_Axis = pin_side_Z_Axis
        self.pin_side_XY_Plane = pin_side_XY_Plane
        self.pin_side_XZ_Plane = pin_side_XZ_Plane
        self.pin_side_YZ_Plane = pin_side_YZ_Plane
        self.post_new_obj(pin_side_Origin)
        self.post_new_obj(pin_side_X_Axis)
        self.post_new_obj(pin_side_Y_Axis)
        self.post_new_obj(pin_side_Z_Axis)
        self.post_new_obj(pin_side_XY_Plane)
        self.post_new_obj(pin_side_XZ_Plane)
        self.post_new_obj(pin_side_YZ_Plane)
        pin_side.recompute()  # recompute after adding object
        
        callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('callsheet') )
        callsheet.Label = self.addPrefix('callsheet')
        self.callsheet = callsheet
        self.post_new_obj(callsheet)
        callsheet.set('A1', 'variableName')
        callsheet.set('A10', 'bottom_s_pocket_radius')
        callsheet.set('A11', 'top_pocket_height')
        callsheet.set('A12', 'top_pocket_radius')
        callsheet.set('A13', 'prism_polygon_height')
        callsheet.set('A14', 'prism_polygon_sides')
        callsheet.set('A15', 'pin_height')
        callsheet.set('A16', 'pin_radius')
        callsheet.set('A17', 'pin_cylinde_y_placement')
        callsheet.set('A18', 'pin_cylinde_z_placement')
        callsheet.set('A19', 'hole_height')
        callsheet.set('A2', 'cylinder_height')
        callsheet.set('A20', 'hole_radius')
        callsheet.set('A3', 'cylinder_radius')
        callsheet.set('A4', 'holeDiaExpansion')
        callsheet.set('A5', 'npt_m_male_height')
        callsheet.set('A6', 'narrow_id_lenghth')
        callsheet.set('A7', 'npt_m_nominalOD')
        callsheet.set('A8', 'bottom_b_pocket_height')
        callsheet.set('A9', 'bottom_b_pocket_radius')
        callsheet.set('B1', 'value')
        callsheet.set('B10', '=0.355 in')
        callsheet.setAlias('B10', 'bottom_s_pocket_radius')
        callsheet.set('B11', '=1.0 in')
        callsheet.setAlias('B11', 'top_pocket_height')
        callsheet.set('B12', '=9.525 mm')
        callsheet.setAlias('B12', 'top_pocket_radius')
        callsheet.set('B13', '=0.5 in')
        callsheet.setAlias('B13', 'prism_polygon_height')
        callsheet.set('B14', '8')
        callsheet.setAlias('B14', 'prism_polygon_sides')
        callsheet.set('B15', '=0.08 in')
        callsheet.setAlias('B15', 'pin_height')
        callsheet.set('B16', '=0.05 in')
        callsheet.setAlias('B16', 'pin_radius')
        callsheet.set('B17', '=0.675 in')
        callsheet.setAlias('B17', 'pin_cylinde_y_placement')
        callsheet.set('B18', '=0.25 in')
        callsheet.setAlias('B18', 'pin_cylinde_z_placement')
        callsheet.set('B19', '=0.12000000000000001 in')
        callsheet.setAlias('B19', 'hole_height')
        callsheet.set('B2', '=0.5 in')
        callsheet.setAlias('B2', 'cylinder_height')
        callsheet.set('B20', '=0.060000000000000005 in')
        callsheet.setAlias('B20', 'hole_radius')
        callsheet.set('B3', '=19.05 mm')
        callsheet.setAlias('B3', 'cylinder_radius')
        callsheet.set('B4', '=0.03 in')
        callsheet.setAlias('B4', 'holeDiaExpansion')
        callsheet.set('B5', '=0.72 in')
        callsheet.setAlias('B5', 'npt_m_male_height')
        callsheet.set('B6', '=0.72 in')
        callsheet.setAlias('B6', 'narrow_id_lenghth')
        callsheet.set('B7', '`1-1/4')
        callsheet.setAlias('B7', 'npt_m_nominalOD')
        callsheet.set('B8', '=1.016 mm')
        callsheet.setAlias('B8', 'bottom_b_pocket_height')
        callsheet.set('B9', '=0.375 in')
        callsheet.setAlias('B9', 'bottom_b_pocket_radius')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C10', 'Y')
        callsheet.set('C11', 'N')
        callsheet.set('C12', 'Y')
        callsheet.set('C13', 'Y')
        callsheet.set('C14', 'Y')
        callsheet.set('C15', 'Y')
        callsheet.set('C16', 'Y')
        callsheet.set('C17', 'N')
        callsheet.set('C18', 'N')
        callsheet.set('C19', 'N')
        callsheet.set('C2', 'Y')
        callsheet.set('C20', 'N')
        callsheet.set('C3', 'Y')
        callsheet.set('C4', 'Y')
        callsheet.set('C5', 'Y')
        callsheet.set('C6', 'Y')
        callsheet.set('C7', 'Y')
        callsheet.set('C8', 'Y')
        callsheet.set('C9', 'Y')
        callsheet.set('D1', 'comment')
        callsheet.set('D15', 'pin_ pad length')
        callsheet.set('D16', 'pin_ y radius')
        callsheet.set('D19', 'r_hole_ pad length')
        callsheet.set('D20', 'r_hole_ y radius')
        callsheet.recompute()  # recompute after adding object
        
        slice0_binder = doc.addObject('PartDesign::SubShapeBinder', self.addPrefix('slice0_binder') )
        slice0_binder.Label = self.addPrefix('slice0_binder')
        self.slice0_binder = slice0_binder
        self.post_new_obj(slice0_binder)
        self.container_append_object(hole_side, slice0_binder)
        slice0_binder.addProperty("App::PropertyMatrix", "Cache_Slice_child0")
        slice0_binder.Cache_Slice_child0 = App.Matrix(1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0)
        slice0_binder.Context = (hole_side, 'slice0_binder.')
        slice0_binder.Support = [(npt_m_handle_split_instance.slice_0, (''))]
        slice0_binder.Visibility = False
        slice0_binder.ViewObject.Visibility = False
        slice0_binder.recompute()  # recompute after adding object
        
        slice1_binder = doc.addObject('PartDesign::SubShapeBinder', self.addPrefix('slice1_binder') )
        slice1_binder.Label = self.addPrefix('slice1_binder')
        self.slice1_binder = slice1_binder
        self.post_new_obj(slice1_binder)
        slice1_binder.addProperty("App::PropertyMatrix", "Cache_Slice_child1")
        slice1_binder.Cache_Slice_child1 = App.Matrix(1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0)
        slice1_binder.Context = (pin_side, 'slice1_binder.')
        slice1_binder.Support = [(npt_m_handle_split_instance.slice_1, (''))]
        slice1_binder.recompute()  # recompute after adding object
        
        hole_basefeature = doc.addObject('PartDesign::FeatureBase', self.addPrefix('hole_basefeature') )
        hole_basefeature.Label = self.addPrefix('hole_basefeature')
        self.hole_basefeature = hole_basefeature
        self.post_new_obj(hole_basefeature)
        self.container_append_object(hole_side, hole_basefeature)
        hole_basefeature.BaseFeature = slice0_binder
        hole_basefeature.Visibility = False
        hole_basefeature.ViewObject.Visibility = False
        hole_basefeature.recompute()  # recompute after adding object
        
        hole_boolean = doc.addObject('PartDesign::Boolean', self.addPrefix('hole_boolean') )
        hole_boolean.Label = self.addPrefix('hole_boolean')
        self.hole_boolean = hole_boolean
        self.post_new_obj(hole_boolean)
        self.container_append_object(hole_side, hole_boolean)
        hole_boolean.BaseFeature = hole_basefeature
        hole_boolean.Group = [r_hole_cylinder_instance.body, l_hole_cylinder_instance.body]
        hole_boolean.Type = 'Cut'
        hole_boolean.UsePlacement = True
        doc.recompute() # recompute whole document for PartDesign::Boolean
        
        pin_boolean = doc.addObject('PartDesign::Boolean', self.addPrefix('pin_boolean') )
        pin_boolean.Label = self.addPrefix('pin_boolean')
        self.pin_boolean = pin_boolean
        self.post_new_obj(pin_boolean)
        self.container_append_object(pin_side, pin_boolean)
        pin_boolean.Group = [slice1_binder, l_pin_cylinder_instance.body, r_pin_cylinder_instance.body]
        pin_boolean.UsePlacement = True
        pin_boolean.Visibility = False
        pin_boolean.ViewObject.Visibility = False
        doc.recompute() # recompute whole document for PartDesign::Boolean
        
        doc.recompute() # recompute before adding PartDesign::Chamfer to avoid error
        pin_chamfer = doc.addObject('PartDesign::Chamfer', self.addPrefix('pin_chamfer') )
        pin_chamfer.Label = self.addPrefix('pin_chamfer')
        self.pin_chamfer = pin_chamfer
        self.post_new_obj(pin_chamfer)
        self.container_append_object(pin_side, pin_chamfer)
        pin_chamfer.Base = (pin_boolean, [get_seName_by_posName(pin_boolean, 'Edge', 'right1'), get_seName_by_posName(pin_boolean, 'Edge', 'right2')])
        pin_boolean.Visibility = False  # hide chamfer base object
        update_obj_prop_jsonDict(pin_chamfer, "pythonFeature",{"Base": [{"seType": "Edge", "posName": "right1"}, {"seType": "Edge", "posName": "right2"}]})
        pin_chamfer.BaseFeature = pin_boolean
        pin_chamfer.recompute()  # recompute after adding object
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        l_pin_cylinder_instance.callsheet.set(l_pin_cylinder_instance.callsheet.getCellFromAlias('radius'), f"=<<{self.addPrefix('callsheet')}>>.pin_radius")
        l_pin_cylinder_instance.callsheet.set(l_pin_cylinder_instance.callsheet.getCellFromAlias('height'), f"=<<{self.addPrefix('callsheet')}>>.pin_height")
        npt_m_handle_split_instance.callsheet.set(npt_m_handle_split_instance.callsheet.getCellFromAlias('top_pocket_radius'), f"=<<{self.addPrefix('callsheet')}>>.top_pocket_radius")
        npt_m_handle_split_instance.callsheet.set(npt_m_handle_split_instance.callsheet.getCellFromAlias('prism_polygon_height'), f"=<<{self.addPrefix('callsheet')}>>.prism_polygon_height")
        npt_m_handle_split_instance.callsheet.set(npt_m_handle_split_instance.callsheet.getCellFromAlias('prism_polygon_sides'), f"=<<{self.addPrefix('callsheet')}>>.prism_polygon_sides")
        npt_m_handle_split_instance.callsheet.set(npt_m_handle_split_instance.callsheet.getCellFromAlias('cylinder_height'), f"=<<{self.addPrefix('callsheet')}>>.cylinder_height")
        npt_m_handle_split_instance.callsheet.set(npt_m_handle_split_instance.callsheet.getCellFromAlias('cylinder_radius'), f"=<<{self.addPrefix('callsheet')}>>.cylinder_radius")
        npt_m_handle_split_instance.callsheet.set(npt_m_handle_split_instance.callsheet.getCellFromAlias('holeDiaExpansion'), f"=<<{self.addPrefix('callsheet')}>>.holeDiaExpansion")
        npt_m_handle_split_instance.callsheet.set(npt_m_handle_split_instance.callsheet.getCellFromAlias('npt_m_male_height'), f"=<<{self.addPrefix('callsheet')}>>.npt_m_male_height")
        npt_m_handle_split_instance.callsheet.set(npt_m_handle_split_instance.callsheet.getCellFromAlias('npt_m_nominalOD'), f"=<<{self.addPrefix('callsheet')}>>.npt_m_nominalOD")
        npt_m_handle_split_instance.callsheet.set(npt_m_handle_split_instance.callsheet.getCellFromAlias('bottom_b_pocket_height'), f"=<<{self.addPrefix('callsheet')}>>.bottom_b_pocket_height")
        npt_m_handle_split_instance.callsheet.set(npt_m_handle_split_instance.callsheet.getCellFromAlias('bottom_b_pocket_radius'), f"=<<{self.addPrefix('callsheet')}>>.bottom_b_pocket_radius")
        npt_m_handle_split_instance.callsheet.set(npt_m_handle_split_instance.callsheet.getCellFromAlias('bottom_s_pocket_radius'), f"=<<{self.addPrefix('callsheet')}>>.bottom_s_pocket_radius")
        r_pin_cylinder_instance.callsheet.set(r_pin_cylinder_instance.callsheet.getCellFromAlias('radius'), f"=<<{self.addPrefix('callsheet')}>>.pin_radius")
        r_pin_cylinder_instance.callsheet.set(r_pin_cylinder_instance.callsheet.getCellFromAlias('height'), f"=<<{self.addPrefix('callsheet')}>>.pin_height")
        callsheet.set(callsheet.getCellFromAlias("top_pocket_height"), f"=prism_polygon_height + cylinder_height + npt_m_male_height - narrow_id_lenghth")
        callsheet.set(callsheet.getCellFromAlias("pin_cylinde_y_placement"), f"=top_pocket_radius + 0.3 in")
        callsheet.set(callsheet.getCellFromAlias("pin_cylinde_z_placement"), f"=prism_polygon_height / 2")
        callsheet.set(callsheet.getCellFromAlias("hole_height"), f"=pin_height + 0.04 in")
        callsheet.set(callsheet.getCellFromAlias("hole_radius"), f"=pin_radius + 0.01 in")
        l_hole_cylinder_instance.body.setExpression('.Placement.Base.z', f"<<{self.addPrefix('callsheet')}>>.pin_cylinde_z_placement")
        l_hole_cylinder_instance.callsheet.set(l_hole_cylinder_instance.callsheet.getCellFromAlias('radius'), f"=<<{self.addPrefix('callsheet')}>>.hole_radius")
        l_hole_cylinder_instance.callsheet.set(l_hole_cylinder_instance.callsheet.getCellFromAlias('height'), f"=<<{self.addPrefix('callsheet')}>>.hole_height")
        l_pin_cylinder_instance.body.setExpression('.Placement.Base.z', f"<<{self.addPrefix('callsheet')}>>.pin_cylinde_z_placement")
        npt_m_handle_split_instance.callsheet.set(npt_m_handle_split_instance.callsheet.getCellFromAlias('top_pocket_height'), f"=<<{self.addPrefix('callsheet')}>>.top_pocket_height")
        r_hole_cylinder_instance.body.setExpression('.Placement.Base.z', f"<<{self.addPrefix('callsheet')}>>.pin_cylinde_z_placement")
        r_hole_cylinder_instance.callsheet.set(r_hole_cylinder_instance.callsheet.getCellFromAlias('radius'), f"=<<{self.addPrefix('callsheet')}>>.hole_radius")
        r_hole_cylinder_instance.callsheet.set(r_hole_cylinder_instance.callsheet.getCellFromAlias('height'), f"=<<{self.addPrefix('callsheet')}>>.hole_height")
        r_pin_cylinder_instance.body.setExpression('.Placement.Base.z', f"<<{self.addPrefix('callsheet')}>>.pin_cylinde_z_placement")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # now we have rebuilt the original npt_m_handle_split_connect doc. Now we apply dynmic call parameters
        print("there can be temporary errors when we applying dynamic call parameters that change original npt_m_handle_split_connect's shape.")
        print("ignore temporary errors, if any, below.")
        callsheet.set(callsheet.getCellFromAlias('bottom_s_pocket_radius'), f'={self.bottom_s_pocket_radius}')
        callsheet.set(callsheet.getCellFromAlias('top_pocket_radius'), f'={self.top_pocket_radius}')
        callsheet.set(callsheet.getCellFromAlias('prism_polygon_height'), f'={self.prism_polygon_height}')
        callsheet.set(callsheet.getCellFromAlias('prism_polygon_sides'), f'{self.prism_polygon_sides}')
        callsheet.set(callsheet.getCellFromAlias('pin_height'), f'={self.pin_height}')
        callsheet.set(callsheet.getCellFromAlias('pin_radius'), f'={self.pin_radius}')
        callsheet.set(callsheet.getCellFromAlias('cylinder_height'), f'={self.cylinder_height}')
        callsheet.set(callsheet.getCellFromAlias('cylinder_radius'), f'={self.cylinder_radius}')
        callsheet.set(callsheet.getCellFromAlias('holeDiaExpansion'), f'={self.holeDiaExpansion}')
        callsheet.set(callsheet.getCellFromAlias('npt_m_male_height'), f'={self.npt_m_male_height}')
        callsheet.set(callsheet.getCellFromAlias('narrow_id_lenghth'), f'={self.narrow_id_lenghth}')
        callsheet.set(callsheet.getCellFromAlias('npt_m_nominalOD'), f'{self.npt_m_nominalOD}')
        callsheet.set(callsheet.getCellFromAlias('bottom_b_pocket_height'), f'={self.bottom_b_pocket_height}')
        callsheet.set(callsheet.getCellFromAlias('bottom_b_pocket_radius'), f'={self.bottom_b_pocket_radius}')
        doc.recompute()
        update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.
        print("ignore temporary errors, if any, above.")
        
        self.update_callsheet()


def main():
    # main_part1
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of npt_m_handle_split_connect
    myInstance = npt_m_handle_split_connect("myInstance", doc, objPrefix="", useLabel=True, importer=None, bottom_b_pocket_height='1.016 mm', bottom_b_pocket_radius='0.375 in', bottom_s_pocket_radius='0.355 in', cylinder_height='0.5 in', cylinder_radius='19.05 mm', holeDiaExpansion='0.03 in', narrow_id_lenghth='0.72 in', npt_m_male_height='0.72 in', npt_m_nominalOD='`1-1/4', pin_height='0.08 in', pin_radius='0.05 in', prism_polygon_height='0.5 in', prism_polygon_sides=8, top_pocket_radius='9.525 mm', )
    
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
