import dataclasses
import math


@dataclasses.dataclass
class Vector:
    x: int
    y: int
    
    def __post_init__(self):
        assert self.x * self.y == 0
    
    def __mul__(self, t: "Vector"):
        return self.y * t.x - self.x * t.y
    
    def __add__(self, t: "Vector"):
        return Vector(self.x + t.x, self.y + t.y)
    
    def inc_length(self, value: int):
        if self.x:
            self.x += math.copysign(value, self.x * value)
        if self.y:
            self.y += math.copysign(value, self.y * value)
    
    @classmethod
    def from_pair(cls, direction, length):
        if direction == "R":
            return cls(length, 0)
        elif direction == "L":
            return cls(-length, 0)
        elif direction == "U":
            return cls(0, length)
        else:
            return cls(0, -length)

    @classmethod
    def from_color(cls, color):
        distance = int(color[2:-2], 16)
        direction = {"0": "R", "1": "D", "2": "L", "3": "U"}[color[-2]]
        return cls.from_pair(direction, distance)


def count_space(lines):
    lines = [t.split() for t in lines]
    vectors = [Vector.from_pair(x, int(y)) for x, y, z in lines]
    return find_space_with_boundary(vectors)


def count_rgb_space(lines):
    lines = [t.split()[2] for t in lines]
    vectors = [Vector.from_color(z) for z in lines]
    return find_space_with_boundary(vectors)


def find_space_with_boundary(vectors):
    # We need to fix vectors to turn them into "exterior" vectors. For example:
    # ###
    # ###
    # ###
    # The exterior length of each side is 3 while the interior length is 2
    # ###..
    # ###..
    # #####
    # The exterior length of the vertical line is 2 and the interior is 2
    # #####
    # ##...
    # ##...
    # #####
    # The exterior length of the vertical line is 2 and the interior is 3
    # I am not sure if this depends on the rotation direction (clockwise or counterclockwise)
    # but it gives the right answer for the input soooo
    for idx, item in enumerate(vectors):
        prev_vector = vectors[idx - 1]
        next_vector = vectors[(idx + 1) % len(vectors)]
        is_interior = item * prev_vector > 0 and next_vector * item > 0
        is_exterior = item * prev_vector > 0 or next_vector * item > 0
        if is_interior:
            item.inc_length(-1)
        elif not is_exterior:
            item.inc_length(1)
    return find_space_within(vectors)


def find_space_within(vectors):
    total = 0
    while len(vectors) >= 4:
        first, second, after_second, before_first = vectors[0], vectors[1], vectors[2], vectors[-1]
        total += first * second
        new_first = first + after_second
        new_second = second + before_first
        vectors = [new_first, *vectors[3:-1], new_second]
    
    return round(abs(total))


with open("r-input.txt") as f:
    lines = f.readlines()
    print(count_space(lines))
    print(count_rgb_space(lines))
