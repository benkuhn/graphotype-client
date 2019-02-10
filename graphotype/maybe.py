import abc
from dataclasses import dataclass
from typing import Generic, TypeVar, Any, Callable, Optional

T = TypeVar("T")
R = TypeVar("R")

CHAINING_SUFFIX = "_"


#class Maybe(Generic[T]):
class Maybe:
    def __getattr__(self, item: str) -> Any:
        if item.endswith(CHAINING_SUFFIX):
            # M a -> name -> M b
            result = self._bind(lambda unwrapped: getattr(unwrapped, item[:-1]))
            return result
        else:
            # M a -> name -> Optional[b]
            result = self._chain(lambda unwrapped: getattr(unwrapped, item))
            return result


    @abc.abstractmethod
    def _chain(self, f: Callable[[T], R]) -> Optional[R]:
        """If self is Nothing, return None. Otherwise return f(*self)."""

    def _bind(self, f: Callable[[T], R]) -> Any:
        """If self is Nothing, return Nothing. Else return Some(f(*self))."""
        result = self._chain(lambda unwrapped: maybe(f(unwrapped))) or Nothing
        return result


class _Nothing(Maybe):
#class _Nothing(Maybe[T]):
    """Implementation of the only Nothing value"""
    def _chain(self, f: Callable[[T], R]) -> Optional[R]:
        return None

    def __repr__(self):
        return "Nothing"


Nothing = _Nothing()


@dataclass
class Some(Maybe):
#class Some(Maybe[T]):
    _value: T

    def __post_init__(self) -> None:
        assert self._value is not None and self._value is not Nothing, "Some() constructor called with None. Use maybe() instead."

    def _chain(self, f: Callable[[T], R]) -> Optional[R]:
        return f(self._value)


def maybe(value: Optional[T]) -> Any:
    """Wrap an optional T into a Maybe[T], giving you Nothing or Some(value).

    'value' must not already be a Maybe.
    """
    assert not isinstance(value, Maybe), "maybe() called on something which is already a Maybe"
    if value is None:
        return Nothing
    return Some(value)
