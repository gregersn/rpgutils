from dataclasses import dataclass
from rpgutils.dice import *
from rpgutils.dice.interpreter import roller


class MonsterStats():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def roll(self):
        stats = []
        for k, v in self.__dict__.items():
            roll = roller(v)
            value = roll()
            stats.append(f"{k}: {value[0]}")

        return ", ".join(stats)

    def __str__(self):
        return self.roll()


GHOUL = MonsterStats(STR="(3D6+6)*5", CON="(2D6+6)*5", SIZ="(2D6+6)*5",
                     DEX="(2D6+6)*5", INT="(2D6+6)*5", POW="(2D6+6)*5")


def main():
    print(GHOUL)


if __name__ == '__main__':
    main()
