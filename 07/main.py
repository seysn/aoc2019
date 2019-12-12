import itertools
import threading
from queue import Queue

class IntCode(threading.Thread):
    def __init__(self, ops, name="IntCode", phase=None, inp=None):
        threading.Thread.__init__(self)
        self.name = name
        self.phase = phase
        self.inp = inp
        self.ops = ops
        self.idx = 0
        self.out = Queue()
        self.before = None
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
        if self.phase is not None:
            self.ops[a] = self.phase
            self.phase = None
            return
        if self.inp is not None:
            self.ops[a] = self.inp
            self.inp = None
            return

        if not self.before:
            raise Exception("before not setted")

        self.ops[a] = self.before.out.get()

    def _output(self, modes, a):
        self.out.put(self.ops[a])

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
                break

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

def run(ops, phases, names=["A", "B", "C", "D", "E"]):
    inp = 0
    assert len(phases) == len(names)
    for i in range(len(phases)):
        intcode = IntCode(ops, names[i], phases[i], inp)
        intcode.run()
        inp = intcode.out.get()
    return inp

assert run([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], (4,3,2,1,0)) == 43210
assert run([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0], (0,1,2,3,4)) == 54321
assert run([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], (1,0,4,3,2)) == 65210

def run2(ops, phases, names=["A", "B", "C", "D", "E"]):
    inp = 0
    assert len(phases) == len(names)

    ic1 = IntCode(ops, names[0], phases[0], inp)
    ic2 = IntCode(ops, names[1], phases[1])
    ic3 = IntCode(ops, names[2], phases[2])
    ic4 = IntCode(ops, names[3], phases[3])
    ic5 = IntCode(ops, names[4], phases[4])
    ic1.before = ic5
    ic2.before = ic1
    ic3.before = ic2
    ic4.before = ic3
    ic5.before = ic4

    ic1.start()
    ic2.start()
    ic3.start()
    ic4.start()
    ic5.start()

    ic5.join()
    return ic5.out.get()

def part1(ops):
    max_signal = (0,(-1,-1,-1,-1))
    for params in itertools.permutations(range(5)):
        signal = run(ops, params)
        if signal > max_signal[0]:
            max_signal = (signal, params)
    return max_signal

def part2(ops):
    max_signal = (0,(-1,-1,-1,-1))
    for params in itertools.permutations(range(5, 10)):
        signal = run2(ops, params)
        if signal > max_signal[0]:
            max_signal = (signal, params)
    return max_signal

if __name__ == "__main__":
    ops = []
    with open("07/input.txt") as f:
        ops = list(map(int, f.readline().split(",")))

    print(part1(ops)) # (398674, (0, 3, 1, 2, 4))
    print(part2(ops)) # (39431233, (7, 8, 5, 9, 6))