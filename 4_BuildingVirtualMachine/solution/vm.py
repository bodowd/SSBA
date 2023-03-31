"""
An example solution to the VM exercise, in Python
"""

# Op codes
LOAD = 0x01
STORE = 0x02
ADD = 0x03
SUB = 0x04
HALT = 0xFF


def compute(memory):
    """
    Given a list representing a 20 "byte" array of memory, run the stored
    program to completion, mutating the list in place.

    The memory format is:

    00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 10 11 12 13
    __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __
    INSTRUCTIONS ---------------------------^ OUT-^ IN-1^ IN-2^
    """
    registers = [
      0x0000,  # PC
      0x0000,  # R1
      0x0000   # R2
    ]

    while True:
        # fetch the next instruction from memory
        pc_value = registers[0]
        op_code = memory[pc_value]

        if op_code == HALT:
            return

        # fetch the opargs: each instruction (other than halt) has two
        arg1, arg2 = memory[pc_value + 1], memory[pc_value + 2]

        # execute the instruction!
        if op_code == LOAD:
            # load 2 bytes (little endian) into the specified register
            registers[arg1] = memory[arg2] + 256*memory[arg2+1]

        elif op_code == STORE:
            # write first (low order) byte to memory
            memory[arg2] = registers[arg1] % 256
            memory[arg2 + 1] = registers[arg1] // 256

        elif op_code == ADD:
            # perform addition and replace arg1 with the result
            registers[arg1] = registers[arg1] + registers[arg2]

        elif op_code == SUB:
            registers[arg1] = registers[arg1] - registers[arg2]

        # update the program counter
        registers[0] += 3


if __name__ == '__main__':
    # 255 + 3 = 258
    memory = [
      0x01, 0x01, 0x10,  # 0x00: load A 0x10
      0x01, 0x02, 0x12,  # 0x03: load B 0x12
      0x03, 0x01, 0x02,  # 0x06: add A B
      0x02, 0x01, 0x0e,  # 0x09: store A 0x0e
      0xff,              # 0x0c: halt
      0x00,              # 0x0d: <<unused>>
      0x00, 0x00,        # 0x0e: output
      0xff, 0x00,        # 0x10: input X = 255
      0x03, 0x00         # 0x12: input Y = 3
    ]

    compute(memory)
    print("Testing 255 + 3 = 258")
    assert memory[0x0e] == 2 and memory[0x0f] == 1
    print(memory)
    print('')

    # 256 - 3 = 253
    memory = [
      0x01, 0x01, 0x10,  # 0x00: load A 0x10
      0x01, 0x02, 0x12,  # 0x03: load B 0x12
      0x04, 0x01, 0x02,  # 0x06: sub A B
      0x02, 0x01, 0x0e,  # 0x09: store A 0x0e
      0xff,              # 0x0c: halt
      0x00,              # 0x0d: <<unused>>
      0x00, 0x00,        # 0x0e: output
      0x00, 0x01,        # 0x10: input X = 256
      0x03, 0x00         # 0x12: input Y = 3
    ]

    compute(memory)
    print("Testing 256 - 3 = 253")
    assert memory[0x0e] == 253 and memory[0x0f] == 0
    print(memory)
    print('')

    print('OK')
