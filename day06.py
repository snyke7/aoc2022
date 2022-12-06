def find_marker_index(packet, num_distinct=4):
    for i in range(len(packet) - num_distinct):
        if len(set(packet[i:i+num_distinct])) == num_distinct:
            return i + num_distinct


def main():
    with open('input/day06_input.txt') as f:
        packet = ''.join(f.readlines()).strip()
    print(find_marker_index('mjqjpqmgbljsphdztnvjfqwrcgsmlb'))
    print(find_marker_index('bvwbjplbgvbhsrlpgdmjqwftvncz'))
    print(find_marker_index('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'))
    print(find_marker_index(packet))
    print()
    print(find_marker_index('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14))
    print(find_marker_index('bvwbjplbgvbhsrlpgdmjqwftvncz', 14))
    print(find_marker_index('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 14))
    print(find_marker_index(packet, 14))


if __name__ == '__main__':
    main()
