def interpolate(row, target_x=None):
    values = list(map(int, row.split(" ")))
    # use lagrange's interpolating polynomial with values from 0 to len(values) - 1 known
    if target_x is None:
        target_x = len(values)
    total = 0
    for idx, val in enumerate(values):
        prod = val
        for id2, val2 in enumerate(values):
            if idx == id2:
                continue
            prod *= (target_x - id2) / (idx - id2)
        total += prod
    return round(total)


with open("i-input.txt") as f:
    lines = f.readlines()
    print(sum(interpolate(x) for x in lines))
    print(sum(interpolate(x, -1) for x in lines))
