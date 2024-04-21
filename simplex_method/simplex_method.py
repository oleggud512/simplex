from simplex_method.simplex_exception import SimplexException
from .simplex_prerequistie import SimplexPrerequistie, show_pr
from .simplex_iteration import SimplexIteration, show_iter
from .jordan import jordan


class SimplexMethod:
    """
    Вирішує ЗЛП використовуючи симплекс метод.
    """
    should_log: bool = False
    iter_num: int = 1
    prereq: SimplexPrerequistie
    iter: SimplexIteration
    real_vars_count: int
    result: list[float] = None

    def __init__(self, prereq: SimplexPrerequistie, should_log: bool = False):
        self.should_log = should_log
        self.real_vars_count = len(prereq.C_coefs)
        self.prereq = prereq
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
        """
        Виконує перетворення Жордана над `iter`, допоки результат не стане оптимальним.
        """
        while not self.iter.is_optimal() and self.iter.can_optimize():
            self.iter = jordan(self.iter)
            self.iter_num += 1
            if self.should_log:
                print(f"table {self.iter_num}:")
                show_iter(self.iter)
        
        # перетворення оптмальної симплкес таблиці на "справжній" результат
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
    
    @property
    def spare_resources(self) -> list[float]:
        """
        Рахує залишок ресурсів після знаходження результату.
        """
        if self.result is None:
            raise SimplexException("Can't compute spare resources without result.")
        
        spare_resources = []
        for  i in range(len(self.prereq.rules)):
            ava_groc = self.prereq.rules[i].result
            used_groc = 0
            for j in range(len(self.prereq.C_coefs)):
                used_groc += self.result[j] * self.prereq.rules[i].coefs[j]
            spare_resources.append(ava_groc - used_groc)
        return spare_resources