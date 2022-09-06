## Inventory of spec and implementation details

### LS8 Files and Descriptions
[ ] call.ls8
    - *ASM code:*
        ```
        ; MAIN

        LDI R1,Mult2Print  ; Load R1 with the subroutine address

        ; multiply a bunch of numbers by 2 and print them
        LDI R0,10
        CALL R1

        LDI R0,15
        CALL R1

        LDI R0,18
        CALL R1

        LDI R0,30
        CALL R1

        HLT

        ; Mult2Print
        ;
        ; Multiply a number in R0 by 2 and print it out

        Mult2Print:
            ADD R0,R0  ; or fake it by adding it to itself
            PRN R0
            RET
        ```
    - *Expected output:*
        ```
        20
        30
        36
        60
        ```
    - Load address of subroutine `Mult2Print` into register `R1`. Load integer `10` into register `R0`. Call register `R1` containing `Mult2Print` subroutine. Load integer `15` into register `R0`. Call register `R1` containing `Mult2Print` subroutine. Load integer `18` into register `R0`. Call register `R1` containing `Mult2Print` subroutine. Load integer `30` into register `R0`. Call register `R1` containing `Mult2Print` subroutine. Terminate program execution.
        - Mult2Print subroutine
            - ADD register to itself and store sum in same register. Print value in register. Return.

[ ] interrupts.ls8
    - *ASM code:*
        ```
        LDI R0,0xF8          ; R0 holds the interrupt vector for I0 (timer)
        LDI R1,IntHandler    ; R1 holds the address of the handler
        ST R0,R1             ; Store handler addr in int vector
        LDI R5,1             ; Enable timer interrupts
        LDI R0,Loop
        Loop:
            JMP R0               ; Infinite spin loop

        ; Interrupt handler
        IntHandler:
            LDI R0,65            ; Load R0 with 'A'
            PRA R0               ; Print it
            IRET
        ```
    - *Expected output:* sequence of "A"s, one per second.
    - Load `interrupt vector` for IO (0xF8) into register `R0`. Load addrees of interrupt hanhler subroutine into register `R1`. Store value of register `R1` into register `R0`. Load integer value `1` into register `R5` to enable timer interrupts. Load subroutine `Loop` into register `R0`.
        - Loop subroutine
            - Jump to subroutine stored in register `R0`.
        - Interrupt handler
            - Load char `A` into register `R0`. Print alphanumeric character stored in register `R0`. Return from interrupt handler.

[ ] keyboards.ls8
    - *ASM code:*
        ```
        ; Hook the keyboard interrupt

        LDI R0,0xF9          ; R0 holds the interrupt vector for I1 (keyboard)
        LDI R1,IntHandler    ; R1 holds the address of the handler
        ST R0,R1             ; Store handler addr in int vector
        LDI R5,2             ; Enable keyboard interrupts
        LDI R0,Loop

        Loop:
            JMP R0               ; Infinite spin loop

        ; Interrupt handler
        IntHandler:
            LDI R0,0xF4          ; Memory location of most recent key pressed
            LD R1,R0             ; load R1 from that memory address
            PRA R1               ; Print it
            IRET
        ```
    - *Expected output:* N/A
    - Load interrupt vector for I1 (keyboard) (0xF9) into register `R0`. Load address of interrupt handler subroutine `IntHandler` into register `R1`. Store address of interrupt handler subroutine `IntHandler` into register `R0`. Load integer value `2` into register `R5` to enable keyboard interrupts. Load subroutine `Loop` into register `R0`. 
        - Loop subroutine
            - Jump to subroutine stored in register `R0`.
        - Interrupt handler
            - Load memory address of most recent key pressed `0xF4` into register `R0`. Load registerA, `R0` with the value at the memory address stored in register `R1`. Print alphanumeric character stored in register `R1`. Return from interrupt handler.

[ ] mult.ls8
    - *ASM code*
        ```
        LDI R0,8
        LDI R1,9
        MUL R0,R1
        PRN R0
        HLT
        ```
    - *Expected output:*
        ```
        72
        ```
    - Load integer `8` into register `R0`. Load integer `9` into register `R1`. Multiply register `R0` by `R1` and load result into register `R0`. Print value of `R0` to console. Terminate program execution.

[ ] print8.ls8
    - *ASM code*
        ```
        LDI R0,8
        PRN R0
        HLT
        ```
    - *Expected output:*
        ```
        8
        ```
    - Load integer `8` into register `R0`. Print value stored in register `R0` to console. Terminate program execution.

[ ] printstr.ls8
    - *ASM code*
        ```
	     LDI R0,Hello         
	     LDI R1,14            
	     LDI R2,PrintStr      
	     CALL R2              
	     HLT                  
        ```
    - *Expected output:*
        ```
        Hello, world!
        ```
    - Load address of `Hello` subroutine contianing address of "Hello, world!" bytes into registor `R0`. Load integer representation of number of bytes to print into register `R1`. Load address of subroutine `PrintStr` into register `R2`. Call register `R2`. Terminate program execution.

[ ] sctest.ls8
    - *ASM code:*
        ```
        LDI R0,10
        LDI R1,20
        LDI R2,Test1
        CMP R0,R1
        JEQ R2       ; Does not jump because R0 != R1
        LDI R3,1
        PRN R3       ; Prints 1

        Test1:

        LDI R2,Test2
        CMP R0,R1
        JNE R2       ; Jumps because R0 != R1
        LDI R3,2
        PRN R3       ; Skipped--does not print

        Test2:

        LDI R1,10
        LDI R2,Test3
        CMP R0,R1
        JEQ R2      ; Jumps becuase R0 == R1
        LDI R3,3
        PRN R3      ; Skipped--does not print

        Test3:

        LDI R2,Test4
        CMP R0,R1
        JNE R2      ; Does not jump because R0 == R1
        LDI R3,4
        PRN R3      ; Prints 4

        Test4:

        LDI R3,5
        PRN R3      ; Prints 5
        LDI R2,Test5
        JMP R2      ; Jumps unconditionally
        PRN R3      ; Skipped-does not print

        Test5:

        HLT
        ```
    - *Expected output:*
        ```
        1
        4
        5
        ```
    - Final test

[ ] stack.ls8
    - *ASM code:*
        ```
        LDI R0,1
        LDI R1,2
        PUSH R0
        PUSH R1
        LDI R0,3
        POP R0
        PRN R0  ; "2"

        LDI R0,4
        PUSH R0
        POP R2
        POP R1
        PRN R2  ; "4"

        PRN R1  ; "1"
        HLT
        ```
    - *Expected output:*
        ```
        2
        4
        1
        ```
    - Tests stack implementation

[ ] stackoverflow.ls8
    - *ASM code:*
        ```
	    LDI R0, 0
	    LDI R1, 1
	    LDI R3, Loop
        Loop:
	        PRN R0
	        ADD R0, R1
	        PUSH R0
	        JMP R3
        ```
    - *Expected output:* N/A
    - Simulates a stack buffer overflow
