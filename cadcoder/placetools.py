from FreeCAD import App, Vector, Placement

def get_trueDiagonal(obj):
    try:
        bb = obj.Shape.BoundBox
    except AttributeError:
        print(f"Object {obj.Name} has no Shape.")
        return None
    trueDiagonal = (App.Vector(bb.XMax, bb.YMax, bb.ZMax) - App.Vector(bb.XMin, bb.YMin, bb.ZMin)).Length
    return trueDiagonal

instanceCount = 0
def placementFunc(doc, objList):
    # place top of the object at next available position
    global instanceCount
    doc.recompute()  # need to recompute before getting bounding box
    for obj in objList:
        if obj.InList:
            # obj has a parent, then not a top-level object, skip it
            continue
        if not hasattr(obj, 'Shape'):
            # obj has no shape, skip it. eg, spreadsheet
            print(f"Skipping placement adjustment for object {obj.Name} as it has no Shape.")
            continue
        bb = obj.Shape.BoundBox
        print(f"name={obj.Name}, label={obj.Label} bounding box: {bb}")
        oldCenter = bb.Center
        print(f"name={obj.Name}, label={obj.Label} center before placement adjustment: {oldCenter}")

        # step = obj.Shape.BoundBox.DiagonalLength + 10  # add some gap
        
        trueDiagonal = get_trueDiagonal(obj)
        if trueDiagonal is None:
            continue
        step = trueDiagonal

        print(f"space needed is trueDiagonal: {step}mm")
        obj.Placement = Placement(Vector(0, step * instanceCount, 0), App.Rotation(0,0,0,1))
        newCenter = obj.Shape.BoundBox.Center
        print(f"name={obj.Name}, label={obj.Label} center after placement adjustment: {newCenter}")
    instanceCount += 1
