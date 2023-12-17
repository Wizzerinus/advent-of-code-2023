import heapq


movement_map = {
    # (dx, dy) -> list of the same things
    (0, 1): [(0, 1), (1, 0), (-1, 0)],
    (0, -1): [(0, -1), (1, 0), (-1, 0)],
    (1, 0): [(0, 1), (1, 0), (0, -1)],
    (-1, 0): [(0, 1), (0, -1), (-1, 0)],
    None: [(0, 1), (1, 0), (0, -1), (-1, 0)],
}

def find_path(board, max_straight, min_turns):
    heap = []
    visited = set()
    heapq.heappush(heap, (0, 0, 0, None, 0, []))
    target = (len(board[0]) - 1, len(board) - 1)
    
    while heap:
        weight, x, y, last_dir, straight_len, path = heapq.heappop(heap)
        if (x, y, last_dir, straight_len) in visited:
            continue
        visited.add((x, y, last_dir, straight_len))
        if (x, y) == target and straight_len >= min_turns:
            return weight
        
        for direction in movement_map[last_dir]:
            if direction == last_dir:
                new_len = straight_len + 1
                if new_len >= max_straight:
                    continue
            else:
                if last_dir is not None and straight_len < min_turns:
                    continue
                new_len = 0
           
            dx, dy = direction
            new_x, new_y = x + dx, y + dy
            if not (0 <= new_x < len(board[0])) or not (0 <= new_y < len(board)):
                continue
            
            new_weight = weight + board[new_y][new_x]
            new_path = path + [(new_x, new_y)]
            heapq.heappush(heap, (new_weight, new_x, new_y, direction, new_len, new_path))


with open("q-input.txt") as f:
    board = [[int(x) for x in y.strip()] for y in f.readlines()]
    print(find_path(board, 3, 0))
    print(find_path(board, 10, 3))
