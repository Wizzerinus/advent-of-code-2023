def do_hash(w):
	value = 0
	for char in w:
		value = 17 * (value + ord(char)) % 256
	return value


def hashmap(words):
	boxes = [{} for _ in range(256)]
	for w in words:
		box, rem, _ = w.partition("-")
		box, eq, val = box.partition("=")
		box_num = do_hash(box)
		if rem:
			boxes[box_num].pop(box, None)
		else:
			boxes[box_num][box] = int(val)
	return boxes


with open("o-input.txt") as f:
	words = f.read().strip().split(",")
	print(sum(do_hash(w) for w in words))
	boxes = hashmap(words)
	print(
		sum(
			(1 + box) * (1 + slot) * length
			for box, items in enumerate(boxes)
			for slot, length in enumerate(items.values())
		)
	)
