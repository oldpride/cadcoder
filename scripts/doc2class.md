``` mermaid
graph TD
    doc1 --doc2class.py--> python1 --myClass.py--> doc2 --doc2class.py--> python2

```

design consideration:
    1. freeCAD doc only has objects, no classes, no instances. Python files have classes and instances.
    therefore, we need to persist the class and instance info into objects, using custom properties.
    2. instance and class information are stored in object's pythonSource property. 
    3. try to use baseclass to handle persistence as much as possible, to avoid code duplication.
    5. import parameters are stored in callsheet object only.
    6. when doc2class.py generates python1, it scans all objects's pythonSource property to determine which classes to import. It doesn't rely on callsheet's import parameter in spreadsheet.
    7. when myClass.py generates doc2, it will set each object's pythonSource property using baseclass's methods.
    8. callsheet's expression can connect to directly imported objects. It cannot connect to indirectly imported objects. - this is for encapsulation.
    9. relationship among callsheet are 1-way, tree structure. this way we will have a top callsheet.
    - we need to sort object by relationship, sort expression by relationship
    - we need to update sub element names (edge, face) after changing shapes.
    - apply import parameters to callsheet by alias name, not by cell address, so that we can easily add/remove cells.

work flow

eg, to create Npt_m_hole.FCStd and Npt_m_hole.py

create Npt_m_hole_replay.py
    class Npt_m_hole(baseClass):
        def __init__(self, instanceName, doc, objPrefix="", useLabel=True, importer=None, ... ):
            ...
            super().__init__(instanceName, doc, objPrefix=objPrefix, useLabel=useLabel, importer=importer)
            
            # # find a class to import, so that you don't have to build from scratch
            from parts.Npt_m import Npt_m
            npt_m_instance = Npt_m('npt_m_instance', doc, objPrefix=self.objPrefix + '', useLabel=True, importer=self)
            self.update_imports(npt_m_instance)

            self.update_callsheet()

run Npt_m_hole.py to generate Npt_m_hole.FCStd

modify Npt_m_hole.FCStd to add holes to the model.

run doc2class.py again against Npt_m_hole.FCStd, save the output python Npt_m_hole.py
    doc2class.py -tc Npt_m_hole

class_new.py Npt_m_handle
class_import.py Npt_m
class_import.py Prism_polygon
class_import.py Cylinder
