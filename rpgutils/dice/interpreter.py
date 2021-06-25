import random
from typing import Union, List
import logging


logger = logging.getLogger(__name__)


INTEGER = 'INTEGER'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
MUL = 'MUL'
DIV = 'DIV'
PLUS = 'PLUS'
MINUS = 'MINUS'
DIE = 'DIE'
EOF = 'EOF'
DICEROLL = 'DICEROLL'
ID = 'ID'
ASSIGN = 'ASSIGN'
LESSTHAN = 'LESSTHAN'
GREATERTHAN = 'GREATERTHAN'
QUESTIONMARK = 'QUESTIONMARK'
COLON = 'COLON'
NEWLINE = 'NEWLINE'


class AST:
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f"<BinOp {self.left} {self.op.value} {self.right}>"


class TernaryOp(AST):
    def __init__(self, condition, first, second):
        self.condition = condition
        self.first = first
        self.second = second


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self) -> str:
        return f"<Num {self.value}>"


class DiceRoll(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"<DiceRoll {self.value}>"


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

    def __repr__(self) -> str:
        return f"<UnaryOp {self.op.value} {self.expr}>"


class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f"<Assign {self.left} {self.right}>"


class Token:
    def __init__(self, _type, value):
        self._type = _type
        self.value = value

    @property
    def type(self):
        return self._type

    def __repr__(self):
        return f"<Token {self._type}: {self.value}>"


class Lexer:
    def __init__(self, command: str):
        self.text = command
        self.pos = 0
        self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace() and self.current_char != '\n':
            self.advance()

    def number(self) -> Token:
        result: str = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char is not None and self.current_char.lower() == 'd' and self.peek().isdigit():
            result += self.current_char
            self.advance()

            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

            return Token('DICEROLL', result.upper())

        return Token('INTEGER', int(result))

    def peek(self):
        peekpos = self.pos + 1
        if peekpos > len(self.text) - 1:
            return None
        return self.text[peekpos]

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        logging.warning(f"Found id: {result}")
        return Token(ID, result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace() and self.current_char != '\n':
                self.skip_whitespace()
                continue

            if self.current_char.lower() == 'd' and self.peek().isdigit():
                return self.number()

            if self.current_char.isalpha():
                return self._id()

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '>':
                self.advance()
                return Token(GREATERTHAN, '>')

            if self.current_char == '<':
                self.advance()
                return Token(LESSTHAN, '<')

            if self.current_char == ':':
                self.advance()
                return Token(ASSIGN, ':')

            if self.current_char == '\n':
                self.advance()
                return Token(NEWLINE, '\n')

            raise Exception(f"Unexpected char {self.current_char}")


class Parser:
    lexer: Lexer
    current_token: Union[Token, None]

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token is not None and self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            if self.current_token is not None:
                self.error(
                    f"Wrong token type: {self.current_token.type}, expected {token_type}")
            else:
                self.error(f"Token underrun.")

    def error(self, msg=''):
        raise Exception(f"Parsing error {msg}")

    def term(self):
        # term: factor((MUL | DIV) factor)*

        node = self.factor()

        while self.current_token is not None and self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def factor(self):
        # factor (PLUS|MINUS) factor | INTEGER | DICEROLL | LPAREN expr RPAREN | variable

        token = self.current_token

        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == DICEROLL:
            self.eat(DICEROLL)
            return DiceRoll(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            node = self.variable()
            return node

    def variable(self):
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def expr(self):
        # expr: term ((PLUS|MINUS) term)*
        node = self.term()

        while self.current_token is not None and self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())
        return node

    def condition(self):

    def conditional(self):
        # conditional: condition QUESTIONMARK expr COLON expr
        node = self.condition()

        if self.current_token is not None and self.current_token == QUESTIONMARK:
            self.eat(QUESTIONMARK)
            first = self.expr()
            self.eat(COLON)
            second = self.expr()

            ternary = TernaryOp(condition=node, first=first, second=second)
            return ternary

        return node

    def declarations(self):
        # declaration: ID: conditional|expr NEWLINE
        decls = []
        while self.current_token is not None and self.current_token.type == ID:
            id = self.current_token
            self.eat(ID)
            token = self.current_token
            self.eat(ASSIGN)
            expr = self.expr()
            self.eat(NEWLINE)

            decls.append(Assign(id, token, expr))

        return decls

    def parse(self):
        return self.expr()


class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')


class Interpreter(NodeVisitor):
    parser: Parser
    average: bool
    tree: Union[AST, List, None]

    def __init__(self, parser):
        self.parser = parser
        self.average = False
        self.tree = None
        self.variables = {}

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)

        if node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)

        if node.op.type == DIV:
            return self.visit(node.left) // self.visit(node.right)

        raise NotImplementedError(f"Unknown BinOp {node.op.type}")

    def visit_DiceRoll(self, node):
        v = node.value.split('D')
        multiplier = int(v[0]) if v[0].isdigit() else 1
        dice_size = int(v[1])

        if self.average:
            return multiplier * (dice_size + 1) / 2
        else:
            return sum([random.randint(1, dice_size) for _ in range(multiplier)])

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        if node.op.value == '-':
            return -self.visit(node.expr)
        return self.visit(node.expr)

    def visit_Var(self, node):
        var_name = node.value
        val = self.variables.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def visit_Assign(self, node: Assign):
        var_name = node.left.value
        self.variables[var_name] = self.visit(node.right)

    def interpret(self, average=False):
        self.average = average
        if self.tree is None:
            self.tree = self.parser.declarations()
        if isinstance(self.tree, list):
            for v in self.tree:
                self.visit(v)
        else:
            return self.visit(self.tree)


class StringVisitor(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.tree = None
        self.average = False

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            left_result, left_repr = self.visit(node.left)
            right_result, right_repr = self.visit(node.right)
            result = left_result + right_result
            return result, f"{left_repr} + {right_repr}"

        if node.op.type == MUL:
            left_result, left_repr = self.visit(node.left)
            right_result, right_repr = self.visit(node.right)
            result = left_result * right_result
            if isinstance(node.left, BinOp):
                if node.left.op.type == PLUS:
                    left_repr = f"({left_repr})"
            return result, f"{left_repr} * {right_repr}"

        raise NotImplementedError(f"Unknown BinOp {node.op.type}")

    def visit_Num(self, node):
        return node.value, str(node.value)

    def visit_UnaryOp(self, node):
        res, repr = self.visit(node.expr)
        if node.op.value == '-':
            return -res, f"-{repr}"
        return res, f"{repr}"

    def visit_DiceRoll(self, node):
        v = node.value.split('D')
        multiplier = int(v[0]) if v[0].isdigit() else 1
        dice_size = int(v[1])

        if self.average:
            # return multiplier * (dice_size + 1) / 2
            avg = (dice_size + 1) / 2
            if multiplier > 1:
                return multiplier * avg, f"{node.value} [{multiplier} * {avg}]"
            return multiplier * avg, f"{node.value} [{avg}]"
        else:
            results = [random.randint(1, dice_size) for _ in range(multiplier)]
            s_results = [f'{r}' for r in results]
            return sum(results), f"{node.value} [{' + '.join(s_results)}]"

    def interpret(self, average=False):
        self.average = average
        if self.tree is None:
            self.tree = self.parser.parse()
        if isinstance(self.tree, list):
            for v in self.tree:
                self.visit(v)
        else:
            return self.visit(self.tree)


def roller(cmd: str):
    lexer = Lexer(cmd)
    parser = Parser(lexer)
    interpreter = StringVisitor(parser)
    return interpreter.interpret


def roll(cmd: str, average: bool = False):
    r = roller(cmd)
    return r(average=average)


def main():
    lexer = Lexer("(3d6 + 6) * 5 + - - 10 + -D5")

    n = lexer.get_next_token()
    while n is not None:
        print(n)
        n = lexer.get_next_token()

    lexer = Lexer("(3d6 + 6) * 5 + - - 10 + -D5")
    parser = Parser(lexer)

    print(parser.parse())

    lexer = Lexer("d20")
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    print(interpreter.interpret())
    print(interpreter.interpret(average=True))

    lexer = Lexer("(3d6 + 6) * 5 + - - 10 + -D5")
    parser = Parser(lexer)
    interpreter = StringVisitor(parser)
    print(interpreter.interpret())
    print(interpreter.interpret(average=True))


if __name__ == '__main__':
    main()
