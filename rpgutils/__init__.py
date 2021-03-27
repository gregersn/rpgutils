from .names import NameGenerator
from .names import NameBase
from .dice import roll as diceroll


import click


@click.group()
def run():
    pass


@click.command()
@click.option('--year', default=1920, type=int, help="Year of birth")
@click.option('--gender', default=None, type=click.Choice(['boy', 'girl']), help="Gender of person")
@click.option('--count', default=1, type=int, help="Number of names to output")
def name(year: int, gender: str, count: int):
    generator = NameGenerator()

    for i in range(count):
        name = generator.get_name(gender=gender, year=year)
        print(name)


@click.command()
@click.argument('command', required=False, default='')
def roll(command: str = ''):
    print(diceroll(command))


run.add_command(name)
run.add_command(roll)
