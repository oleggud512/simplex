"""
короче, то на чем остановился это:
нашел дельту. И все.
осталось найти в дельте минимальный, потом посчитать и найти минимальный среди этой колонки
"""
class SimplexTable:

    rules_count: int
    arguments_count: int

    b_vector: list[float]
    a_rules: list[list[float]]
    c_values: list[float]
    c_base_vector: list[float]

    def __init__(self, rules_count: int, arguments_count: int):
        assert(rules_count != None and rules_count > 1 and arguments_count != None and arguments_count > 1) 
        self.rules_count = rules_count
        self.arguments_count = arguments_count

    def set_C_func(self, c_values: list[float]):
        if len(c_values) != self.arguments_count:
            print("wrong arguments count")
            return
        
        self.c_values = c_values

    def add_rule(self, a_values: list[float], result: float):
        if len(a_values) != self.arguments_count:
            print("wrong arguments count")
            return

        self.a_rules.append(a_values)
        self.b_vector.append(result)

    def compute_delta(self, k: int) -> float:
        ba = 0

        for i in range(self.rules_count):
            ba += self.c_base_vector[i] * self.a_rules[i][k]

        delta_k = ba - self.c_values[k]
        return delta_k

    def get_delta(self) -> list[float]:
        return [self.compute_delta(k=k) for k in range(self.arguments_count)]

    def validate_table(self) -> bool:
        return len(self.b_vector) == self.rules_count and \
                len(self.a_rules) == self.rules_count and \
                len(self.c_values) == self.arguments_count

    def init_c_base_vector(self):
        """
        should be called immediately after filling the table
        """
        if not self.validate_table():
            print("invalid table")
            return None

        if self.c_base_vector is not None:
            print("c_base_vector is already initialized")
            return None

        base_indexes = [0 for _ in range(self.rules_count)]

        for j in range(self.arguments_count):
            one_index = None
            found_non_zero_non_one = False

            for i in range(self.rules_count):
                if self.a_rules[i][j] == 1:
                    one_index = i
                    continue

                if self.a_rules[i][j] != 0:
                    found_non_zero_non_one = True
                    break
            if one_index is None and found_non_zero_non_one:
                break

            base_indexes[i] = one_index
            
        self.c_base_vector = base_indexes




t1 = SimplexTable(rules_count=2, arguments_count=5)

