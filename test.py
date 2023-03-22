support_nodes = []    # list of tuples (a, b)
weights = {}
a = 1
b = 2

support_nodes.append((a, b))
weights[(a,b)] = 0
for i in range(10):
    weights[(a,b)] += 1

print(weights[(a,b)])