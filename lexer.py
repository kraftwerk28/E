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


class Lexer:
    def __init__(self, filename=None):
        self.fdescriptor = open(filename, 'r') if filename else sys.stdin
        self.char = self.fdescriptor.read(1)
        self.sym = None
        self.line = 1

    def read(self):
        self.char = self.fdescriptor.read(1)

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
            self.read()
            self.line += 1
            return (L.TERM, None)

        elif len(ch) == 0:
            return (L.EOF, None)

        elif ch.isdigit():  # integer / float
            s = ''
            while self.char.isdigit() or self.char == '.':
                s += self.char
                self.read()
            if '.' in s:
                return (L.FLOAT, float(s))
            else:
                return (L.INT, int(s))

        elif ch.isspace(): # Pass extra whitespaces
            self.read()
            return self.read_tok()

        elif ch == '"': # String atom
            s = ''
            self.read()
            while self.char != '"':
                s += self.char
                self.read()
            self.read()
            return (L.STRING, s)

        elif ch == '<': # GT operator / assignment
            self.read()
            if self.char == '-':
                self.read()
                return (L.CONST_ASS, None)
            elif self.char == '~':
                self.read()
                return (L.LET_ASS, None)
            else:
                return (L.LT, None)

        elif ch == '>':
            self.read()
            return (L.GT, None)

        elif ch in ('+', '-', '*', '/'):
            # TODO: handle // OPERATOR
            self.read()
            return (L.OPERATOR, ch)

        elif ch == '[':
            self.read()
            return (L.SQBL, None)

        elif ch == ']':
            self.read()
            return (L.SQBR, None)

        elif ch.isalpha():
            s = ''
            while self.char.isalpha():
                s += self.char
                self.read()
            return (L.ID, None)

        elif ch == '?':  # if-expression
            self.read()
            if self.char == ':':
                self.read()
                return (L.IF, None)
            else:
                return (L.ELSE, None)

        else:
            self.fail(f'Unexpected character: [{self.char}]')

    def next_token(self) -> (L, Any):
        # while self.sym == None:
        #     self.read_tok()
        return self.read_tok()

        # return (sym, value)


if __name__ == '__main__':
    l = Lexer('code-samples/simple.xp')
    t = (None, None)
    while t[0] != L.EOF:
        t = l.read_tok()
        print(t)
