import tabulate
from .simplex_rule import SimplexRule
from .simplex_exception import SimplexException

class SimplexIteration:
    """
    Є відображенням однієї симплекс таблиці.
    """
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
        """
        Повертає значення delta для поточної симплекс таблиці.
        """
        delta_values = []
        for k in range(len(self.C_coefs)):
            delta_k = 0
            for i in range(len(self.rules)):
                delta_k += self.C_coefs[self.basis[i]] * self.rules[i].coefs[k]
            delta_k -= self.C_coefs[k]
            delta_values.append(delta_k)
        return delta_values

    def is_optimal(self) -> bool:
        """
        Таблиця є оптимальною, якщо кожне значення `delta_k` є більшим за нуль.
        """
        opt = all(delta_k >= 0 for delta_k in self.delta)
        return opt

    def can_optimize(self) -> bool:
        """
        Неоптимізовану таблицю можна оптимізувати, якщо хоча б одного із негативних значень `delta_k` є позитивне значення a_ik.
        """
        can_opt = False
        for k, delta_k in enumerate(self.delta):
            if delta_k >= 0:
                continue
            has_positive = any(rule.coefs[k] > 0 for rule in self.rules)
            can_opt = can_opt or has_positive
        return can_opt

    @property
    def primary_column_k(self) -> int:
        """
        Якщо рішення не оптимальне, повертає індекс ведучого стовпця (k).
        Якщо оптимальне, викидує виключення.
        """
        if self.is_optimal():
            raise SimplexException(
                    "The answer is optimal. Can't get primary column.")

        # negs = list(filter(lambda delta_k: delta_k < 0, self.delta))
        k = min(range(len(self.delta)), key=lambda k: self.delta[k])
        return k

    @property
    def primary_row_l(self) -> int:
        """
        Якщо рішення не оптимальне, повертає індекс ведучої строки (l).
        Якщо оптимальне, викидує виключення.
        """
        if self.is_optimal():
            raise SimplexException(
                    "The answer is optimal. Can't get primary row.")

        k = self.primary_column_k
        l = None
        for maybe_l, rule in enumerate(self.rules):
            if rule.coefs[k] <= 0:
                continue

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
        """
        Повертає значення змінних x для поточної симплекс таблиці.
        """
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
        """
        Повертає результат цільової функції.
        """
        res = 0
        vals = self.var_values
        for j in range(len(self.C_coefs)):
            res += self.C_coefs[j] * vals[j]
        return res


def show_iter(iter: SimplexIteration):
    """
    Виводить таблицю в термінал.
    """
    preheader = ["", "", "", *[f"{c}" for c in iter.C_coefs]]
    header = ["B", "C_баз", "X",
              *[f"P_{j+1}" for j in range(len(iter.C_coefs))]]
    rows = []
    for i, rule in enumerate(iter.rules):
        rows.append([
            rule.result,
            iter.C_coefs[iter.basis[i]],
            f"x_{iter.basis[i]+1}",
            *iter.rules[i].coefs,
            ])
    delta_row = [
            f"Z={iter.Z_func_result}",
            "",
            "delta_k",
            *iter.delta
            ]

    res = tabulate.tabulate(
        tabular_data=[
            preheader,
            header,
            *rows,
            delta_row
        ],
        tablefmt="grid",
        numalign="center",
        stralign="center"
    )
    print(res)
