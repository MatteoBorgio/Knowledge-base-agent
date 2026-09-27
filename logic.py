import itertools
from abc import ABC, abstractmethod


class Sentence(ABC):
    @abstractmethod
    def evaluate(self, model: dict[str, bool]):
        raise Exception("Nothing to evaluate.")

    def formula(self) -> str:
        return ""

    def symbols(self) -> set[str]:
        return set()

    @classmethod
    def validate(cls, sentence):
        if not isinstance(sentence, Sentence):
            raise TypeError("Sentence to validate must be a logical sentence.")

    @classmethod
    def parenthesize(cls, string: str) -> str | bool:
        def check_if_balanced(string: str) -> bool:
            counter = 0
            for char in string:
                if char == "(":
                    counter += 1
                elif char == ")":
                    if counter <= 0:
                        return False
                    counter -= 1
            return counter == 0

        if (
            not len(string)
            or string.isalpha()
            or (
                string[0] == "("
                and string[-1] == ")"
                and check_if_balanced(string[1:-1])
            )
        ):
            return string
        else:
            return f"({string})"


class Symbol(Sentence):
    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, other) -> bool:
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self) -> int:
        return hash(("symbol", self.name))

    def __repr__(self) -> str:
        return self.name

    def evaluate(self, model: dict[str, bool]):
        try:
            return model[self.name]
        except KeyError:
            raise Exception(f"Variable {self.name} not in model.")

    def formula(self) -> str:
        return self.name

    def symbols(self) -> set[str]:
        return {self.name}
