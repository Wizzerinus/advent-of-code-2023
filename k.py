def count_prefix_sums(count, items):
	ans = []
	j = 0
	for i in range(count):
		while j < len(items) and items[j] < i:
			j = j + 1
		ans.append(j)
	return ans


def count_distances(data, expansion_factor):
	total = 0
	items = []
	
	empty_rows = [i for i in range(len(data)) if all(data[i][k] == "." for k in range(len(data[0])))]
	row_psums = count_prefix_sums(len(data), empty_rows)
	empty_cols = [k for k in range(len(data[0])) if all(data[i][k] == "." for i in range(len(data)))]
	col_psums = count_prefix_sums(len(data[0]), empty_cols)

	for i, row in enumerate(data):
		for j, col in enumerate(row):
			if col == "#":
				items.append((i, j))
	for it in items:
		for jt in items:
			if it > jt:
				upper = min(it[0], jt[0])
				lower = max(it[0], jt[0])
				left = min(it[1], jt[1])
				right = max(it[1], jt[1])
				psum_value = row_psums[lower] - row_psums[upper] + col_psums[right] - col_psums[left]
				psum_added = (expansion_factor - 1) * psum_value
				total += lower - upper + right - left + psum_added
	return total


with open("k-input.txt") as f:
	data = [list(x.strip()) for x in f.readlines()]
	print(count_distances(data, 2))
	print(count_distances(data, 1000000))
