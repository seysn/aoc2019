def fuel(mass):
    return mass // 3 - 2

def rec_fuel(mass):
    f = fuel(mass)
    if f <= 0:
        return 0
    return f + rec_fuel(f)

assert fuel(12) == 2
assert fuel(14) == 2
assert fuel(1969) == 654
assert fuel(100756) == 33583

assert rec_fuel(14) == 2
assert rec_fuel(1969) == 966
assert rec_fuel(100756) == 50346

def part1(masses):
    return sum(map(fuel, masses))


def part2(masses):
    return sum(map(rec_fuel, masses))

if __name__ == "__main__":
    masses = []
    with open("01/input.txt") as f:
        masses = list(map(int, f.readlines()))
    print(part2(masses))