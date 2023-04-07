from collections import defaultdict
from operator import add, sub, mul

import ast
import unittest

X_REGISTER = 'r1'
Y_REGISTER = 'r2'

TYPE_TO_NAME = {
    ast.Add: 'ADD',
    ast.Sub: 'SUB',
    ast.Mult: 'MUL',
}

# Helper to keep track of the next available register
class Registers:
    mapping = {
        'x': X_REGISTER,
        'y': Y_REGISTER,
    }

    def __init__(self):
        self.next_available = 3

    def get_next(self):
        x = self.next_available
        self.next_available += 1
        return f'r{x}'

    def get_mapping(self, name):
        if name not in Registers.mapping:
            raise ValueError(f'unrecognized variable {name}')
        return Registers.mapping[name]

# Returns a program fragment, along with the register that the
# result is placed in after the fragment runs
#
# The is_top_level flag is only used to determine if the output
# should be placed in the output register %r0 instead of a
# temporary intermediate register
def codegen_internal(node, regs, is_top_level=False):
    if type(node) == ast.BinOp:
        result = []
        # Recursively handle the left side, so that the result
        # will come from l_arg
        if type(node.left) == ast.Constant:
            l_arg = f'${node.left.value}'
        else:
            a, l_reg = codegen_internal(node.left, regs)
            result += a
            l_arg = f'%{l_reg}'
        # Recursively handle the right side, so that the result
        # will come from r_arg
        if type(node.right) == ast.Constant:
            r_arg = f'${node.right.value}'
        else:
            b, r_reg = codegen_internal(node.right, regs)
            result += b
            r_arg = f'%{r_reg}'
        # Output a single instruction that performs the correct
        # operation
        op_type = type(node.op)
        if op_type not in TYPE_TO_NAME:
            raise ValueError(f'unsupported op type {node.op}')
        out_reg = 'r0' if is_top_level else regs.get_next()
        result.append(f'{TYPE_TO_NAME[op_type]} {l_arg} {r_arg} %{out_reg}')
        return result, out_reg
    elif type(node) == ast.Constant:
        out_reg = 'r0' if is_top_level else regs.get_next()
        return [f'MOV ${node.value} %{out_reg}'], out_reg
    elif type(node) == ast.Name:
        in_reg = regs.get_mapping(node.id)
        out_reg = 'r0' if is_top_level else regs.get_next()
        return [f'MOV %{in_reg} %{out_reg}'], out_reg
    else:
        raise ValueError(f'unsupported node type {node}')

def codegen(expr):
    regs = Registers()
    program, reg = codegen_internal(expr.body, regs, is_top_level=True)
    return program

OP_TO_FUNCTION = {
    'ADD': add,
    'SUB': sub,
    'MUL': mul,
}

def run_assembly_program(instructions, x, y):
    registers = defaultdict(int)
    registers[X_REGISTER] = x
    registers[Y_REGISTER] = y
    def input_operand(arg):
        if arg[0] == '$':
            return int(arg[1:])
        elif arg[0] == '%':
            if arg[1] != 'r' or not arg[2:].isdigit():
                raise ValueError(f'invalid register {arg}')
            return registers[arg[1:]]
        else:
            raise ValueError(f'invalid input operand {arg}')
    def output_operand(arg):
        if arg[0] != '%':
            raise ValueError(f'invalid output operand {arg}')
        return arg[1:]
    for instruction in instructions:
        parts = instruction.strip().split()
        if parts[0] == 'MOV':
            in1 = input_operand(parts[1])
            out1 = output_operand(parts[2])
            registers[out1] = in1
        elif parts[0] in OP_TO_FUNCTION:
            f = OP_TO_FUNCTION[parts[0]]
            in1 = input_operand(parts[1])
            in2 = input_operand(parts[2])
            out1 = output_operand(parts[3])
            registers[out1] = f(in1, in2)
        else:
            raise ValueError(f'invalid instruction {instruction}')
    return registers['r0']

class TestCodegen(unittest.TestCase):
    def test_codegen(self):
        # For each test case, generate assembly, then run it to make sure
        # it produces the expected answer.
        test_cases = [
            ('1 + 1', (0, 0), 2),
            ('1 + 2 * 3', (0, 0), 7),
            ('1 + 2 * (3 - 4)', (0, 0), -1),
            ('1 + (2 - 3) * 4 + 5', (0, 0), 2),
            ('x', (5, 4), 5),
            ('x + 1', (10, 0), 11),
            ('y + 1', (10, 0), 1),
            ('x + y + 1', (1, 2), 4),
            ('2 * ((x - 1) * (y + 2)) + x', (3, 5), 31),
        ]
        for s, (x, y), expected in test_cases:
            expr = ast.parse(s, mode='eval')
            # Uncomment to print AST for expression
            # print(ast.dump(expr, indent=2))
            program = codegen(expr)
            # Uncomment to print result of codegen
            # print(program)
            actual = run_assembly_program(program, x, y)
            if actual != expected:
                raise AssertionError(f'"{s}": expected "{expected}", got "{actual}"')

if __name__ == '__main__':
    unittest.main()
