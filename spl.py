import tabulate

class SimplexException(BaseException):
    def __init__(self, message: str):
        self.message = message

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

class SimplexRule:
    coefs: list[float]
    result: float

    def __init__(self, coefs: list[float], result: float):
        self.coefs = coefs
        self.result = result

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
    print(f"prerequesties{" (canonized)" if canonized else ""}:")
    print(res)


class SimplexIterationData:
    C_coefs: list[float]
    rules: list[SimplexRule]
    basis: list[float]
    delta: list[float]

    def __init__(self, 
                 C_coefs: list[float],
                 rules: list[SimplexRule], 
                 basis: list[float]):
        self.C_coefs = C_coefs
        self.rules = rules
        self.basis = basis
        self.delta = self._get_delta()
    
    def _get_delta(self) -> list[float]:
        delta_values = []
        for k in range(len(self.C_coefs)):
            delta_k = 0
            for i in range(len(self.rules)):
                delta_k += self.C_coefs[self.basis[i]] * self.rules[i].coefs[k]
            delta_k -= self.C_coefs[k]
            delta_values.append(delta_k)
        return delta_values

    def is_optimal(self) -> bool:
        opt = all(delta_k >= 0 for delta_k in self.delta)
        return opt
    
    def has_answer(self) -> bool:
        has_ans = False
        for k, delta_k in enumerate(self.delta):
            if delta_k >= 0: continue
            has_positive = any(rule.coefs[k] > 0 for rule in self.rules)
            has_ans = has_ans or has_positive
        return has_ans
    
    @property
    def primary_column_k(self) -> int:
        """
        якщо рішення не оптимальне, повертає індекс ведучого стовпця (k)
        викидує виключення якщо рішення оптимальне
        """
        if self.is_optimal():
            raise SimplexException("The answer is optimal. Can't get primary column.")
        
        # negs = list(filter(lambda delta_k: delta_k < 0, self.delta))
        k = min(range(len(self.delta)), key=lambda k: self.delta[k])
        return k
    
    @property
    def primary_row_l(self) -> int:
        """
        якщо рішення не оптимальне, повертає індекс ведучої строки (l)
        викидує виключення якщо рішення оптимальне
        """
        if self.is_optimal():
            raise SimplexException("The answer is optimal. Can't get primary row.")
        
        k = self.primary_column_k
        l = None
        for maybe_l, rule in enumerate(self.rules):
            if rule.coefs[k] <= 0: continue

            if l is None: 
                l = maybe_l
                continue
            
            prev_tetha = self.rules[l].result / self.rules[l].coefs[k]
            tetha = rule.result / rule.coefs[k]

            if tetha < prev_tetha:
                l = maybe_l
        
        return l
    
    @property
    def var_values(self) -> list[float]:
        vals = []
        for j in range(len(self.C_coefs)):
            if j in self.basis:
                i = self.basis.index(j)
                vals.append(self.rules[i].result)
                continue
            vals.append(0)
        return vals
    
    @property
    def Z_func_result(self) -> float:
        res = 0
        vals = self.var_values
        for j in range(len(self.C_coefs)):
            res += self.C_coefs[j] * vals[j]
        return res
            

def show_iter(iter: SimplexIterationData):
    preheader = ["", "", "", *[f"{c}" for c in iter.C_coefs]]
    header = ["B", "C_баз", "X", *[f"P_{j+1}" for j in range(len(iter.C_coefs))]]
    
    res = tabulate.tabulate(
        tabular_data=[
            preheader,
            header,

        ]
    )