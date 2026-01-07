from tree_sitter_language_pack import get_parser , get_language
from typing import List, Dict, Optional
import os

LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".go": "go",
    ".rs": "rust",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "c",
    ".php": "php",
}

NODE_TYPES = {
     "function_definition",      # Python, C++, Go, Rust
    "function_declaration",     # JavaScript, TypeScript, C, C++
    "method_definition",        # Python, JavaScript, TypeScript, Ruby
    "method_declaration",       # Java, C#, Go (interfaces)
    "arrow_function",           # JavaScript, TypeScript
    "generator_function",       # JavaScript
    "func_literal",             # Go (anonymous functions)
    
    # Classes and Objects
    "class_definition",         # Python, Ruby
    "class_declaration",        # JavaScript, TypeScript, Java, C#
    "interface_declaration",    # TypeScript, Java, Go, C#
    "struct_specifier",         # C, C++
    "type_declaration",         # Go, Rust, TypeScript (for types/aliases)
    "enum_declaration",         # Java, C#, TypeScript, Rust
    "protocol_declaration",     # Swift
    
    # Modules and Scoping
    "module",                   # Python (top level), Go, Rust
    "namespace_definition",     # C++, C#
    "program",
}

def detect_lang_from_path(path:str) -> Optional[str]:
    _ , ext = os.path.splitext(path.lower())
    return ext


def parse_code(code:str , file_path:str):
    ext = detect_lang_from_path(file_path)
    if ext not in LANGUAGE_MAP:
        return []

    parser = get_parser(LANGUAGE_MAP[ext])
    tree = parser.parse(bytes(code , "utf8"))
    root = tree.root_node

    blocks = []
    lines = code.splitlines()

    def walk(node):
        if node.type in NODE_TYPES:
            start = node.start_point[0]
            end = node.end_point[0]

            name_node = node.child_by_field_name("name")
            name = (
                name_node.text.decode("utf-8")
                if name_node else "anonymous"
            )

            snippet = "\n".join(lines[start:end + 1])

            blocks.append({
                "symbol": name,
                "type": node.type,
                "start_line": start + 1,
                "end_line": end + 1,
                "code": snippet
            })

        for child in node.children:
            walk(child)

    walk(root)
    return blocks