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
    def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, femaleOD_wall_spec='0.08 in', female_height_spec='0.9 in', holeDiaExpansion_spec='0.03 in', horizontalScale=1.1982, nominalID='`1/4', verticalScale=1.261,  ):
        self.femaleOD_wall_spec = femaleOD_wall_spec
        self.female_height_spec = female_height_spec
        self.holeDiaExpansion_spec = holeDiaExpansion_spec
        self.horizontalScale = horizontalScale
        self.nominalID = nominalID
        self.verticalScale = verticalScale
        
        super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
        
        # import classes and create instances for directly imported objects
        from parts.Npt_m import Npt_m
        npt_m_instance = Npt_m('npt_m_instance', doc, objPrefix=self.objPrefix + '', useLabel=True, importer=self, holeDiaExpansion_spec='0.03 in', horizontalScale=1.1982, male_height_spec='0.9 in', nominalOD='`1/4', verticalScale=1.261, )
        self.npt_m_instance = npt_m_instance # expose as instance variable
        self.update_imports(npt_m_instance) # update import info for the instance
        npt_m_instance.npt_m.Visibility = True  # adjust imported object
        
        # add objects and add static value to objects' properties based on object dependencies
        npt_f = doc.addObject('PartDesign::Body', self.addPrefix('Body001') )
        npt_f.Label = self.addPrefix('npt_f')
        self.npt_f = npt_f # expose as instance variable using Label varname
        self.post_new_obj(npt_f)
        npt_f_Origin = get_LCS_by_prefix(doc, npt_f, 'Origin')
        npt_f_X_Axis = get_LCS_by_prefix(doc, npt_f, 'X_Axis')
        npt_f_Y_Axis = get_LCS_by_prefix(doc, npt_f, 'Y_Axis')
        npt_f_Z_Axis = get_LCS_by_prefix(doc, npt_f, 'Z_Axis')
        npt_f_XY_Plane = get_LCS_by_prefix(doc, npt_f, 'XY_Plane')
        npt_f_XZ_Plane = get_LCS_by_prefix(doc, npt_f, 'XZ_Plane')
        npt_f_YZ_Plane = get_LCS_by_prefix(doc, npt_f, 'YZ_Plane')
        self.npt_f_Origin = npt_f_Origin # expose as instance variable using Label varname
        self.npt_f_X_Axis = npt_f_X_Axis # expose as instance variable using Label varname
        self.npt_f_Y_Axis = npt_f_Y_Axis # expose as instance variable using Label varname
        self.npt_f_Z_Axis = npt_f_Z_Axis # expose as instance variable using Label varname
        self.npt_f_XY_Plane = npt_f_XY_Plane # expose as instance variable using Label varname
        self.npt_f_XZ_Plane = npt_f_XZ_Plane # expose as instance variable using Label varname
        self.npt_f_YZ_Plane = npt_f_YZ_Plane # expose as instance variable using Label varname
        self.post_new_obj(npt_f_Origin)
        self.post_new_obj(npt_f_X_Axis)
        self.post_new_obj(npt_f_Y_Axis)
        self.post_new_obj(npt_f_Z_Axis)
        self.post_new_obj(npt_f_XY_Plane)
        self.post_new_obj(npt_f_XZ_Plane)
        self.post_new_obj(npt_f_YZ_Plane)
        npt_f.Visibility = False
        npt_f.ViewObject.Visibility = False
        npt_f.recompute()  # recompute after adding object
        
        npt_f_callsheet = doc.addObject('Spreadsheet::Sheet', self.addPrefix('Spreadsheet002') )
        npt_f_callsheet.Label = self.addPrefix('npt_f_callsheet')
        self.npt_f_callsheet = npt_f_callsheet # expose as instance variable using Label varname
        self.post_new_obj(npt_f_callsheet)
        npt_f_callsheet.set('A1', 'variableName')
        npt_f_callsheet.set('A10', 'holeDiaExpansion_spec')
        npt_f_callsheet.set('A2', 'nominalID')
        npt_f_callsheet.set('A3', 'horizontalScale')
        npt_f_callsheet.set('A4', 'verticalScale')
        npt_f_callsheet.set('A5', 'femaleOD_wall_spec')
        npt_f_callsheet.set('A6', 'femaleOD_spec')
        npt_f_callsheet.set('A7', 'femaleOD')
        npt_f_callsheet.set('A8', 'female_height_spec')
        npt_f_callsheet.set('A9', 'female_height')
        npt_f_callsheet.set('B1', 'value')
        npt_f_callsheet.set('B10', '=0.03 in')
        npt_f_callsheet.setAlias('B10', 'holeDiaExpansion_spec')
        npt_f_callsheet.set('B2', '`1/4')
        npt_f_callsheet.setAlias('B2', 'nominalID')
        npt_f_callsheet.set('B3', '1.1982')
        npt_f_callsheet.setAlias('B3', 'horizontalScale')
        npt_f_callsheet.set('B4', '1.261')
        npt_f_callsheet.setAlias('B4', 'verticalScale')
        npt_f_callsheet.set('B5', '=0.08 in')
        npt_f_callsheet.setAlias('B5', 'femaleOD_wall_spec')
        npt_f_callsheet.set('B6', '=0.7300000000000001 in')
        npt_f_callsheet.setAlias('B6', 'femaleOD_spec')
        npt_f_callsheet.set('B7', '=0.8746860000000001 in')
        npt_f_callsheet.setAlias('B7', 'femaleOD')
        npt_f_callsheet.set('B8', '=0.9 in')
        npt_f_callsheet.setAlias('B8', 'female_height_spec')
        npt_f_callsheet.set('B9', '=1.1349 in')
        npt_f_callsheet.setAlias('B9', 'female_height')
        npt_f_callsheet.set('C1', 'isCallParam')
        npt_f_callsheet.set('C10', 'Y')
        npt_f_callsheet.set('C2', 'Y')
        npt_f_callsheet.set('C3', 'Y')
        npt_f_callsheet.set('C4', 'Y')
        npt_f_callsheet.set('C5', 'Y')
        npt_f_callsheet.set('C6', 'N')
        npt_f_callsheet.set('C7', 'N')
        npt_f_callsheet.set('C8', 'Y')
        npt_f_callsheet.set('C9', 'N')
        npt_f_callsheet.set('D1', 'comment')
        npt_f_callsheet.set('D3', 'BASF 17-4 xy scale 1.1982')
        npt_f_callsheet.set('D4', 'BASF 17-4 z scale 1.2610')
        npt_f_callsheet.set('D6', '`femaleOD_wall * 2 + <<npt_m_spec>>.RealOD + holeDiaExpansion_spec')
        npt_f_callsheet.set('D7', 'scaled')
        npt_f_callsheet.set('D9', 'scaled')
        npt_f_callsheet.recompute()  # recompute after adding object
        
        npt_f_sketch = doc.addObject('Sketcher::SketchObject', self.addPrefix('Sketch001') )
        npt_f_sketch.Label = self.addPrefix('npt_f_sketch')
        self.npt_f_sketch = npt_f_sketch # expose as instance variable using Label varname
        self.post_new_obj(npt_f_sketch)
        self.container_append_object(npt_f, npt_f_sketch)
        geo0 = npt_f_sketch.addGeometry(Part.Circle(Vector(0.0000, 0.0000, 0.0000), Vector (0.0, 0.0, 1.0), 11.1085))
        npt_f_sketch.addConstraint(Sketcher.Constraint('Coincident', geo0, 3, -1, 1))
        npt_f_sketch.addConstraint(Sketcher.Constraint('Diameter', geo0, 22.2170))
        npt_f_sketch.AttacherEngine = 'Engine Plane'
        npt_f_sketch.AttachmentSupport = (npt_f_XY_Plane, (''))
        npt_f_XY_Plane.Visibility = False  # hide base object
        npt_f_sketch.MapMode = 'FlatFace'
        npt_f_sketch.Visibility = False
        npt_f_sketch.ViewObject.Visibility = False
        npt_f_sketch.recompute()  # recompute after adding object
        
        npt_f_pad = doc.addObject('PartDesign::Pad', self.addPrefix('Pad') )
        npt_f_pad.Label = self.addPrefix('npt_f_pad')
        self.npt_f_pad = npt_f_pad # expose as instance variable using Label varname
        self.post_new_obj(npt_f_pad)
        self.container_append_object(npt_f, npt_f_pad)
        npt_f_pad.Length = 28.826459999999997
        npt_f_pad.Profile = (npt_f_sketch, [''])
        npt_f_pad.ReferenceAxis = (npt_f_sketch, ['N_Axis'])
        npt_f_pad.Visibility = False
        npt_f_pad.ViewObject.Visibility = False
        npt_f_pad.recompute()  # recompute after adding object
        
        Boolean = doc.addObject('PartDesign::Boolean', self.addPrefix('Boolean') )
        Boolean.Label = self.addPrefix('Boolean')
        self.Boolean = Boolean # expose as instance variable using Label varname
        self.post_new_obj(Boolean)
        self.container_append_object(npt_f, Boolean)
        Boolean.BaseFeature = npt_f_pad
        Boolean.Group = [npt_m_instance.npt_m]
        Boolean.Type = 'Cut'
        Boolean.UsePlacement = True
        doc.recompute() # recompute whole document for {obj.TypeId}
        
        Compound = doc.addObject('Part::Compound', self.addPrefix('Compound') )
        Compound.Label = self.addPrefix('Compound')
        self.Compound = Compound # expose as instance variable using Label varname
        self.post_new_obj(Compound)
        Compound.Links = [npt_m_instance.npt_m_helix, npt_f]
        Compound.recompute()  # recompute after adding object
        
        # add delayed static property values
        
        # add expressions to object properties based on expression dependencies
        npt_m_instance.npt_m_callsheet.set(npt_m_instance.npt_m_callsheet.getCellFromAlias('male_height_spec'), f"=<<{self.addPrefix('npt_f_callsheet')}>>.female_height_spec") # call param, B12's alias=male_height_spec
        npt_m_instance.npt_m_callsheet.set(npt_m_instance.npt_m_callsheet.getCellFromAlias('nominalOD'), f"=<<{self.addPrefix('npt_f_callsheet')}>>.nominalID") # call param, B2's alias=nominalOD
        npt_m_instance.npt_m_callsheet.set(npt_m_instance.npt_m_callsheet.getCellFromAlias('horizontalScale'), f"=<<{self.addPrefix('npt_f_callsheet')}>>.horizontalScale") # call param, B3's alias=horizontalScale
        npt_m_instance.npt_m_callsheet.set(npt_m_instance.npt_m_callsheet.getCellFromAlias('verticalScale'), f"=<<{self.addPrefix('npt_f_callsheet')}>>.verticalScale") # call param, B4's alias=verticalScale
        npt_m_instance.npt_m_callsheet.set(npt_m_instance.npt_m_callsheet.getCellFromAlias('holeDiaExpansion_spec'), f"=<<{self.addPrefix('npt_f_callsheet')}>>.holeDiaExpansion_spec") # call param, B6's alias=holeDiaExpansion_spec
        npt_f_callsheet.set(npt_f_callsheet.getCellFromAlias("female_height"), f"=female_height_spec * verticalScale")
        npt_f_pad.setExpression("Length", f"<<{self.addPrefix('npt_f_callsheet')}>>.female_height")
        npt_f_callsheet.set(npt_f_callsheet.getCellFromAlias("femaleOD_spec"), f"=femaleOD_wall_spec * 2 + <<{self.addPrefix('npt_m_spec')}>>.RealOD + holeDiaExpansion_spec")
        npt_f_callsheet.set(npt_f_callsheet.getCellFromAlias("femaleOD"), f"=femaleOD_spec * horizontalScale")
        npt_f_sketch.setExpression("Constraints[1]", f"<<{self.addPrefix('npt_f_callsheet')}>>.femaleOD")
        
        # add trigger objects' expressions
        
        # add delayed expression property values - values, not expressions, eg, enum value
        
        # now we have rebuilt the original Npt_f doc. Now we apply dynmic call parameters
        print("there can be temporary errors when we applying dynamic call parameters that change original Npt_f's shape.")
        print("ignore temporary errors, if any, below.")
        npt_f_callsheet.set(npt_f_callsheet.getCellFromAlias('holeDiaExpansion_spec'), f'={self.holeDiaExpansion_spec}')
        npt_f_callsheet.set(npt_f_callsheet.getCellFromAlias('nominalID'), f'{self.nominalID}')
        npt_f_callsheet.set(npt_f_callsheet.getCellFromAlias('horizontalScale'), f'{self.horizontalScale}')
        npt_f_callsheet.set(npt_f_callsheet.getCellFromAlias('verticalScale'), f'{self.verticalScale}')
        npt_f_callsheet.set(npt_f_callsheet.getCellFromAlias('femaleOD_wall_spec'), f'={self.femaleOD_wall_spec}')
        npt_f_callsheet.set(npt_f_callsheet.getCellFromAlias('female_height_spec'), f'={self.female_height_spec}')
        doc.recompute()
        update_doc_seName(doc, refreshCache=True) # call params may change shape, so we update face/edge names.
        print("ignore temporary errors, if any, above.")
        
        # set callsheet
        self.callsheet = self.npt_f_callsheet
        self.update_callsheet()


def main():
    # main_part1
    from pdfclib.doctools import recreate_tmp_doc
    doc = recreate_tmp_doc()
    
    # create instance of Npt_f
    myInstance = Npt_f("myInstance", doc, objPrefix="", useLabel=True, importer=None, femaleOD_wall_spec='0.08 in', female_height_spec='0.9 in', holeDiaExpansion_spec='0.03 in', horizontalScale=1.1982, nominalID='`1/4', verticalScale=1.261, )
    
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
