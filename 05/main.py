class IntCode(object):
    def __init__(self, ops):
        self.ops = ops
        self.idx = 0
        self.opcodes = {
            1: (3, self._add),
            2: (3, self._mul),
            3: (1, self._input),
            4: (1, self._output),
            5: (2, self._jump_if_true),
            6: (2, self._jump_if_false),
            7: (3, self._less_than),
            8: (3, self._equals)
        }

    def _add(self, modes, a, b, c):
        self.ops[c] = int(self.ops[a] if modes[0] == 0 else a) + int(self.ops[b] if modes[1] == 0 else b)

    def _mul(self, modes, a, b, c):
        self.ops[c] = int(self.ops[a] if modes[0] == 0 else a) * int(self.ops[b] if modes[1] == 0 else b)

    def _input(self, modes, a):
        self.ops[a] = int(input("Input Value: "))

    def _output(self, modes, a):
        print(f"Output Value: {self.ops[a]}")

    def _jump_if_true(self, modes, a, b):
        if int(self.ops[a] if modes[0] == 0 else a) != 0:
            self.idx = int(self.ops[b] if modes[1] == 0 else b)

    def _jump_if_false(self, modes, a, b):
        if int(self.ops[a] if modes[0] == 0 else a) == 0:
            self.idx = int(self.ops[b] if modes[1] == 0 else b)

    def _less_than(self, modes, a, b, c):
        if int(self.ops[a] if modes[0] == 0 else a) < int(self.ops[b] if modes[1] == 0 else b):
            self.ops[c] = 1
        else:
            self.ops[c] = 0

    def _equals(self, modes, a, b, c):
        if int(self.ops[a] if modes[0] == 0 else a) == int(self.ops[b] if modes[1] == 0 else b):
            self.ops[c] = 1
        else:
            self.ops[c] = 0

    def instruction(self, opcode: int):
        opcode = str(opcode).rjust(5, "0")

        # opcode, mode 1st, mode 2nd, mode 3rd
        return int(opcode[3:]), int(opcode[2]), int(opcode[1]), int(opcode[0])

    def run(self):
        while True:
            op, fst, snd, thd = self.instruction(self.ops[self.idx])

            if op == 99:
                return

            if op not in self.opcodes:
                raise Exception(f"Invalid opcode {op} in position {self.idx}")

            nparams, func = self.opcodes[op]
            if nparams == 1:
                a = self.ops[self.idx+1]
                self.idx += 2
                func((fst, snd, thd), a)
            elif nparams == 2:
                a, b = self.ops[self.idx+1:self.idx+3]
                self.idx += 3
                func((fst, snd, thd), a, b)
            else:
                a, b, c = self.ops[self.idx+1:self.idx+4]
                self.idx += 4
                func((fst, snd, thd), a, b, c)

def run(ops):
    intcode = IntCode(ops)
    intcode.run()

if __name__ == "__main__":
    ops = []
    with open("05/input.txt") as f:
        ops = list(map(int, f.readline().split(",")))

    # Part 1 : Input Value: 1 | Output Value: 15508323
    # Part 2 : Input Value: 5 | Output Value: 9006327
    run(ops)