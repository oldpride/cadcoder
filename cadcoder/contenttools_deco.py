import FreeCAD as App
import re

from pprint import pformat

'''
print(obj.Content) agaist straight_m's subtractiveHelix obj.

<Extensions Count="1">
        <Extension type="App::SuppressibleExtension" name="SuppressibleExtension">
        </Extension>
    </Extensions>
    <Properties Count="31" TransientCount="1">
        <_Property name="_Body" type="App::PropertyLinkHidden" status="251658241"/>
        <Property name="AddSubShape" type="Part::PropertyPartShape" status="1">
            <Part ElementMap="0.4" brep="1">
<![CDATA[

CASCADE Topology V1, (c) Matra-Datavision
Locations 0
Curve2ds 0
Curves 0
Polygon3D 0
PolygonOnTriangulations 0
Surfaces 0
Triangulations 0

TShapes 0

*]]>
            </Part>
            <ElementMap/>
        </Property>
        <Property name="AllowMultiFace" type="App::PropertyBool" status="1">
            <Bool value="true"/>
        </Property>
        <Property name="Angle" type="App::PropertyAngle" status="1">
            <Float value="0"/>
        </Property>
        <Property name="Axis" type="App::PropertyVector" status="16777217">
            <PropertyVector valueX="0" valueY="1" valueZ="0"/>
        </Property>
        <Property name="Base" type="App::PropertyVector" status="16777217">
            <PropertyVector valueX="0" valueY="0" valueZ="0"/>
        </Property>
        <Property name="BaseFeature" type="App::PropertyLink" status="9">
            <Link value=""/>
        </Property>
        <Property name="ExpressionEngine" type="App::PropertyExpressionEngine" status="67108864">
            <ExpressionEngine count="0">
            </ExpressionEngine>
        </Property>
        <Property name="Growth" type="App::PropertyDistance" status="5">
            <Float value="0"/>
        </Property>
        <Property name="HasBeenEdited" type="App::PropertyBool" status="67108865">
            <Bool value="false"/>
        </Property>
        <Property name="Height" type="App::PropertyLength" status="1">
            <Float value="30"/>
        </Property>
        <Property name="Label" type="App::PropertyString" status="134217729">
            <String value="s_straight_m_SubtractiveHelixTmpDefault"/>
        </Property>
        <Property name="Label2" type="App::PropertyString" status="67108992">
            <String value=""/>
        </Property>
        <Property name="LeftHanded" type="App::PropertyBool" status="1">
            <Bool value="false"/>
        </Property>
        <Property name="Midplane" type="App::PropertyBool" status="1">
            <Bool value="false"/>
        </Property>
        <Property name="Mode" type="App::PropertyEnumeration" status="1">
            <Integer value="0"/>
        </Property>
        <Property name="Outside" type="App::PropertyBool" status="1">
            <Bool value="false"/>
        </Property>
        <Property name="Pitch" type="App::PropertyLength" status="1">
            <Float value="10"/>
        </Property>
        <Property name="Placement" type="App::PropertyPlacement" status="8388617">
            <PropertyPlacement Px="0" Py="0" Pz="0" Q0="0" Q1="0" Q2="0" Q3="1" A="0" Ox="0" Oy="0" Oz="1"/>
        </Property>
        <Property name="Profile" type="App::PropertyLinkSub" status="1">
            <LinkSub value="" count="0">
            </LinkSub>
        </Property>
        <Property name="ReferenceAxis" type="App::PropertyLinkSub" status="1">
            <LinkSub value="" count="0">
            </LinkSub>
        </Property>
        <Property name="Refine" type="App::PropertyBool" status="1">
            <Bool value="false"/>
        </Property>
        <Property name="Reversed" type="App::PropertyBool" status="1">
            <Bool value="false"/>
        </Property>
        <Property name="Shape" type="Part::PropertyPartShape" status="1">
            <Part ElementMap="0.4" brep="1">
<![CDATA[

CASCADE Topology V1, (c) Matra-Datavision
Locations 0
Curve2ds 0
Curves 0
Polygon3D 0
PolygonOnTriangulations 0
Surfaces 0
Triangulations 0

TShapes 0

*]]>
            </Part>
            <ElementMap/>
        </Property>
        <Property name="ShapeMaterial" type="Materials::PropertyMaterial" status="1">
            <PropertyMaterial uuid="7f9fd73b-50c9-41d8-b7b2-575a030c1eeb"/>
        </Property>
        <Property name="Suppressed" type="App::PropertyBool" status="1">
            <Bool value="false"/>
        </Property>
        <Property name="SuppressedShape" type="Part::PropertyPartShape" status="1">
            <Part ElementMap="0.4" brep="1">
<![CDATA[

CASCADE Topology V1, (c) Matra-Datavision
Locations 0
Curve2ds 0
Curves 0
Polygon3D 0
PolygonOnTriangulations 0
Surfaces 0
Triangulations 0

TShapes 0

*]]>
            </Part>
            <ElementMap/>
        </Property>
        <Property name="Tolerance" type="App::PropertyFloatConstraint" status="1">
            <Float value="0.1"/>
        </Property>
        <Property name="Turns" type="App::PropertyFloatConstraint" status="5">
            <Float value="3"/>
        </Property>
        <Property name="UpToFace" type="App::PropertyLinkSub" status="1">
            <LinkSub value="" count="0">
            </LinkSub>
        </Property>
        <Property name="UpToShape" type="App::PropertyLinkSubList" status="1">
            <LinkSubList count="0">
            </LinkSubList>
        </Property>
        <Property name="Visibility" type="App::PropertyBool" status="649">
            <Bool value="true"/>
        </Property>
    </Properties>
'''

parsedContent_by_docKey_objName = {}

def map_propStatus_by_doc_objName(doc, obj=None, objName=None, refreshCache=False,):
    # we use docKey to distinguish different docs with same Name because we may have tmp docs with same Name.
    docKey = f"{doc.Name},{id(doc)}"

    if docKey not in parsedContent_by_docKey_objName:
        parsedContent_by_docKey_objName[docKey] = {}
    
    if obj is not None:
        objName = obj.Name
    elif objName is not None:
        obj = doc.getObject(objName)
    else:
        raise ValueError("Either obj or objName must be provided")

    if objName not in parsedContent_by_docKey_objName[docKey] or refreshCache:
        parsedContent_by_docKey_objName[docKey][objName] = {}
    else:
        return parsedContent_by_docKey_objName[docKey][objName]
    
    content = obj.Content
    # content is XML

def propIsHidden(obj, propName):
    # statusList = [
    #     'Hidden', 3,
    #     'PropHidden', 26,
    # ]
    # statusnums = obj.getPropertyStatus(propName)
    # print(f"propIsHidden: obj={obj}, propName='{propName}', statusnums={statusnums}")
    # for status in statusList:
    #     if status in statusnums:
    #         return True
    # return False
    
    print(obj.Content)
    # for line in obj.Content.split('\n'):
    #     if f'name="{propName}"' in line:
    #         print(line.strip())
    return False
