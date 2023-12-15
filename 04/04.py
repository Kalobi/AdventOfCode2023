from dataclasses import dataclass
import regex


@dataclass
class Card:
    winning: frozenset[int]
    mine: frozenset[int]

    def points(self):
        winners = len(self.winning & self.mine)
        return 2 ** (winners - 1) if winners >= 1 else 0


def parse_card(card: str) -> Card:
    winning_raw, _, mine_raw = card[card.index(":"):].partition("|")
    return Card(frozenset(int(match) for match in regex.findall(r"\d+", winning_raw)),
                frozenset(int(match) for match in regex.findall(r"\d+", mine_raw)))


if __name__ == '__main__':
    with open("input.txt") as f:
        raw_cards = f.read().splitlines()
    cards = [parse_card(card) for card in raw_cards]
    print(sum(card.points() for card in cards))
