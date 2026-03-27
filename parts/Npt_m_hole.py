from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from cadcoder.baseClass import baseClass
from cadcoder.containertools import get_LCS_by_prefix
from cadcoder.objtools import update_obj_prop_jsonDict
from cadcoder.subelementtools import update_objs_seName, update_doc_seName, get_seName_by_posName

class npt_m_hole(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, bottomHoleDepth='0.5 in', bottomHoleDia0='0.2 in', holeDiaExpansion='0.03 in', male_height='0.6 in', nominalOD='`1/2', topHoleDepth='0.4 in', topHoleDia0='0.3 in',  ):
        self.bottomHoleDepth = bottomHoleDepth
        self.bottomHoleDia0 = bottomHoleDia0
        self.holeDiaExpansion = holeDiaExpansion
        self.male_height = male_height
        self.nominalOD = nominalOD
        self.topHoleDepth = topHoleDepth
        self.topHoleDia0 = topHoleDia0
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        from parts.npt_m import npt_m
        npt_m_instance = npt_m('npt_m_instance', doc, objPrefix=self.objPrefix + 'npt_m_', useLabel=True, importer=self, male_height='0.6 in', nominalOD='`1/2', )
        self.npt_m_instance = npt_m_instance # expose as instance variable
        self.update_imports(npt_m_instance) # update import info for the instance
        npt_m_instance.common_boolean.Visibility = False  # adjust imported object
        
        # add objects and add static value to objects' properties based on object dependencies
        callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('callsheet') )
        callsheet.Label = self.addPrefix('callsheet')
        self.callsheet = callsheet
        self.post_new_obj(callsheet)
        callsheet.set('A1', 'variableName')
        callsheet.set('A2', 'nominalOD')
        callsheet.set('A3', 'holeDiaExpansion')
        callsheet.set('A4', 'male_height')
        callsheet.set('A5', 'topHoleDepth')
        callsheet.set('A6', 'bottomHoleDepth')
        callsheet.set('B1', 'value')
        callsheet.set('B2', '`1/2')
        callsheet.setAlias('B2', 'nominalOD')
        callsheet.set('B3', '=0.03 in')
        callsheet.setAlias('B3', 'holeDiaExpansion')
        callsheet.set('B4', '=0.6 in')
        callsheet.setAlias('B4', 'male_height')
        callsheet.set('B5', '=0.4 in')
        callsheet.setAlias('B5', 'topHoleDepth')
        callsheet.set('B6', '=0.5 in')
        callsheet.setAlias('B6', 'bottomHoleDepth')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C2', 'Y')
        callsheet.set('C3', 'Y')
        callsheet.set('C4', 'Y')
        callsheet.set('C5', 'Y')
        callsheet.set('C6', 'Y')
        callsheet.set('D1', 'comment')
        callsheet.recompute()  # recompute after adding object
        
        callsheet_hole = doc.addObject('Spreadsheet::Sheet', self.addPrefix('callsheet_hole') )
        callsheet_hole.Label = self.addPrefix('callsheet_hole')
        self.callsheet_hole = callsheet_hole
        self.post_new_obj(callsheet_hole)
        callsheet_hole.set('A1', 'variableName')
        callsheet_hole.set('A2', 'topHoleDia0')
        callsheet_hole.set('A3', 'topHoleDia')
        callsheet_hole.set('A4', 'bottomHoleDia0')
        callsheet_hole.set('A5', 'bottomHoleDia')
        callsheet_hole.set('B1', 'value')
        callsheet_hole.set('B2', '=0.3 in')
        callsheet_hole.setAlias('B2', 'topHoleDia0')
        callsheet_hole.set('B3', '=0.33 in')
        callsheet_hole.setAlias('B3', 'topHoleDia')
        callsheet_hole.set('B4', '=0.2 in')
        callsheet_hole.setAlias('B4', 'bottomHoleDia0')
        callsheet_hole.set('B5', '=0.23 in')
        callsheet_hole.setAlias('B5', 'bottomHoleDia')
        callsheet_hole.set('C1', 'isCallParam')
        callsheet_hole.set('C2', 'Y')
        callsheet_hole.set('C3', 'N')
        callsheet_hole.set('C4', 'Y')
        callsheet_hole.set('C5', 'N')
        callsheet_hole.set('D1', 'comment')
        callsheet_hole.recompute()  # recompute after adding object
        
        top_sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('top_sketch') )
        top_sketch.Label = self.addPrefix('top_sketch')
        self.top_sketch = top_sketch
        self.post_new_obj(top_sketch)
        self.container_append_object(npt_m_instance.body, top_sketch)
        geo0 = top_sketch.addGeometry(Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 4.1910))
        top_sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 3, -1, 1))
        top_sketch.addConstraint(Sketcher.Constraint('Diameter', geo0, 8.3820))
        top_sketch.AttacherEngine = 'Engine Plane'
        top_sketch.AttachmentSupport = (npt_m_instance.common_boolean, (get_seName_by_posName(npt_m_instance.common_boolean, 'Face', 'top1')))
        npt_m_instance.common_boolean.Visibility = False  # hide base object
        update_obj_prop_jsonDict(top_sketch, "pythonFeature",{"AttachmentSupport": {"seType": "Face", "posName": "top1"}})
        top_sketch.MapMode = 'FlatFace'
        top_sketch.Visibility = False
        top_sketch.ViewObject.Visibility = False
        top_sketch.recompute()  # recompute after adding object
        
        top_pocket = doc.addObject('PartDesign::Pocket', self.addPrefix('top_pocket') )
        top_pocket.Label = self.addPrefix('top_pocket')
        self.top_pocket = top_pocket
        self.post_new_obj(top_pocket)
        self.container_append_object(npt_m_instance.body, top_pocket)
        top_pocket.BaseFeature = npt_m_instance.common_boolean
        top_pocket.Length = 10.16
        top_pocket.Profile = (top_sketch, [''])
        top_pocket.ReferenceAxis = (top_sketch, ['N_Axis'])
        top_pocket.Visibility = False
        top_pocket.ViewObject.Visibility = False
        top_pocket.recompute()  # recompute after adding object
        
        bottom_sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('bottom_sketch') )
        bottom_sketch.Label = self.addPrefix('bottom_sketch')
        self.bottom_sketch = bottom_sketch
        self.post_new_obj(bottom_sketch)
        self.container_append_object(npt_m_instance.body, bottom_sketch)
        geo0 = bottom_sketch.addGeometry(Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 2.9210))
        bottom_sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 3, -1, 1))
        bottom_sketch.addConstraint(Sketcher.Constraint('Diameter', geo0, 5.8420))
        bottom_sketch.AttacherEngine = 'Engine Plane'
        bottom_sketch.AttachmentSupport = (top_pocket, (get_seName_by_posName(top_pocket, 'Face', 'bottom1')))
        top_pocket.Visibility = False  # hide base object
        update_obj_prop_jsonDict(bottom_sketch, "pythonFeature",{"AttachmentSupport": {"seType": "Face", "posName": "bottom1"}})
        bottom_sketch.MapMode = 'FlatFace'
        bottom_sketch.Visibility = False
        bottom_sketch.ViewObject.Visibility = False
        bottom_sketch.recompute()  # recompute after adding object
        
        bottom_pocket = doc.addObject('PartDesign::Pocket', self.addPrefix('bottom_pocket') )
        bottom_pocket.Label = self.addPrefix('bottom_pocket')
        self.bottom_pocket = bottom_pocket
        self.post_new_obj(bottom_pocket)
        self.container_append_object(npt_m_instance.body, bottom_pocket)
        bottom_pocket.BaseFeature = top_pocket
        bottom_pocket.Length = 12.7
        bottom_pocket.Profile = (bottom_sketch, [''])
        bottom_pocket.ReferenceAxis = (bottom_sketch, ['N_Axis'])
        bottom_pocket.recompute()  # recompute after adding object
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        npt_m_instance.callsheet.set(npt_m_instance.callsheet.getCellFromAlias('nominalOD'), f"=<<{self.addPrefix('callsheet')}>>.nominalOD")
        npt_m_instance.callsheet.set(npt_m_instance.callsheet.getCellFromAlias('male_height'), f"=<<{self.addPrefix('callsheet')}>>.male_height")
        top_pocket.setExpression("Length", f"<<{self.addPrefix('callsheet')}>>.topHoleDepth")
        bottom_pocket.setExpression("Length", f"<<{self.addPrefix('callsheet')}>>.bottomHoleDepth")
        callsheet_hole.set(callsheet_hole.getCellFromAlias("topHoleDia"), f"=topHoleDia0 + <<{self.addPrefix('callsheet')}>>.holeDiaExpansion")
        callsheet_hole.set(callsheet_hole.getCellFromAlias("bottomHoleDia"), f"=bottomHoleDia0 + <<{self.addPrefix('callsheet')}>>.holeDiaExpansion")
        top_sketch.setExpression("Constraints[1]", f"<<{self.addPrefix('callsheet_hole')}>>.topHoleDia")
        bottom_sketch.setExpression("Constraints[1]", f"<<{self.addPrefix('callsheet_hole')}>>.bottomHoleDia")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # now we have rebuilt the original npt_m_hole doc. Now we apply dynmic call parameters
        print("there can be temporary errors when we applying dynamic call parameters that change original npt_m_hole's shape.")
        print("ignore temporary errors, if any, below.")
        callsheet.set(callsheet.getCellFromAlias('nominalOD'), f'{self.nominalOD}')
        callsheet.set(callsheet.getCellFromAlias('holeDiaExpansion'), f'={self.holeDiaExpansion}')
        callsheet.set(callsheet.getCellFromAlias('male_height'), f'={self.male_height}')
        callsheet.set(callsheet.getCellFromAlias('topHoleDepth'), f'={self.topHoleDepth}')
        callsheet.set(callsheet.getCellFromAlias('bottomHoleDepth'), f'={self.bottomHoleDepth}')
        callsheet_hole.set(callsheet_hole.getCellFromAlias('topHoleDia0'), f'={self.topHoleDia0}')
        callsheet_hole.set(callsheet_hole.getCellFromAlias('bottomHoleDia0'), f'={self.bottomHoleDia0}')
        doc.recompute()
        update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.
        print("ignore temporary errors, if any, above.")
        
        self.update_callsheet()


def main():
    # main_part1
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of npt_m_hole
    myInstance = npt_m_hole("myInstance", doc, objPrefix="", useLabel=True, importer=None, bottomHoleDepth='0.5 in', bottomHoleDia0='0.2 in', holeDiaExpansion='0.03 in', male_height='0.6 in', nominalOD='`1/2', topHoleDepth='0.4 in', topHoleDia0='0.3 in', )
    
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
