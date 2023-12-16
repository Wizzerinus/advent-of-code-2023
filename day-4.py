def parse_first(line, exp=True):
    line = line.split(": ")[1]
    winning, mine = map(lambda t: list(map(int, t.split())), line.split(" | "))
    winnings = len([x for x in mine if x in winning])
    if exp:
        return 2 ** (winnings - 1) if winnings else 0
    return winnings


def parse_second(data):
    count = len(data)
    counts = [1 for _ in range(count)]
    for i, line in enumerate(data):
        winnings = parse_first(line, exp=False)
        for j in range(i + 1, min(count, i + winnings + 1)):
            counts[j] += counts[i]
    return sum(counts)


with open("d-input.txt") as f:
    data = f.readlines()
    print(sum(parse_first(line) for line in data))
    print(parse_second(data))

