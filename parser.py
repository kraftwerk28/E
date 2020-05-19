from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, List

from lexer import L, Lexer


class N(Enum):
    PROGRAM = auto()
    EXPR = auto()
    CONST = auto()

@dataclass
class Node:
    kind: N
    value: Any = None
    ops = []


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

    def expr(self):
        pass

    def operation(self):
        pass

    def if_else(self):
        pass

    def assignment(self):
        pass

    def parse(self) -> Node:
        n = Node(N.PROGRAM)
        return n


if __name__ == '__main__':
    lex = Lexer('code-samples/simple.xp')
    parser = Parser(lex)
    print(parser.parse())

