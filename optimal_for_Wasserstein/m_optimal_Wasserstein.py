import math
import gurobipy as gp
from gurobipy import GRB
import matplotlib.pyplot as plt


def min_wasserstein_probability(epsilon, total_piece):
    """
    compute optimal piecewise mechanism under Wasserstein distance
    :param epsilon: privacy budget
    :total_piece: piece number
    :return: Optimal probability list
    """
    m = gp.Model("Quadratic Non-convex")
    m.Params.LogToConsole = 0

    # l_i: interval length of piece i, l_{total / 2} is the center piece
    # p_i: probability of piece i
    # interval region: [0, 1]

    l = m.addMVar(shape=total_piece, vtype=GRB.CONTINUOUS, name="l")
    p = m.addMVar(shape=total_piece, vtype=GRB.CONTINUOUS, name="p")

    m.addConstr(p >= 0, name="cons_1")
    m.addConstr(p[0] >= p[(total_piece - 1) // 2] / math.exp(epsilon), name="cons_2")
    m.addConstr(p[total_piece - 1] >= p[(total_piece - 1) // 2] / math.exp(epsilon), name="cons_2")
    for i in range((total_piece - 1) // 2):
        m.addConstr(p[i] <= p[i + 1], name="cons_2")
    for i in range((total_piece - 1) // 2 + 1, total_piece):
        m.addConstr(p[i - 1] >= p[i], name="cons_2")

    m.addConstr(l >= 0, name="cons_3")
    m.addConstr(sum(l) == 1, name="cons_3")
    m.addConstr(sum(l[i] * p[i] for i in range(total_piece)) == 1, name="cons_3")

    # Encoding for CDF block height
    height = m.addMVar(shape=total_piece, vtype=GRB.CONTINUOUS, name="height")
    for i in range(total_piece):
        if i == 0:
            m.addConstr(height[i] == p[i] * l[i], name="cons_4")
        else:
            m.addConstr(height[i] == height[i - 1] + p[i] * l[i], name="cons_4")

    t = 0  # endpoint

    # Encoding for integration of CDF
    mid_index = (total_piece - 1) // 2
    m.addConstr(sum(l[i] for i in range(mid_index)) <= t, name="cons_5")
    m.addConstr(sum(l[i] for i in range(mid_index + 1)) >= t, name="cons_5")
    left_integration = m.addMVar(shape=(mid_index + 1), vtype=GRB.CONTINUOUS, name="left_integration")
    right_integration = m.addMVar(shape=(mid_index + 1), vtype=GRB.CONTINUOUS, name="left_integration")
    left_length_t = m.addVar(vtype=GRB.CONTINUOUS, name="left_integration")
    m.addConstr(left_length_t == t - sum(l[i] for i in range(mid_index)), name="cons_5")
    height_t = m.addVar(vtype=GRB.CONTINUOUS, name="left_integration")
    m.addConstr(height_t == left_length_t * p[mid_index], name="cons_5")

    for i in range(mid_index + 1):
        if i == 0:
            m.addConstr(left_integration[i] == height[i] * l[i] / 2, name="cons_5")
        elif i < mid_index:
            m.addConstr(left_integration[i] == (height[i] + height[i - 1]) * l[i] / 2, name="cons_5")
        elif i == mid_index:
            m.addConstr(left_integration[i] == left_length_t * (2 * height[i - 1] + height_t) / 2, name="cons_5")
    for i in range(mid_index + 1):
        if i == 0:
            m.addConstr(right_integration[i] == (l[mid_index] - left_length_t) *
                        (height[mid_index] + height_t) / 2, name="cons_5")
        else:
            m.addConstr(right_integration[i] == (height[i + mid_index] + height[i + mid_index - 1]) * l[i + mid_index] / 2, name="cons_5")

    m.setObjective(sum(left_integration) + (1 - t) - sum(right_integration), GRB.MINIMIZE)

    m.setParam("NonConvex", 2)
    m.optimize()

    return p.X, l.X

    # for v in m.getVars():
    #     print(v, v.x)


if __name__ == "__main__":
    res = min_wasserstein_probability(1, 5)
    print(res)
