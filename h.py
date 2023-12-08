def make_node_map(data):
    instruction, nodes = data.split("\n\n")
    node_map = {}
    for item in nodes.split("\n"):
        from_node, _, to_nodes = item.partition(" = ")
        to_nodes = to_nodes[1:-1]
        left, _, right = to_nodes.partition(", ")
        node_map[from_node] = (left, right)
    return node_map, instruction


def parse_first(node_map, instruction, start, predicate):
    count = 0
    node = start
    while True:
        for it in instruction:
            node = node_map[node][it == "R"]
            count += 1
            if predicate(node):
                return count


def gcd(a, b):
    if a == 0 or b == 0:
        return a + b
    return gcd(a % b, b % a)


def lcm(numbers):
    if len(numbers) == 2:
        a, b = numbers
        return a * b / gcd(a, b)
    return lcm([numbers[0], lcm(numbers[1:])])


def parse_second(node_map, instruction):
    all_starts = [x for x in node_map if x.endswith("A")]
    all_counts = [parse_first(node_map, instruction, x, lambda t: t.endswith("Z")) for x in all_starts]
    return lcm(all_counts)


with open("h-input.txt") as f:
    node_map, instruction = make_node_map(f.read())
    print(parse_first(node_map, instruction, "AAA", lambda t: t == "ZZZ"))
    print(parse_second(node_map, instruction))
