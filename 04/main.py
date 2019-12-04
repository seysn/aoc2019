def is_password(pwd):
    if len(pwd) != 6:
        return False
    adj = False
    for a, b in zip(pwd, pwd[1:]):
        if a > b:
            return False
        if a == b:
            adj = True
    if not adj:
        return False
    return True

assert is_password("111111") == True
assert is_password("223450") == False
assert is_password("123789") == False
assert is_password("123477") == True

def is_password2(pwd):
    if not is_password(pwd):
        return False
    adj = 1
    prev = pwd[0]
    for c in pwd[1:]:
        if c == prev:
            adj += 1
        else:
            if adj == 2:
                return True
            adj = 1
        prev = c
    return adj == 2

assert is_password2("112233") == True
assert is_password2("123444") == False
assert is_password2("111122") == True
assert is_password2("223456") == True

def run(func):
    start, end = [int(range) for range in inp.split("-")]
    res = 0
    for i in range(start, end):
        if func(str(i)):
            res += 1
    return res

def part1(inp):
    return run(is_password)

def part2(inp):
    return run(is_password2)

if __name__ == "__main__":
    inp = None
    with open("04/input.txt") as f:
        inp = f.readline()
    print(part1(inp))
    print(part2(inp))