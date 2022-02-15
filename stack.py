from typing import TypeVar

T = TypeVar('T')

class Stack:
    def __init__(self):
        self.vals: list[T] = []

    def __len__(self) -> int:
        return len(self.vals)

    def is_empty(self) -> bool:
        return len(self) == 0

    def push(self, val: T) -> None:
        self.vals.append(val)

    def pop(self) -> None | T:
        if self.is_empty():
            return 0
        return self.vals.pop(-1)
