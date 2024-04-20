from spl import (SimplexPrerequistie, SimplexRule, show_pr,
                 show_iter, SimplexIterationData)
from zhordan import zhordan

pr = SimplexPrerequistie(
    C_coefs=[-1, 1, 4],
    rules=[
        SimplexRule([1, 2, -3], 3),
        SimplexRule([2, -1, 4], 1)
    ]
)

canon = pr.canonized()
show_pr(pr)
show_pr(canon, canonized=True)
basis = canon.get_basis()
print(f"basis: {basis}")

iter1D = SimplexIterationData(
    C_coefs=canon.C_coefs,
    rules=canon.rules,
    basis=basis
)

print(f"delta: {iter1D.delta}")
print(f"is_optimal: {iter1D.is_optimal()}")
print(f"has_answer: {iter1D.has_answer()}")

print(f"primary_column_k: {iter1D.primary_column_k}")
print(f"primary_row_l: {iter1D.primary_row_l}")

print("first table: ")
show_iter(iter1D)

zh = zhordan(iter1D)
print("second table: ")
show_iter(zh)
zh1 = zhordan(zh)
print("third table: ")
show_iter(zh1)
# from simplex_table import SimplexTable, SimplexRule

# t1 = SimplexTable(
#     C_coefs = [-1, 1, 4],
#     rules = [
#         SimplexRule([1, 2, -3], 3),
#         SimplexRule([2, -1, 4], 1)
#     ]
# )
