import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class GM_1_1:

    def __init__(self):
        self.test_data = np.array(())  # 实验数据集
        self.add_data = np.array(())  # 一次累加产生数据
        self.argu_a = 0  # 参数a
        self.argu_b = 0  # 参数b
        self.MAT_B = np.array(())  # 矩阵B
        self.MAT_Y = np.array(())  # 矩阵Y
        self.modeling_result_arr = np.array(())  # 对实验数据的拟合值
        self.P = 0  # 小误差概率
        self.C = 0  # 后验方差比值

    def set_model(self, arr: list):
        self.__acq_data(arr)
        self.__compute()
        self.__modeling_result()

    def __acq_data(self, arr: list):  # 构建并计算矩阵B和矩阵Y
        self.test_data = np.array(arr).flatten()
        add_data = list()
        sum = 0
        for i in range(len(self.test_data)):
            sum = sum + self.test_data[i]
            add_data.append(sum)
        self.add_data = np.array(add_data)
        ser = list()
        for i in range(len(self.add_data) - 1):
            temp = (-1) * ((1 / 2) * self.add_data[i] + (1 / 2) * self.add_data[i + 1])
            ser.append(temp)
        B = np.vstack((np.array(ser).flatten(), np.ones(len(ser), ).flatten()))
        self.MAT_B = np.array(B).T
        Y = np.array(self.test_data[1:])
        self.MAT_Y = np.reshape(Y, (len(Y), 1))

    def __compute(self):  # 计算灰参数 a,b
        temp_1 = np.dot(self.MAT_B.T, self.MAT_B)
        temp_2 = np.matrix(temp_1).I
        temp_3 = np.dot(np.array(temp_2), self.MAT_B.T)
        vec = np.dot(temp_3, self.MAT_Y)
        self.argu_a = vec.flatten()[0]
        self.argu_b = vec.flatten()[1]

    def __predict(self, k: int) -> float:  # 定义预测计算函数
        part_1 = 1 - pow(np.e, self.argu_a)
        part_2 = self.test_data[0] - self.argu_b / self.argu_a
        part_3 = pow(np.e, (-1) * self.argu_a * k)
        return part_1 * part_2 * part_3

    def __modeling_result(self):  # 获得对实验数据的拟合值
        ls = [self.__predict(i + 1) for i in range(len(self.test_data) - 1)]
        ls.insert(0, self.test_data[0])
        self.modeling_result_arr = np.array(ls)

    def predict(self, number: int) -> list:  # 外部预测接口，预测后指定个数的数据
        prediction = [self.__predict(i + len(self.test_data)) for i in range(number)]
        return prediction

    def precision_evaluation(self):  # 模型精度评定函数
        error = [
            self.test_data[i] - self.modeling_result_arr[i]
            for i in range(len(self.test_data))
        ]
        aver_error = sum(error) / len(error)
        aver_test_data = np.sum(self.test_data) / len(self.test_data)
        temp1 = 0
        temp2 = 0
        for i in range(len(error)):
            temp1 = temp1 + pow(self.test_data[i] - aver_test_data, 2)
            temp2 = temp2 + pow(error[i] - aver_error, 2)
        square_S_1 = temp1 / len(self.test_data)
        square_S_2 = temp2 / len(error)
        self.C = np.sqrt(square_S_2) / np.sqrt(square_S_1)
        ls = [i
              for i in range(len(error))
              if np.abs(error[i] - aver_error) < (0.6745 * np.sqrt(square_S_1))
              ]
        self.P = len(ls) / len(error)
        print("精度指标P,C值为：", self.P, self.C)

    def plot(self):  # 绘制实验数据拟合情况（粗糙绘制，可根据需求自定义更改）
        plt.figure()
        plt.plot(self.test_data, marker='*', c='b', label='row value')
        plt.plot(self.modeling_result_arr, marker='^', c='r', label='fit value')
        plt.legend()
        plt.grid()
        plt.xlabel('Time')
        plt.ylabel('Temperature')
        return plt


if __name__ == "__main__":
    GM = GM_1_1()
    x = [1.6138, 1.6314, 1.7130, 1.9387, 2.1723, 2.3126, 2.6702, 3.0603, 3.1244, 3.5639, 4.0818]
    GM.set_model(x)
    print("模型拟合数据为：", GM.modeling_result_arr)
    GM.precision_evaluation()
    print("后两个模型预测值为：", GM.predict(10))
    a = []
    a = GM.predict(10)
    c = pd.DataFrame(a)

    p = GM.plot()
    p.show()
#
# import numpy as np
# import math as mt
# import matplotlib.pyplot as plt
#
#
# X0 = [1.6138, 1.6314, 1.7130, 1.9387, 2.1723, 2.3126, 2.6702, 3.0603, 3.1244, 3.5639, 4.0818]  # 原始输入数列数据（至少4年数据）
# for i in range(len(X0)-1):
#     l = X0[i]/X0[i+1]
#     if l <= mt.exp(-2/(len(X0)+1)) or l >= mt.exp(2/(len(X0)+1)):
#         break
#     else:
#         pass
# if i == len(X0)-2 and l > mt.exp(-2/(len(X0)+1)) and l < mt.exp(2/(len(X0)+1)):
#     print('级比检验通过')
# else:
#     print('级比检验不通过')
#
# # 累加数列
# X1 = [X0[0]]
# add = X0[0] + X0[1]
# X1.append(add)
# i = 2
# while i < len(X0):
#     add = add + X0[i]
#     X1.append(add)
#     i += 1
#
# # 紧邻均值序列
# Z = []
# j = 1
# while j < len(X1):
#     num = (X1[j] + X1[j - 1]) / 2
#     Z.append(num)
#     j = j + 1
#
# # 最小二乘法计算
# Y = []
# x_i = 0
# while x_i < len(X0) - 1:
#     x_i += 1
#     Y.append(X0[x_i])
# Y = np.mat(Y)
# Y = Y.reshape(-1, 1)
# B = []
# b = 0
# while b < len(Z):
#     B.append(-Z[b])
#     b += 1
# B = np.mat(B)
# B = B.reshape(-1, 1)
# c = np.ones((len(B), 1))
# B = np.hstack((B, c))
# print("B", B)
#
# # 求出参数
# alpha = np.linalg.inv(B.T.dot(B)).dot(B.T).dot(Y)
# a = alpha[0, 0]
# b = alpha[1, 0]
# print('alpha', alpha)
# print("a=", a)
# print("b=", b)
#
# # 生成预测模型
# GM = []
# GM.append(X0[0])
# did = b / a
# k = 1
# while k < len(X0):
#     GM.append((X0[0] - did) * mt.exp(-a * k) + did)
#     k += 1
#
# # 做差得到预测序列
# G = []
# G.append(X0[0])
# g = 1
# while g < len(X0):
#     G.append(round(GM[g] - GM[g - 1]))
#     g += 1
# print("预测数列为：", G)
#
# # 模型检验
# X0 = np.array(X0)
# G = np.array(G)
# e = X0 - G  #残差
# q = e / X0  # 相对误差
# w = 0
# for q_i in q:
#     w += q_i
# w = w/len(X0)
# print('精度为{}%'.format(round((1-w)*100, 2)))
#
# s0 = np.var(X0)
# s1 = np.var(e)
# S0 = mt.sqrt(s0)
# S1 = mt.sqrt(s1)
# C = S1 / S0
# print('方差比为：', C)
#
# p = 0
# for s in range(len(e)):
#     if (abs(e[s]-np.mean(e)) < 0.6745 * S1):
#         p = p + 1
# P = p / len(e)
# print('小概率误差为：', P)
#
# # 绘图
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
#
# G = [g-37315 for g in G]
# r = range(len(X0))
# t = list(r)
# plt.plot(t, X0, color='r', linestyle="--", label='true')
# plt.plot(t, G, color='b', linestyle="--", label="predict")
# plt.legend()
# plt.show()
