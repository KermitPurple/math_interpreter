from typing import Iterator
from op_info import *
from enum import Enum

class State(Enum):
    '''
    States for token_scanner
    NONE: not currently scanning anything
    NUM: currently scanning a number
    '''
    NONE = 0
    NUM = 1

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
