from simplex_prerequistie import SimplexPrerequistie, SimplexRule, show_pr
from simplex_iteration import show_iter, SimplexIteration
from zhordan import zhordan
from simplex_method import SimplexMethod

pr = SimplexPrerequistie(
    C_coefs=[-1, 1, 4],
    rules=[
        SimplexRule([1, 2, -3], 3),
        SimplexRule([2, -1, 4], 1)
    ]
)

solver = SimplexMethod(pr)
solver.solve()
print(solver.result)

pr1 = SimplexPrerequistie(
    C_coefs=[9, 5, 4, 3, 2, 0],
    rules=[
        SimplexRule([1, -2, 2, 0, 0, 1], 6),
        SimplexRule([1, 2, 1, 1, 0, 0], 24),
        SimplexRule([2, 1, -4, 0, 1, 0], 30)
    ]
)

s1 = SimplexMethod(pr1)
s1.solve()
print(s1.result)
# canon = pr.canonized()
# show_pr(pr)
# show_pr(canon, canonized=True)
# basis = canon.get_basis()
# print(f"basis: {basis}")

# iter1D = SimplexIteration(
#     C_coefs=canon.C_coefs,
#     rules=canon.rules,
#     basis=basis
# )

# print(f"delta: {iter1D.delta}")
# print(f"is_optimal: {iter1D.is_optimal()}")
# print(f"has_answer: {iter1D.can_optimize()}")

# print(f"primary_column_k: {iter1D.primary_column_k}")
# print(f"primary_row_l: {iter1D.primary_row_l}")

# print("first table: ")
# show_iter(iter1D)

# zh = zhordan(iter1D)
# print("second table: ")
# show_iter(zh)
# zh1 = zhordan(zh)
# print("third table: ")
# show_iter(zh1)

# print(f"is_optimal: {zh1.is_optimal()}")
# print(f"has_answer: {zh1.can_optimize()}")