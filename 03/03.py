from dataclasses import dataclass
from functools import reduce
from itertools import repeat
from operator import or_
from typing import Iterable, Pattern

import regex

re_number = regex.compile(r"\d+")
re_symbol = regex.compile(r"[^.\d]")
re_gear = regex.compile(r"\*")


class Number:
    def __init__(self, value: int, first_column: int, last_column: int, row: int):
        self.value = value
        self.coords = frozenset(zip(range(first_column, last_column), repeat(row)))

    def __eq__(self, other: "Number"):
        return self.coords == other.coords

    def __hash__(self):
        return hash(self.coords)


@dataclass(frozen=True)
class Symbol:
    column: int
    row: int

    @property
    def coord(self):
        return self.column, self.row


@dataclass
class ParsedGrid:
    numbers: set[Number]
    symbols: set[Symbol]

    def __or__(self, other: "ParsedGrid"):
        return ParsedGrid(self.numbers | other.numbers, self.symbols | other.symbols)


def is_adjacent(number: Number, symbol: Symbol) -> bool:
    return any(abs(symbol.column - coord[0]) <= 1 and abs(symbol.row - coord[1]) <= 1 for coord in number.coords)


def parse_line(line: str, row_number: int, symbol_regex: Pattern[str]) -> ParsedGrid:
    line = line.strip()
    return ParsedGrid({Number(int(match.group()), match.start(), match.end(), row_number)
                       for match in regex.finditer(re_number, line)},
                      {Symbol(match.start(), row_number)
                       for match in regex.finditer(symbol_regex, line)})


def parse_grid(grid: Iterable[str], symbol_regex: Pattern[str]) -> ParsedGrid:
    return reduce(or_,
                  (parse_line(line, row_number, symbol_regex)
                   for row_number, line in enumerate(grid)),
                  ParsedGrid(set(), set()))


def part_numbers(raw_grid: Iterable[str]) -> list[Number]:
    grid = parse_grid(raw_grid, re_symbol)
    return [number for number in grid.numbers
            if any(is_adjacent(number, symbol) for symbol in grid.symbols)]


def sum_numbers(nums: Iterable[Number]) -> int:
    return sum(number.value for number in nums)


def gear_ratios(raw_grid: Iterable[str]) -> list[int]:
    grid = parse_grid(raw_grid, re_gear)
    ratios = []
    for potential_gear in grid.symbols:
        numbers = [number for number in grid.numbers if is_adjacent(number, potential_gear)]
        if len(numbers) == 2:
            ratios.append(numbers[0].value * numbers[1].value)
    return ratios


if __name__ == '__main__':
    with open("input.txt") as f:
        # print(sum_numbers(part_numbers(f)))
        print(sum(gear_ratios(f)))
