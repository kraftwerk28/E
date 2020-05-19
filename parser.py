import sys
from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, List

from lexer import L, Lexer


# Node kind
class N(Enum):
    PROGRAM = auto()
    EMPTY = auto()
    EXPR = auto()
    CONST = auto()
    LET = auto()
    IF = auto()
    RANGE = auto()
    FUNC_DECL = auto()
    FUNC = auto()
    ATOM = auto()
    ID = auto()


class Node:
    kind: N
    ops: List[Any]

    def __init__(self, kind, *args):
        self.kind = kind
        self.ops = list(args)

    def __str__(self):
        return self.__repr__()

    def __repr__(self, indent=0):
        ops = ', '.join(repr(op) for op in self.ops if op)
        return f'{self.kind}: ({ops})'


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    def fail(self, reason):
        print('Parser error:', reason)
        self.lexer.line_report()

    def expect(self, kind: L) -> (L, Any):
        v = self.lexer.next_token()
        if v[0] != kind:
            self.fail(f'Unexpected token: {v[v]}. Expected {kind}')
        return v

    def nt(self): return self.lexer.next_token()

    def expr(self):
        kind, value = self.nt()
        if kind == L.ID:
            k2, v2 = self.nt()
            # Assignments
            if k2 == L.CONST_ASS:
                return Node(N.CONST, value, self.expr())
            elif k2 == L.LET_ASS:
                return Node(N.LET, value, self.expr())
            elif k2 == L.FUNC_DECL:
                return self.func_decl(value)
            else:
                return self.funcall(value, (k2, v2))

        elif kind == L.BL:
            return self.paren_expr()

        else:
            self.fail(f'Unexpected token inside expression: {kind}')

    def funcall(self, funcname, first_arg):
        args = []
        kind, value = first_arg
        while True:
            if L.isatom(kind):
                n = Node(N.ATOM, kind, value)
            elif kind == L.ID:
                n = Node(N.ID, value)
            elif kind == L.BL:
                n = self.paren_expr()
            elif kind == L.TERM:
                break
            else:
                self.fail(f'Unexpected token inside function call: {kind}')
                break
            kind, value = self.nt()
            args.append(n)
        return Node(N.FUNC, funcname, args)

    def func_decl(self, funcname: str):
        arg = self.nt()
        argnames = []
        while arg[0] == L.ID:
            argnames.append(arg[1])
            arg = self.nt()
        if arg[0] != L.FUNC_ARROW:
            self.fail('Expected function arrow after argument list')
        return Node(N.FUNC_DECL, funcname, argnames, self.expr())

    def paren_expr(self):
        self.nt()
        e = self.expr()
        self.expect(L.BR)
        return e

    def operation(self):
        pass

    def if_else(self):
        pass

    def assignment(self):
        id = self.nt()

    def parse(self) -> Node:
        # self.lexer.next_token()
        statements = []
        n = Node(N.PROGRAM, self.expr())
        return n


if __name__ == '__main__':
    lex = Lexer(
        sys.argv[1] if len(sys.argv) > 1 else 'code-samples/hello-world.xp'
    )
    parser = Parser(lex)
    ast = parser.parse()
    print(ast)
