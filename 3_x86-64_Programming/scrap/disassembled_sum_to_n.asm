; Disassembly of file: /home/bing/code/SSBA/3_x86-64_Programming/sum_to_n.o
; Sat Mar 25 18:53:34 2023
; Type: ELF64
; Syntax: NASM
; Instruction set: 8086, x64

default rel

global sum_to_n: function


SECTION .text   align=1 execute                         ; section number 1, code

sum_to_n:; Function begin
        endbr64                                         ; 0000 _ F3: 0F 1E. FA
        push    rbp                                     ; 0004 _ 55
        mov     rbp, rsp                                ; 0005 _ 48: 89. E5
        mov     dword [rbp-14H], edi                    ; 0008 _ 89. 7D, EC
        mov     dword [rbp-8H], 0                       ; 000B _ C7. 45, F8, 00000000
        mov     dword [rbp-4H], 0                       ; 0012 _ C7. 45, FC, 00000000
        jmp     ?_002                                   ; 0019 _ EB, 0A

?_001:  mov     eax, dword [rbp-4H]                     ; 001B _ 8B. 45, FC
        add     dword [rbp-8H], eax                     ; 001E _ 01. 45, F8
        add     dword [rbp-4H], 1                       ; 0021 _ 83. 45, FC, 01
?_002:  mov     eax, dword [rbp-4H]                     ; 0025 _ 8B. 45, FC
        cmp     eax, dword [rbp-14H]                    ; 0028 _ 3B. 45, EC
        jle     ?_001                                   ; 002B _ 7E, EE
        mov     eax, dword [rbp-8H]                     ; 002D _ 8B. 45, F8
        pop     rbp                                     ; 0030 _ 5D
        ret                                             ; 0031 _ C3
; sum_to_n End of function


SECTION .data   align=1 noexecute                       ; section number 2, data


SECTION .bss    align=1 noexecute                       ; section number 3, bss


SECTION .note.gnu.property align=8 noexecute            ; section number 4, const

        db 04H, 00H, 00H, 00H, 10H, 00H, 00H, 00H       ; 0000 _ ........
        db 05H, 00H, 00H, 00H, 47H, 4EH, 55H, 00H       ; 0008 _ ....GNU.
        db 02H, 00H, 00H, 0C0H, 04H, 00H, 00H, 00H      ; 0010 _ ........
        db 03H, 00H, 00H, 00H, 00H, 00H, 00H, 00H       ; 0018 _ ........


