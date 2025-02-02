from simplex_method.simplex_pre_rule import Sign, SimplexPreRule
from simplex_method.simplex_prerequistie import SimplexPrerequistie, SimplexRule, show_pr
from simplex_method.simplex_iteration import show_iter, SimplexIteration
from simplex_method.jordan import jordan
from simplex_method.simplex_method import SimplexMethod

pr = SimplexPrerequistie(
    C_coefs=[-1, 1, 4],
    rules=[
        SimplexPreRule([1, 2, -3], Sign.leq, 3),
        SimplexPreRule([2, -1, 4], Sign.leq, 1)
    ]
)

solver = SimplexMethod(pr, should_log=True)
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

s1 = SimplexMethod(pr1, should_log=True)
s1.solve()
print(s1.result)

pr2 = SimplexPrerequistie(
    C_coefs=[6, 2, 3, 5],
    rules=[
        SimplexPreRule([3, 1, 0, 2], Sign.leq, 900),
        SimplexPreRule([4, 0, 1, 4], Sign.leq, 800),
        SimplexPreRule([0, 1, 2, 1], Sign.leq, 600)
    ]
)

s2 = SimplexMethod(pr2, should_log=True)
s2.solve()
print(s2.result)

pr3 = SimplexPrerequistie(
    C_coefs=[50, 40, 35],
    rules=[
        SimplexPreRule([0.4, 0.6, 0.5], Sign.leq, 800),
        SimplexPreRule([0.4, 0.4, 0.3], Sign.leq, 600),
        SimplexPreRule([0.2, 0, 0.2], Sign.leq, 50),
        SimplexPreRule([0.1, 0, 0.08], Sign.leq, 30)
    ]
)

s3 = SimplexMethod(pr3, should_log=True)
s3.solve()
print(s3.result)
print(f"resources: {[rule.result for rule in s3.prereq.rules]}\nspare: {s3.spare_resources}")