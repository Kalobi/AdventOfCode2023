import regex
from functools import reduce
from itertools import product
from collections import Counter

re_number = regex.compile(r"\d+")
re_symbol = regex.compile(r"[^.\d]")


def parse_line(line, index):
    line = line.strip()
    number_positions = {
        ((match.start() - 1, match.end() + 1), index): int(match.group())
        for match in regex.finditer(re_number, line)
    }
    symbol_positions = {(match.start(), index) for match in regex.finditer(re_symbol, line)}
    return number_positions, symbol_positions


def parse_grid(grid):
    return reduce(lambda data, new: (data[0] | new[0], data[1] | new[1]),
                  (parse_line(line, index) for index, line in enumerate(grid)),
                  ({}, set()))


def part_numbers(data):
    return [number for pos_range, number in data[0].items()
            if any(pos in data[1]
                   for pos in product(range(*pos_range[0]),
                                      range(pos_range[1] - 1, pos_range[1] + 2)))]


def part_witnesses(data):
    witnesses = []
    for pos_range, number in data[0].items():
        for pos in product(range(*pos_range[0]),
                           range(pos_range[1] - 1, pos_range[1] + 2)):
            if pos in data[1]:
                witnesses.append((number, (pos_range[0][0] + 1, pos_range[0][1] - 2), pos_range[1], pos))
    return witnesses


def print_invalid_witnesses(witnesses):
    for witness in witnesses:
        if witness[0] == 814:
            print(witness)


if __name__ == '__main__':
    with open("input.txt") as f:
        data = parse_grid(f)
    # print(Counter(part_numbers(data)))
    print_invalid_witnesses(part_witnesses(data))
    nums = part_numbers(data)
    print(sum(nums))
    print(nums)
