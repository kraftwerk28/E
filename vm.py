import os
import sys

from std import functions as std_functions
from lexer import Lexer, L
from parser import Parser, N


class VM:
    def __init__(self):
        self.funcs = {**std_functions}
        self.consts = {}
        self.lets = {}

    def fail(self, reason):
        print('-> VM error:', reason)
        sys.exit(1)

    def id(self, n):
        if n in self.consts:
            return self.consts[n]
        if n in self.lets:
            return self.lets[n]
        self.fail(f'Variable not declared: {n}')

    def const(self, ops):
        result, = self.run_op(ops[1])
        self.consts[ops[0]] = result


    def call_func(self, funcname, args):
        if funcname in std_functions:
            return std_functions[funcname](*args)
        if funcname in self.funcs:
            signature, sub_ast = self.funcs[funcname]
            for i, a in enumerate(args):
                self.consts[signature[i]] = a
            return self.run_op(sub_ast)
        self.fail(f'Function not declared: {funcname}')

    def decl_func(self, name, args, expr):
        self.funcs[name] = (args, expr)

    def run_op(self, op):
        kind = op.kind
        ops = op.ops

        if kind == N.FUNC_CALL:
            name, args = op.ops
            a = [self.run_op(a) for a in args]
            return self.call_func(name, a)

        elif kind == N.FUNC_DECL:
            name, args, expr = ops
            self.funcs[name] = (args, expr)

        elif kind == N.ID:
            # if (ops[0] not in self.consts) or (ops[0] not in self.lets):
            #     self.fail(f'Variable {ops[0]} not declared')
            return self.id(ops[0])

        elif kind == N.BRANCH:
            # passed = self.run_op()
            pass

        elif kind == N.ATOM:
            return ops[0]

        elif kind == N.CONST:
            self.const(ops)

        else:
            self.fail(f'Unexpected opcode {kind}')

    def run(self, ast):
        if ast.kind != N.PROGRAM:
            self.fail('Bad AST tree root type')
        for op in ast.ops:
            self.run_op(op)


if __name__ == '__main__':
    lex = Lexer(
        sys.argv[1] if len(sys.argv) > 1 else 'code-samples/hello-world.xp'
    )

    parser = Parser(lex)
    ast = parser.parse()
    print('AST', ast)

    vm = VM()

    print('RESULT: ')
    vm.run(ast)
