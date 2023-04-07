from operator import add, sub, mul

import ast
import unittest

TYPE_TO_FUNCTION = {
    ast.Add: add,
    ast.Sub: sub,
    ast.Mult: mul,
}

def optimize(node):
    if type(node) == ast.Expression:
        node.body = optimize(node.body)
        return node
    elif type(node) == ast.BinOp:
        left = optimize(node.left)
        right = optimize(node.right)
        if type(left) == ast.Constant and type(right) == ast.Constant:
            a = left.value
            b = right.value
            op_type = type(node.op)
            if op_type not in TYPE_TO_FUNCTION:
                raise ValueError(f'unsupported op type {node.op}')
            op_function = TYPE_TO_FUNCTION[op_type]
            value = op_function(a, b)
            return ast.Constant(value)
        else:
            node.left = left
            node.right = right
            return node
    elif type(node) == ast.Name:
        return node
    elif type(node) == ast.Constant:
        return node
    else:
        raise ValueError(f'unsupported node type {node}')

class TestOptimize(unittest.TestCase):
    def test_optimize(self):
        test_cases = [
            ('1 + 2 * 3', '7'),
            ('x + 1', 'x + 1'),
            ('(2 + 3) * x + y * (z + (2 - 1) * 3)', '5 * x + y * (z + 3)'),
        ]
        for s, expected in test_cases:
            expr = ast.parse(s, mode='eval')
            # Uncomment to print AST for expression
            # print(ast.dump(expr, indent=2))
            optimized = optimize(expr)
            actual = ast.unparse(optimized)
            if actual != expected:
                raise AssertionError(f'"{s}": expected "{expected}", got "{actual}"')

if __name__ == '__main__':
    unittest.main()
