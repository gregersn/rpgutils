# RPG Utils

A small utiltiy to do some RPG GMing related tasks.

- Simple dice rolling from command line
- Random Norwegian names based on statistics from SSB.

## Installation

In the source folder, run

`$ pip install .`

## Example usage

To generate a list of 10 names

`$ rpgutils name --count 10`

To roll 3D6

`$ rpgutils roll 3d6`

Run

`$ rpgutils --help`

to get a list of available commands.

## Disclaimer

Altough the name generating tool in its current form is very binary-gendered, this is not a reflection on the authors view about genders, but a product of writing a tool that for the time being meets a specific need to generate more or less typical names for Norway, that fits within those conformities. Its primary use is to generate names for use with the Call of Cthulhu role playing game, with a setting of Norway in the 1920s. Name data up to 2020 is included because it was available.

## Licences

Copyright [Statisics Norway](https://www.ssb.no/):

- `data/PersonerProsentGutter.csv`
- `data/PersonerProsentJenter.csv`

licensed under the [Norwegian Licence for Open Government Data (NLOD) 2.0](https://data.norge.no/nlod/en/2.0/
)

Python code is copyrighted by Greger Stolt Nilsen, and made available
under the GPL3.0-license.
