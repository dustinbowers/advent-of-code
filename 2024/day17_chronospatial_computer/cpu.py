class CPU:
    def __init__(self, a, b, c, prog):
        self.A = a
        self.B = b
        self.C = c
        self.MEM = prog

        self.PC = 0
        self.OUTPUT = []

    def run(self):
        while self.step():
            pass

    def step(self):
        if self.PC >= len(self.MEM):
            return False

        # Load
        opcode = self.MEM[self.PC]
        operand = self.MEM[self.PC + 1]

        # Decode
        decoded_combo = self.decode_combo_operand(operand)

        # Eval
        if opcode == 0:  # ADV COMBO
            self.A = self.A // (2 ** decoded_combo)
        elif opcode == 1:  # BXL LITERAL
            self.B ^= operand
        elif opcode == 2:  # BST COMBO
            self.B = decoded_combo % 8
        elif opcode == 3:  # JNZ LITERAL
            if self.A != 0:
                self.PC = operand
                return True
        elif opcode == 4:  # BXC IGNORED
            self.B ^= self.C
        elif opcode == 5:  # OUT COMBO
            self.OUTPUT.append(str(decoded_combo % 8))
        elif opcode == 6:  # BDV COMBO
            self.B = self.A // (2 ** decoded_combo)
        elif opcode == 7:  # CDV COMBO
            self.C = self.A // (2 ** decoded_combo)
        else:
            raise ValueError('invalid opcode')

        self.PC += 2
        return True

    def decode_combo_operand(self, operand):
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self.A
        elif operand == 5:
            return self.B
        elif operand == 6:
            return self.C
        else:
            raise ValueError('invalid combo operand')
