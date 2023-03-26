section .text
global pangram
pangram:
    xor rax, rax ; zero out the rax result register
    cmp [rdi], byte 0 ; check edge case if input is empty string, otherwise iterate through the string
    jz emptyString
L1:
    cmp [rdi], byte 0 ; check if we are at the end of the string
    jz done ; if so, go to done
    cmp [rdi], byte 122
    jle gt97 ; if <= 122, check if >97
    jmp next ; otherwise the character is not a-z or A-Z, go to next iteration
gt97:
    ; check if value >= 97. if yes then it's a lower case a-z
    cmp [rdi], byte 97
    jge toUpper
    jl lt90 ; check if it is upper case AZ char
lt90:
    cmp [rdi], byte 90
    jle gt65 ; if <= 90, check if >= 65
    jmp next ; otherwise its not AZ char
gt65:
    cmp [rdi], byte 65
    mov r8, [rdi] ; move to r8 for setting bits
    jge setBits; it is an upper case AZ char
    jmp next ; otherwise it's not a azAZ char
toUpper:
    mov r8, [rdi]
    sub r8, 32
    jmp setBits
setBits: 
    ; at this point, upper case char is stored in r8
    sub r8, 65 ; change range of the current number to between 0 and 25 by subtracting 65. 
                ; This is to represent a char in alphabet, and we will shift by that amount
    mov rcx, r8 ; we will shift by the ascii number. Shift count must go in rcx
    mov r11, 1 ; we will store the result of the bit shift in r11. First set it to 1
    shl r11, cl ; shift r11 left by the normalized number in r13
    or rax, r11 ; OR rax and r11 to mark if we have seen a character
                ; each bit from 0 to 25 represents a character
                ; if we have seen it, we mark it as 1
                ; OR lets us keep the 1 no matter if we see duplicates or a new character
    jmp next
next:
    add rdi, 1 ; increment pointer to next element in array
    jmp L1 ; continue the loop
emptyString:
    ret
done:
    ; mov r12, 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0011_1111_1111_1111_1111_1111_1111
    mov r12, 67108863
    ; xor rax, r12 ; xor rax with r12, rax will store the result
    ; cmp rax, 0 ; if everything zeroed out, then we found everything
    cmp rax, r12
    je retTrue 
    mov rax, 0 ; otherwise, return false
    ret
retTrue:
    mov rax, 1 ; return true
	ret
