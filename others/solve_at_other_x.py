import math
import gurobipy as gp
from gurobipy import GRB


def solve_probabilities_at_x(epsilon, x, endpoint_a=0, endpoint_b=1, total_piece=5):
    mid = (total_piece - 1) // 2
    m_1 = gp.Model("Quadratic Non-convex")
    m_1.Params.LogToConsole = 0

    # l_i: interval end-points
    # p_i: probability of piece i

    l = m_1.addMVar(shape=total_piece + 1, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="l")
    p = m_1.addMVar(shape=total_piece, lb=0, vtype=GRB.CONTINUOUS, name="p")

    m_1.addConstr(p[0] >= p[mid] / math.exp(epsilon), name="cons_2")
    m_1.addConstr(p[total_piece - 1] >= p[mid] / math.exp(epsilon), name="cons_2")
    for i in range(mid):
        m_1.addConstr(p[i] <= p[i + 1], name="cons_2")
    for i in range(mid + 1, total_piece):
        m_1.addConstr(p[i - 1] >= p[i], name="cons_2")

    m_1.addConstr(l[0] == endpoint_a, name="cons_3")
    m_1.addConstr(l[total_piece] == endpoint_b, name="cons_3")
    for i in range(total_piece):
        m_1.addConstr(l[i] <= l[i + 1], name="cons_3")
    m_1.addConstr(sum((l[i + 1] - l[i]) * p[i] for i in range(total_piece)) == 1, name="cons_3")
    # worst-case error: middle piece at x
    m_1.addConstr(l[mid] <= x, name="cons_3")
    m_1.addConstr(x <= l[mid + 1], name="cons_3")

    # bilinear encoding (Gurobi does not support 3-order variable multiplication) of the objective
    obj_tmp = m_1.addMVar(shape=total_piece, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj_i")
    for i in range(total_piece):
        m_1.addConstr(obj_tmp[i] == l[i + 1] * l[i + 1] - l[i] * l[i], name="cons_4")
    obj_center = m_1.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj")
    m_1.addConstr(obj_center == l[mid] * l[mid] + l[mid + 1] * l[mid + 1], name="cons_4")

    # encoding proved correct
    # see `distance_metric.py` for details
    left_distance = m_1.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj")
    m_1.addConstr(
        left_distance == sum(
            x * p[i] * (l[i + 1] - l[i]) - obj_tmp[i] / 2 * p[i] for i in range(mid)), name="cons_4")
    right_distance = m_1.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj")
    m_1.addConstr(right_distance == sum(
        obj_tmp[i] / 2 * p[i] - x * p[i] * (l[i + 1] - l[i]) for i in
        range(mid + 1, total_piece)),
                  name="cons_4")

    m_1.setObjective(left_distance + right_distance +
                     x * x * p[mid] - x * p[mid] * l[mid] - p[
                         mid] * x * l[mid + 1] +
                     obj_center / 2 * p[mid], GRB.MINIMIZE)

    m_1.setParam("NonConvex", 2)
    m_1.optimize()

    # for v in m_1.getVars():
    #     print(v, v.x)

    # m_1.computeIIS()
    # m_1.write("debug.ilp")

    probabilities = p.X
    for i in range(mid):
        probabilities[i] = p.X[total_piece - 1 - i]
    return p.X, l.X, m_1.objVal


if __name__ == "__main__":
    epsilon = 1
    x = 0
    p_list, length_list, obj = solve_probabilities_at_x(epsilon, x)
    print(p_list, length_list, obj)
