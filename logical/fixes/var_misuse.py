import ast

def detect_var_misuse(tree, source: str):
    issues = []
    assigned = set()

    class Visitor(ast.NodeVisitor):
        def visit_Assign(self, node):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned.add(target.id)
            self.generic_visit(node)

        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Load):
                if node.id not in assigned and node.id not in ("True", "False", "None"):
                    issues.append({
                        "rule": "var_misuse",
                        "line": node.lineno,
                        "col": node.col_offset,
                        "message": f"Variable '{node.id}' used before assignment.",
                        "suggestion": "Initialize variable before using it."
                    })
            self.generic_visit(node)

    Visitor().visit(tree)
    return issues
