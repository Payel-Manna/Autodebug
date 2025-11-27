import ast

def detect_unreachable_code(tree, source: str):
    issues = []

    class Visitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            unreachable = False
            for stmt in node.body:
                if unreachable:
                    issues.append({
                        "rule": "unreachable_code",
                        "line": stmt.lineno,
                        "col": stmt.col_offset,
                        "message": "Unreachable code detected.",
                        "suggestion": "Remove or refactor unreachable statements."
                    })

                if isinstance(stmt, (ast.Return, ast.Raise)):
                    unreachable = True

            self.generic_visit(node)

    Visitor().visit(tree)
    return issues
