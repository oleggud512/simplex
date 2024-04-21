from .simplex_prerequistie import SimplexPrerequistie, show_pr
from .simplex_iteration import SimplexIteration, show_iter
from .zhordan import zhordan


class SimplexMethod:
    should_log: bool = False
    iter_num: int = 1
    iter: SimplexIteration
    real_vars_count: int
    result: list[float] = None

    def __init__(self, prereq: SimplexPrerequistie, should_log: bool = False):
        self.should_log = should_log
        self.real_vars_count = len(prereq.C_coefs)
        
        canon = prereq.canonized()

        self.iter = SimplexIteration(
            C_coefs=canon.C_coefs,
            rules=canon.rules,
            basis=canon.get_basis()
        )

        if self.should_log:
            print("prereq:")
            show_pr(prereq)
            print("canonized:")
            show_pr(canon)
            print("table 1:")
            show_iter(self.iter)
    
    def solve(self):
        while not self.iter.is_optimal() and self.iter.can_optimize():
            self.iter = zhordan(self.iter)
            self.iter_num += 1
            if self.should_log:
                print(f"table {self.iter_num}:")
                show_iter(self.iter)
        
        res = []
        for j in range(self.real_vars_count):
            if j in self.iter.basis:
                i = self.iter.basis.index(j)
                res.append(self.iter.rules[i].result)
                continue
            res.append(0)

        self.result = res

        if self.should_log:
            print(f"result: {self.result}")