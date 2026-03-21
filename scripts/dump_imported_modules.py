import sys

# Get a list of the names of all currently imported modules
imported_module_names = list(sys.modules.keys())

# Print each imported module name
for module_name in sorted(imported_module_names):
    print(module_name)
