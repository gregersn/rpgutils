import rpgutils


def test_generator():
    monster = rpgutils.character.generate(
        './tests/testmonster.yml', average=True)
    assert monster['CON'] == 65
