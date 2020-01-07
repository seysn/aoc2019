class Fft(object):
    def __init__(self, inp: str, offset=0):
        self.signal = list(map(int, list(inp.strip())))
        self.offset = offset
        self.length = len(inp)
        self.last_digit = None

    def get_pattern(self, pos=0, base=[0, 1, 0, -1]):
        pattern = None
        if pos == 0:
            pattern = base
        else:
            pattern = [item for sub in [[i] * (pos + 1) for i in base] for item in sub]

        res = []
        while len(res) < len(self.signal) + 1:
            res += pattern
        return res[1:len(self.signal)+2]

    def digit(self, pos):
        if pos * 2 > self.length:
            if self.last_digit is not None:
                tmp = self.last_digit - self.signal[pos-1]
                if tmp < 0:
                    tmp += 10
                self.last_digit = tmp
            else:
                self.last_digit = int(str(sum(self.signal[pos:]))[-1])
            return self.last_digit
        tmp = [0] * pos
        tmp += map(lambda x, y: x * y, self.get_pattern(pos)[pos:], self.signal[pos:])
        self.last_digit = int(str(sum(tmp))[-1])
        return self.last_digit

    def phase(self):
        res = [0] * self.offset
        for i in range(self.offset, len(self.signal)):
            res.append(self.digit(i))
        self.last_digit = None
        self.signal = res

    def run(self, times=100):
        for _ in range(times):
            self.phase()
        return "".join(map(str, self.signal))

def teq(expected, actual):
    """test assert equals"""
    assert expected == actual, f"expected: {expected}, actual: {actual}"

teq("48226158", Fft("12345678").run(1))
teq("01029498", Fft("12345678").run(4))

def part1(inp):
    print(">> running part1")
    return Fft(inp).run()[:8]

teq("24176176", part1("80871224585914546619083218645595"))
teq("73745418", part1("19617804207202209144916044189917"))
teq("52432133", part1("69317163492948606335995924319873"))
print("> tests part1 done")

def part2(inp):
    print(">> running part2")
    offset = int(inp[:7])
    return Fft(inp * 10000, offset).run()[offset:offset+8]

teq("84462026", part2("03036732577212944063491565474664"))
teq("78725270", part2("02935109699940807407585447034323"))
teq("53553731", part2("03081770884921959731165446850517"))
print("> tests part2 done")

if __name__ == "__main__":
    inp = None
    with open("16/input.txt") as f:
        inp = f.readline().strip()

    print(part1(inp)) # 22122816
    print(part2(inp)) # 41402171