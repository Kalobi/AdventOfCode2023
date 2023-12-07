from operator import methodcaller
import regex


forward_regex = regex.compile(raw := r"\d|zero|one|two|three|four|five|six|seven|eight|nine")
backward_regex = regex.compile("(?r)" + raw)


def total_digits(lines):
    total = 0
    for line in lines:
        digits = "".join(filter(methodcaller("isdecimal"), line))
        total += int(digits[0] + digits[-1])
    return total


digit_names = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def translate_digits(name):
    return digit_names.index(name) if name in digit_names else int(name)


def maybe_spelled(lines):
    total = 0
    for line in lines:
        first = regex.search(forward_regex, line)[0]
        last = regex.search(backward_regex, line)[0]
        total += 10*translate_digits(first) + translate_digits(last)
    return total


if __name__ == "__main__":
    total = 0
    with open("input.txt") as f:
        print(maybe_spelled(f))
