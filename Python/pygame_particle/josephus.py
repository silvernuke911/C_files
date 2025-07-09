def josephus_cyclical(N, k):
    soldiers = list(range(1, N + 1))
    index = 0
    elimination_order = []

    while len(soldiers) > 1:
        index = (index + k - 1) % len(soldiers)
        elimination_order.append(soldiers.pop(index))

    survivor = soldiers[0]
    return elimination_order, survivor

# Example usage
N = 41
k = 2
for j in range(1, N+1):
    eliminated, survivor = josephus_cyclical(j, k)
    print(f"N = {j}, eliminated: {eliminated}, survivor: {survivor}")
