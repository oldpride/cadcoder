import sys
import re
import argparse
# import FreeCAD

def dump_modules(pattern: str = None):
    module_names = sorted(sys.modules.keys())
    print(f"Total loaded modules: {len(module_names)}")
    for module_name in module_names:
        path = getattr(sys.modules[module_name], '__file__', 'built-in or unknown')
        cached = getattr(sys.modules[module_name], '__cached__', 'N/A')
        if pattern.lower() == 'all' or re.search(pattern, module_name) or (path and re.search(pattern, path)):
            indent = "    "
            # FreeCAD.Console.PrintMessage(f"module={module_name}\n")
            # FreeCAD.Console.PrintMessage(f"{indent}path={path}\n")
            # FreeCAD.Console.PrintMessage(f"{indent}time={cached}\n")
            print(f"module={module_name}")
            print(f"{indent}path={path}")
            print(f"{indent}time={cached}")

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(description="Dump loaded Python modules in FreeCAD.")
    '''
    pattern is an optional positional argument.
    If provided, only modules whose names match the pattern will be printed.
    '''
    parser.add_argument("pattern", nargs="?", default='github', help="Regex pattern to filter module names.")
    try:
        args = parser.parse_args()
        return args
    except SystemExit:
        return None
    
if __name__ == "__main__":
    print("Dumping loaded Python modules in FreeCAD...")
    args = parse_args()
    print(f"Pattern: {args.pattern}")

    dump_modules(args.pattern)
