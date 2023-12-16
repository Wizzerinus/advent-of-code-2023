digits = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def first_digit(s):
    return next(t for t in s if t in "0123456789")


def replace_letters(s):
    for string, val in digits.items():
        s = s.replace(string, string[0] + str(val) + string[1:])
    return s


def parse(x):
    x = replace_letters(x)
    # print(x)
    d = first_digit(x)
    e = first_digit(x[::-1])
    return int(d + e)


with open("a-input.txt") as f:
    data = f.readlines()
    print(sum(parse(x) for x in data))
