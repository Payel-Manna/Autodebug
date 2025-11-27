import ast

def detect_wrong_return(tree, source: str):
    issues = []

    class Visitor(ast.NodeVisitor):
        def visit_FunctionDef(self, func):
            returns = []
            for node in ast.walk(func):
                if isinstance(node, ast.Return):
                    returns.append(node.value)

            # If mixed: some return value, some return None
            if len(returns) > 1:
                has_value = any(r is not None for r in returns)
                has_none = any(r is None for r in returns)

                if has_value and has_none:
                    issues.append({
                        "rule": "wrong_return",
                        "line": func.lineno,
                        "col": func.col_offset,
                        "message": "Inconsistent return values in function.",
                        "suggestion": "Ensure all code paths return the same type."
                    })

    Visitor().visit(tree)
    return issues