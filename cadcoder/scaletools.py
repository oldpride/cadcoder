import re

import FreeCAD as App
import FreeCADGui as Gui
import Draft

scale_by_key = {
    "BASF-17-4": (1.1982, 1.1982, 1.2610),
}

def print_scale_key_map():
    print("scale_by_key:")
    for key in sorted(scale_by_key.keys()):
        xScale, yScale, zScale = scale_by_key[key]
        print(f"  {key}: xScale={xScale}, yScale={yScale}, zScale={zScale}")

def scale_clone(obj, key_pattern, cloneLabel=None, export_stl=False):
    default_label = None
    if key_pattern == "list":
        print_scale_key_map()
        return
    elif m := re.match(f"(\d+.)?\d+,(\d+.)?\d+,(\d+.)?\d+$", key_pattern):
        # if key is in format of "1.2,1.2,1.3", parse it to get xScale, yScale, zScale
        xScale, yScale, zScale = map(float, key_pattern.split(","))
        default_label = f"{obj.Label}_scaled_{key_pattern}"
    else:
        match_keys = [k for k in scale_by_key.keys() if re.search(key_pattern, k, re.IGNORECASE)]
        if not match_keys:
            raise ValueError(f"key={key_pattern} is not in scale_by_key and not in format of 'xScale,yScale,zScale'")
        elif len(match_keys) > 1:
            raise ValueError(f"key={key_pattern} matches multiple keys in scale_by_key: {match_keys}")
        else:
            xScale, yScale, zScale = scale_by_key[match_keys[0]]
            default_label = f"{obj.Label}_scaled_{match_keys[0]}"
    
    doc = obj.Document
    if cloneLabel is None:
        cloneLabel = default_label

    for obj2 in doc.Objects:
        if obj2.Label == cloneLabel:
            print(f"cloneLabel={cloneLabel} already exists in doc. recreating it.")
            doc.removeObject(obj2.Name)
        
    clone = Draft.make_clone([obj], forcedraft=True)
    clone.Label = cloneLabel
    clone.Scale = App.Vector(xScale, yScale, zScale)
    clone_corr = (App.Vector(0.0, 0.0, 0.0) - clone.Placement.Base).scale(*App.Vector(1-xScale, 1-yScale, 1-zScale))
    clone.Placement.move(clone_corr)
    doc.recompute()

    if export_stl:
        import os
        import Mesh

        FCStd_path = doc.FileName
        Without_ext = FCStd_path.replace('.FCStd', '')
        FCStd_dir = os.path.dirname(FCStd_path)
        stl_path = os.path.join(FCStd_dir, f"{Without_ext}-{clone.Label}.stl")
        if hasattr(Mesh, "exportOptions"):
            options = Mesh.exportOptions(stl_path)
            Mesh.export([clone], stl_path, options)
        else:
            Mesh.export([clone], stl_path)
        print(f"Exported {clone.Label} to {stl_path}")
    
    
