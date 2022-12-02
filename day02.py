def match_result(player1, player2):  # 0 if player2 loses, 1 for a draw, 2 for a win
    index_diff = ((player2 - 1) - (player1 - 1)) % 3  # 1 for a win, 0 for a draw, 2 for a loss
    return (index_diff + 1) % 3


def get_score(player1, player2):
    return match_result(player1, player2) * 3 + player2


def choose_hand(player1, desired_result):
    offset = desired_result - 2
    return (player1 - 1 + offset) % 3 + 1


def main():
    with open('input/day02_input.txt') as f:
        lines = f.readlines()
        matches = [(ord(line.strip()[0]) - ord('A') + 1, ord(line.strip()[2]) - ord('X') + 1) for line in lines]
        print(sum([get_score(*match) for match in matches]))
        print(sum([get_score(match[0], choose_hand(match[0], match[1])) for match in matches]))


if __name__ == '__main__':
    main()
