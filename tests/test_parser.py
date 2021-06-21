from rpgutils.dice.interpreter import *


def test_lexer():
    lexer = Lexer("STR: (3d6 + 6) * 5")

    tok = lexer.get_next_token()
    assert tok.type == ID

    tok = lexer.get_next_token()
    assert tok.type == ASSIGN

    tok = lexer.get_next_token()
    assert tok.type == LPAREN

    tok = lexer.get_next_token()
    assert tok.type == DICEROLL

    tok = lexer.get_next_token()
    assert tok.type == PLUS

    tok = lexer.get_next_token()
    assert tok.type == INTEGER

    tok = lexer.get_next_token()
    assert tok.type == RPAREN

    tok = lexer.get_next_token()
    assert tok.type == MUL

    tok = lexer.get_next_token()
    assert tok.type == INTEGER


def test_parser():
    lexer = Lexer("STR: (3d6 + 6) * 5")

    parser = Parser(lexer)

    ast = parser.declarations()
    assert len(ast) == 1

    lexer = Lexer("STR: (3d6 + 6) * 5\nCON: (2d6 + 6) * 5")
    parser = Parser(lexer)

    ast = parser.declarations()
    assert len(ast) == 2

    lexer = Lexer(
        "STR: (3d6 + 6) * 5\nCON: (2d6 + 6) * 5\nFOO: (CON + STR) / 10")
    parser = Parser(lexer)

    ast = parser.declarations()
    assert len(ast) == 3


def test_interpreter():
    lexer = Lexer(
        "STR: (3d6 + 6) * 5\nCON: (2d6 + 6) * 5\nFOO: (CON + STR) / 10")
    parser = Parser(lexer)

    interpreter = Interpreter(parser)

    result = interpreter.interpret(average=True)

    assert interpreter.variables['STR'] == 82.5
    assert interpreter.variables['CON'] == 65.0
    assert interpreter.variables['FOO'] == 14.0
