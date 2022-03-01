from typing import Iterator
from op_info import *

def parse_infix(tokens: Iterator[str | int | float]) -> None | int | float:
    '''
    parses a mathmatical expression in infix notation using optional parenthesis
    e.g. 1 + 2 * 3 -> 7
    e.g. (1 + 2) * 3 -> 9
    :tokens: iterator over tokens containing operators, parentheses, and numbers
    :returns: the result of the evaluated tokens; returns None if the expression is invalid
    '''
    paren_count = 0
    def get_single() -> None | int | float:
        nonlocal paren_count
        a = next(tokens, None)
        if isinstance(a, int | float):
            return a
        elif a == '-':
            a = get_single()
            if not isinstance(a, int | float):
                return None
            return -a
        elif a == '(':
            paren_count += 1
            return helper()
        return None
    def helper(a: None | float | int = None) -> None | int | float:
        nonlocal paren_count
        if a is None: # if no a is given
            a = get_single()
        if a is None: # if there is nothing in token iterator
            return None # fail
        op = next(tokens, None) # get operator
        if op == ')':
            paren_count -= 1
            if paren_count < 0:
                return None
        if op is None or op == ')': # if no operator or operator is closing paren
            return a # return the evaluated a
        if op in ADD_OPS: # if operation is adding or subtracting
            b = helper() # calculate the rest first
        elif op in MUL_OPS: # if operation is multiplying or dividing
            b = get_single() # get just the next one
        else: # not an add op or mul op
            return None # fail
        if b is None: # could not get b 
            return None # fail
        result = OPS[op](a, b) # calculate the operation on a and b
        if op in ADD_OPS: # if add/sub
            return result # return the result
        elif op in MUL_OPS: # if mul/div
            return helper(result) # calculate the rest with the result as the given a
    result = helper() # evaluate expression
    if next(tokens, None) is not None or paren_count != 0: # if the iterator isn't empty
        return None # fail
    return result # return evaluated expression

