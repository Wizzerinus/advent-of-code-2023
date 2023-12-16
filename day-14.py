def tilt_north(data):
	for idx, row in enumerate(data):
		for jdx, cell in enumerate(row):
			if cell == "O":
				try:
					obstacle = next(rdx for rdx in range(idx - 1, -1, -1) if data[rdx][jdx] != ".")
				except StopIteration:
					obstacle = -1
				new_row = obstacle + 1
				data[idx][jdx] = "."
				data[new_row][jdx] = "O"


def calculate(data):
	total = 0
	for idx, row in enumerate(data):
		for jdx, cell in enumerate(row):
			if cell == "O":
				total += len(data) - idx
	return total


def rot_right(data):
	matrix = [[] for _ in range(len(data[0]))]
	for row in data:
		for idx, cell in enumerate(row):
			matrix[idx].append(cell)
	return [x[::-1] for x in matrix]


def single_cycle(data):
	# roll north
	tilt_north(data)
	# roll west
	data = rot_right(data)
	tilt_north(data)
	data = rot_right(rot_right(rot_right(data)))
	# roll south
	data = rot_right(rot_right(data))
	tilt_north(data)
	data = rot_right(rot_right(data))
	# roll east
	data = rot_right(rot_right(rot_right(data)))
	tilt_north(data)
	data = rot_right(data)
	
	return data


def tilt_loop(data):
	map_to_turn_count = {}
	first_turn = None
	last_turn = None
	for i in range(10**10):
		data = single_cycle(data)
		new_string = stringify(data)
		if new_string in map_to_turn_count:
			first_turn = map_to_turn_count[new_string]
			last_turn = i
			break
		else:
			map_to_turn_count[new_string] = i
	
	cycle_count = 1000000000 - 1  # 0-indexed
	cycle_length = last_turn - first_turn
	map_number = (cycle_count - first_turn) % cycle_length + first_turn
	for map_string, value in map_to_turn_count.items():
		if value == map_number:
			return destringify(map_string)
	assert False


def destringify(content):
	return [list(row) for row in content.split()]
def stringify(data):
	return "\n".join("".join(t) for t in data)


with open("n-input.txt") as f:
	content = f.read()
	data = destringify(content)
	tilt_north(data)
	print(calculate(data))
	data = destringify(content)
	data = tilt_loop(data)
	print(calculate(data))
