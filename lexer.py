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
    THEN = auto()
    ELIF = auto()

    BL = auto()
    BR = auto()
    COMMENT = auto()
    FUNC_DECL = auto()
    FUNC_ARROW = auto()

    def isatom(kind):
        return kind in (L.FLOAT, L.INT, L.STRING, L.OPERATOR)


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
        self.tok = (None, None)

    def eat(self, amount=1):
        self.char = self.fdescriptor.read(amount)

    def line_report(self):
        pos = self.fdescriptor.tell()
        self.fdescriptor.seek(0)

        print('Line:', self.line)
        while self.line > 1:
            self.line -= 1
            self.fdescriptor.readline()

        line_start = self.fdescriptor.tell()
        report = self.fdescriptor.readline()
        report += ' ' * (pos - line_start - 2) + '^'
        print(report)

    def fail(self, reason):
        print('-> Lexer error:', reason)
        self.line_report()

    def cur_tok(self): return self.tok

    def read_tok(self):
        ch = self.char
        tok = None

        if ch == '\n':
            self.eat()
            self.line += 1
            return self.read_tok()

        if ch == '.':
            self.eat()
            tok = (L.TERM, None)

        elif len(ch) == 0:
            tok = (L.EOF, None)

        elif ch.isdigit():  # integer OR float
            s = ''
            while self.char.isdigit() or self.char == '.':
                s += self.char
                self.eat()
            if '.' in s:
                tok = (L.FLOAT, float(s))
            else:
                tok = (L.INT, int(s))

        elif ch.isspace():  # Pass out extra whitespaces
            self.eat()
            # return self.read_tok()
            tok = self.read_tok()

        elif ch == '"':  # String atom
            s = ''
            self.eat()
            while self.char != '"':
                s += self.char
                self.eat()
            self.eat()
            tok = (L.STRING, s)

        elif ch == '<':  # GT operator OR assignment
            self.eat()
            if self.char == '-':
                self.eat()
                tok = (L.CONST_ASS, None)
            elif self.char == '~':
                self.eat()
                tok = (L.LET_ASS, None)
            else:
                tok = (L.LT, None)

        elif ch == '>':
            self.eat()
            tok = (L.GT, None)

        # Comments processing
        elif ch == '-':
            self.eat()
            if self.char == '{':
                self.eat()
                s = ''
                while self.char != '}':
                    s += self.char
                    self.eat()
                self.eat()
                self.eat() # Eat }-
                tok = (L.COMMENT, s)
            elif self.char == '>':
                self.eat()
                tok = (L.FUNC_ARROW, None)

            else:
                tok = (L.OPERATOR, ch)

        elif ch in self.OPERATORS:
            # TODO: handle // OPERATOR
            self.eat()
            tok = (L.OPERATOR, ch)

        elif ch in self.SYMBOLS:
            self.eat()
            tok = (self.SYMBOLS[ch], None)

        elif ch.isalpha():
            s = ''
            while self.char.isalpha():
                s += self.char
                self.eat()
            tok = (L.ID, s)

        elif ch == '?':  # if-else-expression
            # TODO: handle infinite else expression
            self.eat()
            if self.char == ':':
                self.eat()
                tok = (L.IF, None)
            else:
                tok = (L.ELIF, None)

        elif ch == ':':
            self.eat()
            if self.char == ':':
                tok = (L.FUNC_DECL, None)
            elif self.char == '?':
                tok = (L.ELSE, None)
            self.eat()

        elif ch == '|':
            self.eat()
            tok = (L.THEN, None)

        else:
            self.fail(f'Unexpected character: [{self.char}]')
            return
        self.tok = tok
        return tok

    def next_token(self) -> (L, Any):
        return self.read_tok()


if __name__ == '__main__':
    l = Lexer(sys.argv[1] if len(sys.argv) > 1 else 'code-samples/simple.xp')
    t = (None, None)
    while t[0] != L.EOF:
        t = l.next_token()
        print(t)
