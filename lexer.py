import sys
from enum import Enum, auto
from typing import Any


class L(Enum):
    EOF = auto()
    SQBL = auto()
    SQBR = auto()
    FLOAT = auto()
    INT = auto()
    STRING = auto()
    OPERATOR = auto()
    CONST_ASS = auto()
    LET_ASS = auto()
    GT = auto()
    LT = auto()
    EQ = auto()
    ID = auto()
    TERM = auto()
    IF = auto()
    ELSE = auto()
    BL = auto()
    BR = auto()
    COMMENT = auto()


class Lexer:
    SYMBOLS = {
        '[': L.SQBL,
        ']': L.SQBR,
        '(': L.BL,
        ')': L.BR,
    }
    OPERATORS = ['+', '-', '*', '/']

    def __init__(self, filename=None):
        self.fdescriptor = open(filename, 'r') if filename else sys.stdin
        self.char = self.fdescriptor.read(1)
        self.sym = None
        self.line = 1

    def eat(self, amount=1):
        self.char = self.fdescriptor.read(amount)

    def fail(self, reason):
        print('-> Lexer error:', reason)

        pos = self.fdescriptor.tell()
        self.fdescriptor.seek(0)

        print('Line:', self.line)
        while self.line > 1:
            self.line -= 1
            self.fdescriptor.readline()

        line_start = self.fdescriptor.tell()
        report = self.fdescriptor.readline()
        report += ' ' * (pos - line_start - 1) + '^'
        print(report)

    def read_tok(self):
        ch = self.char

        if ch == '\n':
            self.eat()
            self.line += 1
            return (L.TERM, None)

        elif len(ch) == 0:
            return (L.EOF, None)

        elif ch.isdigit():  # integer OR float
            s = ''
            while self.char.isdigit() or self.char == '.':
                s += self.char
                self.eat()
            if '.' in s:
                return (L.FLOAT, float(s))
            else:
                return (L.INT, int(s))

        elif ch.isspace():  # Pass out extra whitespaces
            self.eat()
            return self.read_tok()

        elif ch == '"':  # String atom
            s = ''
            self.eat()
            while self.char != '"':
                s += self.char
                self.eat()
            self.eat()
            return (L.STRING, s)

        elif ch == '<':  # GT operator OR assignment
            self.eat()
            if self.char == '-':
                self.eat()
                return (L.CONST_ASS, None)
            elif self.char == '~':
                elf.eat()
                return (L.LET_ASS, None)
            else:
                return (L.LT, None)

        elif ch == '>':
            self.eat()
            return (L.GT, None)

        # Comments processing
        if ch == '-':
            self.eat()
            if self.char == '{':
                self.eat()
                s = ''
                while self.char != '}':
                    s += self.char
                    self.eat()
                self.eat()
                return (L.COMMENT, s)

            else:
                return (L.OPERATOR, ch)

        elif ch in self.OPERATORS:
            # TODO: handle // OPERATOR
            self.eat()
            return (L.OPERATOR, ch)

        elif ch in self.SYMBOLS:
            self.eat()
            return (self.SYMBOLS[ch], None)

        elif ch.isalpha():
            s = ''
            while self.char.isalpha():
                s += self.char
                self.eat()
            return (L.ID, None)

        elif ch == '?':  # if-else-expression
            # TODO: handle infinite else expression
            self.eat()
            if self.char == ':':
                self.eat()
                return (L.IF, None)
            else:
                return (L.ELSE, None)

        else:
            self.fail(f'Unexpected character: [{self.char}]')

    def next_token(self) -> (L, Any):
        return self.read_tok()


if __name__ == '__main__':
    l = Lexer('code-samples/simple.xp')
    t = (None, None)
    while t[0] != L.EOF:
        t = l.next_token()
        print(t)
