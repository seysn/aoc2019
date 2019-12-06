class Obj(object):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.orbit = []

    def count(self, cpt=0):
        if self.orbit:
            return cpt + sum([o.count(cpt + 1) for o in self.orbit])
        return cpt

    def count_jump(self, dest, cpt=0, caller=None):
        if (self.parent and dest == self.parent.name) or dest in self.orbit:
            return cpt

        if caller is None or (caller is not None and self.parent and self.parent != caller):
            res = self.parent.count_jump(dest, cpt + 1, self.name)
            if res:
                return res

        for o in self.orbit:
            if o == caller:
                continue
            res = o.count_jump(dest, cpt + 1, self.name)
            if res:
                return res

        return None

    def get_top_parent(self):
        if self.parent:
            return self.parent.get_top_parent()
        return self

    def __iadd__(self, orbit):
        self.orbit.append(orbit)

    def __eq__(self, name: str):
        return self.name == name

class Map(object):
    def __init__(self, map):
        self._top = map[0][0]
        self._map = {}
        self._init_objs(map)

    def _init_objs(self, map):
        for o in map:
            o1, o2 = None, None

            if o[0] not in self._map:
                o1 = Obj(o[0])
                self._map[o[0]] = o1
            else:
                o1 = self._map[o[0]]

            if o[1] not in self._map:
                o2 = Obj(o[1], o1)
                self._map[o[1]] = o2
            else:
                o2 = self._map[o[1]]
                o2.parent = o1

            o1 += o2

    def count_orbits(self):
        return self._map[self._top].get_top_parent().count()

    def count_transfert(self, from_obj="YOU", to_obj="SAN"):
        start = self._map[from_obj]
        return start.count_jump(to_obj) - 1

def parse_input(inp):
    if inp[0][-1] == "\n":
        return [l[:-1].split(")") for l in inp]
    return [l.split(")") for l in inp]

def part1(inp):
    map = Map(inp)
    return map.count_orbits()

test1 = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""
res1 = part1(parse_input(test1.split("\n")))
assert res1 == 42, res1

def part2(inp):
    map = Map(inp)
    return map.count_transfert()

test2 = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""
res2 = part2(parse_input(test2.split("\n")))
assert res2 == 4, res2

if __name__ == "__main__":
    inp = None
    with open("06/input.txt") as f:
        inp = parse_input(f.readlines())
    print(part1(inp)) # 234446
    print(part2(inp)) # 385