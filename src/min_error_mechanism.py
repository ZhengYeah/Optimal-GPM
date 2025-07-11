import math
import gurobipy as gp
from gurobipy import GRB


class MinErrorMechanism(object):
    """
    Min error mechanism class for given parameters D, epsilon, m
    See Figure: solving flow
    """

    def __init__(self):
        pass

    def solve_probabilities(self) -> [list, list, float]:
        """
        Solve the optimal probability p_i
        :return: [interval list, probability list, optimal error]
        """
        pass

    def solve_lr(self, x) -> [list, float]:
        """
        Solve the l_i and r_i for x using p_i
        :param x: private input x
        :return: [[l_i, r_i], optimal error]
        """
        pass


class MinL1Mechanism(MinErrorMechanism):
    def __init__(self, endpoint_a, endpoint_b, epsilon, total_piece, probabilities=None):
        r"""
        distance = |y - x|
        :param endpoint_a: left endpoint of the bound
        :param endpoint_b: right endpoint of the bound
        :param epsilon: privacy budget
        :param total_piece: piece number
        :param probabilities: optimal probability list
        """
        super().__init__()
        assert endpoint_a < endpoint_b
        self.endpoint_a, self.endpoint_b = endpoint_a, endpoint_b
        self.epsilon = epsilon
        self.total_piece = total_piece
        self.probabilities = probabilities

    def solve_probabilities(self):
        mid = (self.total_piece - 1) // 2
        m_1 = gp.Model("Quadratic Non-convex")
        m_1.setParam("OutputFlag", 0)

        # l_i: interval end-points
        # p_i: probability of piece i

        l = m_1.addMVar(shape=self.total_piece + 1, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="l")
        p = m_1.addMVar(shape=self.total_piece, lb=0, vtype=GRB.CONTINUOUS, name="p")

        m_1.addConstr(p[0] >= p[mid] / math.exp(self.epsilon), name="cons_2")
        m_1.addConstr(p[self.total_piece - 1] >= p[mid] / math.exp(self.epsilon), name="cons_2")
        for i in range(mid):
            m_1.addConstr(p[i] <= p[i + 1], name="cons_2")
        for i in range(mid + 1, self.total_piece):
            m_1.addConstr(p[i - 1] >= p[i], name="cons_2")

        m_1.addConstr(l[0] == self.endpoint_a, name="cons_3")
        m_1.addConstr(l[self.total_piece] == self.endpoint_b, name="cons_3")
        for i in range(self.total_piece):
            m_1.addConstr(l[i] <= l[i + 1], name="cons_3")
        m_1.addConstr(sum((l[i + 1] - l[i]) * p[i] for i in range(self.total_piece)) == 1, name="cons_3")
        # worst-case error
        m_1.addConstr(l[mid] <= self.endpoint_a, name="cons_3")
        m_1.addConstr(self.endpoint_a <= l[mid + 1], name="cons_3")

        # bilinear encoding (Gurobi does not support 3-order variable multiplication)
        obj_tmp = m_1.addMVar(shape=self.total_piece, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj_i")
        for i in range(self.total_piece):
            m_1.addConstr(obj_tmp[i] == l[i + 1] * l[i + 1] - l[i] * l[i], name="cons_4")
        obj_center = m_1.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj")
        m_1.addConstr(obj_center == l[mid] * l[mid] + l[mid + 1] * l[mid + 1], name="cons_4")

        # encoding proved correct
        left_distance = m_1.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj")
        m_1.addConstr(
            left_distance == sum(
                self.endpoint_a * p[i] * (l[i + 1] - l[i]) - obj_tmp[i] / 2 * p[i] for i in range(mid)), name="cons_4")
        right_distance = m_1.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj")
        m_1.addConstr(right_distance == sum(
            obj_tmp[i] / 2 * p[i] - self.endpoint_a * p[i] * (l[i + 1] - l[i]) for i in
            range(mid + 1, self.total_piece)),
                      name="cons_4")

        m_1.setObjective(left_distance + right_distance +
                         self.endpoint_a * self.endpoint_a * p[mid] - self.endpoint_a * p[mid] * l[mid] - p[
                             mid] * self.endpoint_a * l[mid + 1] +
                         obj_center / 2 * p[mid], GRB.MINIMIZE)

        m_1.setParam("NonConvex", 2)
        m_1.optimize()

        # for v in m_1.getVars():
        #     print(v, v.x)

        # m_1.computeIIS()
        # m_1.write("debug.ilp")

        self.probabilities = p.X
        for i in range(mid):
            self.probabilities[i] = p.X[self.total_piece - 1 - i]
        return p.X, l.X, m_1.objVal

    def solve_lr(self, x):
        assert self.endpoint_a <= x <= self.endpoint_b
        p = self.probabilities
        assert len(p) == self.total_piece

        mid = (self.total_piece - 1) // 2
        m_2 = gp.Model("Quadratic Non-convex 2")
        m_2.setParam("OutputFlag", 0)

        # l_i: interval end-points
        l = m_2.addMVar(shape=self.total_piece + 1, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="l")

        m_2.addConstr(l[0] == self.endpoint_a, name="cons_3")
        m_2.addConstr(l[self.total_piece] == self.endpoint_b, name="cons_3")
        for i in range(self.total_piece):
            m_2.addConstr(l[i] <= l[i + 1], name="cons_3")
        m_2.addConstr(sum((l[i + 1] - l[i]) * p[i] for i in range(self.total_piece)) == 1, name="cons_3")
        m_2.addConstr(l[mid] <= x, name="cons_3")
        m_2.addConstr(x <= l[mid + 1], name="cons_3")

        # bilinear encoding (Gurobi does not support 3-order variable multiplication)
        obj_tmp = m_2.addMVar(shape=self.total_piece, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj_i")
        for i in range(self.total_piece):
            m_2.addConstr(obj_tmp[i] == l[i + 1] * l[i + 1] - l[i] * l[i], name="cons_4")
        obj_center = m_2.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj")
        m_2.addConstr(obj_center == l[mid] * l[mid] + l[mid + 1] * l[mid + 1], name="cons_4")

        # encoding proved correct
        left_distance = m_2.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj")
        m_2.addConstr(left_distance == sum(x * p[i] * (l[i + 1] - l[i]) - obj_tmp[i] / 2 * p[i] for i in range(mid)),
                      name="cons_4")
        right_distance = m_2.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj")
        m_2.addConstr(right_distance == sum(
            obj_tmp[i] / 2 * p[i] - x * p[i] * (l[i + 1] - l[i]) for i in range(mid + 1, self.total_piece)),
                      name="cons_4")

        m_2.setObjective(left_distance + right_distance +
                         x * x * p[mid] - x * p[mid] * l[mid] - p[mid] * x * l[mid + 1] +
                         obj_center / 2 * p[mid], GRB.MINIMIZE)
        m_2.setParam("NonConvex", 2)
        m_2.optimize()

        # for v in m_2.getVars():
        #     print(v, v.x)

        # m_2.computeIIS()
        # m_2.write("debug.ilp")

        return l.X, m_2.objVal


class MinWassersteinMechanism(MinErrorMechanism):
    def __init__(self, endpoint_a, endpoint_b, epsilon, total_piece, probabilities=None):
        r"""
        distance = |\int_{a}^{y} f_1(t) dt - \int_{a}^{y} f_2(t) dt|
        :param endpoint_a: left endpoint of the bound
        :param endpoint_b: right endpoint of the bound
        :param epsilon: privacy budget
        :param total_piece: piece number
        """
        super().__init__()
        assert endpoint_a < endpoint_b
        self.endpoint_a, self.endpoint_b = endpoint_a, endpoint_b
        self.epsilon = epsilon
        self.total_piece = total_piece
        self.probabilities = probabilities

    def solve_probabilities(self):
        mid = (self.total_piece - 1) // 2

        m_1 = gp.Model("Quadratic Non-convex")
        m_1.setParam("OutputFlag", 0)

        # l_i: interval length of piece i, l_{total / 2} is the center piece
        # p_i: probability of piece i

        l = m_1.addMVar(shape=self.total_piece, vtype=GRB.CONTINUOUS, name="l")
        p = m_1.addMVar(shape=self.total_piece, vtype=GRB.CONTINUOUS, name="p")

        m_1.addConstr(p >= 0, name="cons_1")
        m_1.addConstr(p[0] >= p[mid] / math.exp(self.epsilon), name="cons_2")
        m_1.addConstr(p[self.total_piece - 1] >= p[mid] / math.exp(self.epsilon), name="cons_2")
        for i in range(mid):
            m_1.addConstr(p[i] <= p[i + 1], name="cons_2")
        for i in range(mid + 1, self.total_piece):
            m_1.addConstr(p[i - 1] >= p[i], name="cons_2")

        m_1.addConstr(l >= 0, name="cons_3")
        m_1.addConstr(sum(l) == self.endpoint_b - self.endpoint_a, name="cons_3")
        m_1.addConstr(sum(l[i] * p[i] for i in range(self.total_piece)) == 1, name="cons_3")

        # Encoding for CDF block height
        height = m_1.addMVar(shape=self.total_piece, vtype=GRB.CONTINUOUS, name="height")
        for i in range(self.total_piece):
            if i == 0:
                m_1.addConstr(height[i] == p[i] * l[i], name="cons_4")
            else:
                m_1.addConstr(height[i] == height[i - 1] + p[i] * l[i], name="cons_4")

        # encoding for integration of CDF
        # worst-case error
        m_1.addConstr(sum(l[i] for i in range(mid)) <= 0, name="cons_5")
        m_1.addConstr(sum(l[i] for i in range(mid + 1)) >= 0, name="cons_5")

        left_integration = m_1.addMVar(shape=(mid + 1), vtype=GRB.CONTINUOUS, name="left_integration")
        right_integration = m_1.addMVar(shape=(mid + 1), vtype=GRB.CONTINUOUS, name="left_integration")
        left_length_x = m_1.addVar(vtype=GRB.CONTINUOUS, name="left_integration")
        m_1.addConstr(left_length_x == 0, name="cons_5")
        height_t = m_1.addVar(vtype=GRB.CONTINUOUS, name="left_integration")
        m_1.addConstr(height_t == left_length_x * p[mid], name="cons_5")

        for i in range(mid + 1):
            if i == 0:
                m_1.addConstr(left_integration[i] == height[i] * l[i] / 2, name="cons_5")
            elif i < mid:
                m_1.addConstr(left_integration[i] == (height[i] + height[i - 1]) * l[i] / 2, name="cons_5")
            elif i == mid:
                m_1.addConstr(left_integration[i] == left_length_x * (2 * height[i - 1] + height_t) / 2, name="cons_5")
        for i in range(mid + 1):
            if i == 0:
                m_1.addConstr(right_integration[i] == (l[mid] - left_length_x) * (height[mid] + height_t) / 2,
                              name="cons_5")
            else:
                m_1.addConstr(right_integration[i] == (height[i + mid] + height[i + mid - 1]) * l[i + mid] / 2,
                              name="cons_5")

        m_1.setObjective(sum(left_integration) + (self.endpoint_b - self.endpoint_a) - sum(right_integration), GRB.MINIMIZE)

        m_1.setParam("NonConvex", 2)
        m_1.optimize()

        # for v in m_1.getVars():
        #     print(v, v.x)

        self.probabilities = p.X
        for i in range(mid):
            self.probabilities[i] = p.X[self.total_piece - 1 - i]
        return p.X, l.X, m_1.objVal

    def solve_lr(self, x):
        assert self.endpoint_a <= x <= self.endpoint_b
        p = self.probabilities
        assert len(p) == self.total_piece

        mid = (self.total_piece - 1) // 2
        m_2 = gp.Model("Quadratic Non-convex")
        m_2.setParam("OutputFlag", 0)

        # l_i: interval length of piece i, l_{total / 2} is the center piece
        # interval region: [0, 1]

        l = m_2.addMVar(shape=self.total_piece, vtype=GRB.CONTINUOUS, name="l")
        m_2.addConstr(l >= 0, name="cons_3")
        m_2.addConstr(sum(l) == self.endpoint_b - self.endpoint_a, name="cons_3")
        m_2.addConstr(sum(l[i] * p[i] for i in range(self.total_piece)) == 1, name="cons_3")

        # Encoding for CDF block height
        height = m_2.addMVar(shape=self.total_piece, vtype=GRB.CONTINUOUS, name="height")
        for i in range(self.total_piece):
            if i == 0:
                m_2.addConstr(height[i] == p[i] * l[i], name="cons_4")
            else:
                m_2.addConstr(height[i] == height[i - 1] + p[i] * l[i], name="cons_4")

        # Encoding for integration of CDF
        m_2.addConstr(sum(l[i] for i in range(mid)) <= x - self.endpoint_a, name="cons_5")
        m_2.addConstr(sum(l[i] for i in range(mid + 1)) >= x - self.endpoint_a, name="cons_5")
        left_integration = m_2.addMVar(shape=(mid + 1), vtype=GRB.CONTINUOUS, name="left_integration")
        right_integration = m_2.addMVar(shape=(mid + 1), vtype=GRB.CONTINUOUS, name="left_integration")
        left_length_x = m_2.addVar(vtype=GRB.CONTINUOUS, name="left_integration")
        m_2.addConstr(left_length_x == x - self.endpoint_a - sum(l[i] for i in range(mid)), name="cons_5")
        height_t = m_2.addVar(vtype=GRB.CONTINUOUS, name="left_integration")
        m_2.addConstr(height_t == left_length_x * p[mid], name="cons_5")

        for i in range(mid + 1):
            if i == 0:
                m_2.addConstr(left_integration[i] == height[i] * l[i] / 2, name="cons_5")
            elif i < mid:
                m_2.addConstr(left_integration[i] == (height[i] + height[i - 1]) * l[i] / 2, name="cons_5")
            elif i == mid:
                m_2.addConstr(left_integration[i] == left_length_x * (2 * height[i - 1] + height_t) / 2, name="cons_5")
        for i in range(mid + 1):
            if i == 0:
                m_2.addConstr(right_integration[i] == (l[mid] - left_length_x) * (height[mid] + height_t) / 2, name="cons_5")
            else:
                m_2.addConstr(right_integration[i] == (height[i + mid] + height[i + mid - 1]) * l[i + mid] / 2,
                              name="cons_5")

        m_2.setObjective(sum(left_integration) + (self.endpoint_b - self.endpoint_a - x) - sum(right_integration), GRB.MINIMIZE)

        m_2.setParam("NonConvex", 2)
        m_2.optimize()

        # for v in m_2.getVars():
        #     print(v, v.x)

        return l.X, m_2.objVal


class MinL2Mechanism(MinErrorMechanism):
    def __init__(self, endpoint_a, endpoint_b, epsilon, total_piece, probabilities=None):
        r"""
        distance = (y - x)^2
        :param endpoint_a: left endpoint of the bound
        :param endpoint_b: right endpoint of the bound
        :param epsilon: privacy budget
        :param total_piece: piece number
        :param probabilities: optimal probability list
        """
        super().__init__()
        assert endpoint_a < endpoint_b
        self.endpoint_a, self.endpoint_b = endpoint_a, endpoint_b
        self.epsilon = epsilon
        self.total_piece = total_piece
        self.probabilities = probabilities

    def solve_probabilities(self):
        mid = (self.total_piece - 1) // 2
        m_1 = gp.Model("Quadratic Non-convex")
        m_1.setParam("OutputFlag", 0)

        # l_i: interval end-points
        # p_i: probability of piece i

        l = m_1.addMVar(shape=self.total_piece + 1, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="l")
        p = m_1.addMVar(shape=self.total_piece, lb=0, vtype=GRB.CONTINUOUS, name="p")

        m_1.addConstr(p[0] >= p[mid] / math.exp(self.epsilon), name="cons_2")
        m_1.addConstr(p[self.total_piece - 1] >= p[mid] / math.exp(self.epsilon), name="cons_2")
        for i in range(mid):
            m_1.addConstr(p[i] <= p[i + 1], name="cons_2")
        for i in range(mid + 1, self.total_piece):
            m_1.addConstr(p[i - 1] >= p[i], name="cons_2")

        m_1.addConstr(l[0] == self.endpoint_a, name="cons_3")
        m_1.addConstr(l[self.total_piece] == self.endpoint_b, name="cons_3")
        for i in range(self.total_piece):
            m_1.addConstr(l[i] <= l[i + 1], name="cons_3")
        m_1.addConstr(sum((l[i + 1] - l[i]) * p[i] for i in range(self.total_piece)) == 1, name="cons_3")
        # worst-case error
        m_1.addConstr(l[mid] <= self.endpoint_a, name="cons_3")
        m_1.addConstr(self.endpoint_a <= l[mid + 1], name="cons_3")

        # bilinear encoding (Gurobi does not support 3-order variable multiplication)
        var_tmp = m_1.addMVar(shape=self.total_piece + 1, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj_i")
        for i in range(self.total_piece + 1):
            m_1.addConstr(var_tmp[i] == (l[i] - self.endpoint_a) * (l[i] - self.endpoint_a), name="cons_4")
        var_tmp_2 = m_1.addMVar(shape=self.total_piece + 1, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj_i")
        for i in range(self.total_piece + 1):
            m_1.addConstr(var_tmp_2[i] == var_tmp[i] * (l[i] - self.endpoint_a), name="cons_4")

        # encoding proved correct
        obj = m_1.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj")
        m_1.addConstr(obj == sum((var_tmp_2[i + 1] - var_tmp_2[i]) * p[i] * (1 / 3) for i in range(self.total_piece)), name="obj")

        m_1.setObjective(obj, GRB.MINIMIZE)

        m_1.setParam("NonConvex", 2)
        m_1.optimize()

        # for v in m_1.getVars():
        #     print(v, v.x)

        # m_1.computeIIS()
        # m_1.write("debug.ilp")

        self.probabilities = p.X
        for i in range(mid):
            self.probabilities[i] = p.X[self.total_piece - 1 - i]
        return p.X, l.X, m_1.objVal

    def solve_lr(self, x):
        assert self.endpoint_a <= x <= self.endpoint_b
        p = self.probabilities
        assert len(p) == self.total_piece

        mid = (self.total_piece - 1) // 2
        m_2 = gp.Model("Quadratic Non-convex 2")
        m_2.setParam("OutputFlag", 0)

        # l_i: interval end-points
        l = m_2.addMVar(shape=self.total_piece + 1, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="l")

        m_2.addConstr(l[0] == self.endpoint_a, name="cons_3")
        m_2.addConstr(l[self.total_piece] == self.endpoint_b, name="cons_3")
        for i in range(self.total_piece):
            m_2.addConstr(l[i] <= l[i + 1], name="cons_3")
        m_2.addConstr(sum((l[i + 1] - l[i]) * p[i] for i in range(self.total_piece)) == 1, name="cons_3")
        m_2.addConstr(l[mid] <= x, name="cons_3")
        m_2.addConstr(x <= l[mid + 1], name="cons_3")

        # bilinear encoding (Gurobi does not support 3-order variable multiplication)
        var_tmp = m_2.addMVar(shape=self.total_piece + 1, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj_i")
        for i in range(self.total_piece + 1):
            m_2.addConstr(var_tmp[i] == (l[i] - x) * (l[i] - x), name="cons_4")
        var_tmp_2 = m_2.addMVar(shape=self.total_piece + 1, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj_i")
        for i in range(self.total_piece + 1):
            m_2.addConstr(var_tmp_2[i] == var_tmp[i] * (l[i] - x), name="cons_4")

        # encoding proved correct
        obj = m_2.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj")
        m_2.addConstr(obj == sum((var_tmp_2[i + 1] - var_tmp_2[i]) * p[i] * (1 / 3) for i in range(self.total_piece)),
                      name="obj")

        m_2.setObjective(obj, GRB.MINIMIZE)

        m_2.setParam("NonConvex", 2)
        m_2.optimize()

        # for v in m_1.getVars():
        #     print(v, v.x)

        # m_1.computeIIS()
        # m_1.write("debug.ilp")

        return l.X, m_2.objVal


class MinL2MechanismAblation(MinErrorMechanism):
    def __init__(self, in_endpoint_a, in_endpoint_b, out_endpoint_a, out_endpoint_b, epsilon, total_piece, probabilities=None):
        r"""
        distance = (y - x)^2
        :param in_endpoint_a: left endpoint of the input bound
        :param in_endpoint_b: right endpoint of the input bound
        :param epsilon: privacy budget
        :param total_piece: piece number
        :param probabilities: optimal probability list
        """
        super().__init__()
        assert in_endpoint_a < in_endpoint_b
        assert out_endpoint_a < out_endpoint_b
        self.in_endpoint_a, self.in_endpoint_b = in_endpoint_a, in_endpoint_b
        self.out_endpoint_a, self.out_endpoint_b = out_endpoint_a, out_endpoint_b
        self.epsilon = epsilon
        self.total_piece = total_piece
        self.probabilities = probabilities

    def solve_probabilities(self):
        mid = (self.total_piece - 1) // 2
        m_1 = gp.Model("Quadratic Non-convex")
        m_1.setParam("OutputFlag", 0)

        # l_i: interval end-points
        # p_i: probability of piece i

        l = m_1.addMVar(shape=self.total_piece + 1, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="l")
        p = m_1.addMVar(shape=self.total_piece, lb=0, vtype=GRB.CONTINUOUS, name="p")

        m_1.addConstr(p[0] >= p[mid] / math.exp(self.epsilon), name="cons_2")
        m_1.addConstr(p[self.total_piece - 1] >= p[mid] / math.exp(self.epsilon), name="cons_2")
        for i in range(mid):
            m_1.addConstr(p[i] <= p[i + 1], name="cons_2")
        for i in range(mid + 1, self.total_piece):
            m_1.addConstr(p[i - 1] >= p[i], name="cons_2")

        m_1.addConstr(l[0] == self.out_endpoint_a, name="cons_3")
        m_1.addConstr(l[self.total_piece] == self.out_endpoint_b, name="cons_3")
        for i in range(self.total_piece):
            m_1.addConstr(l[i] <= l[i + 1], name="cons_3")
        m_1.addConstr(sum((l[i + 1] - l[i]) * p[i] for i in range(self.total_piece)) == 1, name="cons_3")
        # worst-case error
        m_1.addConstr(l[mid] <= self.out_endpoint_a, name="cons_3")
        m_1.addConstr(self.out_endpoint_a <= l[mid + 1], name="cons_3")

        # bilinear encoding (Gurobi does not support 3-order variable multiplication)
        var_tmp = m_1.addMVar(shape=self.total_piece + 1, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj_i")
        for i in range(self.total_piece + 1):
            m_1.addConstr(var_tmp[i] == (l[i] - self.in_endpoint_a) * (l[i] - self.in_endpoint_a), name="cons_4")
        var_tmp_2 = m_1.addMVar(shape=self.total_piece + 1, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj_i")
        for i in range(self.total_piece + 1):
            m_1.addConstr(var_tmp_2[i] == var_tmp[i] * (l[i] - self.in_endpoint_a), name="cons_4")

        # encoding proved correct
        obj = m_1.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj")
        m_1.addConstr(obj == sum((var_tmp_2[i + 1] - var_tmp_2[i]) * p[i] * (1 / 3) for i in range(self.total_piece)), name="obj")

        m_1.setObjective(obj, GRB.MINIMIZE)

        m_1.setParam("NonConvex", 2)
        m_1.optimize()

        # for v in m_1.getVars():
        #     print(v, v.x)

        # m_1.computeIIS()
        # m_1.write("debug.ilp")

        self.probabilities = p.X
        for i in range(mid):
            self.probabilities[i] = p.X[self.total_piece - 1 - i]
        return p.X, l.X, m_1.objVal

    def solve_lr(self, x):
        assert self.in_endpoint_a <= x <= self.in_endpoint_b
        p = self.probabilities
        assert len(p) == self.total_piece

        mid = (self.total_piece - 1) // 2
        m_2 = gp.Model("Quadratic Non-convex 2")
        m_2.setParam("OutputFlag", 0)

        # l_i: interval end-points
        l = m_2.addMVar(shape=self.total_piece + 1, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="l")

        m_2.addConstr(l[0] == self.out_endpoint_a, name="cons_3")
        m_2.addConstr(l[self.total_piece] == self.out_endpoint_b, name="cons_3")
        for i in range(self.total_piece):
            m_2.addConstr(l[i] <= l[i + 1], name="cons_3")
        m_2.addConstr(sum((l[i + 1] - l[i]) * p[i] for i in range(self.total_piece)) == 1, name="cons_3")
        m_2.addConstr(l[mid] <= x, name="cons_3")
        m_2.addConstr(x <= l[mid + 1], name="cons_3")

        # bilinear encoding (Gurobi does not support 3-order variable multiplication)
        var_tmp = m_2.addMVar(shape=self.total_piece + 1, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj_i")
        for i in range(self.total_piece + 1):
            m_2.addConstr(var_tmp[i] == (l[i] - x) * (l[i] - x), name="cons_4")
        var_tmp_2 = m_2.addMVar(shape=self.total_piece + 1, lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj_i")
        for i in range(self.total_piece + 1):
            m_2.addConstr(var_tmp_2[i] == var_tmp[i] * (l[i] - x), name="cons_4")

        # encoding proved correct
        obj = m_2.addVar(lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="obj")
        m_2.addConstr(obj == sum((var_tmp_2[i + 1] - var_tmp_2[i]) * p[i] * (1 / 3) for i in range(self.total_piece)),
                      name="obj")

        m_2.setObjective(obj, GRB.MINIMIZE)

        m_2.setParam("NonConvex", 2)
        m_2.optimize()

        # for v in m_1.getVars():
        #     print(v, v.x)

        # m_1.computeIIS()
        # m_1.write("debug.ilp")

        return l.X, m_2.objVal
