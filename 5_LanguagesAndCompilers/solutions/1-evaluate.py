from operator import add, sub, mul

import ast
import unittest

TYPE_TO_FUNCTION = {
    ast.Add: add,
    ast.Sub: sub,
    ast.Mult: mul,
}

def evaluate(node):
    if type(node) == ast.Expression:
        return evaluate(node.body)
    elif type(node) == ast.BinOp:
        a = evaluate(node.left)
        b = evaluate(node.right)
        op_type = type(node.op)
        if op_type not in TYPE_TO_FUNCTION:
            raise ValueError(f'unsupported op type {node.op}')
        op_function = TYPE_TO_FUNCTION[op_type]
        return op_function(a, b)
    elif type(node) == ast.Constant:
        return node.value
    else:
        raise ValueError(f'unsupported node type {node}')

class TestEvaluate(unittest.TestCase):
    def test_evaluate(self):
        test_cases = [
            ('1 + 1', 2),
            ('1 + 2 * 3', 7),
            ('1 + 2 * (3 - 4)', -1),
            ('1 + (2 - 3) * 4 + 5', 2),
        ]
        for s, expected in test_cases:
            expr = ast.parse(s, mode='eval')
            # Uncomment to print AST for expression
            # print(ast.dump(expr, indent=2))
            actual = evaluate(expr)
            if actual != expected:
                raise AssertionError(f'"{s}": expected {expected}, got {actual}')

if __name__ == '__main__':
    unittest.main()
