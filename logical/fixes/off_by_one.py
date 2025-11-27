import ast

def detect_off_by_one(tree, source: str):
    issues = []

    class Visitor(ast.NodeVisitor):
        def visit_For(self, node):
            # Detect: for i in range(len(arr) + 1):
            if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name):
                if node.iter.func.id == "range" and node.iter.args:
                    arg = node.iter.args[0]
                    if isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Add):
                        if isinstance(arg.right, ast.Constant) and arg.right.value == 1:
                            issues.append({
                                "rule": "off_by_one_logic",
                                "line": node.lineno,
                                "col": node.col_offset,
                                "message": "Possible off-by-one error in loop.",
                                "suggestion": "Ensure iteration bounds are correct."
                            })
            self.generic_visit(node)

    Visitor().visit(tree)
    return issues
