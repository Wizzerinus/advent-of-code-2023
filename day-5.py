def convert_seeds(seed, ranges):
    for row in ranges:
        dest_start, src_start, length = map(int, row.split())
        if length + src_start > seed >= src_start:
            return seed + dest_start - src_start
    return seed


def find_location(data):
    # part 1
    seed_row, *transforms = data.split("\n\n")
    seeds = list(map(int, seed_row.split(": ")[1].split()))
    for transform in transforms:
        ranges = [row for row in transform.split("\n")[1:] if row]
        seeds = [convert_seeds(seed, ranges) for seed in seeds]
    
    return min(seeds)


def convert_seed_ranges(seed_ranges, ranges):
    output = []
    range_list = []
    converted = []
    for row in ranges:
        dest_start, src_start, row_length = map(int, row.split())
        src_end = src_start + row_length
        range_list.append((dest_start, src_start, src_end))
    
    for it in seed_ranges:
        remaining_ranges = [it]
        while remaining_ranges:
            start, seed_length = remaining_ranges.pop()
            end = start + seed_length
            for dest_start, src_start, src_end in range_list:
                if start <= src_start < end:
                    # src_start splits the current seed range
                    # so we need to start the transformed range at src_start
                    # and end some time later
                    true_start = src_start
                    true_end = min(end, src_end)
                    converted.append((dest_start, true_end - true_start))
                    if true_start != start:
                        remaining_ranges.append((start, true_start - start))
                    if true_end != end:
                        remaining_ranges.append((true_end, end - true_end))
                    break
                elif start < src_end < end:
                    # src_end splits the current seed range but src_start is to the left
                    # so we need to start the transformed range at start and end in the middle
                    true_start = start
                    true_end = src_end
                    true_dest_start = dest_start + true_start - src_start
                    converted.append((true_dest_start, src_end - start))
                    remaining_ranges.append((true_end, end - true_end))
                    break
                elif src_start <= start < end <= src_end:
                    # current range is fully inside
                    converted.append((start + dest_start - src_start, seed_length))
                    break
            else:
                converted.append((start, seed_length))
    
    return converted


def find_double_range_location(data):
    # part 2
    seed_row, *transforms = data.split("\n\n")
    seeds = list(map(int, seed_row.split(": ")[1].split()))
    # Each range is a tuple of (start, length)
    seed_ranges = list(zip(seeds[::2], seeds[1::2]))
    for transform in transforms:
        ranges = [row for row in transform.split("\n")[1:] if row]
        seed_ranges = convert_seed_ranges(seed_ranges, ranges)
    
    return min([k[0] for k in seed_ranges])


with open("e-input.txt") as f:
    data = f.read()
    print(find_location(data))
    print(find_double_range_location(data))
