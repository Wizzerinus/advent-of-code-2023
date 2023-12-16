import math
import re

num_regex = re.compile("([0-9]+)")


def parse(time_line, distance_line, one_race=False):
    # so the duration equals x * (time - x) > record
    # x*x - x*time + record > 0
    # D = time ** 2 - 4 * record
    if one_race:
        time_line = time_line.replace(" ", "")
        distance_line = distance_line.replace(" ", "")
    time_values = [int(x) for x in num_regex.findall(time_line)]
    distance_values = [int(x) for x in num_regex.findall(distance_line)]
    prod = 1
    for time, record in zip(time_values, distance_values):
        d = time ** 2 - 4 * record
        dsqrt = math.sqrt(d)
        x_min = math.ceil((time - dsqrt) / 2 + 0.001)
        x_max = math.floor((time + dsqrt) / 2 - 0.001)
        prod *= x_max - x_min + 1
    return prod


with open("f-input.txt") as f:
    lines = f.readlines()
    print(parse(*lines, one_race=False))
    print(parse(*lines, one_race=True))
