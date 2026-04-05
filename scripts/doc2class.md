Goal is to design FreeCAD part like Python coding.

``` mermaid
graph TD
    mypart.FCStd --doc2class.py--> mypart.py -- python interpreter --> mypart.FCStd 

```

design consideration:
    1. freeCAD doc only has objects, no classes, no instances. Python files have classes and instances.
    therefore, we need to persist the class and instance info into objects, using custom properties.
    2. instance and class information are stored in object's pythonSource property. 
    3. try to use baseclass to handle persistence as much as possible, to avoid code duplication.
    5. import parameters are stored in main callsheet object only. 
    6. when doc2class.py uses mypart.FCStd to generate mypart.py, it scans all objects's pythonSource property to determine which classes to import.
    7. when mypart.py generates mypart.FCStd, it will set each object's pythonSource property using baseclass's methods.
    8. callsheet's expression can connect to directly imported objects. It cannot connect to indirectly imported objects. - this is for encapsulation.
    9. relationship among callsheet are 1-way, tree structure. this way we will have a top callsheet.
    - we need to sort object by relationship, sort expression by relationship
    - we need to update sub element names (edge, face) after changing shapes.
    - apply import parameters to callsheet by alias name, not by cell address, so that we can easily add/remove cells.
    10. callsheets can be many, named 'callsheet', 'callsheet2', 'callsheet3', ... Only the main callsheet, named 'callsheet', can have callParam (callParam=Y). The other callsheets are needed to avoid using 'hiddenref()' which causes a recompute deadloop.
    Spreadsheet (callsheet) is fast. Extra callsheets will not slow down FreeCAD.
    11. all expression with computations should be moved to callsheet.

work flow

eg, to create npt_m_hole.FCStd and npt_m_hole.py

create npt_m_hole_replay.py
    class npt_m_hole(baseClass):
        def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, ... ):
            ...
            super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
            
            # # find a class to import, so that you don't have to build from scratch
            from parts.Npt_m import Npt_m
            npt_m_instance = Npt_m('npt_m_instance', doc, objPrefix=self.objPrefix + 'npt_m', useLabel=True, importer=self)
            self.update_imports(npt_m_instance)


run npt_m_hole.py to generate npt_m_hole.FCStd

modify npt_m_hole.FCStd to add holes to the model.

run doc2class.py again against npt_m_hole.FCStd, save the output python npt_m_hole.py
    doc2class.py -tc npt_m_hole

class_new.py npt_fxf
class_import.py npt_f -op s_npt_f
class_import.py npt_f -op b_npt_f
