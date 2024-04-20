from enum import Enum
from simplex_rule import SimplexRule


class Sign(Enum):
    eq = "eq"
    leq = "leq"

class SimplexPreRule(SimplexRule):
    sign: Sign

    def __init__(self, coefs: list[float], sign: Sign, result: float):
        super(coefs, result)
        self.sign = sign