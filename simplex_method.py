from simplex_prerequistie import SimplexPrerequistie
from simplex_iteration import SimplexIteration
from zhordan import zhordan


class SimplexMethod:
    iter_num: int = 1
    iter: SimplexIteration
    real_vars_count: int
    result: list[float] = None

    def __init__(self, prereq: SimplexPrerequistie):
        self.real_vars_count = len(prereq.C_coefs)
        canon = prereq.canonized()
        self.iter = SimplexIteration(
            C_coefs=canon.C_coefs,
            rules=canon.rules,
            basis=canon.get_basis()
        )
    
    def solve(self):
        while not self.iter.is_optimal() and self.iter.can_optimize():
            self.iter = zhordan(self.iter)
            self.iter_num += 1
        
        res = []
        for j in range(self.real_vars_count):
            if j in self.iter.basis:
                i = self.iter.basis.index(j)
                res.append(self.iter.rules[i].result)
                continue
            res.append(0)

        self.result = res