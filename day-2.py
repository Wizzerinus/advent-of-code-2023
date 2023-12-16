def parse_raw(x):
    gn, gd = x.split(": ")
    games = gd.split("; ")
    mins = {"red": 0, "green": 0, "blue": 0}
    for g in games:
        for c in g.split(", "):
            count, color = c.split()
            count = int(count)
            mins[color] = max(mins[color], count)
    return mins


def parse_first(idx, x):
    mins = parse_raw(x)
    return idx + 1 if (mins["red"] <= 12 and mins["green"] <= 13 and mins["blue"] <= 14) else 0


def parse_second(x):
    mins = parse_raw(x)
    return mins["red"] * mins["green"] * mins["blue"]


with open("b-input.txt") as f:
    data = f.readlines()
    print(sum(parse_first(idx, x) for idx, x in enumerate(data)))
    print(sum(parse_second(x) for x in data))
