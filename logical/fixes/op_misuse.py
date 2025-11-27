import ast

def detect_op_misuse(tree, source: str):
    issues = []

    class Visitor(ast.NodeVisitor):
        def visit_If(self, node):
            # Detect accidental bitwise use instead of boolean
            if isinstance(node.test, ast.BinOp) and isinstance(node.test.op, ast.BitAnd):
                issues.append({
                    "rule": "op_misuse",
                    "line": node.lineno,
                    "col": node.col_offset,
                    "message": "Bitwise '&' used inside condition.",
                    "suggestion": "Use 'and' instead of '&' for boolean logic."
                })
            self.generic_visit(node)

    Visitor().visit(tree)
    return issues
