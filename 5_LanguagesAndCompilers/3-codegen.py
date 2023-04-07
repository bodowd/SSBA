from collections import defaultdict
from operator import add, sub, mul

import ast
import unittest

X_REGISTER = "r1"
Y_REGISTER = "r2"


def operations(
    left_register, right_register, left_const, right_const, output_register, op
):
    if left_const:
        left_operand = f"${left_const}"
    else:
        left_operand = f"%r{left_register}"

    if right_const:
        right_operand = f"${right_const}"
    else:
        right_operand = f"%r{right_register}"

    if isinstance(op, ast.Sub):
        return [f"SUB {left_operand} {right_operand} %r{output_register}"]
    elif isinstance(op, ast.Mult):
        return [f"MUL {left_operand} {right_operand} %r{output_register}"]
    elif isinstance(op, ast.Add):
        return [f"ADD {left_operand} {right_operand} %r{output_register}"]


def _codegen(node, instructions, left_reg, right_reg, out_reg):
    if isinstance(node, ast.BinOp):
        left = node.left
        right = node.right
        op = node.op

    if isinstance(left, ast.BinOp):
        left_instructions, out_reg = _codegen(
            left, instructions, left_reg, right_reg, out_reg
        )

        instructions = [*instructions, *left_instructions]
        # print(instructions)

    if isinstance(right, ast.BinOp):
        right_instructions, out_reg = _codegen(
            right, instructions, left_reg, right_reg, out_reg
        )

        instructions = [*instructions, *right_instructions]
        # print(instructions)

    # if isinstance(left, ast.Constant):
    # print(instructions)
    # instructions = [
    #     *instructions,
    #     *operations(
    #         left_register=left_reg,
    #         right_register=right_reg,
    #         left_const=left.value,
    #         right_const=None,
    #         output_register=out_reg,
    #         op=op,
    #     ),
    # ]

    if isinstance(left, ast.Constant) and isinstance(right, ast.Constant):
        print(left.value, right.value)
        instructions = [
            *instructions,
            *operations(
                left_register=None,
                right_register=None,
                left_const=left.value,
                right_const=right.value,
                output_register=out_reg,
                op=op,
            ),
        ]

    # instructions = [
    #     *instructions,
    #     *operations(
    #         _codegen(left, instructions, left_reg, right_reg, out_reg),
    #         _codegen(right, instructions, left_reg, right_reg, out_reg),
    #         op,
    #     ),
    # ]
    return instructions, out_reg


def codegen(node):
    # TODO
    instructions = []
    if isinstance(node, ast.Expression):
        # out_reg will be the last register the output is in
        generated, out_reg = _codegen(node.body, instructions, 1, 2, 3)

    move_to_output = [f"MOV %r{out_reg} %r0"]
    final = [*generated, *move_to_output]
    return final


OP_TO_FUNCTION = {
    "ADD": add,
    "SUB": sub,
    "MUL": mul,
}


def run_assembly_program(instructions, x, y):
    registers = defaultdict(int)
    registers[X_REGISTER] = x
    registers[Y_REGISTER] = y

    def input_operand(arg):
        if arg[0] == "$":
            return int(arg[1:])
        elif arg[0] == "%":
            if arg[1] != "r" or not arg[2:].isdigit():
                raise ValueError(f"invalid register {arg}")
            return registers[arg[1:]]
        else:
            raise ValueError(f"invalid input operand {arg}")

    def output_operand(arg):
        if arg[0] != "%":
            raise ValueError(f"invalid output operand {arg}")
        return arg[1:]

    for instruction in instructions:
        parts = instruction.strip().split()
        if parts[0] == "MOV":
            in1 = input_operand(parts[1])
            out1 = output_operand(parts[2])
            registers[out1] = in1
        elif parts[0] in OP_TO_FUNCTION:
            f = OP_TO_FUNCTION[parts[0]]
            in1 = input_operand(parts[1])
            in2 = input_operand(parts[2])
            out1 = output_operand(parts[3])
            registers[out1] = f(in1, in2)
            print(in1, in2, out1)
        else:
            raise ValueError(f"invalid instruction {instruction}")
    return registers["r0"]


class TestCodegen(unittest.TestCase):
    def test_codegen(self):
        # For each test case, generate assembly, then run it to make sure
        # it produces the expected answer.
        test_cases = [
            # ("1 + 1", (0, 0), 2),
            ("1 + 2 * 3", (0, 0), 7),
            # ("1 + 2 * (3 - 4)", (0, 0), -1),
            # ("1 + (2 - 3) * 4 + 5", (0, 0), 2),
            # ("x", (5, 4), 5),
            # ("x + 1", (10, 0), 11),
            # ("y + 1", (10, 0), 1),
            # ("x + y + 1", (1, 2), 4),
            # ("2 * ((x - 1) * (y + 2)) + x", (3, 5), 31),
        ]
        for s, (x, y), expected in test_cases:
            expr = ast.parse(s, mode="eval")
            # Uncomment to print AST for expression
            # print(ast.dump(expr, indent=2))
            program = codegen(expr)
            # Uncomment to print result of codegen
            print(program)
            actual = run_assembly_program(program, x, y)
            if actual != expected:
                raise AssertionError(f'"{s}": expected "{expected}", got "{actual}"')


if __name__ == "__main__":
    unittest.main()
