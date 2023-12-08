letter_order = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
letter_dict = dict([(u, v) for v, u in enumerate(letter_order)])
letter_order_2 = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]
letter_dict_2 = dict([(u, v) for v, u in enumerate(letter_order_2)])


def parse_hand_first(line):
    letters = list(line)
    letters = [letter_dict[t] for t in letters]
    hand = sorted(letters, key=lambda t: letters.count(t))
    # The reason this works is because the evaluation works as follows (and is sorted)
    # 5-of-a-kind - (5, -1) 4-of-akind - (4, -2) FH- (3, -2) 3-of-akind - (3, -3)
    # two pairs - (2, -3) pair - (2, -4) all different - (1, -5)
    return (letters.count(hand[-1]), -len(set(letters)), letters)


def parse_hand_second(line):
    letters = list(line)
    letters = [letter_dict_2[t] for t in letters]
    hand = sorted(letters, key=lambda t: letters.count(t) if t != 0 else -100)
    # So the reason this works is it is strictly optimal to reveal J as the card you have most copies of in hand
    # (other than J itself), and we need to do the -1 check below in case the hand is JJJJJ
    max_card_count = letters.count(hand[-1]) + (letters.count(0) if hand[-1] != 0 else 0)
    distinct_count = len(set(letters) - {0}) + (hand[-1] == 0)
    return (max_card_count, -distinct_count, letters)


def make_hand(line, sorter):
    hand, cost = line.strip().split()
    cost = int(cost)
    hand = sorter(hand)
    return hand, cost


def solve(lines, sorter):
    hands = [make_hand(line, sorter) for line in lines]
    hands = sorted(hands)
    return sum((idx + 1) * hand[1] for idx, hand in enumerate(hands))


with open("g-input.txt") as f:
    lines = f.readlines()
    print(solve(lines, parse_hand_first))
    print(solve(lines, parse_hand_second))
