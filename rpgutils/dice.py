import re
import random
from typing import Dict, List


class Die():
    count: int
    sides: int
    modifier: int

    def __init__(self, sides: int, count: int = 1, modifier: int = 0):
        self.count = count
        self.sides = sides
        self.modifier = modifier

    def __str__(self):
        modifier = ''
        if self.modifier != 0:
            modifier = f'{"+" if self.modifier > 0 else "-"}{abs(self.modifier)}'
        return f'{self.count}D{self.sides}{modifier}'

    def roll(self):
        total = self.modifier
        for i in range(self.count):
            total += random.randint(1, self.sides)
        return total


class Roll():
    _advantage: int
    _disadvantage: int
    _dice: List[Die]

    def __init__(self):
        self._advantage = 0
        self._disadvantage = 0
        self._dice = []

    def __str__(self):
        return " ".join([self.dice(), "giving", str(self.roll())])

    def roll(self):
        return sum(d.roll() for d in self._dice)

    def advantage(self):
        self._advantage += 1

    def disadvantage(self):
        self._disadvantage += 1

    def add_die(self, sides: int, amount: int = 1, modifier: int = 0):
        self._dice.append(Die(sides, amount, modifier))

    def dice(self) -> str:
        return ' '.join(str(die) for die in self._dice)

    def count(self) -> int:
        return len(self._dice)


DICE_MATCH = r'(\d+)?d(\d+)([\+\-]\d+)?'


def roll(commands: str = ""):
    tokens = commands.split(" ")

    roll = Roll()
    for tok in tokens:
        if tok == '+':
            roll.advantage()
            continue

        if tok == '-':
            roll.disadvantage()
            continue

        match = re.match(DICE_MATCH, tok)
        if match:
            quantity = int(match.group(1)) if match.group(1) else 1
            die = int(match.group(2)) if match.group(2) else 0
            modifier = int(match.group(3)) if match.group(3) else 0
            roll.add_die(die, quantity, modifier)

    if roll.count() < 1:
        roll.add_die(100)

    return roll


def main():
    print(roll())
    print(roll("d20"))
    print(roll("3d6"))
    print(roll("+"))
    print(roll("-"))
    print(roll("d4+1"))


if __name__ == '__main__':
    main()
