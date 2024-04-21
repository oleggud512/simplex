from simplex_method.simplex_method import SimplexMethod
from simplex_method.simplex_pre_rule import Sign, SimplexPreRule
from simplex_method.simplex_prerequistie import SimplexPrerequistie, show_pr

def finput(mes: str = None) -> float:
    res = input(mes)
    try:
        return float(res)
    except ValueError:
        return 0.0

pastry_count = int(input("Введіть кількість кондитерських виробів:\n"))
groceries_count = int(input("Введіть кількість інгредієнтів, що необхідні для виготовлення всіх кондитерських виробів:\n"))

pastries = []
groceries = []

print(f"\nВведіть назви всіх ({pastry_count}) кондитерських виробів:")
for i in range(pastry_count):
    pastry = input(f"{i+1}: ")
    pastries.append(pastry)

print(f"\nВведіть назви всіх ({groceries_count}) інгредієнтів:")
for i in range(groceries_count):
    grocery = input(f"{i+1}: ")
    groceries.append(grocery)

available_groceries = []
print(f"\nВведіть кількість наявних інгредієнтів (у кілограмах):")
for groc in groceries:
    ava_amount = finput(f"{groc}: ")
    available_groceries.append(ava_amount)

pastries_prices = []
print(f"\nВведіть ціни на кожний виріб (за 1 кг):")
for pst in pastries:
    price = finput(f"{pst}: ")
    pastries_prices.append(price)

groceries_needed = []
print(f"""
Введіть кількість інгредієнтів (у кілограмах) необхідних для пригтоування одного кілограму 
кондитерського виробу (введіть 0 якщо інгредієнт не потрібен):""")
for pst in pastries:
    pst_grocs = []
    print(f"\n{pst}:")
    for groc in groceries:
        amount = finput(f"    {groc}: ")
        pst_grocs.append(amount)
    groceries_needed.append(pst_grocs)
    
print("\nВведення даних завершено.\nВхідні дані задачі:")

pr = SimplexPrerequistie(
    C_coefs=pastries_prices,
    rules=[SimplexPreRule([pst_grocs[i] for pst_grocs in groceries_needed], Sign.leq, available_groceries[i]) 
           for i in range(len(groceries))]
)

show_pr(pr, x_names=pastries, rule_names=groceries, z_name="Ціни ->")

solver = SimplexMethod(pr)
solver.solve()

results = []
for i in range(len(solver.result)):
    if solver.result[i] == 0:
        continue
    results.append(f"{solver.result[i]:.3f} кг \"{pastries[i]}\"")
results = ", ".join(results)

spare_groceries = []
for i, spare in enumerate(solver.spare_resources):
    if spare <= 0: 
        continue
    spare_groceries.append(f"{spare:.2f} кг \"{groceries[i]}\"")
spare_groceries = ", ".join(spare_groceries)

print(f"""Прибуток від продажу кондитерських виробів буде максимальним, та складатиме {solver.iter.Z_func_result:.2f} ум. од. 
якщо за заданих запасах інгредієнтів пригтувати {results}. 
Залишки інгредієнтів після пригтування: {spare_groceries}""")
