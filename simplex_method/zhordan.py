from .simplex_prerequistie import SimplexRule
from .simplex_iteration import SimplexIteration

def zhordan(it: SimplexIteration) -> SimplexIteration:
    k = it.primary_column_k
    ll = it.primary_row_l
    # print(f"zhordan: k={k}, l={ll}")
    a_lk = it.rules[ll].coefs[k]
    # спочатку знайти коефіцієнти для базового рядка
    l_rule_coefs = [a_lj/a_lk for a_lj in it.rules[ll].coefs]
    l_rule_result = it.rules[ll].result/a_lk
    # print(f"primary_rule_coefs: {l_rule_coefs}")
    next_rules = []
    for i in range(len(it.rules)):
        if i == ll:
            next_rules.append(SimplexRule(
                coefs=l_rule_coefs,
                result=l_rule_result
                ))
            continue
        # потім, за допомогою коефіцієнтів базового рядка знайти 
        # коефіцієнти інших рядків
        i_rule_coefs = [a_ij - it.rules[i].coefs[k] * l_rule_coefs[j]
                        for j, a_ij in enumerate(it.rules[i].coefs)]
        i_rule_result = \
            it.rules[i].result - it.rules[i].coefs[k] * l_rule_result
        next_rules.append(SimplexRule(
            coefs=i_rule_coefs,
            result=i_rule_result
            ))
    next_basis = [k if basis_num == ll else it.basis[basis_num]
                  for basis_num in range(len(it.basis))]
    # print("next rules: ")
    # [print(r) for r in next_rules]
    return SimplexIteration(
            C_coefs=it.C_coefs,
            rules=next_rules,
            basis=next_basis
            )
