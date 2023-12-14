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


def valid_games_total_id(games):
    return sum(int(game.partition(": ")[0].removeprefix("Game ")) for game in games if is_game_valid(game, bag))


def minimum_bag(game: str):
    parsed = parse_game(game)
    bag = {}
    for subgame in parsed:
        for color, count in subgame.items():
            if color not in bag or bag[color] < count:
                bag[color] = count
    return bag


def power(bag: dict):
    return bag.get("red", 0) * bag.get("green", 0) * bag.get("blue", 0)


def total_minimum_power(games):
    return sum(power(minimum_bag(game)) for game in games)


if __name__ == '__main__':
    total = 0
    bag = {"red": 12, "green": 13, "blue": 14}
    with open("input.txt") as f:
        print(total_minimum_power(f))
