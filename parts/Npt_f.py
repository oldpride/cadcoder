from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as App
import FreeCADGui as Gui
from pdfclib.baseClass import baseClass
from pdfclib.containertools import get_LCS_by_prefix
from pdfclib.objtools import update_obj_prop_jsonDict
from pdfclib.subelementtools import update_objs_seName, update_doc_seName, get_seName_by_posName

class Npt_f(baseClass):
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, femaleOD_wall_spec='0.08 in', female_height_spec='0.6 in', holeDiaExpansion_spec='0.03 in', horizontalScale=1.1982, nominalID='`1/16', verticalScale=1.261,  ):
        self.femaleOD_wall_spec = femaleOD_wall_spec
        self.female_height_spec = female_height_spec
        self.holeDiaExpansion_spec = holeDiaExpansion_spec
        self.horizontalScale = horizontalScale
        self.nominalID = nominalID
        self.verticalScale = verticalScale
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        from parts.Npt_m import Npt_m
        npt_m_instance = Npt_m('npt_m_instance', doc, objPrefix=self.objPrefix + 'npt_m_', useLabel=True, importer=self, holeDiaExpansion_spec='0.03 in', horizontalScale=1.1982, male_height_spec='0.6 in', nominalOD='`1/16', verticalScale=1.261, )
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
        callsheet.set('A10', 'holeDiaExpansion_spec')
        callsheet.set('A2', 'nominalID')
        callsheet.set('A3', 'horizontalScale')
        callsheet.set('A4', 'verticalScale')
        callsheet.set('A5', 'femaleOD_wall_spec')
        callsheet.set('A6', 'femaleOD_spec')
        callsheet.set('A7', 'femaleOD')
        callsheet.set('A8', 'female_height_spec')
        callsheet.set('A9', 'female_height')
        callsheet.set('B1', 'value')
        callsheet.set('B10', '=0.03 in')
        callsheet.setAlias('B10', 'holeDiaExpansion_spec')
        callsheet.set('B2', '`1/16')
        callsheet.setAlias('B2', 'nominalID')
        callsheet.set('B3', '1.1982')
        callsheet.setAlias('B3', 'horizontalScale')
        callsheet.set('B4', '1.261')
        callsheet.setAlias('B4', 'verticalScale')
        callsheet.set('B5', '=0.08 in')
        callsheet.setAlias('B5', 'femaleOD_wall_spec')
        callsheet.set('B6', '=0.5025000000000001 in')
        callsheet.setAlias('B6', 'femaleOD_spec')
        callsheet.set('B7', '=0.6020955 in')
        callsheet.setAlias('B7', 'femaleOD')
        callsheet.set('B8', '=0.6 in')
        callsheet.setAlias('B8', 'female_height_spec')
        callsheet.set('B9', '=0.7565999999999998 in')
        callsheet.setAlias('B9', 'female_height')
        callsheet.set('C1', 'isCallParam')
        callsheet.set('C10', 'Y')
        callsheet.set('C2', 'Y')
        callsheet.set('C3', 'Y')
        callsheet.set('C4', 'Y')
        callsheet.set('C5', 'Y')
        callsheet.set('C6', 'N')
        callsheet.set('C7', 'N')
        callsheet.set('C8', 'Y')
        callsheet.set('C9', 'N')
        callsheet.set('D1', 'comment')
        callsheet.set('D3', 'BASF 17-4 xy scale 1.1982')
        callsheet.set('D4', 'BASF 17-4 z scale 1.2610')
        callsheet.set('D6', '`femaleOD_wall * 2 + <<npt_m_spec>>.RealOD + holeDiaExpansion_spec')
        callsheet.set('D7', 'scaled')
        callsheet.set('D9', 'scaled')
        callsheet.recompute()  # recompute after adding object
        
        sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('sketch') )
        sketch.Label = self.addPrefix('sketch')
        self.sketch = sketch
        self.post_new_obj(sketch)
        self.container_append_object(body, sketch)
        geo0 = sketch.addGeometry(Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 7.6466))
        sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 3, -1, 1))
        sketch.addConstraint(Sketcher.Constraint('Diameter', geo0, 15.2932))
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
        pad.Length = 19.217639999999996
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
        npt_m_instance.callsheet.set(npt_m_instance.callsheet.getCellFromAlias('male_height_spec'), f"=<<{self.addPrefix('callsheet')}>>.female_height_spec")
        npt_m_instance.callsheet.set(npt_m_instance.callsheet.getCellFromAlias('nominalOD'), f"=<<{self.addPrefix('callsheet')}>>.nominalID")
        npt_m_instance.callsheet.set(npt_m_instance.callsheet.getCellFromAlias('horizontalScale'), f"=<<{self.addPrefix('callsheet')}>>.horizontalScale")
        npt_m_instance.callsheet.set(npt_m_instance.callsheet.getCellFromAlias('verticalScale'), f"=<<{self.addPrefix('callsheet')}>>.verticalScale")
        npt_m_instance.callsheet.set(npt_m_instance.callsheet.getCellFromAlias('holeDiaExpansion_spec'), f"=<<{self.addPrefix('callsheet')}>>.holeDiaExpansion_spec")
        callsheet.set(callsheet.getCellFromAlias("female_height"), f"=female_height_spec * verticalScale")
        pad.setExpression("Length", f"<<{self.addPrefix('callsheet')}>>.female_height")
        callsheet.set(callsheet.getCellFromAlias("femaleOD_spec"), f"=femaleOD_wall_spec * 2 + <<{self.addPrefix('npt_m_spec')}>>.RealOD + holeDiaExpansion_spec")
        callsheet.set(callsheet.getCellFromAlias("femaleOD"), f"=femaleOD_spec * horizontalScale")
        sketch.setExpression("Constraints[1]", f"<<{self.addPrefix('callsheet')}>>.femaleOD")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # now we have rebuilt the original Npt_f doc. Now we apply dynmic call parameters
        print("there can be temporary errors when we applying dynamic call parameters that change original Npt_f's shape.")
        print("ignore temporary errors, if any, below.")
        callsheet.set(callsheet.getCellFromAlias('holeDiaExpansion_spec'), f'={self.holeDiaExpansion_spec}')
        callsheet.set(callsheet.getCellFromAlias('nominalID'), f'{self.nominalID}')
        callsheet.set(callsheet.getCellFromAlias('horizontalScale'), f'{self.horizontalScale}')
        callsheet.set(callsheet.getCellFromAlias('verticalScale'), f'{self.verticalScale}')
        callsheet.set(callsheet.getCellFromAlias('femaleOD_wall_spec'), f'={self.femaleOD_wall_spec}')
        callsheet.set(callsheet.getCellFromAlias('female_height_spec'), f'={self.female_height_spec}')
        doc.recompute()
        update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.
        print("ignore temporary errors, if any, above.")
        
        self.update_callsheet()


def main():
    # main_part1
    from pdfclib.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of Npt_f
    myInstance = Npt_f("myInstance", doc, objPrefix="", useLabel=True, importer=None, femaleOD_wall_spec='0.08 in', female_height_spec='0.6 in', holeDiaExpansion_spec='0.03 in', horizontalScale=1.1982, nominalID='`1/16', verticalScale=1.261, )
    
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
