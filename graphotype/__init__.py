from typing import TypeVar, Generic

T = TypeVar('T')

class Schema(Generic[T]):
    def __init__(self, filename: str):
        pass

class Query:
    def __init__(self, s: Schema, text: str):
        pass

