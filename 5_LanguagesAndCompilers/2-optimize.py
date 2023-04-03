import ast
import unittest


def fold_constants(left, right, op):
    """
    If the left and right nodes are both constants, we compute the arithmetic
    and return that result as a constant.
    Otherwise, we just return the node so that it bubbles back up in recursion
    """
    if isinstance(left, ast.Constant) and isinstance(right, ast.Constant):
        left = left.value
        right = right.value
        if isinstance(op, ast.Sub):
            return ast.Constant(left - right)
        elif isinstance(op, ast.Mult):
            return ast.Constant(left * right)
        elif isinstance(op, ast.Add):
            return ast.Constant(left + right)
    else:
        return ast.BinOp(left=left, right=right, op=op)


def optimize(node):
    # TODO
    if isinstance(node, ast.Expression):
        left = node.body.left
        right = node.body.right
        op = node.body.op
    elif isinstance(node, ast.BinOp):
        left = node.left
        right = node.right
        op = node.op
    elif isinstance(node, ast.Constant) or isinstance(node, ast.Name):
        # other base cases
        return node

    if isinstance(left, ast.Constant) and isinstance(right, ast.Constant):
        # base case where the leaf nodes are both constants
        # if only one node is a constant and the other node is not, then
        # you can't fold it
        return fold_constants(left, right, op)

    return fold_constants(optimize(left), optimize(right), op)


class TestOptimize(unittest.TestCase):
    def test_optimize(self):
        test_cases = [
            ("1 + 2 * 3", "7"),
            ("x + 1", "x + 1"),
            ("(2 + 3) * x + y * (z + (2 - 1) * 3)", "5 * x + y * (z + 3)"),
        ]
        for s, expected in test_cases:
            expr = ast.parse(s, mode="eval")
            # Uncomment to print AST for expression
            # print(ast.dump(expr, indent=2))
            optimized = optimize(expr)
            actual = ast.unparse(optimized)
            print(ast.dump(optimized, indent=2))

            if actual != expected:
                raise AssertionError(f'"{s}": expected "{expected}", got "{actual}"')


if __name__ == "__main__":
    unittest.main()
