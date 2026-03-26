from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.baseClass import baseClass
from cadcoder.containertools import get_LCS_by_prefix
from cadcoder.objtools import update_obj_prop_jsonDict
from cadcoder.subelementtools import update_objs_seName, update_doc_seName, get_seName_by_posName

class npt_f(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, diaExpansion='0.03 in', femaleOD_wall='0.08 in', female_height='0.6 in', nominalID='`2',  ):
        self.diaExpansion = diaExpansion
        self.femaleOD_wall = femaleOD_wall
        self.female_height = female_height
        self.nominalID = nominalID
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        from parts.npt_m import npt_m
        npt_m_instance = npt_m('npt_m_instance', doc, objPrefix=self.objPrefix + 'npt_m_', useLabel=True, importer=self, diaExpansion='0.03 in', male_height='0.6 in', nominalOD='`2', )
        self.npt_m_instance = npt_m_instance # expose as instance variable
        self.update_imports(npt_m_instance) # update import info for the instance
        
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
        callsheet.set('A2', 'nominalID')
        callsheet.set('A3', 'femaleOD_wall')
        callsheet.set('A4', 'femaleOD')
        callsheet.set('A5', 'female_height')
        callsheet.set('A6', 'diaExpansion')
        callsheet.set('B1', 'value')
        callsheet.set('B2', '`2')
        callsheet.setAlias('B2', 'nominalID')
        callsheet.set('B3', '=0.08 in')
        callsheet.setAlias('B3', 'femaleOD_wall')
        callsheet.set('B4', '=2.565 in')
        callsheet.setAlias('B4', 'femaleOD')
        callsheet.set('B5', '=0.6 in')
        callsheet.setAlias('B5', 'female_height')
        callsheet.set('B6', '=0.03 in')
        callsheet.setAlias('B6', 'diaExpansion')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C2', 'Y')
        callsheet.set('C3', 'Y')
        callsheet.set('C4', 'N')
        callsheet.set('C5', 'Y')
        callsheet.set('C6', 'Y')
        callsheet.set('D1', 'comment')
        callsheet.recompute()  # recompute after adding object
        
        sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('sketch') )
        sketch.Label = self.addPrefix('sketch')
        self.sketch = sketch
        self.post_new_obj(sketch)
        self.container_append_object(body, sketch)
        geo0 = sketch.addGeometry(Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 32.5755))
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 3, -1, 1))
        sketch.addConstraint(Sketcher.Constraint('Diameter', geo0, 65.1510))
        sketch.AttacherEngine = 'Engine Plane'
        sketch.AttachmentSupport = (body_XY_Plane, (''))
        body_XY_Plane.Visibility = False  # hide base object
        sketch.MapMode = 'FlatFace'
        sketch.Visibility = False
        sketch.ViewObject.Visibility = False
        sketch.recompute()  # recompute after adding object
        
        pad = doc.addObject('PartDesign::Pad', self.addPrefix('pad') )
        pad.Label = self.addPrefix('pad')
        self.pad = pad
        self.post_new_obj(pad)
        self.container_append_object(body, pad)
        pad.Length = 15.239999999999998
        pad.Profile = (sketch, [''])
        pad.ReferenceAxis = (sketch, ['N_Axis'])
        pad.Visibility = False
        pad.ViewObject.Visibility = False
        pad.recompute()  # recompute after adding object
        
        boolean = doc.addObject('PartDesign::Boolean', self.addPrefix('boolean') )
        boolean.Label = self.addPrefix('boolean')
        self.boolean = boolean
        self.post_new_obj(boolean)
        self.container_append_object(body, boolean)
        boolean.BaseFeature = pad
        boolean.Group = [npt_m_instance.body]
        boolean.Type = 'Cut'
        boolean.UsePlacement = True
        doc.recompute() # recompute whole document for PartDesign::Boolean
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        npt_m_instance.callsheet.set(npt_m_instance.callsheet.getCellFromAlias('nominalOD'), f"=<<{self.addPrefix('callsheet')}>>.nominalID")
        npt_m_instance.callsheet.set(npt_m_instance.callsheet.getCellFromAlias('diaExpansion'), f"=<<{self.addPrefix('callsheet')}>>.diaExpansion")
        npt_m_instance.callsheet.set(npt_m_instance.callsheet.getCellFromAlias('male_height'), f"=<<{self.addPrefix('callsheet')}>>.female_height")
        pad.setExpression("Length", f"<<{self.addPrefix('callsheet')}>>.female_height")
        callsheet.set(callsheet.getCellFromAlias("femaleOD"), f"=femaleOD_wall * 2 + <<{self.addPrefix('npt_m_spec')}>>.RealOD + diaExpansion")
        sketch.setExpression("Constraints[1]", f"<<{self.addPrefix('callsheet')}>>.femaleOD")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # now we have rebuilt the original npt_f doc. Now we apply dynmic call parameters
        print("there can be temporary errors when we applying dynamic call parameters that change original npt_f's shape.")
        print("ignore temporary errors, if any, below.")
        callsheet.set(callsheet.getCellFromAlias('nominalID'), f'{self.nominalID}')
        callsheet.set(callsheet.getCellFromAlias('femaleOD_wall'), f'={self.femaleOD_wall}')
        callsheet.set(callsheet.getCellFromAlias('female_height'), f'={self.female_height}')
        callsheet.set(callsheet.getCellFromAlias('diaExpansion'), f'={self.diaExpansion}')
        doc.recompute()
        update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.
        print("ignore temporary errors, if any, above.")
        
        self.update_callsheet()


def main():
    # main_part1
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of npt_f
    myInstance = npt_f("myInstance", doc, objPrefix="", useLabel=True, importer=None, diaExpansion='0.03 in', femaleOD_wall='0.08 in', female_height='0.6 in', nominalID='`2', )
    
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
