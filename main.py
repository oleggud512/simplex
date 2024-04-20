from simplex_pre_rule import Sign, SimplexPreRule
from simplex_prerequistie import SimplexPrerequistie, SimplexRule, show_pr
from simplex_iteration import show_iter, SimplexIteration
from zhordan import zhordan
from simplex_method import SimplexMethod

pr = SimplexPrerequistie(
    C_coefs=[-1, 1, 4],
    rules=[
        SimplexPreRule([1, 2, -3], Sign.leq, 3),
        SimplexPreRule([2, -1, 4], Sign.leq, 1)
    ]
)

solver = SimplexMethod(pr)
solver.solve()
print(solver.result)

pr1 = SimplexPrerequistie(
    C_coefs=[9, 5, 4, 3, 2],
    rules=[
        SimplexPreRule([1, -2,  2, 0, 0], Sign.leq,  6),
        SimplexPreRule([1,  2,  1, 1, 0], Sign.eq,  24),
        SimplexPreRule([2,  1, -4, 0, 1], Sign.eq,  30)
    ]
)

s1 = SimplexMethod(pr1)
s1.solve()
print(s1.result)