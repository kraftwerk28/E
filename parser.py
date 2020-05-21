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
    BRANCH = auto()
    RANGE = auto()
    FUNC_DECL = auto()
    FUNC_CALL = auto()
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

    def __repr__(self):
        ind = lambda s: '\n'.join('\t' + s for s in s.split('\n'))
        ops = '\n'.join(ind(repr(op)) for op in self.ops if op)
        return f'{self.kind} (\n{ops}\n)'


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    def fail(self, reason):
        print('-> Parser error:', reason)
        self.lexer.line_report()
        sys.exit(1)

    def expect(self, *kinds) -> (L, Any):
        v = self.lexer.next_token()
        if v[0] not in kinds:
            exp = ', '.join(str(k) for k in kinds)
            self.fail(f'Unexpected token: {v[0]} ({v[1]}). Expected {exp}')
        return v

    def nt(self): return self.lexer.next_token()
    def ct(self): return self.lexer.tok

    def expr(self):

        kind, value = self.nt()

        if kind == L.COMMENT:
            return self.expr()

        if kind == L.ID or L.isatom(kind):
            k2, v2 = self.nt()

            # Assignments
            if k2 == L.CONST_ASS:
                return Node(N.CONST, value, self.expr())
            elif k2 == L.LET_ASS:
                return Node(N.LET, value, self.expr())
            elif k2 == L.FUNC_DECL:
                return self.func_decl(value)

            elif L.isatom(k2) or k2 in (L.ID, L.BL):
                return self.funcall(value, (k2, v2))
            elif kind == L.ID:
                return Node(N.ID, value)
            else:
                return Node(N.ATOM, value)

        elif kind == L.BL:
            return self.paren_expr()

        elif kind == L.IF:
            return self.if_else()

        elif kind in (L.EOF,):
            return Node(N.EMPTY)

        else:
            self.fail(f'Unexpected token inside expression: {kind}')

    def funcall(self, funcname, first_arg):
        args = []
        kind, value = first_arg
        while True:
            n = None
            if kind in (L.TERM, L.BR, L.THEN, L.EOF):
                break
            elif L.isatom(kind):
                n = Node(N.ATOM, value)
            elif kind == L.ID:
                n = Node(N.ID, value)
            elif kind in (L.BL,):
                n = self.expr()
            else:
                self.fail(f'Unexpected token inside function call: {kind}')
            args.append(n)
            kind, value = self.nt()

        return Node(N.FUNC_CALL, funcname, args)

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
        e = self.expr()
        if self.ct()[0] != L.BR:
            self.fail(f'Expected L.BR. Instead got {self.ct()}')
        return e

    def operation(self):
        pass

    def if_else(self):
        cond = self.expr()
        self.expect(L.THEN)
        then = self.expr()
        self.expect(L.ELSE)
        els = self.expr()
        return Node(N.BRANCH, cond, then, els)

    def assignment(self):
        id = self.nt()

    def parse(self) -> Node:
        # self.lexer.next_token()
        statements = []
        while True:
            current_kind, _ = self.ct()
            if current_kind == L.EOF: break
            statements.append(self.expr())
        return Node(N.PROGRAM, *statements)
        # return Node(N.PROGRAM, self.expr())


if __name__ == '__main__':
    lex = Lexer(
        sys.argv[1] if len(sys.argv) > 1 else 'code-samples/hello-world.xp'
    )
    parser = Parser(lex)
    ast = parser.parse()
    print(ast)
