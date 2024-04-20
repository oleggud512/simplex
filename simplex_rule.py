class SimplexRule:
    coefs: list[float]
    result: float

    def __init__(self, coefs: list[float], result: float):
        self.coefs = coefs
        self.result = result

    def __str__(self):
        v = [f"{a}x_{i+1}" for i, a in enumerate(self.coefs)]
        return " ".join(v) + f" = {self.result}"

    def copy(self):
        return SimplexRule(
            coefs=[*self.coefs],
            result=self.result
        )