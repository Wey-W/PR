import numpy as np
from gurobipy import *
import random
import xlrd
import xlwt
import pandas as pd
import cplex

# # 构建数学模型（单个问题航班为例）
# model = cplex.Cplex()
# model.objective.set_sense(model.objective.sense.minimize)
#
# # 定义变量
# d_c_s = 15  # 单位时间旅客延误成本(s)（后续根据数据进行更改）
# n_c_f = 200  # 单位航段数量变化延误成本(段)（后续根据数据进行更改）
# num_passengers = 10  # 单个问题航班中的乘客组数
# num_flights = 5  # 行程数
# num_classes = 3  # 座位等级数
# max_passengers_per_flight = [100, 200, 150, 250, 300]  # 每个行程的人数上限
# max_seats_per_class_per_flight = [[30, 40, 50], [40, 50, 60], [20, 30, 40], [30, 40, 50], [50, 60, 70]]  # 每个行程每种座位等级的数量上限
# costs = [[[10, 20, 30], [20, 30, 40], [30, 40, 50], [40, 50, 60], [50, 60, 70]],
#          [[20, 30, 40], [30, 40, 50], [40, 50, 60], [50, 60, 70], [60, 70, 80]],
#          [[30, 40, 50], [40, 50, 60], [50, 60, 70], [60, 70, 80], [70, 80, 90]],
#          [[40, 50, 60], [50, 60, 70], [60, 70, 80], [70, 80, 90], [80, 90, 100]],
#          [[50, 60, 70], [60, 70, 80], [70, 80, 90], [80, 90, 100], [90, 100, 110]]]  # 将每个乘客组分配到每个行程的每种座位等级的成本
#
# y = [model.variables.add(obj=[0], types=[model.variables.type.binary], names=["y_%d" % p]) for p in range(num_passengers)]
# x = [[[model.variables.add(obj=[costs[i][j][p]], types=[model.variables.type.binary], names=["x_%d_%d_%d" % (i, j, p)]) for j in range(num_classes)] for i in range(num_flights)] for p in range(num_passengers)]
#
# # 添加约束条件
# for p in range(num_passengers):
#     model.linear_constraints.add(
#         lin_expr=[cplex.SparsePair(ind=[i, j] for i in range(num_flights) for j in range(num_classes))] + [cplex.SparsePair(ind=[p], val=[1]) for p in range(num_passengers)],
#                                    senses=["E"]*(num_flights*num_classes) + ["L"]*num_passengers, rhs=[1]*num_flights*num_classes + [1]*num_passengers,
#                                    names=["flight_%d_%d" % (i, j) for i in range(num_flights) for j in range(num_classes)] + ["passenger_%d" % p for p in range(num_passengers)])
#
# for i in range(num_flights):
#     model.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=[j*num_passengers+p for j in range(num_classes) for p in range(num_passengers)]),
#                                            cplex.SparsePair(ind=[i], val=[-1])], senses=["L"], rhs=[-max_passengers_per_flight[i]], names=["flight_%d" % i])
#
# for i in range(num_flights):
#     for j in range(num_classes):
#         model.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=[i*num_classes+j*num_passengers+p for p in range(num_passengers)]),
#                                                cplex.SparsePair(ind=[j, i], val=[-1, 1])], senses=["L"], rhs=[0], names=["flight_%d_class_%d" % j % i])
#
# # 添加目标函数
# model.objective.set_linear([(y[p], 0) for p in range(num_passengers)] + [(x[p][i][j], costs[i][j][p]) for p in range(num_passengers) for i in range(num_flights) for j in range(num_classes)])
#
# # 求解模型
# model.solve()
#
# # 输出结果
# print("最小成本为: %f" % model.solution.get_objective_value())
# for p in range(num_passengers):
#     for i in range(num_flights):
#         for j in range(num_classes):
#             if model.solution.get_values(x[p][i][j]) == 1:
#                 print("将乘客组 %d 分配到 %d 号行程的 %d 等座位，成本为 %f" % (p+1, i+1, j+1, costs[i][j][p]))
#                 break
#         if model.solution.get_values(y[p]) == 1:
#             print("将乘客组 %d 取消行程" % (p+1))
#             break

import gurobipy as gp
from gurobipy import GRB

# 创建模型
model = gp.Model()

# 需用到的前置参数
P =  # 乘客组数量
I =  # 可接受新乘客的行程数量
J = 3  # 座位等级数量
Number_seats =  # 可用于恢复各行程不同等级座位的数量
Number_p =  # 各乘客组人数
c =  # 不同乘客组的恢复成本
cancel =  # 不同乘客组的取消成本


# 创建决策变量
x = {}
y = {}
for p in range(1, P+1):
    for i in range(1, I+1):
        for j in range(1, J+1):
            x[p, i, j] = model.addVar(vtype=GRB.BINARY, name=f'x_{p}_{i}_{j}')
    y[p] = model.addVar(vtype=GRB.BINARY, name=f'y_{p}')

# 添加约束
# 乘客要么被取消行程要么完成恢复过程
for p in range(1, P+1):
    model.addConstr(gp.quicksum(x[p, i, j] for i in range(1, I+1) for j in range(1, J+1)) + y[p] == 1)

# 得到恢复的乘客数量不能超过现有的座位数量
for i in range(1, I+1):
    for j in range(1, J+1):
        model.addConstr(gp.quicksum(x[p, i, j] for p in range(1, P+1)) <= Number_seats[i][j])

# 一个乘客组只能被分配在某一行程的某一等级座位上
for p in range(1, P+1):
    model.addConstr(gp.quicksum(x[p, i, j] for i in range(1, I+1) for j in range(1, J+1)) == 1)

# 设置目标函数

cost_expr = gp.LinExpr()  # 乘客组恢复成本目标函数
for p in range(1, P+1):
    for i in range(1, I+1):
        for j in range(1, J+1):
            cost_expr += c[p, i, j] * x[p, i, j]

CancellationCost = 0
for p in range(1, P+1):
    CancellationCost += cancel[p] * y[p]  # 行程取消成本之和

cost_expr += CancellationCost  # 乘客恢复总成本

model.setObjective(cost_expr, GRB.MINIMIZE)

# 求解模型
model.optimize()

# 打印结果
if model.status == GRB.OPTIMAL:
    for p in range(1, P+1):
        for i in range(1, I+1):
            for j in range(1, J+1):
                if x[p, i, j].x == 1:
                    print(f'Assign group {p} to itinerary {i}, seat class {j}')
    for p in range(1, P+1):
        if y[p].x == 1:
            print(f'Cancel group {p} itinerary')

# 释放资源
model.dispose()

