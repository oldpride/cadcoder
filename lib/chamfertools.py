from pprint import pformat
from pdfclib.edgetools import get_edgeName_by_position


def add_chamfer(doc, label, containerObj, shapeObj, position, chamfer_size):
    print(f"containerObj Name={containerObj.Name}, Label={containerObj.Label}, Type={type(containerObj)}")
    print(f"shapeObj Name={shapeObj.Name}, Label={shapeObj.Label}, Type={type(shapeObj)}")
    # label = f"{className}_chamfer_{position}"
    chamfer = doc.addObject('PartDesign::Chamfer', label )
    chamfer.Label = label
    
    print(f"container group before extend={pformat(containerObj.Group)}")
    container_group:list = containerObj.Group
    container_group.append(chamfer)
    containerObj.Group = container_group
    print(f"container group after extend={pformat(containerObj.Group)}")
    chamfer.Base = (shapeObj, [get_edgeName_by_position(shapeObj, position)])
    doc.recompute()
    chamfer.Size = chamfer_size

    return chamfer
        