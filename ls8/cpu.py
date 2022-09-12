"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        self.sp = 0xF4
        self.ir = 0
        self.fl = 0
        self.__OPERAND_COUNT_MASK = 0b11000000
        self.__IS_ALU_OP_MASK = 0b00100000
        self.__SETS_PC_MASK = 0b00010000
        self.__INSTRUCTION_IDENT_MASK = 0b00001111

        # Instrustion Identifiers
        self.__HLT = 0b0001
        self.__LDI = 0b0010
        self.__PRN = 0b0111

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def ram_read(self, MAR):
        """
        Reads the value stored at the given `Memory Address Register` in RAM.
        """
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        """
        Given a Memory Address Register and Memory Data Register, writes the
        value in MDR to RAM at MAR. Returns nothing.
        """
        self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""
        while True:
            instruction = self.ram_read(self.pc)
            instr_ident = instruction & self.__INSTRUCTION_IDENT_MASK
            op_count = instruction & self.__OPERAND_COUNT_MASK
            is_alu_op = instruction & self.__IS_ALU_OP_MASK
            sets_pc = instruction & self.__SETS_PC_MASK
            print(
                f"instruction : {bin(instruction)}, instr_ident : {bin(instr_ident)}, op_count : {bin(op_count)}, is_alu_op : {bin(is_alu_op)}, sets_pc : {bin(sets_pc)}"
            )
            break
