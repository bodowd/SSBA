LOAD  = 0x01
STORE = 0x02
ADD   = 0x03
HALT  = 0xFF
PC    = 0x00
A     = 0x01
B     = 0x02

def virtual_computer(memory, registers)
 while memory[registers[PC]] != HALT do
   op = memory[registers[PC]]
   registers[PC] += 1
   case op
   when LOAD
     register_address = memory[registers[PC]]
     registers[PC] += 1
     word_address = memory[registers[PC]]
     registers[PC] += 1
     # load both bytes in word
     registers[register_address] = memory[word_address] + (256 * memory[word_address + 1])
   when STORE
     register_address = memory[registers[PC]]
     registers[PC] += 1
     word_address = memory[registers[PC]]
     registers[PC] += 1
     # write first (low order) byte
     memory[word_address] = registers[register_address] % 256
     # write second (high order) byte
     memory[word_address + 1] = registers[register_address] / 256
   when ADD
     register_address_a = memory[registers[PC]]
     registers[PC] += 1
     register_address_b = memory[registers[PC]]
     registers[PC] += 1
     # peform computation on values in registers
     registers[register_address_a] = registers[register_address_a] + registers[register_address_b]
   end
 end
end

memory = [
 1,1,0x10, # 0x00: load A 0x10
 1,2,0x12, # 0x03: load B 0x12
 3,1,2,    # 0x06: add A B
 2,1,0x0e, # 0x09: store A 0x0E
 0xFF,     # 0x0C: halt
 0,        # 0x0D: <<unused>>
 0,0,      # 0x0E: output
 2,0,      # 0x10: input X = 2
 3,0       # 0x12: input Y = 3
]

registers = [ # 2 bytes wide
 0x0000, # PC
 0x0000, # A
 0x0000  # B
]

virtual_computer(memory, registers)
p memory[0x0E] == 5 # test the program worked
p memory # check out the new memory state
