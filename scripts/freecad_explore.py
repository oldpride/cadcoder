from pprint import pformat
import sys
from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part
import FreeCAD as app
import FreeCADGui

print(f"sys.path={pformat(sys.path)}")

# add current path to PYTHONPATH to find lib.*
# current_dir = os.path.dirname(os.path.abspath(__file__))

# if current_dir not in sys.path:
#     sys.path.append(current_dir)


from lib.logger import logstack

doc = app.activeDocument()

if doc is None:
    raise RuntimeError("No active document found")

# get the body in PartDesign WB
# try selection first (if running in the GUI)
try:
    sel = FreeCADGui.Selection.getSelection()
except Exception:
    sel = doc.Objects

if not sel:
    sel = doc.Objects

bodies = []
for o in sel:
    logstack(f"Checking selected object: {o.Name}, TypeId={o.TypeId}")
    # two ways to check if the object is a PartDesign Body
    if getattr(o, "TypeId", "").startswith("PartDesign::Body"):
    # if o.isDerivedFrom("PartDesign::Body"):
        logstack(f"Found Body in selection: {o.Name}")
        bodies.append(o)

if not bodies:
    raise RuntimeError("No PartDesign Body found in selection")

for body in bodies:
    logstack(f"Exploring Body: {body.Name}")

    # list all attributes of the body
    attrs = dir(body)
    print()
    logstack(f"Body {body.Name} has the following attributes:")
    for attr in attrs:
        logstack(f" - {attr}")

    # list all features in the body
    features = body.Group
    logstack(f"Body {body.Name} has {len(features)} features")

    for feature in features:
        logstack(f"Feature: {feature.Name}, TypeId={feature.TypeId}")

    origin = body.Origin
    # list all attributes of the origin
    origin_attrs = dir(origin)
    print()
    logstack(f"Origin of Body {body.Name} has the following attributes:")
    for attr in origin_attrs:
        logstack(f" - {attr}")

    # list all properties of the origin
    origin_props = origin.PropertiesList
    print()
    logstack(f"Origin of Body {body.Name} has the following properties:")
    for prop in origin_props:
        logstack(f" - {prop}")

    # for plane_name in ['XY-plane', 'XZ-plane', 'YZ-plane']:
    #     plane = origin.get(plane_name)
    #     logstack(f" - {plane_name}: {plane}")
    # x_axis = origin.Xaxis
    # logstack(f"X-axis: {pformat(x_axis)}")

    # # list all elements in the origin
    # origin_elements = origin.Elements
    # logstack(f"Origin of Body {body.Name} has {len(origin_elements)} elements")
    # for elem in origin_elements:
    #     logstack(f" - Element: {elem.Name}, TypeId={elem.TypeId}")
    #     elem_attrs = dir(elem)
    #     logstack(f"   Element {elem.Name} has the following attributes:")
    #     for attr in elem_attrs:
    #         logstack(f"    - {attr}")

    
