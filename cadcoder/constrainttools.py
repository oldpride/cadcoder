def get_constraints(obj, printDetail=False):
    print("# Save Python code to recreate constraints")
    print("constraints = []")
    print("sketch = App.ActiveDocument.ActiveObject  # or your sketch name")

    for i, c in enumerate(obj.Constraints):
        args = []
        for attr in ["First", "FirstPos", "Second", "SecondPos", 
                    "Third", "ThirdPos", "Fourth", "FourthPos"]:
            if hasattr(c, attr):
                val = getattr(c, attr)
                if val != -1:
                    args.append(str(val))
        
        if hasattr(c, "Value"):
            try:
                datum = obj.getDatum(i)
                args.append(f"App.Units.Quantity('{str(datum)}')")
            except:
                args.append(str(c.Value))  # fallback to raw float
        
        print(f"constraints.append(Sketcher.Constraint('{c.Type}', {', '.join(args)})) # constraint{i+1}")
        
        if hasattr(c, "Name") and c.Name:
            print(f"# Named: '{c.Name}' → after adding: sketch.renameConstraint({i}, '{c.Name}')")

    print("sketch.addConstraint(constraints)")
    print("sketch.solve()")
    print("App.ActiveDocument.recompute()")

def get_constraints_old(obj, printDetail=False):
    try:
        constraints = obj.Constraints
    except Exception as e:
        print(f"Error getting constraints: {e}")
        return None
    
    keys = [ 'First', 'FirstPos', 'Second', 'SecondPos', 'Third', 'ThirdPos', 'Fourth', 'FourthPos',
             'Value', 'Name', 'Driven', 'Type',
            ]
    
    print("Constraints to recreate the sketch:")
    print("constraints = []")
    print("sketch = App.ActiveDocument.ActiveObject  # or your sketch")
    
    for i, c in enumerate(constraints):
        v_by_k = {}
        args = []

        # print(f"#{i:3d}: {c.Type:15} ", end="")
        
        # # Show the args/indices (depends on constraint type)
        # if hasattr(c, "Value"):  # dimensional
        #     val_str = f", Value={c.Value:.4f}"
        # else:
        #     val_str = ""

        for k in keys:
            if hasattr(c, k):
                # print(f" {k}={getattr(c, k)}", end="")
                v = getattr(c, k)
                v_by_k[k] = f"{v}"
            else:
                v_by_k[k] = ""

            args.append(v_by_k[k])

        print(f"#{i+1} ({v_by_k['First']}, {v_by_k['FirstPos']}, {v_by_k['Second']}, {v_by_k['SecondPos']}, {v_by_k['Third']}, {v_by_k['ThirdPos']}, {v_by_k['Fourth']}, {v_by_k['FourthPos']}){v_by_k['Value']}")
        print(f"    Name='{v_by_k['Name']}', Driven={v_by_k['Driven']}, Type={v_by_k['Type']}")
        
        # If driven / reference
        # if c.Driven:
        #     print("    (Driven/reference)")
        
        print()  # blank line between constraints
        
        # if hasattr(c, "Value") and c.Value is not None:
        if v_by_k['Value']:
            args.append(f"App.Units.Quantity('{v_by_k['Value']} {c.getUnitString()}')")  # or just float(c.Value)
        
        # print(f"constraints.append(Sketcher.Constraint('{c.Type}', {', '.join(args)}))")
        print(f"constraints.append(Sketcher.Constraint('{v_by_k['Type']}', {', '.join(args)}))")
        
        # if c.Name:
        #     print(f"sketch.setDatum({i}, App.Units.Quantity('{c.Value} {c.getUnitString()}'))  # if needed")
        #     print(f"# Name: {c.Name}")
        if v_by_k['Name']:
            print(f"sketch.setDatum({i}, App.Units.Quantity('{v_by_k['Value']} {c.getUnitString()}'))  # if needed")
            print(f"# Name: {v_by_k['Name']}")
    

        print("sketch.addConstraint(constraints)")
        print("sketch.solve()")
