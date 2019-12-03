def path(wire):
    res = []
    x, y = 0, 0
    for w in wire:
        direction, step = w[0], int(w[1:])
        inc = None
        if direction == "U":
            inc = (0, 1)
        elif direction == "D":
            inc = (0, -1)
        elif direction == "R":
            inc = (1, 0)
        else:
            inc = (-1, 0)

        for i in range(0, step):
            x, y = x + inc[0], y + inc[1]
            res.append((x, y))
    return res

def intersections(pos1, pos2, part2=False):
    res = []
    i = 0
    for p in pos1:
        if p in pos2:
            if part2:
                res.append((p, i, pos2.index(p)))
            else:
                res.append(p)
        i += 1
    return res

def distance(pos, part2=False):
    if part2:
        return pos[1] + pos[2] + 2
    return abs(pos[0]) + abs(pos[1])

def part1(wires):
    path1, path2 = path(wires[0]), path(wires[1])
    inters = intersections(path1, path2)
    return min([distance(inter) for inter in inters])

w1 = ["R75","D30","R83","U83","L12","D49","R71","U7","L72"]
w2 = ["U62","R66","U55","R34","D71","R55","D58","R83"]
test1 = part1((w1, w2))
assert test1 == 159, test1
w3 = ["R98","U47","R26","D63","R33","U87","L62","D20","R33","U53","R51"]
w4 = ["U98","R91","D20","R16","D67","R40","U7","R15","U6","R7"]
test2 = part1((w3, w4))
assert test2 == 135, test2

def part2(wires):
    path1, path2 = path(wires[0]), path(wires[1])
    inters = intersections(path1, path2, True)
    return min([distance(inter, True) for inter in inters])

test3 = part2((w1, w2))
assert test3 == 610, test3
test4 = part2((w3, w4))
assert test4 == 410, test4

if __name__ == "__main__":
    wires = None
    with open("03/input.txt") as f:
        wire1 = f.readline().split(",")
        wire2 = f.readline().split(",")
        wires = (wire1, wire2)
    # print(part1(wires)) # 2180
    print(part2(wires)) # 112316