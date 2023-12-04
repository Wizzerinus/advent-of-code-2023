def parse(x):
    gn, gd = x.split(": ")
    games = gd.split("; ")
    mins = {"red": 0, "green": 0, "blue": 0}
    for g in games:
        for c in g.split(", "):
            count, color = c.split()
            count = int(count)
            mins[color] = max(mins[color], count)
    return mins["red"] * mins["green"] * mins["blue"]


with open("b-input.txt") as f:
    data = f.readlines()
    print(sum(parse(x) for x in data))
