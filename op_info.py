OPS = { # operations assigned to operators
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
}
ADD_OPS = {
    '+': OPS['+'],
    '-': OPS['-'],
}
MUL_OPS = {
    '*': OPS['*'],
    '/': OPS['/'],
}
PARENS = ['(', ')']
PRECEDENCE = {
    '+': 0,
    '-': 0,
    '*': 1,
    '/': 1,
}
