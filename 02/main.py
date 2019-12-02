def opcode(ops, pos=0):
    op = ops[pos]
    if op == 99:
        return ops

    a, b, c = ops[pos+1:pos+4]
    if op == 1:
        ops[c] = ops[a] + ops[b]
    elif op == 2:
        ops[c] = ops[a] * ops[b]
    else:
        raise Exception(f"Invalid opcode {op} in position {pos}")

    return opcode(ops, pos + 4)

assert opcode([1, 0, 0, 0, 99]) == [2, 0, 0, 0, 99]
assert opcode([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99]
assert opcode([2, 4, 4, 5, 99, 0]) == [2, 4, 4, 5, 99, 9801]
assert opcode([1, 1, 1, 4, 99, 5, 6, 0, 99]) == [30, 1, 1, 4, 2, 5, 6, 0, 99]
assert opcode([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]) == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]

def part1(ops):
    ops[1] = 12
    ops[2] = 2
    return opcode(ops)

def part2(ops):
    VAL = 19690720
    for noun in range(0, 100):
        for verb in range(0, 100):
            tmp = ops[:]
            tmp[1] = noun
            tmp[2] = verb
            res = opcode(tmp)
            if res[0] == VAL:
                return 100 * noun + verb
    return None

if __name__ == "__main__":
    ops = []
    with open("02/input.txt") as f:
        ops = list(map(int, f.readline().split(",")))
    print(part2(ops))