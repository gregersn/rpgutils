import context
import rpgutils


def test_app(capsys, example_fixture):
    # pylint disable=W0612,W0613

    rpgutils.NameGenerator.run()
    captured = capsys.readouterr()

    assert "My name is MUD" in captured.out


def test_name_base(capsys):
    base = rpgutils.NameBase('./data/PersonerProsentGutter.csv')
    name = base.get_random(1920)
    assert base.count > 1
    assert name == 'anne', name
