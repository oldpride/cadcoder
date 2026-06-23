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
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, holeDiaExpansion='0.03 in', male_height='0.6 in', nominalOD='`1/2', outDiaExpansion='0 in', wall_thick='0.125 in',  ):
        self.holeDiaExpansion = holeDiaExpansion
        self.male_height = male_height
        self.nominalOD = nominalOD
        self.outDiaExpansion = outDiaExpansion
        self.wall_thick = wall_thick
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        from parts.npt_m import npt_m
        npt_m_instance = npt_m('npt_m_instance', doc, objPrefix=self.objPrefix + 'npt_m_', useLabel=True, importer=self, diaExpansion='0.0 in', male_height='0.6 in', nominalOD='`1/2')
        self.npt_m_instance = npt_m_instance # expose as instance variable
        self.update_imports(npt_m_instance) # update import info for the instance
        npt_m_instance.common_boolean.Visibility = False
        
        # add objects and add static value to objects' properties based on object dependencies
        callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('callsheet') )
        callsheet.Label = self.addPrefix('callsheet')
        self.callsheet = callsheet
        self.post_new_obj(callsheet)
        callsheet.set('A1', 'variableName')
        callsheet.set('A2', 'nominalOD')
        callsheet.set('A3', 'outDiaExpansion')
        callsheet.set('A4', 'holeDiaExpansion')
        callsheet.set('A5', 'male_height')
        callsheet.set('A6', 'wall_thick')
        callsheet.set('B1', 'value')
        callsheet.set('B2', '`1/2')
        callsheet.setAlias('B2', 'nominalOD')
        callsheet.set('B3', '=0 in')
        callsheet.setAlias('B3', 'outDiaExpansion')
        callsheet.set('B4', '=0.03 in')
        callsheet.setAlias('B4', 'holeDiaExpansion')
        callsheet.set('B5', '=0.6 in')
        callsheet.setAlias('B5', 'male_height')
        callsheet.set('B6', '=0.125 in')
        callsheet.setAlias('B6', 'wall_thick')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C2', 'Y')
        callsheet.set('C3', 'Y')
        callsheet.set('C4', 'Y')
        callsheet.set('C5', 'Y')
        callsheet.set('C6', 'Y')
        callsheet.set('D1', 'comment')
        callsheet.recompute()  # recompute after adding object
        
        callsheet2 = doc.addObject('Spreadsheet::Sheet', self.addPrefix('callsheet2') )
        callsheet2.Label = self.addPrefix('callsheet2')
        self.callsheet2 = callsheet2
        self.post_new_obj(callsheet2)
        callsheet2.set('A1', 'variableName')
        callsheet2.set('A2', 'holeDia')
        callsheet2.set('B1', 'value')
        callsheet2.set('B2', '=0.49628324000000007 in')
        callsheet2.setAlias('B2', 'holeDia')
        callsheet2.set('C1', 'isCallParam')
        callsheet2.set('C2', 'N')
        callsheet2.set('D1', 'comment')
        callsheet2.recompute()  # recompute after adding object
        
        sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('sketch') )
        sketch.Label = self.addPrefix('sketch')
        self.sketch = sketch
        self.post_new_obj(sketch)
        self.container_append_object(npt_m_instance.body, sketch)
        geo0 = sketch.addGeometry(Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 6.3028))
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 3, -1, 1))
        sketch.addConstraint(Sketcher.Constraint('Diameter', geo0, 12.6056))
        sketch.AttacherEngine = 'Engine Plane'
        sketch.AttachmentSupport = (npt_m_instance.common_boolean, (get_seName_by_posName(npt_m_instance.common_boolean, 'Face', 'top1')))
        npt_m_instance.common_boolean.Visibility = False  # hide base object
        update_obj_prop_jsonDict(sketch, "pythonFeature",{"AttachmentSupport": {"seType": "Face", "posName": "top1"}})
        sketch.MapMode = 'FlatFace'
        sketch.Visibility = False
        sketch.ViewObject.Visibility = False
        sketch.recompute()  # recompute after adding object
        
        pocket = doc.addObject('PartDesign::Pocket', self.addPrefix('pocket') )
        pocket.Label = self.addPrefix('pocket')
        self.pocket = pocket
        self.post_new_obj(pocket)
        self.container_append_object(npt_m_instance.body, pocket)
        pocket.BaseFeature = npt_m_instance.common_boolean
        pocket.Profile = (sketch, [''])
        pocket.ReferenceAxis = (sketch, ['N_Axis'])
        pocket.Type = 'ThroughAll'
        pocket.recompute()  # recompute after adding object
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        npt_m_instance.callsheet.set(npt_m_instance.callsheet.getCellFromAlias('nominalOD'), f"=<<{self.addPrefix('callsheet')}>>.nominalOD")
        npt_m_instance.callsheet.set(npt_m_instance.callsheet.getCellFromAlias('diaExpansion'), f"=<<{self.addPrefix('callsheet')}>>.outDiaExpansion")
        npt_m_instance.callsheet.set(npt_m_instance.callsheet.getCellFromAlias('male_height'), f"=<<{self.addPrefix('callsheet')}>>.male_height")
        callsheet2.set(callsheet2.getCellFromAlias('holeDia'), f"=<<{self.addPrefix('npt_m_spec')}>>.RealOD - <<{self.addPrefix('npt_m_spec')}>>.Pitch * 1.732 - <<{self.addPrefix('callsheet')}>>.wall_thick * 2 + <<{self.addPrefix('callsheet')}>>.holeDiaExpansion")
        sketch.setExpression('Constraints[1]', f"<<{self.addPrefix('callsheet2')}>>.holeDia")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # now we have rebuilt the original npt_m_hole doc. Now we apply dynmic call parameters
        print("there can be temporary errors when we applying dynamic call parameters that change original npt_m_hole's shape.")
        print("ignore temporary errors, if any, below.")
        callsheet.set(callsheet.getCellFromAlias('nominalOD'), f'{self.nominalOD}')
        callsheet.set(callsheet.getCellFromAlias('outDiaExpansion'), f'={self.outDiaExpansion}')
        callsheet.set(callsheet.getCellFromAlias('holeDiaExpansion'), f'={self.holeDiaExpansion}')
        callsheet.set(callsheet.getCellFromAlias('male_height'), f'={self.male_height}')
        callsheet.set(callsheet.getCellFromAlias('wall_thick'), f'={self.wall_thick}')
        doc.recompute()
        update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.
        print("ignore temporary errors, if any, above.")
        
        self.update_callsheet()


def main():
    # main_part1
    from cadcoder.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of npt_m_hole
    myInstance = npt_m_hole("myInstance", doc, objPrefix="", useLabel=True, importer=None, holeDiaExpansion='0.03 in', male_height='0.6 in', nominalOD='`1/2', outDiaExpansion='0 in', wall_thick='0.125 in', )
    
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
