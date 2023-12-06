import math
import gurobipy as gp
from gurobipy import GRB


def min_wasserstein_mechanism(epsilon, total_piece, delta, x=0):
    """
    compute optimal piecewise mechanism under Wasserstein distance
    :param epsilon: privacy budget
    :param total_piece: piece number
    :param delta: probabilistic-DP delta
    :param x: ture data, end-point has the largest error
    :return: Optimal probability list
    """
    assert (0 <= x <= 1)
    mid = (total_piece - 1) // 2

    m = gp.Model("Quadratic Non-convex")
    m.Params.LogToConsole = 0

    # l_i: interval length of piece i, l_{total / 2} is the center piece
    # p_i: probability of piece i
    # interval region: [0, 1]

    l = m.addMVar(shape=total_piece, vtype=GRB.CONTINUOUS, name="l")
    p = m.addMVar(shape=total_piece, vtype=GRB.CONTINUOUS, name="p")

    m.addConstr(p >= 0, name="cons_1")
    m.addConstr(p[0] >= p[mid] / math.exp(epsilon), name="cons_2")
    m.addConstr(p[total_piece - 1] >= p[mid] / math.exp(epsilon) - delta, name="cons_2")
    for i in range(mid):
        m.addConstr(p[i] <= p[i + 1], name="cons_2")
    for i in range(mid + 1, total_piece):
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

    # Encoding for integration of CDF
    m.addConstr(sum(l[i] for i in range(mid)) <= x, name="cons_5")
    m.addConstr(sum(l[i] for i in range(mid + 1)) >= x, name="cons_5")
    left_integration = m.addMVar(shape=(mid + 1), vtype=GRB.CONTINUOUS, name="left_integration")
    right_integration = m.addMVar(shape=(mid + 1), vtype=GRB.CONTINUOUS, name="left_integration")
    left_length_x = m.addVar(vtype=GRB.CONTINUOUS, name="left_integration")
    m.addConstr(left_length_x == x - sum(l[i] for i in range(mid)), name="cons_5")
    height_t = m.addVar(vtype=GRB.CONTINUOUS, name="left_integration")
    m.addConstr(height_t == left_length_x * p[mid], name="cons_5")

    for i in range(mid + 1):
        if i == 0:
            m.addConstr(left_integration[i] == height[i] * l[i] / 2, name="cons_5")
        elif i < mid:
            m.addConstr(left_integration[i] == (height[i] + height[i - 1]) * l[i] / 2, name="cons_5")
        elif i == mid:
            m.addConstr(left_integration[i] == left_length_x * (2 * height[i - 1] + height_t) / 2, name="cons_5")
    for i in range(mid + 1):
        if i == 0:
            m.addConstr(right_integration[i] == (l[mid] - left_length_x) *
                        (height[mid] + height_t) / 2, name="cons_5")
        else:
            m.addConstr(right_integration[i] == (height[i + mid] + height[i + mid - 1]) * l[i + mid] / 2, name="cons_5")

    m.setObjective(sum(left_integration) + (1 - x) - sum(right_integration), GRB.MINIMIZE)

    m.setParam("NonConvex", 2)
    m.optimize()

    return p.X, l.X, m.objVal

    # for v in m.getVars():
    #     print(v, v.x)


if __name__ == "__main__":
    res = min_wasserstein_mechanism(8, 3, 0)
    print(res)
