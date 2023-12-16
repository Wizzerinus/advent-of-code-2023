def interact(cell, dx, dy):
	match cell:
		# empty
		case ".":
			return [(dx, dy)]
		# mirrors
		case "/":
			# up (dy = -1) is now right (dx = 1)
			return [(-dy, -dx)]
		case "\\":
			# up (dy = -1) is now left (dy = -1)
			return [(dy, dx)]
		# splitters
		case "-":
			# right = (1, 0) remains as is, down = (0, 1) turns into (1, 0) and (-1, 0)
			return [(dx + dy, 0), (dx - dy, 0)]
		case "|":
			return [(0, dy + dx), (0, dy - dx)]


def calculate_beams(board, starting_cell):
	existing_beams = set()
	energized_cells = set()
	# (1, 0) = right facing, (0, 0) = top left currently
	beam_heads = [starting_cell]
	while beam_heads:
		new_heads = []
		for beam in beam_heads:
			if beam in existing_beams:
				continue
			existing_beams.add(beam)

			dx, dy, x, y = beam
			if x < 0 or y < 0:
				continue
			try:
				current_cell = board[y][x]
			except IndexError:
				continue
			energized_cells.add((x, y))
			
			shifts = interact(current_cell, dx, dy)
			for dx, dy in shifts:
				new_heads.append((dx, dy, x + dx, y + dy))
		beam_heads = new_heads
	
	return len(energized_cells)


def get_maximum_board(board):
	width = len(board[0])
	height = len(board)
	return max(
		*[calculate_beams(board, (1, 0, 0, t)) for t in range(height)],
		*[calculate_beams(board, (-1, 0, width - 1, t)) for t in range(height)],
		*[calculate_beams(board, (0, 1, t, 0)) for t in range(width)],
		*[calculate_beams(board, (0, -1, t, height - 1)) for t in range(width)],
	)


with open("p-input.txt") as f:
	board = [x.strip() for x in f.readlines()]
	print(calculate_beams(board, (1, 0, 0, 0)))
	print(get_maximum_board(board))
