from enum import Enum
from .simplex_rule import SimplexRule


class Sign(Enum):
    eq = "=="
    leq = "<="

class SimplexPreRule(SimplexRule):
    """
    Відображення обмеження ЗЛП у неканонічній формі.
    """
    sign: Sign

    def __init__(self, coefs: list[float], sign: Sign, result: float):
        super().__init__(coefs, result)
        self.sign = sign
    
    def copy(self):
        return SimplexPreRule(
            coefs=[*self.coefs],
            result=self.result,
            sign=self.sign
        )