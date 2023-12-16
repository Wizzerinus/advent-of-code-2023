from multiprocessing import Pool
from collections import defaultdict


def check_prefix(current, target, strict=True):
	if strict:
		return target[:len(current)] == current
	return target[:len(current) - 1] == current[:-1] and \
		len(target) >= len(current) and \
		target[len(current) - 1] >= current[-1]


def count_subline(block, numbers):
	numbers = tuple(numbers)
	dp = {}
	current_sym_count = 0
	# Indexed by: (last_sym, current_number_list) -> count
	if block[0] != "#":
		dp[(".", ())] = 1
	if block[0] != "." and numbers:
		dp[("#", (1, ))] = 1
	
	for idx, item in enumerate(block):
		if idx == 0:
			continue
		new_dp = defaultdict(int)
		for (last_sym, current_numbers), count in dp.items():
			if item != "#":
				if check_prefix(current_numbers, numbers, strict=True):
					new_dp[(".", current_numbers)] += count
			if item != ".":
				if last_sym == "#":
					next_numbers = (*current_numbers[:-1], current_numbers[-1] + 1)
				else:
					next_numbers = (*current_numbers, 1)
				if check_prefix(next_numbers, numbers, strict=False):
					new_dp[("#", next_numbers)] += count
		dp = new_dp
	return dp[("#", numbers)] + dp[(".", numbers)]


def count_picrosses(line):
	items, counts = line.split()
	counts = list(map(int, counts.split(",")))
	return count_subline(items, counts)


def count_picrosses_expanded(line):
	items, counts = line.split()
	counts = list(map(int, counts.split(",")))
	counts *= 5
	items = f"{items}?" * 4 + items
	return count_subline(items, counts)


if __name__ == "__main__":
	with open("l-input.txt") as f:
		data = f.readlines()
		print(sum(count_picrosses(x) for x in data))
		with Pool(16) as p:
			print(sum(p.map(count_picrosses_expanded, data)))
