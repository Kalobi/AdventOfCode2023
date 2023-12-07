from operator import methodcaller

if __name__ == "__main__":
    total = 0
    with open("input.txt") as f:
        for line in f:
            digits = "".join(filter(methodcaller("isdecimal"), line))
            total += int(digits[0] + digits[-1])
    print(total)
