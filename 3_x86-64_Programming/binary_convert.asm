section .text
global binary_convert
binary_convert:
    mov rdx, -1  ; intialize place
    mov rax, 0 ; initialize total
    mov rsi, rdi ; copy rdi to rsi to do first iteration to get string length
strlen:
    cmp [rsi], byte 0 ; iterate through string and count the length
    jz .L1 ; go to the next loop if we hit the end of the string
    inc rdx ; increment the place counter
    add rsi, 1 ; go to next element in the array
    jmp strlen
.L1:
    cmp [rdi], byte 0 ; check if this element is the null byte -- end of string
    jz done ; if null byte, exit
    cmp [rdi], byte 49 ; check if the current element is equal to 49 the ascii code for '1'
    jz .calc
    jmp .next_iteration
.calc:
    mov rcx, rdx ; shift count must go in rcx, set it to current place
    mov r10, 1 ; store the result of bit shift in r10. first set it to 1
    shl r10, cl ; shift left to calculate 2 ** place
    add rax, r10 ; add the current amount to the total
    jmp .next_iteration
.next_iteration:
    dec rdx ; decrement place
    add rdi, 1 ; next element in the array
    jmp .L1 ; go to top of the loop

done:
	ret
