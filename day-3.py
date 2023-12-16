from collections import defaultdict
import itertools


def valid(data, index, start, end):
    if index < 0 or index >= len(data):
        return False
    if start < 0:
        start = 0
    return any(item not in "0123456789.\n" for item in data[index][start:end])


def has_gear(data, index, start, end):
    if index < 0 or index >= len(data):
        yield None
        return
    if start < 0:
        start = 0
    yield from ((index, k) for k, item in enumerate(data[index]) if item == "*" and end > k >= start)


def find_numbers(line, data):
    current_numbers = []
    start_index = -1
    current_string = ""
    for j, item in enumerate(line):
        if item in "0123456789":
            current_string += item
            if start_index == -1:
                start_index = j
        elif current_string:
            current_numbers.append((start_index, j, int(current_string)))
            current_string = ""
            start_index = -1
    return current_numbers


def parse_first(line, index, data):
    current_numbers = find_numbers(line, data)
    
    summ = 0
    for start, end, value in current_numbers:
        if any(valid(data, index + k, start - 1, end + 1) for k in range(-1, 2)):
            summ += value
    return summ


def find_numbers_with_index(line, index, data):
    return [(a, b, c, index) for a, b, c in find_numbers(line, data)]


def find_gears(data):
    all_numbers = [find_numbers_with_index(line, index, data) for index, line in enumerate(data)]
    gears = defaultdict(list)
    for start, end, value, line in itertools.chain.from_iterable(all_numbers):
        for shift in range(-1, 2):
            for gear in has_gear(data, shift + line, start - 1, end + 1):
                if gear:
                    gears[gear].append(value)
    
    summ = 0
    for k in gears.values():
        if len(k) == 2:
            summ += k[0] * k[1]
    return summ


with open("c-input.txt") as f:
    data = f.readlines()
    print(sum(parse_first(line, index, data) for index, line in enumerate(data)))
    print(find_gears(data))
