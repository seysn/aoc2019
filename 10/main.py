class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __str__(self):
        return f"Position({self.x}, {self.y})"

    def __repr__(self):
        return f"Position({self.x}, {self.y})"

    def clone(self):
        return Position(self.x, self.y)

    def direction(self, other):
        return (other.x - self.x, other.y - self.y)

    def reduce_direction(self, other):
        d = self.direction(other)
        d0, d1 = abs(d[0]), abs(d[1])
        m0, m1 = -1 if d[0] < 0 else 1, -1 if d[1] < 0 else 1

        if min(d0, d1) == 1:
            return d, False

        if d0 == 0:
            return (0, m1), d1 != m1

        if d1 == 0:
            return (m0, 0), d1 != m1

        x, y = None, None
        for i in range(1, d0 + 1):
            y = (d1 / d0) * i
            if y.is_integer():
                y = int(y * m1)
                x = i * m0
                break

        if x == None:
            return d, False
        return (x, y), (x, y) != d

        # if min(d0, d1) == d0:
        #     if d1 % d0 == 0:
        #         return (m0, (d1 // d0) * m1), True
        # else:
        #     if d0 % d1 == 0:
        #         return ((d0 // d1) * m0, m1), True
        # return d, False

assert Position(1, 1).direction(Position(2, 0)) == (1, -1)
assert Position(1, 0).reduce_direction(Position(3, 4)) == ((1, 2), True)
assert Position(1, 0).reduce_direction(Position(4, 3)) == ((1, 1), True)
assert Position(1, 0).direction(Position(0, 2)) == (-1, 2)
assert Position(1, 0).reduce_direction(Position(0, 2)) == ((-1, 2), False)
assert Position(4, 0).reduce_direction(Position(2, 4)) == ((-1, 2), True)
assert Position(0, 1).reduce_direction(Position(9, 7)) == ((3, 2), True)

class Map(object):
    def __init__(self, inp):
        self.m = Map.parse(inp)
        self.ast = self.asteroids()

    def __len__(self):
        return len(self.m)

    @staticmethod
    def parse(inp):
        return [list(a.strip()) for a in inp.split("\n")]

    def asteroids(self):
        res = []
        for y, a in enumerate(self.m):
            for x, b in enumerate(a):
                if b == "#":
                    res.append(Position(x, y))
        return res

    def is_visible(self, pos, ast):
        if pos == ast:
            return True

        direction, reduced = pos.reduce_direction(ast)
        if not reduced:
            return True

        p = pos.clone()
        while p != ast:
            p += Position(direction[0], direction[1])
            if p in self.ast and p != ast:
                return False
        return True
        # return (pos + Position(direction[0], direction[1])) not in self.ast

    def count(self, pos, debug=False):
        res = []
        for a in self.ast:
            if self.is_visible(pos, a) and pos != a:
                res.append(a)
        if debug:
            print(f"count({pos}) == {res}")
        return len(res)

    def get(self, pos):
        return self.m[pos.y][pos.x]

assert Map(".#\n..").get(Position(1, 0)) == "#"
assert Map(".#.\n..#").ast == [Position(1, 0), Position(2, 1)]
assert Map(".#\n.#\n.#").is_visible(Position(1, 0), Position(1, 2)) == False
assert Map("#..\n...\n.#.\n...\n..#").is_visible(Position(0, 0), Position(1, 2)) == True
assert Map("#..\n...\n.#.\n...\n..#").is_visible(Position(0, 0), Position(2, 4)) == False

def part1(inp):
    m = Map(inp)
    best = (0, None)
    for pos in m.ast:
        res = m.count(pos)
        if res > best[0]:
            best = (res, (pos.x, pos.y))
    return best, m

if __name__ == "__main__":
    import tests
    tests.run_tests(part1)

    inp = None
    with open("10/input.txt") as f:
        inp = "".join(f.readlines())

    print(part1(inp))