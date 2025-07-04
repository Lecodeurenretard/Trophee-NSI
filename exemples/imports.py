# Pas de moi, c'est de ChatGPT
# si seulement Python avait un système d'import normal...

import importlib.util
import sys
import os

def import_from_filepath(path):
    module_name = os.path.splitext(os.path.basename(path))[0]
    module_dir = os.path.dirname(os.path.abspath(path))

    # Temporarily add the module's directory to sys.path
    sys.path.insert(0, module_dir)
    
    try:
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load specification for '{path}'")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        # Clean up: remove the path from sys.path afterwards
        if module_dir in sys.path:
            sys.path.remove(module_dir)