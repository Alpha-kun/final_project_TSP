import gurobipy as grb
import numpy as np
import heuristic
from gurobipy import GRB
from readtxt import read_txt
from mincut import globalMinCut
from collections import defaultdict


# convert a solution to a graph expressed in adjacency matrix
def sol2graph(sol):
    A = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            A[i, j] = A[j, i] = sol[pair2index[i, j]].x
    return A


# read in problem graph
G = read_txt("hk48.txt")
n = G.shape[0]  # number of nodes
m = n * (n - 1) // 2  # number of edges

c = []
pair2index = np.zeros((n, n))
index2pair = []
counter = 0
for i in range(0, n):
    for j in range(i + 1, n):
        c.append(G[i, j])
        pair2index[i, j] = pair2index[j, i] = counter
        index2pair.append((i, j))
        counter += 1

# create model
TSP_Master = grb.Model()

# define x variables and set objective values
x = TSP_Master.addVars(m, obj=c, lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, name="x")

# set objective function sense
TSP_Master.modelSense = GRB.MINIMIZE

# add constraints to model
for i in range(n):
    expr = sum([x[pair2index[i, j]] for j in list(filter(lambda idx: (idx != i), range(n)))])
    TSP_Master.addConstr(expr == 2)

# Let Gurobi know that the model has changed
TSP_Master.update()

# write out the lp in a lp-file
TSP_Master.write("TSP.lp")

# use heuristic to compute an upper bound of the optimum
tc = 1e9
T = []
for i in range(G.shape[0]):
    # run a nearest neighbour starting from each node
    NNT = heuristic.nearest_neighbour(G, i)
    # and further optimize with 2-opt
    TOT = heuristic.two_opt(G, NNT)
    if heuristic.cost(G, TOT) < tc:
        tc = heuristic.cost(G, TOT)
        T = TOT

global_lower_bound = tc
global_opt_sol = [0 for e in range(m)]
for i in range(n):
    global_opt_sol[int(pair2index[i, (i + 1) % n])] = 1


def branch_and_bound(TSP_problem):
    # use the following global variables
    global global_lower_bound
    global global_opt_sol
    global x

    # solve the LP
    TSP_problem.optimize()

    # if LP relaxation worse than best know IP solution, immediately return
    if TSP_problem.objVal > global_lower_bound:
        return

    # repeatedly add subtour elimination constraints as needed
    while True:
        # convert LP solution to graph
        A = sol2graph(x)
        # compute the global mincut of the graph
        w, cut = globalMinCut(A)
        if w < 2.0 - 1e-9:
            # find the complement of cut
            tuc = list(filter(lambda idx: (idx not in cut), range(n)))
            # add cut
            edge_list = [pair2index[i, j] for i in cut for j in tuc]
            expr = sum(x[e] for e in edge_list)
            TSP_problem.addConstr(expr >= 2)
            # update model
            TSP_problem.update()
            # resolve the model
            TSP_problem.optimize()
            # if LP relaxation worse than best know IP solution, immediately return
            if TSP_problem.objVal > global_lower_bound:
                return
        else:
            break

    # find the first fractional variable
    fracid = -1
    for e in range(m):
        if abs(x[e].x - 0.5) < 0.5 - 1e-9:
            fracid = e
            break

    if fracid == -1:
        # solution is integral, no further branch needed
        if TSP_problem.objVal < global_lower_bound:
            # new lower bound found, update global optimum
            global_lower_bound = TSP_problem.objVal
            global_opt_sol = [x[e].x for e in range(m)]
    else:
        # x[fracid] is fractional
        # first branch it to 0
        x[fracid].lb = x[fracid].ub = 0
        TSP_problem.update()
        branch_and_bound(TSP_problem)
        # then branch it to 1
        x[fracid].lb = x[fracid].ub = 1
        TSP_problem.update()
        branch_and_bound(TSP_problem)
        # reset bounds
        x[fracid].lb = 0
        x[fracid].ub = 1
        TSP_problem.update()
    return


branch_and_bound(TSP_Master)
print(global_lower_bound)

# print final output in the required format
connections = defaultdict(list)
for i in range(m):
    if global_opt_sol[i] == 0:
        continue
    start, end = index2pair[i]
    connections[start].append(end)
    connections[end].append(start)

# connect the edges one by one
results = [] # (end1, end2, weight)
start = -1
end1 = -1
end2 = 0
while end2 != start:
    end1 = end2
    if not connections[end1]: break
    end2 = connections[end1][0]
    connections[end2].remove(end1)
    connections[end1].remove(end2)
    weight = G[end1][end2]
    results.append((end1, end2, weight))
    print(end1, end2, weight, '\n')

print("The cost of the best tour is: ", global_lower_bound)
