from collections import Counter

class Image(object):
    WIDTH = 25
    HEIGHT = 6

    def __init__(self, inp, width=None, height=None):
        self.width = Image.WIDTH if width is None else width
        self.height = Image.HEIGHT if height is None else height
        self.size = self.width * self.height
        self.layers = [inp[i:i+self.size] for i in range(0, len(inp), self.size)]
        self._decode()

    def __getitem__(self, key):
        return self.layers[key]

    def __iter__(self):
        for l in self.layers:
            yield l

    def __len__(self):
        return len(self.layers)

    def _decode(self):
        self.decoded = ""
        for i in range(self.size):
            for l in self.layers:
                if l[i] != "2":
                    self.decoded += l[i]
                    break

def part1(inp):
    img = Image(inp)
    layer = (None, None)
    for l in img:
        c = Counter(l)
        if layer[0] is None or layer[0] > c["0"]:
            layer = (c["0"], c)
    return layer[1]["1"] * layer[1]["2"]

def part2(inp):
    img = Image(inp)
    res = [img.decoded[i:i+img.width].replace("1", " ").replace("0", "█") for i in range(0, img.size, img.width)]
    return res

test2 = Image("0222112222120000", 2, 2)
assert test2.decoded == "0110", test2.decoded

if __name__ == "__main__":
    inp = None
    with open("08/input.txt") as f:
        inp = f.readline()[:-1]
    print(part1(inp)) # 2193
    print()
    print("\n".join(part2(inp)))