def find_directed_loop(data, vpos, hpos, start_vpos, start_hpos, shift, current_loop):
	while True:  # python does not support tail recursion lmao
		current_loop.append((vpos, hpos, data[vpos][hpos]))
		vpos += shift[0]
		hpos += shift[1]
		if (vpos, hpos) == (start_vpos, start_hpos):
			return current_loop
		if vpos >= len(data) or hpos >= len(data[0]) or vpos < 0 or hpos < 0:
			return None
		
		next_item = data[vpos][hpos]
		if next_item in ("|", "-"):
			pass  # We continue going in the same direction
		elif next_item in ("L", "7"):  # we change direction
			shift = (shift[1], shift[0])
		elif next_item in ("F", "J"):
			shift = (-shift[1], -shift[0])
		else:
			return None


def find_loop(data):
	for row_idx, row in enumerate(data):
		if "S" in row:
			vpos = row_idx
			hpos = row.index("S")
			break
	
	shifts = [(0, 1), (0, -1), (1, 0), (-1, 0)]
	available_shifts = {}
	for shift in shifts:
		loop = find_directed_loop(data, vpos, hpos, vpos, hpos, shift, [])
		if loop:
			return loop


def kitten_qualifies(loop, i, j):
	possible_connections = [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]
	top, left, down, right = [loop.get(t) for t in possible_connections]
	# We still need to check that they actually connect to S because may be like
	# F---7
	# L7S-J
	#  LJ 
	# and only two of them connect but all 4 are in the loop
	left = left in ("L", "F", "-")
	right = right in ("7", "J", "-")
	top = top in ("7", "F", "|")
	down = down in ("L", "J", "|")
	assert left + right + top + down == 2
	return down


def find_area_inside(height, width, loop):
	loop = {(i, j): k for i, j, k in loop}
	kitten_good = None
	for (i, j), k in loop.items():
		if k == "S":
			kitten_good = kitten_qualifies(loop, i, j)
	assert kitten_good is not None
	total = 0
	for i in range(height):
		for j in range(width):
			if (i, j) in loop:
				continue
			
			symbol_count = 0
			for k in range(width - j):
				cur_sym = loop.get((i, j + k))
				if cur_sym in ("|", "F", "7"):
					symbol_count += 1
				elif cur_sym == "S" and kitten_good:
					symbol_count += 1
			if symbol_count % 2:
				total += 1
	return total


with open("j-input.txt") as f:
	data = f.readlines()
	loop = find_loop(data)
	print((len(loop) + 1) // 2)
	# we subtract one because there is the newline symbol
	print(find_area_inside(len(data), len(data[0]) - 1, loop))
