def out(arg):
    print(arg)

def add(*args):
    return args[0] + args[1]

def pred(a): return a - 1

functions = {
    'add': add,
    'out': out,
    'pred': pred,
}
