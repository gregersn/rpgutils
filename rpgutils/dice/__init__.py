import re
import random
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class Result:
    total: int
    rolls: List[int]
    modifier: int

    def __str__(self):
        modifier = ''
        if self.modifier != 0:
            modifier = f'{" + " if self.modifier > 0 else " - "}{abs(self.modifier)}'

        if len(self.rolls) > 1:
            return f"({' + '.join(str(r) for r in self.rolls)}){modifier} = {self.total}"

        if self.modifier != 0:
            return f"{self.rolls[0]}{modifier} = {self.total}"

        return f"{self.total}"


class Die():
    sides: int

    def __init__(self, sides: int):
        self.sides = sides

    def __str__(self):
        return f"D{self.sides}"

    def __int__(self):
        return random.randint(1, self.sides)


class Roll():
    count: int
    die: Die
    modifier: int

    def __init__(self, die: Die, count: int = 1,  modifier:  int = 0):
        self.count = count
        self.die = die
        self.modifier = modifier

    def __str__(self):
        modifier = ''
        if self.modifier != 0:
            modifier = f'{"+" if self.modifier > 0 else "-"}{abs(self.modifier)}'
        return f'{self.count}D{self.die.sides}{modifier}'

    def __int__(self):
        return sum([int(self.die) for _ in range(self.count)]) + self.modifier

    def roll(self) -> Result:
        rolls = [random.randint(1, self.die.sides) for i in range(self.count)]
        total = self.modifier + sum(rolls)

        return Result(total, rolls, self.modifier)


class Roller():
    _advantage: int
    _disadvantage: int
    _dice: List[Roll]

    def __init__(self):
        self._advantage = 0
        self._disadvantage = 0
        self._dice = []

    def __str__(self):
        return " ".join([self.dice(), "giving", ", ".join(self.roll())])

    def roll(self):
        results = [str(d.roll()) for d in self._dice]
        return results

    def advantage(self):
        self._advantage += 1

    def disadvantage(self):
        self._disadvantage += 1

    def add_die(self, sides: int, amount: int = 1, modifier: int = 0):
        self._dice.append(Roll(Die(sides), amount, modifier))

    def dice(self) -> str:
        return ' '.join(str(die) for die in self._dice)

    def count(self) -> int:
        return len(self._dice)


DICE_MATCH = r'(\d+)?[dD](\d+)([\+\-]\d+)?'


def roll(commands: str = ""):
    tokens = commands.split(" ")

    roll = Roller()
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

            if quantity > 100:
                return "too many dice!"
            roll.add_die(die, quantity, modifier)

    if roll.count() < 1:
        roll.add_die(100)

    return roll


def main():
    print(roll())
    print(roll("d20"))
    print(roll("3d6"))
    print(roll("1d6+3 1d20"))
    print(roll("+"))
    print(roll("-"))
    print(roll("d4+1"))
    print(roll("100d4"))
    print(roll("(2D6+6)*5"))


if __name__ == '__main__':
    main()
