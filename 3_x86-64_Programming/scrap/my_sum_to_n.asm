; Disassembly of file: /home/bing/code/SSBA/3_x86-64_Programming/my_sum_to_n.o
; Sat Mar 25 19:13:06 2023
; Type: ELF64
; Syntax: NASM
; Instruction set: 8086, x64

default rel

global main: function


SECTION .text   align=1 execute                         ; section number 1, code

main:   ; Function begin
        endbr64                                         ; 0000 _ F3: 0F 1E. FA
        push    rbp                                     ; 0004 _ 55
        mov     rbp, rsp                                ; 0005 _ 48: 89. E5
        mov     dword [rbp-8H], 0                       ; 0008 _ C7. 45, F8, 00000000
        mov     dword [rbp-4H], 0                       ; 000F _ C7. 45, FC, 00000000
        jmp     ?_002                                   ; 0016 _ EB, 0A

?_001:  mov     eax, dword [rbp-4H]                     ; 0018 _ 8B. 45, FC
        add     dword [rbp-8H], eax                     ; 001B _ 01. 45, F8
        add     dword [rbp-4H], 1                       ; 001E _ 83. 45, FC, 01
?_002:  cmp     dword [rbp-4H], 10                      ; 0022 _ 83. 7D, FC, 0A
        jle     ?_001                                   ; 0026 _ 7E, F0
        mov     eax, dword [rbp-8H]                     ; 0028 _ 8B. 45, F8
        pop     rbp                                     ; 002B _ 5D
        ret                                             ; 002C _ C3
; main End of function


SECTION .data   align=1 noexecute                       ; section number 2, data


SECTION .bss    align=1 noexecute                       ; section number 3, bss


SECTION .note.gnu.property align=8 noexecute            ; section number 4, const

        db 04H, 00H, 00H, 00H, 10H, 00H, 00H, 00H       ; 0000 _ ........
        db 05H, 00H, 00H, 00H, 47H, 4EH, 55H, 00H       ; 0008 _ ....GNU.
        db 02H, 00H, 00H, 0C0H, 04H, 00H, 00H, 00H      ; 0010 _ ........
        db 03H, 00H, 00H, 00H, 00H, 00H, 00H, 00H       ; 0018 _ ........


