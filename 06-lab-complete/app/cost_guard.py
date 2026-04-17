cost = 0.0

def add_cost(amount: float, limit: float):
    global cost
    cost += amount
    if cost > limit:
        raise Exception("Budget exceeded")