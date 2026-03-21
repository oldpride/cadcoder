#! /usr/bin/env python

import sys
import importlib
import os
import traceback
from pprint import pformat

print(f"__file__={__file__}")
prog = os.path.basename(__file__)
print(f"{prog}: sys.path={pformat(sys.path)}")

# try to import the module
module_names = [
    
    # the following files are .pyd files. 'pyd' files are like .dll files.
    # therefore vscode can import them but pylance cannot find their source code.
    # so pylance will report "import could not be resolved" error.
    # a workaround is to create a stub file (.pyi) for each module using
    # mypy's stubgen tool or our enhanced ptstubgen.py script.    
    'FreeCAD',  # I made a stub file FreeCAD.pyi for it using ptstubgen.py.
    'Part',
    'Sketcher',
    'FreeCADGui',

    # FreeCAD GUI is built on top of PySide2.
    'PySide2',

    # test PyQt
    'PyQt',
    'PyQt2',

    'pip',   # pip command does not exist under freecad, but pip module should exist
    'mypy',  # this has stubgen

    'logging',  # standard module

    'ipykernel', # for jupyter notebook kernel
    'ipython',   # for jupyter notebook

    'numpy',
    'pandas',

]

for module_name in module_names:
    print("\n----------------------------------------")
    imported = None
    try:
        imported = importlib.import_module(module_name)
        print(f"module {module_name} imported successfully")
        # try to get module version
    except Exception as e:
        print(f"module {module_name} import failed: {e}")
        traceback.print_exc()
        continue

    try:
        module_version = imported.__version__
        print(f"module {module_name} version={module_version}")
    except Exception as e:
        print(f"module {module_name} version not found: {e}")

    module_file = getattr(imported, '__file__', None)
    if module_file:
        print(f"module {module_name} file location: {module_file}")
    else:
        print(f"module {module_name} file location not found")

print()
print("full list of available property types")
import FreeCAD as App
tmpDocName = "tmpDocNoSave"

# close all docs with names starting with docName
for d in App.listDocuments().values():
    if d.Name.startswith(tmpDocName):
        App.closeDocument(d.Name)

# create new tmp doc
doc = App.newDocument(tmpDocName)

supported_props = doc.addObject("Part::FeaturePython", "dummy").supportedProperties()
supported_props.sort()
for p in supported_props:
    print(f" - {p}")
'''
12:51:09   - App::PropertyAcceleration
12:51:09   - App::PropertyAmountOfSubstance
12:51:09   - App::PropertyAngle
12:51:09   - App::PropertyArea
12:51:09   - App::PropertyBool
12:51:09   - App::PropertyBoolList
12:51:09   - App::PropertyColor
12:51:09   - App::PropertyColorList
12:51:09   - App::PropertyCompressiveStrength
12:51:09   - App::PropertyCurrentDensity
12:51:09   - App::PropertyDensity
12:51:09   - App::PropertyDirection
12:51:09   - App::PropertyDissipationRate
12:51:09   - App::PropertyDistance
12:51:09   - App::PropertyDynamicViscosity
12:51:09   - App::PropertyElectricCharge
12:51:09   - App::PropertyElectricCurrent
12:51:09   - App::PropertyElectricPotential
12:51:09   - App::PropertyElectricalCapacitance
12:51:09   - App::PropertyElectricalConductance
12:51:09   - App::PropertyElectricalConductivity
12:51:09   - App::PropertyElectricalInductance
12:51:09   - App::PropertyElectricalResistance
12:51:09   - App::PropertyEnumeration
12:51:09   - App::PropertyExpressionEngine
12:51:09   - App::PropertyFile
12:51:09   - App::PropertyFileIncluded
12:51:09   - App::PropertyFloat
12:51:09   - App::PropertyFloatConstraint
12:51:09   - App::PropertyFloatList
12:51:09   - App::PropertyFont
12:51:09   - App::PropertyForce
12:51:09   - App::PropertyFrequency
12:51:09   - App::PropertyHeatFlux
12:51:09   - App::PropertyInteger
12:51:09   - App::PropertyIntegerConstraint
12:51:09   - App::PropertyIntegerList
12:51:09   - App::PropertyIntegerSet
12:51:09   - App::PropertyInverseArea
12:51:09   - App::PropertyInverseLength
12:51:09   - App::PropertyInverseVolume
12:51:09   - App::PropertyKinematicViscosity
12:51:09   - App::PropertyLength
12:51:09   - App::PropertyLink
12:51:09   - App::PropertyLinkChild
12:51:09   - App::PropertyLinkGlobal
12:51:09   - App::PropertyLinkHidden
12:51:09   - App::PropertyLinkList
12:51:09   - App::PropertyLinkListChild
12:51:09   - App::PropertyLinkListGlobal
12:51:09   - App::PropertyLinkListHidden
12:51:09   - App::PropertyLinkSub
12:51:09   - App::PropertyLinkSubChild
12:51:09   - App::PropertyLinkSubGlobal
12:51:09   - App::PropertyLinkSubHidden
12:51:09   - App::PropertyLinkSubList
12:51:09   - App::PropertyLinkSubListChild
12:51:09   - App::PropertyLinkSubListGlobal
12:51:09   - App::PropertyLinkSubListHidden
12:51:09   - App::PropertyLuminousIntensity
12:51:09   - App::PropertyMagneticFieldStrength
12:51:09   - App::PropertyMagneticFlux
12:51:09   - App::PropertyMagneticFluxDensity
12:51:09   - App::PropertyMagnetization
12:51:09   - App::PropertyMap
12:51:09   - App::PropertyMass
12:51:09   - App::PropertyMaterial
12:51:09   - App::PropertyMaterialList
12:51:09   - App::PropertyMatrix
12:51:09   - App::PropertyMoment
12:51:09   - App::PropertyPath
12:51:09   - App::PropertyPercent
12:51:09   - App::PropertyPersistentObject
12:51:09   - App::PropertyPlacement
12:51:09   - App::PropertyPlacementLink
12:51:09   - App::PropertyPlacementList
12:51:09   - App::PropertyPosition
12:51:09   - App::PropertyPower
12:51:09   - App::PropertyPrecision
12:51:09   - App::PropertyPressure
12:51:09   - App::PropertyPythonObject
12:51:09   - App::PropertyQuantity
12:51:09   - App::PropertyQuantityConstraint
12:51:09   - App::PropertyRotation
12:51:09   - App::PropertyShearModulus
12:51:09   - App::PropertySpecificEnergy
12:51:09   - App::PropertySpecificHeat
12:51:09   - App::PropertySpeed
12:51:09   - App::PropertyStiffness
12:51:09   - App::PropertyStiffnessDensity
12:51:09   - App::PropertyStress
12:51:09   - App::PropertyString
12:51:09   - App::PropertyStringList
12:51:09   - App::PropertyTemperature
12:51:09   - App::PropertyThermalConductivity
12:51:09   - App::PropertyThermalExpansionCoefficient
12:51:09   - App::PropertyThermalTransferCoefficient
12:51:09   - App::PropertyTime
12:51:09   - App::PropertyUUID
12:51:09   - App::PropertyUltimateTensileStrength
12:51:09   - App::PropertyVacuumPermittivity
12:51:09   - App::PropertyVector
12:51:09   - App::PropertyVectorDistance
12:51:09   - App::PropertyVectorList
12:51:09   - App::PropertyVelocity
12:51:09   - App::PropertyVolume
12:51:09   - App::PropertyVolumeFlowRate
12:51:09   - App::PropertyVolumetricThermalExpansionCoefficient
12:51:09   - App::PropertyWork
12:51:09   - App::PropertyXLink
12:51:09   - App::PropertyXLinkList
12:51:09   - App::PropertyXLinkSub
12:51:09   - App::PropertyXLinkSubHidden
12:51:09   - App::PropertyXLinkSubList
12:51:09   - App::PropertyYieldStrength
12:51:09   - App::PropertyYoungsModulus
12:51:09   - Materials::PropertyMaterial
12:51:09   - Part::PropertyFilletEdges
12:51:09   - Part::PropertyGeometryList
12:51:09   - Part::PropertyPartShape
12:51:09   - Part::PropertyShapeCache
12:51:09   - Part::PropertyShapeHistory
12:51:09   - Part::PropertyTopoShapeList
12:51:09   - Sketcher::PropertyConstraintList
'''

print()
print("list of available object types - Only object types with a name ending in Python can be used for scripted objects.")
supported_objTypes = doc.supportedTypes()
supported_objTypes.sort()
for t in supported_objTypes:
    print(f" - {t}")
