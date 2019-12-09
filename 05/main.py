def instruction(opcode: str):
    opcode = opcode.rjust(5, "0")

    # opcode, mode 1st, mode 2nd, mode 3rd
    return int(opcode[3:]), int(opcode[2]), int(opcode[1]), int(opcode[0])

assert instruction("1002") == (2, 0, 1, 0)

def opcode(ops, pos=0):
    op, fst, snd, thd = instruction(str(ops[pos]))
    if op == 99:
        return ops

    if op in [1, 2, 7, 8]:
        a, b, c = ops[pos+1:pos+4]
        if op == 1:
            ops[c] = int(ops[a] if fst == 0 else a) + int(ops[b] if snd == 0 else b)
        elif op == 2:
            ops[c] = int(ops[a] if fst == 0 else a) * int(ops[b] if snd == 0 else b)
        elif op == 7:
            if int(ops[a] if fst == 0 else a) < int(ops[b] if snd == 0 else b):
                ops[c] = 1
            else:
                ops[c] = 0
        elif op == 8:
            if int(ops[a] if fst == 0 else a) == int(ops[b] if snd == 0 else b):
                ops[c] = 1
            else:
                ops[c] = 0
        return opcode(ops, pos + 4)
    elif op in [3, 4]:
        a = ops[pos+1]
        if op == 3:
            inp = input("Input Value: ")
            ops[a] = int(inp)
        elif op == 4:
            print(f"Output Value: {ops[a]}")

        return opcode(ops, pos + 2)
    elif op in [5, 6]:
        a, b = ops[pos+1:pos+3]
        if op == 5:
            # print("jump-if-true", a, b)
            if int(ops[a] if fst == 0 else a) != 0:
                return opcode(ops, int(ops[b] if snd == 0 else b))
        elif op == 6:
            # print("jump-if-false", a, b)
            if int(ops[a] if fst == 0 else a) == 0:
                return opcode(ops, int(ops[b] if snd == 0 else b))
        return opcode(ops, pos + 3)
    else:
        raise Exception(f"Invalid opcode {op} in position {pos}")

def part1(ops):
    opcode(ops)

def part2(ops):
    return opcode(ops)

def run(inp):
    return opcode(list(map(int, inp.split(","))))

if __name__ == "__main__":
    ops = []
    with open("05/input.txt") as f:
        ops = list(map(int, f.readline().split(",")))
    #part1(ops) # Input Value: 1 | Output Value: 15508323
    print(part2(ops))