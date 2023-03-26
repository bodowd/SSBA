section .text
global sum_to_n
sum_to_n:
;     mov rax, 0  ; initialize total to 0
;     mov r8, 0  ; initialize i to 0 for the loop
;     jmp .L1
; .L1:
;     cmp r8, rdi
;     jle .L2
; 	ret
; .L2:
;     add rax, r8
;     inc r8 ; i++ to go to next interation in loop
;     jmp .L1
    mov rax, rdi
    add rax, 1
    imul rax, rdi
    mov rcx, 2 ; to divde we need to put the bottom number in rcx
    mov rdx, 0  ; the remainder goes into rdx. This needs to be zeroed out before the division
    div rcx ; divide rax by rcx

    ret


