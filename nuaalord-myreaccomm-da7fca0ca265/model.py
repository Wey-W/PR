from pnr import *
from flight import *
from write import *
from parameter import *
import gurobipy as gp
from gurobipy import GRB
import os
import time
import traceback
import pandas as pd
import matplotlib.pyplot as plt


class Model:
    def __init__(self):  # 文件存储函数
        self.schedule_file = os.path.join(os.getcwd(), "data", "schedule.dat")   # 文件路径写入当前路径的子目录，得到的是data目录下的dat文件
        self.avail_file = os.path.join(os.getcwd(), "data", "output.dat")
        # self.avail_file = os.path.join(os.getcwd(), "data", "availability.dat")
        self.pax_file = os.path.join(os.getcwd(), "data", "sup_test.dat")
        # self.pax_file = os.path.join(os.getcwd(), "data", "passengers.dat")
        self.itinerary_file = os.path.join(os.getcwd(), "data", "pnrFlights.dat")

    def read_input_data(self):  # 数据读取函数
        Flight.read_flight_data(self.schedule_file)  # 得到allFlights字典，键值对为：flt_id-schedule.dat主要信息
        Flight.read_availability_data(self.avail_file)  # 得到availability字典，键值对为：Cabin[J/Y/F]-剩余可载客量
        PNR.read_pnr_data(self.pax_file)  # 得到allPNRs字典，键值对为：pnr_id-passengers.dat主要信息
        PNR.read_pnr_flights_data(self.itinerary_file)

    @staticmethod   # 静态方法 使后续函数可以同时被实例或类调用
    def show_info():
        Write.show_passenger_itineraries()

    @classmethod
    def review_passengers(cls):  # 判断一整个乘客组的延误情况
        from datetime import timedelta
        for _pnr in PNR.allPNRs.values():
            _pnr.disruption = DisruptionType.NoDisruption
            prev_flt = None
            for pnr_flight in _pnr.flights:  # pnr_id的全部航班列表循环（主要信息为航班id与舱位等级信息）
                _flight = pnr_flight.get("flight")
                if _flight.status is False:
                    _pnr.disruption = DisruptionType.FlightCancel
                    break
                if prev_flt is not None:  # 永远不会执行？？？
                    if _flight.act_dep_time - prev_flt.act_arr_time < timedelta(hours=1):
                        _pnr.disruption = DisruptionType.TimeMissConnect
                    break
                prev_flt = _flight

    @classmethod
    def itinerary_generation(cls):  # 筛选出受到延误的乘客的可用恢复航班信息，储存在candidate_itineraries中
        for _pnr in PNR.allPNRs.values():
            if _pnr.disruption == DisruptionType.NoDisruption:
                continue
            # if _pnr.sch_start_airport == _pnr.end_airport

            # itineraries with one flight leg
            for flt_id, _flt in Flight.allFlights.items():
                if _flt.act_dep_airport != _pnr.start_airport:
                    continue
                if _flt.act_arr_airport != _pnr.end_airport:
                    continue
                if _flt.sch_dep_time < _pnr.sch_start_time:
                    continue
                _pnr.candidate_itineraries.append(flt_id)

    # @classmethod
    # def organize_info(cls):
    #     disruption_allPNRs = {}
    #     for pnr_id, pnr_info in PNR.allPNRs.items():
    #         if pnr_info.disruption == DisruptionType.NoDisruption:
    #             continue
    #         temp = pnr_id
    #         disruption_allPNRs[temp] = pnr_info
    #

    def optimize(self):
        try:
            # 创建模型
            model = gp.Model()

            # model.setParam("OutputFlag", 0)

            start_time = time.time()

            J = 3  # 座位等级数量

            # 需用到的前置参数
            # 创建 参数 类的实例
            pnr_instance = Parameter()

            # 调用 organize_pnr_info 方法以获取数据结构
            p_allPNRs, I, As, itineraries_list = pnr_instance.organize_pnr_info()
            priority_level = Parameter.priority_level
            # p_allPNRs 所有遭遇不正常航班现象的乘客组信息
            # I 可接受新乘客的行程(对于不同乘客组)
            # itineraries_list 所有乘客组的可用航班信息
            # As（Availability_seats） 所有用于恢复航班的可用座位数量信息
            # priority_level 乘客优先级指数字典信息

            c_t = Parameter.c_t  # 不同舱位的单位时间恢复成本/h
            c_c = Parameter.c_c  # 不同舱位的平均单张票价
            c_f = Parameter.c_f  # 航段数量变化补偿/航段
            c_cal = Parameter.c_cal  # 航班取消额外补偿/人

            # 创建决策变量
            x = {}
            y = {}
            for p in p_allPNRs.keys():
                for i in I[p]:
                    for j in range(1, J + 1):
                        x[p, i, j] = model.addVar(vtype=GRB.BINARY, name=f'x_{p}_{i}_{j}')
                y[p] = model.addVar(vtype=GRB.BINARY, name=f'y_{p}')

            # 添加约束
            # 乘客要么被取消行程要么完成恢复过程
            for p in p_allPNRs.keys():
                for i in I[p]:
                    for j in range(1, J + 1):
                        model.addConstr(x[p, i, j] + y[p] == 1)

            # 得到恢复的乘客数量不能超过现有的座位数量
            seats_required = {}  # 每个航班不同舱位等级的座位需求
            for i in itineraries_list:
                for j in range(1, J + 1):
                    # 初始化座位需求为0
                    seats_required[(i, j)] = 0
                    # 检查并添加非零项
                    for p in p_allPNRs.keys():
                        if (p, i, j) in x:
                            seats_required[(i, j)] += x[p, i, j] * p_allPNRs[p].num_pax

            # 添加约束条件，确保每个航班和舱位等级的座位数不超过可用座位数量
            for i in itineraries_list:
                for j in range(1, J + 1):
                    model.addConstr(seats_required[i, j] <= As[i, j], name=f"SeatsConstraint_{i}_{j}")

            # 一个乘客组只能被分配在某一行程的某一等级座位上
            for p in p_allPNRs.keys():
                model.addConstr(gp.quicksum(x[p, i, j] for i in I[p] for j in range(1, J + 1)) <= 1)

            # 乘客组的起始地点必须保持一致
            for p in p_allPNRs.keys():
                for i in I[p]:
                    # if p_allPNRs[p].current_airport != Flight.allFlights[i].sch_dep_airport:
                    if p_allPNRs[p].start_airport != Flight.allFlights[i].act_dep_airport:
                        for j in range(1, J + 1):
                            model.addConstr(x[p, i, j] == 0)

            # 乘客组的延误时间控制在12h以内
            for p in p_allPNRs.keys():
                for i in I[p]:
                    # import ipdb; ipdb.set_trace()
                    if (Flight.allFlights[i].sch_dep_time - p_allPNRs[p].current_start_time).total_seconds()/3600 > 12:
                        for j in range(1, J + 1):
                            model.addConstr(x[p, i, j] == 0)

            # 设置目标函数
            cost_expr = gp.LinExpr()  # 乘客组恢复成本目标函数
            # 乘客恢复的时间延误补偿
            for p in p_allPNRs.keys():
                for i in I[p]:
                    for j in range(1, J + 1):
                        # import ipdb; ipdb.set_trace()
                        cost_expr += \
                            (Flight.allFlights[i].sch_arr_time - p_allPNRs[p].sch_end_time).total_seconds()/3600 *\
                            c_t[j] * PNR.allPNRs[p].num_pax * x[p, i, j] * priority_level[p]

            # 乘客恢复的舱位变化补偿
            for p in p_allPNRs.keys():
                for i in I[p]:
                    for j in range(1, J + 1):
                        # import ipdb; ipdb.set_trace()
                        if p_allPNRs[p].cabin == j:
                            cost_expr += 0
                        else:
                            tmp = (c_c[j] - p_allPNRs[p].average_fare) * p_allPNRs[p].num_pax * priority_level[p]
                            tmp = (tmp ** 2) ** 0.5
                            tmp = tmp * x[p, i, j]
                            cost_expr += tmp

                        # cost_expr += abs((c_c[j] - p_allPNRs[pnr_ids[p - 1]].average_fare) * p_allPNRs[pnr_ids[p - 1]].num_pax * x[p, i, j] * df[df[0] == pnr_ids[p - 1]].iloc[0, -1])

            # 乘客恢复的航段数量变化补偿
            # for p in range(1, P + 1):
            #     for i in range(1, I + 1):
            #         for j in range(1, J + 1):
            #             cost_expr += (len(p_allPNRs[pnr_ids[p - 1]].flights) - len(PNR.allPNRs[pnr_ids[p - 1]].boarded_flights) - 1) * c_f * PNR.allPNRs[pnr_ids[p - 1]].num_pax * x[p, i, j] * df[df[0] == pnr_ids[p - 1]].iloc[0, -1]

            # 行程取消成本之和
            CancellationCost = 0
            for p in p_allPNRs.keys():
                CancellationCost += p_allPNRs[p].num_pax * (PNR.allPNRs[p].average_fare + c_cal) * y[p]

            cost_expr += CancellationCost  # 乘客恢复总成本

            model.setObjective(cost_expr, GRB.MINIMIZE)

            # 求解模型
            model.optimize()

            end_time = time.time()

            import ipdb; ipdb.set_trace()

            print('solve_time', end_time - start_time)

            # 在模型求解后，获取决策变量的值
            if model.status == GRB.OPTIMAL:
                solution = {}
                for p in p_allPNRs.keys():
                    for i in I[p]:
                        for j in range(1, J + 1):
                            solution[p, i, j] = x[p, i, j].x
                # 现在，solution 字典包含了决策变量的具体值
            else:
                print("No solution found.")

            # 初始化计数器
            count_x_0 = 0  # 0值的x[p, i, j]的数量
            count_x_1 = 0  # 1值的x[p, i, j]的数量
            count_y_0 = 0  # 0值的y[p]的数量
            count_y_1 = 0  # 1值的y[p]的数量

            # 遍历决策变量并统计数量
            for p in p_allPNRs.keys():
                for i in itineraries_list:
                    for j in range(1, J + 1):
                        if (p, i, j) in x:
                            if x[p, i, j].x == 0:
                                count_x_0 += 1
                            elif x[p, i, j].x == 1:
                                count_x_1 += 1

                if y[p].x == 0:
                    count_y_0 += 1
                elif y[p].x == 1:
                    count_y_1 += 1

            # 数量信息
            categories = ['x[p, i, j] with value 0', 'x[p, i, j] with value 1', 'y[p] with value 0',
                          'y[p] with value 1']
            counts = [count_x_0, count_x_1, count_y_0, count_y_1]

            # 创建条形图
            fig, ax = plt.subplots()
            bars = plt.bar(categories, counts)
            plt.xlabel("Categories")
            plt.ylabel("Counts")
            plt.title("Counts of Decision Variables(200)")

            # 在柱状的顶部显示具体的数量信息
            for bar, count in zip(bars, counts):
                ax.annotate(str(count), xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                            xytext=(0, 3), textcoords='offset points', ha='center', va='bottom')

            # 调整x轴标签的显示
            plt.xticks(rotation=15, ha="right")

            plt.tight_layout()
            plt.show()

            if model.Status == gp.GRB.Status.INFEASIBLE:
                model.computeIIS()
                model.write("model.ilp")

            print(f"Optimal cost = {model.Objval}")

        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()  # 输出错误栈信息，包括代码行的位置
