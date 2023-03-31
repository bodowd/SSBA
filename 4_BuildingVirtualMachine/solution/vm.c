#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define LOAD_WORD 0x01
#define STORE_WORD 0x02
#define ADD 0x03
#define SUB 0x04
#define HALT 0xff

void run_vm(uint8_t *memory) {
  uint16_t registers[3] = {0x0000, 0x0000, 0x0000};

  while (1) {
    uint16_t pc = registers[0];
    uint8_t instruction = memory[pc];

    // Handle halt separately because it doesn't have any args.
    if (instruction == HALT) {
      return;
    }

    uint8_t arg1 = memory[pc + 1];
    uint8_t arg2 = memory[pc + 2];

    uint8_t *byte_pointer;
    uint16_t *word_pointer;

    switch (instruction) {
    // load_word reg (addr)
    case LOAD_WORD:
      byte_pointer = memory + arg2;
      word_pointer = (uint16_t *)byte_pointer;

      registers[arg1] = *word_pointer;
      break;

    // store_word reg (addr)
    case STORE_WORD:
      byte_pointer = memory + arg2;
      word_pointer = (uint16_t *)byte_pointer;

      *word_pointer = registers[arg1];
      break;

    // add reg1 reg2
    case ADD:
      registers[arg1] += registers[arg2];
      break;

    // sub reg1 reg2
    case SUB:
      registers[arg1] -= registers[arg2];
      break;

    default:
      printf("Unrecognized instruction: 0x%x\n", instruction);
      exit(1);
    }

    // Aside from halt, all instructions advance the program counter
    // by the same amount.
    registers[0] += 3;
  }
}

int main() {
  uint8_t memory[20] = {
      0x01, 0x01, 0x10, // load_word r1 (0x10)
      0x01, 0x02, 0x12, // load_word r2 (0x12)
      0x03, 0x01, 0x02, // add r1 r2
      0x02, 0x01, 0x0e, // store_word r1 (0x0E)
      0xff,             // halt
      0x00,             // unused
      0x00, 0x00,       // output
      0xa1, 0x14,       // input 1
      0x0c, 0x00        // input 2
  };

  printf("input 1: %d\n", *(uint16_t *)(memory + 0x10));
  printf("input 2: %d\n", *(uint16_t *)(memory + 0x12));

  run_vm(memory);

  printf("output: %d\n", *(uint16_t *)(memory + 0x0e));
}
