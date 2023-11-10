import math
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import matplotlib.pyplot as plt

def m_optimal_piecewise(epsilon, total_piece):
    """
    :param epsilon: privacy budget
    :return: probability list, interval endpoint list
    """
    mid = (total_piece - 1) // 2

    m = gp.Model("Quadratic Non-convex")
    m.Params.LogToConsole = 0

    # l_i: interval end-points
    # p_i: probability of piece i
    # interval region: [0, 1]

    l = m.addMVar(shape=total_piece + 1, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="l")
    p = m.addMVar(shape=total_piece, lb=0, vtype=GRB.CONTINUOUS, name="p")

    m.addConstr(p[0] >= p[mid] / math.exp(epsilon), name="cons_2")
    m.addConstr(p[total_piece - 1] >= p[mid] / math.exp(epsilon), name="cons_2")
    for i in range(mid):
        m.addConstr(p[i] <= p[i + 1], name="cons_2")
    for i in range(mid + 1, total_piece):
        m.addConstr(p[i - 1] >= p[i], name="cons_2")

    m.addConstr(l[0] <= 0, name="cons_3")
    m.addConstr(l[total_piece] >= 1, name="cons_3")
    m.addConstr(l[total_piece] - 1 == - l[0], name="cons_3")
    for i in range(total_piece):
        m.addConstr(l[i] <= l[i + 1], name="cons_3")
    m.addConstr(sum((l[i + 1] - l[i]) * p[i] for i in range(total_piece)) == 1, name="cons_3")

    # fixed output domain to be [0, 1]
    m.addConstr(l[total_piece] == 1, name="cons_3")

    # bilinear encoding (Gurobi does not support 3-order variable multiplication)
    obj_tmp = m.addMVar(shape=total_piece, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj_i")
    for i in range(total_piece):
        m.addConstr(obj_tmp[i] == l[i + 1] * l[i + 1] - l[i] * l[i], name="cons_4")
    obj_center = m.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj")
    m.addConstr(obj_center == l[mid] * l[mid] + l[mid + 1] * l[mid + 1], name="cons_4")

    # end point, known the worst-case error is at endpoint
    x = 0
    m.addConstr(l[mid] <= x, name="cons_3")
    m.addConstr(x <= l[mid + 1], name="cons_3")

    # minimize the L_1 distance for all x
    # encoding proved correct
    left_distance = m.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj")
    m.addConstr(left_distance == sum(x * p[i] * (l[i + 1] - l[i]) - obj_tmp[i] / 2 * p[i] for i in range(mid)), name="cons_4")
    right_distance = m.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj")
    m.addConstr(right_distance == sum(obj_tmp[i] / 2 * p[i] - x * p[i] * (l[i + 1] - l[i]) for i in range(mid + 1, total_piece)), name="cons_4")

    m.setObjective(left_distance + right_distance +
                   x * x * p[mid] - x * p[mid] * l[mid] - p[mid] * x * l[mid + 1] +
                   obj_center / 2 * p[mid], GRB.MINIMIZE)

    m.setParam("NonConvex", 2)
    m.optimize()

    # for v in m.getVars():
    #     print(v, v.x)

    # m.computeIIS()
    # m.write("debug.ilp")

    return p.X, l.X


if __name__ == "__main__":
    # true_data = np.linspace(0, 1, 10, endpoint=False)
    probabilities, intervals = m_optimal_piecewise(epsilon=1, total_piece=3)
    print(probabilities, intervals)
