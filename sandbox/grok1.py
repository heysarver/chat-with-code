# write a python script that accepts a .py code file and extracts all functions and classes into a nested list representing the structure of the file.  Classes may have nested functions and functions may have nested functions.

import ast

def get_function_and_class_names(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        tree = ast.parse(content)
        function_and_class_names = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_and_class_names.append(node.name)
            elif isinstance(node, ast.ClassDef):
                function_and_class_names.append(node.name)

        return function_and_class_names

def get_nested_structure(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        tree = ast.parse(content)
        nested_structure = []

        class_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        function_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

        for class_node in class_nodes:
            class_nested_structure = []
            for function_node in function_nodes:
                if function_node.col_offset >= class_node.col_offset and function_node.col_offset <= class_node.end_col_offset:
                    class_nested_structure.append(function_node.name)
            nested_structure.append([class_node.name, class_nested_structure])

        return nested_structure

def main():
    file_path = input("Enter the path to your .py code file: ")
    function_and_class_names = get_function_and_class_names(file_path)
    nested_structure = get_nested_structure(file_path)

    print("\nAll functions and classes in the file:")
    for name in function_and_class_names:
        print(name)

    print("\nNested structure of functions and classes in the file:")
    for item in nested_structure:
        print(item)

if __name__ == "__main__":
    main()
