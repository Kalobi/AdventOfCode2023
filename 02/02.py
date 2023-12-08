from operator import methodcaller


def parse_subgame(subgame: str):
    pairs = subgame.split(", ")
    return {color: int(num) for num, color in map(methodcaller("split"), pairs)}


def parse_game(game: str):
    return [parse_subgame(sub) for sub in game.partition(": ")[2].split("; ")]


def is_subgame_valid(subgame: dict, bag: dict):
    return all(bag.get(color, 0) >= count for color, count in subgame.items())


def is_game_valid(game: str, bag: dict):
    return all(is_subgame_valid(subgame, bag) for subgame in parse_game(game))


if __name__ == '__main__':
    total = 0
    bag = {"red": 12, "green": 13, "blue": 14}
    with open("input.txt") as f:
        print(sum(int(line.partition(": ")[0].removeprefix("Game ")) for line in f if is_game_valid(line, bag)))
