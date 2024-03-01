import ast
import os
import astunparse

def extract_functions_and_classes(file_path):
    with open(file_path, "r") as source:
        tree = ast.parse(source.read())

    def extract(node, result=None):
        if result is None:
            result = []
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.ClassDef)):
                result.append({
                    'type': 'class' if isinstance(child, ast.ClassDef) else 'function',
                    'name': child.name,
                    'body': astunparse.unparse(child).strip()
                })
        return result

    return extract(tree)

# Test the function
print(extract_functions_and_classes('../data/double-entry-accounting/app/routes/transactions.py'))
