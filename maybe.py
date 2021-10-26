from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar("T", covariant=True)


@dataclass(frozen=True)
class Maybe(Generic[T]):
    def bind(self, f):
        if isinstance(self, Nothing):
            return Nothing()

        try:
            x = f(self.get())
            return Just(x)
        except:
            return Nothing()

    def __rshift__(self, f):
        return self.bind(f)


@dataclass(frozen=True)
class Just(Maybe):
    value: T

    def get(self):
        return self.value

    def __repr__(self):
        x = self.get()
        return "Just {}".format(str(x) if type(x) is not str else f'"{x}"')


@dataclass(frozen=True)
class Nothing(Maybe):
    def get(self):
        return None

    def __repr__(self):
        return "Nothing"


x = Just("1")


y = (
    x
    >> int
    >> (lambda x: -x)
    >> (lambda x: x + 3)
    >> (lambda x: x ** 2)
    >> (lambda x: list(range(x)))
)
print(x, y)
