from typing import TypeVar, Generic

class Query:
    pass

T = TypeVar('T')

class Schema(Generic[T]):
    def __init__(self, filename: str):
        pass
    def query(self, query: str) -> Query:
        pass
