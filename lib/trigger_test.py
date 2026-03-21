import FreeCAD as App

# Ensure you have a Spreadsheet object in your document, e.g., named "Spreadsheet" 
# and a cell with the alias "TriggerValue"

'''
oldpride: what does this do?

GitHub Copilot: This line creates a **bidirectional link** between a FreeCAD object and a Python proxy class.

## What's happening:

- `obj` is a FreeCAD document object (like a feature, part, or custom object)
- `self` is the Python class instance (the "proxy" that adds custom behavior)
- `Proxy` is a special attribute that FreeCAD uses to connect objects with Python code

## Why it matters:

This pattern is fundamental to FreeCAD's **scripted objects** system. By setting `obj.Proxy = self`, you're telling FreeCAD: *"This Python class controls the behavior of this object."*

After this assignment:
- FreeCAD will call methods on `self` when events occur (like `execute()` for recalculation, `onChanged()` for property changes, etc.)
- You can access the FreeCAD object from the proxy via `self.Object` (if you've also set that)

## Typical pattern:

```python
class MyCustomObject:
    def __init__(self, obj):
        obj.Proxy = self  # Link object to this proxy
        self.Object = obj  # Store reference back to object
    
    def execute(self, obj):
        # Called when FreeCAD recalculates the object
        pass
```

**Gotcha:** Without this line, your custom Python class won't actually control the FreeCAD object's behavior - it would just be a disconnected Python object with no effect on the document.
'''
class TriggeringFeature:
    def __init__(self, obj):
        obj.Proxy = self
        
        # 1. Add a dummy property that will hold the spreadsheet value via Expression
        # We use PropertyFloat for numerical values, but PropertyString/Integer work too.
        obj.addProperty("App::PropertyFloat", "WatchedValue", "Base", "Value watched from the spreadsheet.")
        
        # 2. Get the document and spreadsheet object for setting the expression later
        self.doc = App.activeDocument()
        
    def execute(self, obj):
        """
        This method is triggered by FreeCAD's recompute mechanism 
        whenever the linked spreadsheet cell value changes.
        """
        # 3. Access the value that triggered the recompute
        current_value = obj.WatchedValue
        
        # 4. --- YOUR PYTHON CODE GOES HERE ---
        
        print("-" * 30)
        print(f"Spreadsheet Trigger Fired!")
        print(f"WatchedValue is now: {current_value}")
        
        if current_value > 50.0:
            print("Action: Value exceeds 50. Creating a new Part Box.")
            self.create_box(current_value)
        else:
            print("Action: Value is 50 or less. No new action taken.")
            
        print("-" * 30)

    def create_box(self, size):
        """Example function to execute a complex action."""
        try:
            # Check if an existing box is present, otherwise create one
            box = self.doc.getObjectsByLabel("TriggeredBox")[0]
        except:
            box = self.doc.addObject("Part::Box", "TriggeredBox")
            box.Label = "TriggeredBox"
            
        box.Length = size
        box.Width = size
        box.Height = size / 2.0
        self.doc.recompute()

def create_trigger(spreadsheet_label, alias_name):
    """
    Creates the custom feature and links its 'WatchedValue' property 
    to the specified spreadsheet cell alias.
    """
    doc = App.ActiveDocument
    
    # 1. Create the custom feature object
    obj = doc.addObject("App::FeaturePython", "SpreadsheetTrigger")
    TriggeringFeature(obj)
    
    # 2. Find the spreadsheet object by its Label
    try:
        spreadsheet_obj = doc.getObjectsByLabel(spreadsheet_label)[0]
    except IndexError:
        print(f"Error: Spreadsheet with label '{spreadsheet_label}' not found.")
        doc.removeObject(obj.Name)
        return
        
    # 3. Construct the expression string
    expression_string = f"{spreadsheet_obj.Name}.{alias_name}"
    
    # 4. Set the expression on the custom property
    # This registers the dependency!
    obj.setExpression("WatchedValue", expression_string)
    
    doc.recompute()
    return obj

# --- FINAL USAGE ---
# To make this work:
# 1. Open a FreeCAD document.
# 2. Create a Spreadsheet (default label is "Spreadsheet").
# 3. Put a value (e.g., 10.0) in a cell (e.g., A1).
# 4. Right-click A1 and set its Alias to "TriggerValue".
# 5. Run the following code in the Python console:

# create_trigger(
#     spreadsheet_label='Spreadsheet', 
#     alias_name='TriggerValue'
# )

# Now, go to the spreadsheet and change the value in the "TriggerValue" cell.
# When you press Enter, the model will recompute, and the Python code 
# in the TriggeringFeature's execute() method will run.

def main():
    create_trigger(
        spreadsheet_label='Spreadsheet', 
        alias_name='TriggerValue'
    )   
if __name__ == "__main__":
    main()
