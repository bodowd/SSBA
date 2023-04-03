import ast
import unittest


def operations(left, right, op):
    if isinstance(op, ast.Sub):
        return left - right
    elif isinstance(op, ast.Mult):
        return left * right
    elif isinstance(op, ast.Add):
        return left + right


def evaluate(node):
    # TODO
    if isinstance(node, ast.Expression):
        left = node.body.left
        right = node.body.right
        op = node.body.op
    elif isinstance(node, ast.BinOp):
        left = node.left
        right = node.right
        op = node.op
    elif isinstance(node, ast.Constant):
        # base case, return value of the leaf node
        return node.value

    return operations(evaluate(left), evaluate(right), op)


class TestEvaluate(unittest.TestCase):
    def test_evaluate(self):
        test_cases = [
            ("1 + 1", 2),
            ("1 + 2 * 3", 7),
            ("1 + 2 * (3 - 4)", -1),
            ("1 + (2 - 3) * 4 + 5", 2),
        ]
        for s, expected in test_cases:
            expr = ast.parse(s, mode="eval")
            # Uncomment to print AST for expression
            print(ast.dump(expr, indent=2))
            actual = evaluate(expr)
            if actual != expected:
                raise AssertionError(f'"{s}": expected {expected}, got {actual}')


if __name__ == "__main__":
    unittest.main()
