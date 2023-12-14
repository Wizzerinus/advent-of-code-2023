def pp(block):
	return "\n".join("".join(t) for t in block)


def transpose(block):
	matrix = [[] for _ in range(len(block[0]))]
	for row in block:
		for idx, cell in enumerate(row):
			matrix[idx].append(cell)
	return matrix


def find_directional(block, exclusion=0):
	values = set()
	for middle_idx in range(1, len(block)):
		bottom_idx = min(middle_idx * 2, len(block))
		top_idx = middle_idx * 2 - bottom_idx
		reversed_block = block[bottom_idx - 1:top_idx - 1:-1]
		if not top_idx:  # fuck python
			reversed_block = block[bottom_idx - 1::-1]
		if block[top_idx:bottom_idx] == reversed_block:
			values.add(middle_idx)
	# The problem is that we actually can have multiple values
	# At least 0 and len(block) count (although we don't include them)
	# So we assume that's not a problem
	values.discard(exclusion)
	if values:
		assert len(values) == 1, (values, exclusion)
		return list(values)[0]
	return 0


def find_reflections(block, exclusion=0):
	value = (find_directional(transpose(block), exclusion % 100), find_directional(block, exclusion // 100))
	return value[0] + value[1] * 100


def swap(block, i, j):
	if block[i][j] == ".":
		block[i][j] = "#"
	else:
		block[i][j] = "."


def find_adjusted_reflections(block):
	og_val = find_reflections(block)
	exclusion = og_val
	for i in range(len(block)):
		for j in range(len(block[0])):
			swap(block, i, j)
			val = find_reflections(block, exclusion)
			swap(block, i, j)
			if val:
				return val
	assert 0, "\n" + pp(block)
	return 0


def make_blocks(data):
	return [[list(t) for t in w.strip().split()] for w in data.strip().split("\n\n")]


with open("m-input.txt") as f:
	blocks = make_blocks(f.read())
	print(sum(find_reflections(x) for x in blocks))
	print(sum(find_adjusted_reflections(x) for x in blocks))
