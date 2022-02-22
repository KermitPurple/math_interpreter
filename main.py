#!/usr/bin/env python3

from typing import Iterator
from stack import Stack
from enum import Enum
import sys

class State(Enum):
    '''
    States for token_scanner
    NONE: not currently scanning anything
    NUM: currently scanning a number
    '''
    NONE = 0
    NUM = 1

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

def token_scanner(expr: str) -> Iterator[str | int | float]:
    '''
    takes a string of operators operands and parentheses and splits them, making sure to group correctly
    :expr: str; the expression that will be turned into indivdual tokens
    :returns: iterator of str int and floats
    '''
    state = State.NONE
    expr = expr.strip() + ' ' # add space at end of expr to always send last meaningful character
    start_index = 0 # start index of current group
    num_parse_fn = int # function to parse numbers
    for index, ch in enumerate(expr):
        if state == State.NONE: # no current parse target
            if ch in OPS or ch in PARENS: # yield character if valuable
                yield ch
            elif ch.isnumeric(): # is a number
                # set to start parsing a number
                state = State.NUM
                start_index = index
                num_parse_fn = int
        elif state == State.NUM: # currently parsing number
            if ch == '.': # this means it's a floating point number
                num_parse_fn = float
            elif not ch.isnumeric() and ch != '.': # if the character isn't part of the number
                # number is over set to parsing nothing
                state = State.NONE
                yield num_parse_fn(expr[start_index:index]) # yield number
                if ch in OPS or ch in PARENS: # yield character if valuable
                    yield ch

def parse_prefix(tokens: Iterator[str | int | float]) -> None | int | float:
    '''
    parses a mathmatical expression in prefix format
    e.g. + 1 * 2 3 -> 7
    :tokens: iterator over tokens containing operators, parentheses, and numbers
    :returns: the result of the evaluated tokens; returns None if the expression is invalid
    '''
    def helper() -> None | int | float:
        '''Helper function for parsing tokens'''
        result = next(tokens, None) # get next token
        if isinstance(result, int | float): # if token is a number
            return result # return it
        if result in OPS: # if token is an operator
            a = helper() # get first operand
            b = helper() # get second operand
            if None in [a, b]: # if either of them are None
                return None # fail
            return OPS[result](a, b) # perform the operation
        return None # fail
    result = helper() # evaluate expression
    if next(tokens, None) is not None: # if the iterator isn't empty
        return None # fail
    return result # return evaluated expression

def parse_postfix(tokens: Iterator[str | int | float]) -> None | int | float:
    '''
    parses a mathmatical expression in postfix notation
    e.g. 1 2 3 * + -> 7
    :tokens: iterator over tokens containing operators, parentheses, and numbers
    :returns: the result of the evaluated tokens; returns None if the expression is invalid
    '''
    operands = Stack() # store stack for operands
    for token in tokens: # cycle over tokens
        if isinstance(token, int | float): # if token is number
            operands.push(token) # add it to operands
        elif token in OPS: # if the token is an operator
            if len(operands) < 2: # if there aren't enough operands
                return None # fail
            b, a = (operands.pop() for _ in range(2)) # get operands
            operands.push(OPS[token](a, b)) # perform operation
        else:
            return None # fail
    if len(operands) == 1: # if only one remaining
        return operands.pop() # return result
    else:
        return None # fail

def parse_paren_infix(tokens: Iterator[str | int | float]) -> None | int | float:
    '''
    parses a mathmatical expression in infix notation using parenthesis
    e.g. (1 + (2 * 3)) -> 7
    :tokens: iterator over tokens containing operators, parentheses, and numbers
    :returns: the result of the evaluated tokens; returns None if the expression is invalid
    '''
    def helper() -> None | int | float:
        '''Helper function for parsing tokens'''
        result = next(tokens, None) # get next token
        if isinstance(result, int | float): # if it's an number
            return result # return it
        if result == '(': # if it's an opening paren
            a = helper() # get first operand
            op = next(tokens, None) # get operator
            b = helper() # get second operand
            if next(tokens, None) != ')' or None in [a, op, b]: # if not missing anything
                return None # fail
            return OPS[op](a, b) # perform operation
        return None # fail
    result = helper() # evaluate expression
    if next(tokens, None) is not None: # if the iterator isn't empty
        return None # fail
    return result # return evaluated expression

def parse_infix(tokens: Iterator[str | int | float]) -> None | int | float:
    '''
    parses a mathmatical expression in infix notation using optional parenthesis
    e.g. 1 + 2 * 3 -> 7
    e.g. (1 + 2) * 3 -> 9
    :tokens: iterator over tokens containing operators, parentheses, and numbers
    :returns: the result of the evaluated tokens; returns None if the expression is invalid
    '''
    def helper(a: None | float | int = None) -> None | int | float:
        if a is None:
            a = next(tokens, None)
        if a is None:
            return None
        elif a == '(':
            a = helper()
        op = next(tokens, None)
        if op is None or op == ')':
            return a
        if op in ADD_OPS:
            b = helper()
        if op in MUL_OPS:
            b = next(tokens, None)
        if not isinstance(b, int | float):
            return None
        result = OPS[op](a, b)
        if op in ADD_OPS:
            return result
        elif op in MUL_OPS:
            return helper(result)
    result = helper() # evaluate expression
    if next(tokens, None) is not None: # if the iterator isn't empty
        return None # fail
    return result # return evaluated expression

def get_int(prompt: str, min_value: int, max_value: int) -> int:
    '''
    prompt user for input for a number between {min_value} and {max_value}
    will loop until user enters an ok response
    :prompt: prompt to show every loop
    :min_value: smallest accepted value
    :max_value: greatest accepted value
    :returns: a value >= min_value and <= max_value chosen by the user and parsed using int
    '''
    while 1:
        num = input(f'{prompt}\nEnter an integer between {min_value} and {max_value}> ')
        try:
            num = int(num)
        except ValueError:
            print('The input could not be converted to an integer\n')
            continue
        if num < min_value:
            print(f'The input is not allowed to be less than {min_value}')
            continue
        elif num > max_value:
            print(f'The input is not allowed to be more than {max_value}')
            continue
        return num

def main():
    '''Driver Code'''
    while 1:
        choice = get_int(
            '''What kind of mathmatical expressions do you want to parse?
1) prefix                e.g. + 1 * 2 3
2) postfix               e.g. 1 2 3 * +
3) parenthetical infix   e.g. (1 + (2 * 3))
4) infix                 e.g. 1 + 2 * 3
5) quit
''',
            1,
            5
        )
        match choice:
            case 1:
                parser_name = 'prefix'
                parser = parse_prefix
            case 2:
                parser_name = 'postfix'
                parser = parse_postfix
            case 3:
                parser_name = 'parenthetical infix'
                parser = parse_paren_infix
            case 4:
                parser_name = 'infix'
                parser = parse_infix
            case 5:
                return
        while 1:
            try:
                expr = input(f'Enter {parser_name} expression> ')
            except EOFError:
                break
            if expr == 'quit' or expr == 'q':
                break
            invalid = False
            operators = Stack()
            result = parser(token_scanner(expr))
            if result is None:
                print(f'\033[41mError:\033[0m Invalid expression {expr!r}')
            else:
                print(f'{expr} = {result}')

if __name__ == '__main__':
    main()
