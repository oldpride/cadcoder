import traceback
from cadcoder.objtools import normalize_label
from cadcoder.proptools import float2str, propValue2python
import FreeCAD as App
import FreeCADGui as Gui
import Part


'''
11:48:41      modified: MainObject-Geometry
11:48:41        Object value:
11:48:41          propType: Part::PropertyGeometryList
11:48:41          propValue: [<Ellipse object>, 
<Line segment (7.3218e-17,12.7,0) (-7.3218e-17,-12.7,0) >, 
<Line segment (-7.62,-2.64698e-23,0) (7.62,-4.81778e-24,0) >, 
<Point (9.15225e-17,10.16,0) >, 
<Point (-9.15225e-17,-10.16,0) >]
11:48:41          readonly: False
11:48:41          valueClass: list
11:48:41          valueClassTree: {'list/Ellipse', 'list/Point', 'list/LineSegment'}
11:48:41          valueObjName: None
11:48:41          valuePython: [
Part.Ellipse(Vector(-0.0000, 0.0000, 0.0000), 12.700000000000001, 7.62), 
Part.LineSegment(Vector (7.321795933535117e-17, 12.7, 0.0), Vector (-7.321795933535117e-17, -12.7, 0.0)), 
Part.LineSegment(Vector (-7.62, -2.646977976809723e-23, 0.0), Vector (7.62, -4.817780799070853e-24, 0.0)), 
Part.Point(Vector(0.0000, 10.1600, 0.0000)), 
Part.Point(Vector(-0.0000, -10.1600, 0.0000))]
11:48:41          valueTypeId: None
11:48:41          prefixPython: [Part.Ellipse(Vector(-0.0000, 0.0000, 0.0000), 12.700000000000001, 7.62), Part.LineSegment(Vector (7.321795933535117e-17, 12.7, 0.0), Vector (-7.321795933535117e-17, -12.7, 0.0)), Part.LineSegment(Vector (-7.62, -2.646977976809723e-23, 0.0), Vector (7.62, -4.817780799070853e-24, 0.0)), Part.Point(Vector(0.0000, 10.1600, 0.0000)), Part.Point(Vector(-0.0000, -10.1600, 0.0000))]
'''


def sketch2python( obj, 
                objVarName=None,   # object variable name in the generated code
                objectList=None,   # list of existing objects to refer to
                printDetail=False,
                ):

    if objVarName is None:
        objVarName = normalize_label(obj.Label)

    geometries = obj.getPropertyByName('Geometry')
    gflist = obj.GeometryFacadeList

    lines = []

    def add_line(line):
        lines.append(line)
        if printDetail:
            print(line)

    n = 0
    exposing = 0
    exposed = []
    for geo in geometries:
        prefixedPython = propValue2python(geo, objectList)['prefixed']

        if exposing > 0:
            exposed.append(n)
            exposing = exposing - 1
        else:
            # exposing == 0
            add_line(f'geo{n} = {objVarName}.addGeometry({prefixedPython})')
            if gflist[n].Construction:
                add_line(f'{objVarName}.toggleConstruction(geo{n})')

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

            if isinstance(geo, Part.BSplineCurve):
                poles = len(geo.getPoles())
                exposing = poles - 2
                if exposing < 2:
                    exposing = 2
            elif isinstance(geo, Part.ArcOfParabola):
                exposing = 2
            elif isinstance(geo, Part.ArcOfHyperbola):
                exposing = 3
            elif isinstance(geo, Part.ArcOfEllipse):
                exposing = 4
            elif isinstance(geo, Part.Circle):
                exposing = 0
            elif isinstance(geo, Part.Ellipse):
                exposing = 4
            elif isinstance(geo, Part.LineSegment):
                exposing = 0
            elif isinstance(geo, Part.Point):
                exposing = 0
            if exposing > 0:
                add_line(f'{objVarName}.exposeInternalGeometry({n})')

        n = n + 1

    def get_geo_arg(geoVarName):
        if geoVarName[:3] != 'geo':
            return geoVarName
        
        geoIndex = int(geoVarName[3:])
        if geoIndex in exposed:
            return f"{geoIndex}"
        else:
            return geoVarName

    splinecount = 0
    concount = 0
    # prop = obj.getPropertyByName('Constraints')
    for con in obj.Constraints:
        conargs = con.Value
        contype = con.Type
        if con.First < 0:
            first = str(con.First)
        else:
            first = f'geo{con.First}'

        if con.Second < 0:
            sec = str(con.Second)
        else:
            sec = f'geo{con.Second}'

        if con.Third < 0 :
            third = str(con.Third)
        else:
            third = f'geo{con.Third}'

        if con.Type == 'Coincident':
            conargs = f'{get_geo_arg(first)}, {con.FirstPos}, {get_geo_arg(sec)}, {con.SecondPos}'
        elif con.Type == 'PointOnObject':
            conargs = f'{get_geo_arg(first)}, {con.FirstPos}, {get_geo_arg(sec)}'

        elif con.Type == 'Vertical':
            if sec[:3] == 'geo':
                # Two points.
                conargs = f'{get_geo_arg(first)}, {con.FirstPos}, {get_geo_arg(sec)}, {con.SecondPos}'
            else:
                # Line.
                conargs = str(first)

        elif con.Type == 'Horizontal':
            if sec[:3] == 'geo':
                # Two points.
                conargs = f'{first}, {con.FirstPos}, {get_geo_arg(sec)}, {con.SecondPos}'
            else:
                # Line.
                conargs = str(first)
        elif con.Type == 'Parallel':
            conargs = f'{first}, {get_geo_arg(sec)}'

        elif con.Type == 'PerpendicularViaPoint':
            conargs = f'{first}, {sec}, {third}, {con.ThirdPos}'
        elif con.Type == 'Perpendicular':
            if con.FirstPos == 0:
                conargs = f'{first}, {sec}'
            elif third[:3] == 'geo':
                contype = 'PerpendicularViaPoint'  # compatiblity to FreeCAD 2.20
                conargs = f'{first}, {sec}, {get_geo_arg(third)}, {con.ThirdPos}'
            elif con.SecondPos == 0:
                conargs = f'{first}, {con.FirstPos}, {sec}'
            else:
                conargs = f'{first}, {con.FirstPos}, {sec}, {con.SecondPos}'

        elif con.Type == 'TangentViaPoint':
            conargs = f'{first}, {sec}, {third}, {con.ThirdPos}'
        elif con.Type == 'Tangent':
            if con.Second < 0:
                conargs = f'{first}, {con.FirstPos}'
            elif third[:3] == 'geo':
                contype = 'TangentViaPoint'  # compatiblity to FreeCAD 2.20
                conargs = f'{first}, {sec}, {get_geo_arg(third)}, {con.ThirdPos}'
            elif con.SecondPos == 0:
                conargs = f'{first}, {con.FirstPos}, {sec}'
            else:
                conargs = f'{first}, {con.FirstPos}, {sec}, {con.SecondPos}'

        elif con.Type == 'Equal':
            conargs = f'{first}, {sec}'

        elif con.Type == 'Symmetric':
            conargs = f'{first}, {con.FirstPos}, {sec}, {con.SecondPos}, {third}, {con.ThirdPos}'
        elif con.Type == 'Block':
            conargs = str(first)

        elif con.Type == 'Distance':
            if sec[:3] != 'geo':
                conargs = f'{first}, {float2str(con.Value)}'
            elif con.FirstPos == 0:
                conargs = f'{first}, {get_geo_arg(sec)}, {float2str(con.Value)}'
            elif con.SecondPos == 0:
                conargs = f'{first}, {con.FirstPos}, {get_geo_arg(sec)}, {float2str(con.Value)}'
            else:
                conargs = f'{first}, {con.FirstPos}, {get_geo_arg(sec)}, {con.SecondPos}, {float2str(con.Value)}'
        elif con.Type == 'DistanceX' or con.Type == 'DistanceY':
            if sec[:3] != 'geo':
                conargs = f'{first}, {con.FirstPos}, {float2str(con.Value)}'
            else:
                conargs = f'{first}, {con.FirstPos}, {get_geo_arg(sec)}, {con.SecondPos}, {float2str(con.Value)}'

        elif con.Type == 'AngleViaPoint':
            conargs = f'{first}, {sec}, {third}, {float2str(con.Value)}'
        elif con.Type == 'Angle':
            if con.FirstPos == 0:
                conargs = f'{first}, {sec}, {float2str(con.Value)}'
            elif third[:3] == 'geo':
                contype = 'AngleViaPoint'  # compatiblity to FreeCAD 2.20
                conargs = f'{first}, {sec}, {get_geo_arg(third)}, {float2str(con.Value)}'
            else:
                conargs = f'{first}, {con.FirstPos}, {sec}, {con.SecondPos}, {float2str(con.Value)}'

        elif con.Type == 'Weight' or con.Type == 'Radius' or con.Type == 'Diameter':
            conargs = f'{first}, {float2str(con.Value)}'
            splinecount = 0

        elif con.Type == 'InternalAlignment':
            if con.Second > con.First:
                contype = 'InternalAlignment:Sketcher::BSplineControlPoint'
                conargs = f'{first}, {con.FirstPos}, {sec}, {splinecount}'
                splineindex = con.Second
                splinecount = splinecount + 1
            else:
                conargs = None
        else:
            msg = f"Unsupported constraint type={con.Type} in obj Label={obj.Label}, Name={obj.Name}"
            print(msg)
            traceback.print_stack()
            
        if conargs is not None:
            add_line(
                f"{objVarName}.addConstraint(Sketcher.Constraint('{contype}', {conargs}))")

        if con.Name != "":
            add_line(f"{objVarName}.renameConstraint({concount}, '{con.Name}')")
            
        concount = concount + 1

    return lines
