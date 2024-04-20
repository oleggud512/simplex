import tabulate
from simplex_exception import SimplexException
from simplex_rule import SimplexRule


def is_unit_vector(vector: list[float]) -> bool:
    zeros = 0
    ones = 0

    for x in vector:
        if x == 0:
            zeros += 1
        if x == 1:
            ones += 1

    if zeros + ones != len(vector):
        return False
    return True


class SimplexPrerequistie:

    C_coefs: list[float]
    rules: list[SimplexRule]

    def __init__(self,
                 C_coefs: list[float],
                 rules: list[SimplexRule]):
        var_count = len(C_coefs)
        for rule in rules:
            if len(rule.coefs) != var_count:
                raise SimplexException("incorrect rule coefs count")

        self.C_coefs = C_coefs
        self.rules = rules

    def canonized(self):
        # add zeros to the end
        canon_C_coefs = [*self.C_coefs, *[0 for _ in range(len(self.rules))]]
        canon_rules = []
        for i, rule in enumerate(self.rules):
            canon_rule = SimplexRule(
                coefs=[
                    *rule.coefs,
                    # add zero or one
                    *[1 if i == s_i else 0 for s_i in range(len(self.rules))]
                    ],
                result=rule.result
            )
            canon_rules.append(canon_rule)

        return SimplexPrerequistie(canon_C_coefs, canon_rules)

    def get_basis(self) -> list[float]:
        """
        повертає список індексів базисних змінних
        """
        basis_vars = []
        for vector_i in range(len(self.C_coefs)):
            if len(basis_vars) == len(self.rules):
                break

            a_vector = [rule.coefs[vector_i] for rule in self.rules]
            if is_unit_vector(a_vector):
                basis_vars.append(vector_i)

        if len(basis_vars) != len(self.rules):
            raise SimplexException("unable to find basis")

        return basis_vars


def show_pr(pr: SimplexPrerequistie, canonized: bool = False) -> str:
    header = ["", *[f"x_{i+1}" for i in range(len(pr.C_coefs))], "", ""]
    Z_func = ["Z = ", *[f"{c}" for c in pr.C_coefs], "", ""]
    rules = []
    for i, rule in enumerate(pr.rules):
        rule = ["", *rule.coefs, "=" if canonized else "<=", f"{rule.result}"]
        rules.append(rule)
    res = tabulate.tabulate(
        headers=header,
        tabular_data=[
            Z_func,
            *rules
        ],
        tablefmt="grid"
    )
    print(f"prerequesties{' (canonized)' if canonized else ''}:")
    print(res)