"""
Starter code for the VM exercise, in Python
"""

# Op codes
LOAD = 0x01
STORE = 0x02
ADD = 0x03
SUB = 0x04
HALT = 0xFF

# Stretch goals
ADDI = 0x05
SUBI = 0x06
JUMP = 0x07
BEQZ = 0x08


def compute(memory):
    """
    Given a list representing a 20 "byte" array of memory, run the stored
    program to completion, mutating the list in place.

    The memory format is:

    00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 10 11 12 13
    __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __
    INSTRUCTIONS ---------------------------^ OUT-^ IN-1^ IN-2^
    """
    registers = [0x00, 0x00, 0x00]  # PC, R1, and R2

    while True:
        # TODO: fetch the next instruction from memory
        # op = ...
        # instructions are a single byte each
        # parameters are also a single byte
        pc = registers[0]
        op = memory[pc]

        # TODO: decode and execute
        if op == HALT:
            return

        arg1, arg2 = memory[pc + 1], memory[pc + 2]

        if op == LOAD:
            # load 2 bytes (little endian) into register -- least significant bytes come first
            # arg2 points to 0x0e for example. Because this is one number split across two bytes
            # and little endian, we have to put the hexadecimal number together

            registers[arg1] = memory[arg2] + 256 * memory[arg2 + 1]
            # print(registers[arg1], memory[arg2], memory[arg2 + 1])
        elif op == ADD:
            # add reg1 to reg2 and store back in reg1
            registers[1] = registers[1] + registers[2]
        elif op == SUB:
            registers[1] = registers[1] - registers[2]
        elif op == STORE:
            # write the first (low order) byte to memory
            # if you don't split it back into two bytes, you get the wrong answers
            # because it expects the OUTPUT to be split across memory addr 0x0e and 0x0f
            memory[arg2] = registers[arg1] % 256
            memory[arg2 + 1] = registers[arg1] // 256
        # update PC to point to the next instruction 3 bytes away
        registers[0] += 0x03


if __name__ == "__main__":
    # 255 + 3 = 258
    memory = [
        0x01,
        0x01,
        0x10,  # 0x00: load A 0x10
        0x01,
        0x02,
        0x12,  # 0x03: load B 0x12
        0x03,
        0x01,
        0x02,  # 0x06: add A B
        0x02,
        0x01,
        0x0E,  # 0x09: store A 0x0e
        0xFF,  # 0x0c: halt
        0x00,  # 0x0d: <<unused>>
        0x00,
        0x00,  # 0x0e: output
        0xFF,  # 255
        0x00,  # 0x10: input X = 255
        0x03,  # 3
        0x00,  # 0x12: input Y = 3
    ]

    compute(memory)
    print("Testing 255 + 3 = 258")
    print(memory)
    # output is also little endian. So the low order bytes come first in 0x0E
    # this gives a number 0x0102 => 258
    assert memory[0x0E] == 2 and memory[0x0F] == 1
    print("")

    # 256 - 3 = 253
    memory = [
        0x01,
        0x01,
        0x10,  # 0x00: load A 0x10
        0x01,
        0x02,
        0x12,  # 0x03: load B 0x12
        0x04,
        0x01,
        0x02,  # 0x06: sub A B
        0x02,
        0x01,
        0x0E,  # 0x09: store A 0x0e
        0xFF,  # 0x0c: halt
        0x00,  # 0x0d: <<unused>>
        0x00,
        0x00,  # 0x0e: output
        0x00,
        0x01,  # 0x10: input X = 256 little endian. so after combining you get 0x0100 => 256
        0x03,
        0x00,  # 0x12: input Y = 3
    ]

    compute(memory)
    print("Testing 256 - 3 = 253")
    print(memory)
    assert memory[0x0E] == 253 and memory[0x0F] == 0
    print("")

    print("OK")
