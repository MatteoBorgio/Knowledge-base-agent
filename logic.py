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
    def validate(cls, sentence) -> None:
        if not isinstance(sentence, Sentence):
            raise TypeError("Sentence to validate must be a logical sentence.")

    @classmethod
    def parenthesize(cls, string: str) -> str:
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

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, Symbol) and self.name == value.name

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


class Not(Sentence):
    def __init__(self, operand: Sentence) -> None:
        Sentence.validate(operand)
        self.operand = operand

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, Not) and self.operand == value.operand

    def __hash__(self) -> int:
        return hash(("not", self.operand))

    def __repr__(self) -> str:
        return f"Not({self.operand})"

    def evaluate(self, model: dict[str, bool]):
        return not self.operand.evaluate(model)

    def formula(self) -> str:
        return "¬" + Sentence.parenthesize(self.operand.formula())

    def symbols(self) -> set[str]:
        return self.operand.symbols()


class And(Sentence):
    def __init__(self, *conjuncts: Sentence) -> None:
        for conjunct in conjuncts:
            Sentence.validate(conjunct)
        self.conjuncts = list(conjuncts)

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, And) and self.conjuncts == value.conjuncts

    def __hash__(self) -> int:
        return hash(("and", tuple(hash(conjunct) for conjunct in self.conjuncts)))

    def __repr__(self) -> str:
        conjuncts = ", ".join((str(conjunct) for conjunct in self.conjuncts))
        return f"And({conjuncts})"

    def add(self, conjunct) -> None:
        Sentence.validate(conjunct)
        self.conjuncts.append(conjunct)

    def evaluate(self, model: dict[str, bool]):
        return all(conjunct.evaluate(model) for conjunct in self.conjuncts)

    def formula(self) -> str:
        if len(self.conjuncts) == 1:
            return self.conjuncts[0].formula()
        return " ∧ ".join(
            [Sentence.parenthesize(conjunct.formula()) for conjunct in self.conjuncts]
        )

    def symbols(self) -> set[str]:
        return set.union(*[conjunct.symbols() for conjunct in self.conjuncts])


class Or(Sentence):
    def __init__(self, *disjuncts: Sentence) -> None:
        for disjunct in disjuncts:
            Sentence.validate(disjunct)
        self.disjuncts = list(disjuncts)

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, Or) and self.disjuncts == value.disjuncts

    def __hash__(self) -> int:
        return hash(("or", tuple(hash(disjunct) for disjunct in self.disjuncts)))

    def __repr__(self) -> str:
        disjuncts = ", ".join((str(disjunct) for disjunct in self.disjuncts))
        return f"Or({disjuncts})"

    def evaluate(self, model: dict[str, bool]):
        return any(disjunct.evaluate(model) for disjunct in self.disjuncts)

    def formula(self) -> str:
        if len(self.disjuncts) == 1:
            return self.disjuncts[0].formula()
        return " ∧ ".join(
            [Sentence.parenthesize(disjunct.formula()) for disjunct in self.disjuncts]
        )

    def symbols(self) -> set[str]:
        return set.union(*[disjunct.symbols() for disjunct in self.disjuncts])
