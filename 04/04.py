from dataclasses import dataclass
import regex


@dataclass
class Card:
    winning: frozenset[int]
    mine: frozenset[int]

    def points(self):
        winners = len(self.winning & self.mine)
        return 2 ** (winners - 1) if winners >= 1 else 0

    def __post_init__(self):
        self.winners = len(self.winning & self.mine)


def parse_card(card: str) -> Card:
    winning_raw, _, mine_raw = card[card.index(":"):].partition("|")
    return Card(frozenset(int(match) for match in regex.findall(r"\d+", winning_raw)),
                frozenset(int(match) for match in regex.findall(r"\d+", mine_raw)))


def total_cards(initial: list[Card]) -> int:
    winnings = {index: card.winners for index, card in enumerate(initial)}
    slots = len(initial)
    new_cards = [1]*slots
    total = 0
    while any(new_cards):
        total += sum(new_cards)
        old_cards = new_cards
        new_cards = [0]*slots
        for pos, count in enumerate(old_cards):
            for i in range(pos + 1, pos + 1 + winnings[pos]):
                if i < slots:
                    new_cards[i] += count
    return total


if __name__ == '__main__':
    with open("input.txt") as f:
        raw_cards = f.read().splitlines()
    cards = [parse_card(card) for card in raw_cards]
    # print(sum(card.points() for card in cards))
    print(total_cards(cards))
