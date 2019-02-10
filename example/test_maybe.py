from dataclasses import dataclass
from typing import Optional

from graphotype.maybe import Maybe, maybe, Nothing

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

m1: Maybe[Root] = maybe(None)

#m1.cows
#reveal_type(m1.foo)
reveal_type(m1.delicious())
#reveal_type(m1.foo_)
#reveal_type(m1.foo_.bar)
#reveal_type(m1.foo_.bar_.value)
#reveal_type(m1.foo_.bar_.value_)



#assert maybe(None).cows is Nothing
#assert maybe(0) is not Nothing
#assert maybe(example1) is not Nothing
