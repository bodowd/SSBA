section .text
global _start
_start:
    mov rax, 0  ; initialize total to 0
    mov r8, 0  ; initialize i to 0 for the loop
    jmp .L1
.L1:
    cmp r8, 10
    jle .L2
	ret
.L2:
    add rax, r8
    inc r8 ; i++ to go to next interation in loop
    jmp .L1

