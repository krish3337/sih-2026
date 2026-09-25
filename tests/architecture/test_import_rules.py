import ast
import os
import pytest

def get_python_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)

def check_imports_in_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=filepath)
        except SyntaxError:
            return []

    bad_imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if "ai_core.impl" in alias.name:
                    bad_imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module and "ai_core.impl" in node.module:
                bad_imports.append(node.module)
    return bad_imports

def test_ai_core_implementation_encapsulation():
    """Fail if any module other than config.py imports from ai_core.impl."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ai_core_dir = os.path.join(project_root, "ai_core")
    
    config_path = os.path.join(ai_core_dir, "config.py")
    
    for filepath in get_python_files(ai_core_dir):
        if filepath == config_path:
            continue
            
        # Ignore the impl folder itself importing from itself
        if "impl" in filepath.split(os.sep):
            continue

        bad_imports = check_imports_in_file(filepath)
        assert not bad_imports, f"File {filepath} illegally imports from ai_core.impl: {bad_imports}"

def test_api_layer_encapsulation():
    """Fail if api/ imports from ai_core.impl."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    api_dir = os.path.join(project_root, "api")
    
    for filepath in get_python_files(api_dir):
        bad_imports = check_imports_in_file(filepath)
        assert not bad_imports, f"API File {filepath} illegally imports from ai_core.impl: {bad_imports}"
