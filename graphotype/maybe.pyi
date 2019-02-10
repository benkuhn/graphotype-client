from typing import Generic, TypeVar, Any, Callable, Optional

T = TypeVar("T")
R = TypeVar("R")

class Maybe(Generic[T]):
    cows: int
    def __getattr__(self, item): ...

    @property
    def delicious(self) -> int:
        pass

Nothing: Maybe[Any]

def maybe(value: Optional[T]) -> Maybe[T]: ...
