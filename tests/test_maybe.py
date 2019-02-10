from dataclasses import dataclass
from typing import Optional

from graphotype.maybe import maybe, Nothing

@dataclass
class Bar:
    value: int = 0

@dataclass
class Foo:
    bar: Optional[Bar]

@dataclass
class Root:
    foo: Optional[Foo]


example1 = Root(Foo(Bar(1)))
example2 = Root(Foo(None))
example3 = Root(None)


def test_maybe_fn():
    assert maybe(None) is Nothing
    assert maybe(0) is not Nothing
    assert maybe(example1) is not Nothing


def test_chaining_to_optional():
    assert maybe(example1).foo is not None
    assert maybe(example2).foo is not None
    assert maybe(example3).foo is None


def test_chaining_to_maybe():
    assert maybe(example1).foo_ is not Nothing
    assert maybe(example2).foo_ is not Nothing
    assert maybe(example3).foo_ is Nothing


def test_multi_step_chaining():
    assert maybe(example1).foo_.bar is not None
    assert maybe(example2).foo_.bar is None
    assert maybe(example3).foo_.bar is None

    assert maybe(example1).foo_.bar_.value == 1
    assert maybe(example2).foo_.bar_.value is None
    assert maybe(example3).foo_.bar_.value is None


