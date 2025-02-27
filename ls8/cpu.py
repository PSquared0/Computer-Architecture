"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.IR = 0
        self.reg[7] = 0xf4
        self.SP = 7
        self.E = 0
        self.L = 0
        self.G = 0
        self.live = True
        pass

    def ram_read(self, address):
        return self.ram[address]        

    def ram_write(self, address, value):
        self.ram[address] = value

    def push(self, a):
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = self.reg[a]
    
    def pop(self, a):
        self.reg[a] = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1

    def load(self):
        """Load a program into memory."""
        address = 0
        with open(sys.argv[1]) as f:
            for line in f:
                if line[0] != '#' and line != '\n':
                    self.ram[address] = int(line[0:8], 2)
                    address += 1
            f.closed    
    

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'CMP':
            if self.reg[reg_a] == self.reg[reg_b]:
                self.E = 1
                self.L = 0
                self.G = 0
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.E = 0
                self.L = 1
                self.G = 0
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.E = 0
                self.L = 0
                self.G = 1
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        pass
