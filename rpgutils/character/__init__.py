import yaml
import dataclasses
from rpgutils.dice.interpreter import roller
from typing import Dict


def dict2rules(d: Dict[str, str]):
    t = []
    for k, v in d.items():
        t.append(f"{k}: {v}")

    return "\n".join(t)


class Generator:
    def __init__(self, rules):
        self.rules = rules

    def generate(self, average: bool = False):
        stats = {

        }
        r = roller(dict2rules(self.rules['stats']))
        return stats


def generate(filename: str, average: bool = False):
    with open(filename, 'r') as f:
        rules = yaml.safe_load(f)
    generator = Generator(rules)
    return generator.generate(average=average)
