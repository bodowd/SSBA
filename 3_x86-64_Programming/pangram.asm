section .text
global pangram
pangram:
    xor rax, rax ; zero out the rax result register
    cmp [rdi], byte 0 ; check edge case if input is empty string, otherwise iterate through the string
    jz emptyString
L1:
    mov r8, 122 ; reset-- if 122 - current ascii dec rep >= 25, it is a lower case number
    mov r9, 0 ; reset --use this to convert to uppper case
    mov r10, 90 ; reset -- use this to check if upper case 
    ; mov r13, 0 ; reset -- store upper case letters in r13
    
    cmp [rdi], byte 0 ; check if we are at the end of the string
    jz done ; if so, go to done
    sub r8, [rdi] ; if 122 - rdi <= 25, it is lower case
    cmp r8, 25 
    jle toUpper ; subtract 32 from rdi to convert it to upper case
    sub r10, [rdi]  ; other wise the number is not a lower case, check if it is upper case
    cmp r10, 25
    jle storeUpper ; if this value is <=25 it is upper case
    jmp next ; otherwise the character is not a-z or A-Z, go to next iteration
toUpper:
    mov r9, [rdi]
    sub r9, 32 ; subtracting 32 converts it to upper case. Between 65 and 90
    mov r13, r9 ; store upper case in r13
    jmp setBits
storeUpper:
    mov r13, [rdi] ; rdi is already upper case, store it in r13
    jmp setBits
setBits: 
    ; at this point, upper case char is stored in r13
    sub r13, 65 ; change range of the current number to between 0 and 25 by subtracting 65. 
                ; This is to represent a char in alphabet, and we will shift by that amount
    mov rcx, r13 ; we will shift by the ascii number. Shift count must go in rcx
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
