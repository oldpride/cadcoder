from FreeCAD import Vector, Placement, Rotation
import Part
import FreeCAD as App
import FreeCADGui as Gui

from cadcoder.proptools import propValue2python


'''
in most cases, 

C++ classname          ->      Python class wrapper

Part::GeomCircle       ->      Part.Circle
Part::GeomEllipse      ->      Part.Ellipse
Part::GeomLineSegment  ->      Part.LineSegment

example:
    if geo.TypeId == 'Part::GeomEllipse':
        ...

    if isinstance(geo, Part.Ellipse):
        ...

inheritance check
if geo.isDerivedFrom("Part::Geometry"):
    # This catches anything that is a geometry object
    if geo.isDerivedFrom("Part::GeomCurve"):
        # This catches lines, circles, ellipses, splines
        pass
'''

def get_geometry(obj, printDetail=False, decimals=4):
    try:
        geometries = obj.getPropertyByName('Geometry')
    except Exception as e:
        print(f"Error getting geometry: {e}")
        return None
    
    geoInfos = []
    for geo in geometries:
        geoInfo = get_geoInfo(geo)
        geoInfos.append(geoInfo)
        if printDetail:
            print_geoInfo(geoInfo, decimals=decimals)
            print()

    return geoInfos
                  
def get_geoInfo(geo):
    attrs = [
        'TypeId', 'StartPoint', 'EndPoint', 'Center', 'Radius', 'MajorRadius', 'MinorRadius',
        'MajorAxis', 'MinorAxis', 'FocalDistance', 'Angles', 'ArcLength',

        'Axis', # normal axis for circle, ellipse, perpendicular to the plane
        'XAxis', # major axis for ellipse
        'YAxis', # minor axis for ellipse
        'ZAxis', # may not exist
        'AngleXU', 'AngleYU', 'AngleZU', # major axis angles from X, Y, Z axes

        'Matrix',
        'FirstPoint', 'SecondPoint', 'ThirdPoint', 'FourthPoint',
        'EllipseType', 'HyperbolaType', 'ParabolaType',
    ]

    geoInfo = {}
    for attr in attrs:
        if hasattr(geo, attr):
            value = getattr(geo, attr)
            geoInfo[attr] = value

    return geoInfo

def print_geoInfo(geoInfo, decimals=4):
    for key in sorted(geoInfo.keys()):
        value = geoInfo[key]
        print(f"  {key}: {trim_decimals(value, decimals=decimals)}")


def trim_decimals(value, decimals=4):
    if isinstance(value, float):
        format_str = f"{{:.{decimals}f}}"
        return format_str.format(value)
    elif isinstance(value, Vector):
        return f"Vector({trim_decimals(value.x, decimals)}, {trim_decimals(value.y, decimals)}, {trim_decimals(value.z, decimals)})"

    return value

def get_internalGeometry_count( 
        pythonCode, # code to create the geometry object
        ):
    
    '''
    pythonCode example:
    Part.Ellipse(Vector(0.0000, 12.7000, 0.0000), Vector(-7.6200, 0.0000, 0.0000), Vector(0.0000, 0.0000, 0.0000))
    
    even the same class, if the parameters are different, the number of internal geometries may be different.
    '''

    from cadcoder.doctools import recreate_tmp_doc

    saved_active_doc = App.ActiveDocument
    saved_selection = App.Gui.Selection.getSelection()

    doc = recreate_tmp_doc()
    sketch = doc.addObject('Sketcher::SketchObject', 'TempSketch')
    before_count = sketch.GeometryCount
    geoIndex = sketch.addGeometry( eval(pythonCode) )
    try:
        sketch.exposeInternalGeometry(geoIndex)
    except Exception as e:
        pass
    after_count = sketch.GeometryCount -1
    doc.removeObject('TempSketch')

    App.setActiveDocument(saved_active_doc.Name)
    App.Gui.Selection.clearSelection()
    for obj in saved_selection:
        Gui.Selection.addSelection(obj)

    return after_count - before_count

def get_obj_internalGeometry_count( 
        obj, # Sketch object
        printDetail=False, decimals=4,
        ):

    '''
    return the number of internal geometries exposed in the given sketch object
    '''

    doc = obj.Document
    objectList = doc.Objects

    geometry = obj.getPropertyByName('Geometry')
    for n, geo in enumerate(geometry):
        geoInfo = get_geoInfo(geo)
        if printDetail:
            print_geoInfo(geoInfo, decimals=decimals)
        prefixedPython = propValue2python(geo, objectList)['prefixed']
        internalGeo_count = get_internalGeometry_count(prefixedPython)
        if printDetail:
            print(f"  internalGeometry_count= {internalGeo_count}")
            print()
