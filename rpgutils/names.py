import logging
import csv
from typing import List, Dict, Set, Tuple, Union
import random
import pathlib

LOGGER = logging.getLogger(__name__)


DATA_FOLDER = pathlib.Path(__file__).parent.parent.joinpath('data')


class NameList:
    names: List[str]
    weights: List[float]

    def __init__(self):
        self.names = []
        self.weights = []

    def get_random(self):
        return random.choices(self.names, self.weights)[0]

    def add_name(self, name: str, weight: float):
        self.names.append(name)
        self.weights.append(weight)


class NameBase:
    names: Set[str]
    years: Dict[int, NameList]

    def __init__(self, filename: Union[str, pathlib.Path]):
        self.names = set()
        self.years = {}

        assert pathlib.Path(filename).is_file(), filename

        with open(filename, 'r') as f:
            LOGGER.debug(f"Opening database {filename}")
            dialect = csv.Sniffer().sniff(f.read(1024))
            f.seek(0)
            reader = csv.DictReader(f, dialect=dialect)
            LOGGER.debug(f"Reading data")
            for row in reader:
                self.names.add(row['fornavn'])
                year = int(row['år'], 10)
                if year not in self.years:
                    self.years[year] = NameList()

                percent = 0.0
                try:
                    percent = float(row['Andel av fødte (prosent)'])
                except:
                    pass
                self.years[year].add_name(row['fornavn'], percent)

    def get_random(self, year: int) -> str:
        return self.years[year].get_random()

    @ property
    def count(self) -> int:
        return len(self.names)

    @ property
    def range(self) -> Tuple[int, int]:
        years = list(sorted(self.years.keys()))
        return (years[0], years[-1])


class NameGenerator:
    bases: Dict[str, NameBase]

    def __init__(self):
        LOGGER.debug("Init name databases")
        self.bases = {}
        self.bases['boy'] = NameBase(
            DATA_FOLDER.joinpath('PersonerProsentGutter.csv'))
        self.bases['girl'] = NameBase(
            DATA_FOLDER.joinpath('PersonerProsentJenter.csv'))

    def get_name(self, gender: Union[str, None], year: int, surname: bool = False) -> str:
        # If gender is not specified, pick one at random
        if gender is None:
            gender = random.choice(list(self.bases.keys()))

        # Make sure year is within the available range,
        # clip value.
        year = max(self.bases[gender].range[0], year)
        year = min(self.bases[gender].range[1], year)

        # Get a random name for the decided year
        name = self.bases[gender].get_random(year)
        patronym = self.get_patronym(gender, year)
        return f"{gender} born {year} named {name} {patronym}"

    def get_patronym(self, gender: str, year: int, parent_range: Tuple[int, int] = (18, 50)) -> str:
        """Create a patronym with some silly logic."""
        range = self.bases['boy'].range
        parent_year = max(range[0], random.randint(
            year-max(parent_range), year-min(parent_range)))
        name = self.bases['boy'].get_random(parent_year)

        if gender == 'girl':
            return f"{name}sdatter"
        else:
            return f"{name}sen"
