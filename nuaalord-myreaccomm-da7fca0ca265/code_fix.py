import numpy as np
import pandas as pd
from pnr import *
from flight import *
from write import *
from parameter import *
import random
import os

# # 定义文件路径
# file_path = 'D:/研究生/论文写作/PR_TEST_OLD/nuaalord-myreaccomm-da7fca0ca265/data/pnrData.csv'

# # 读取CSV文件
# data = pd.read_csv(file_path, header=None)
#
# # 假设您想要乘的两列是 'column1' 和 'column2'
# # 乘这两列并求和
# result = (data[1] * (data[2] + 50)).sum()
#
# print(result)

# # 创建判断矩阵
# A = np.array([
#     [1, 1 / 2, 1 / 7],
#     [2, 1, 1 / 3],
#     [7, 3, 1]
# ])
#
# # 计算特征值和特征向量
# eigenvalues, eigenvectors = np.linalg.eig(A)
#
# # 获取最大特征值（Eigenvalue）
# lambda_max = max(eigenvalues)
#
# # 计算一致性指数（CI）
# n = A.shape[0]  # 矩阵大小
# CI = (lambda_max - n) / (n - 1)
#
# # 随机一致性指数（RI），对于4x4矩阵，通常为0.9
# RI = 0.9
#
# # 计算一致性比率（CR）
# CR = CI / RI
#
# print("最大特征值：", lambda_max)
# print("一致性指数（CI）：", CI)
# print("一致性比率（CR）：", CR)
#
# # 检查是否通过一致性检验
# if CR <= 0.1:
#     print("通过一致性检验")
# else:
#     print("未通过一致性检验，需要重新调整判断矩阵")

# candidate_itineraries = []
# my_dict = {"apple": 1, "banana": 2, "cherry": 3}
#
# for key, value in my_dict.items():
#     candidate_itineraries.append(key)
#     print(key)
#
# for i in candidate_itineraries():
#     print(i)

# # 导入枚举类型
# from enum import Enum
#
# # 枚举类型 <Cabin>，请根据实际情况替换为你的枚举类型
# class Cabin(Enum):
#     Y = 1
#     J = 2
#     F = 3
#
# # 给定的字典
# cabin_data = {Cabin.J: 0, Cabin.Y: 9, Cabin.F: 0}
#
# # 读取字典中的数据
# # for cabin, count in cabin_data.items():
# #     print(f"舱位等级 {cabin.name} 的数量为 {count}")
#
# for i in Cabin:
#     print(i.value)
#     # print(type(i.name))
#
# print(Cabin['Y'].value)

# # 创建一个空列表
# my_list = []
#
# list_1 = [1, 2, 3, 4]
# list_2 = [4, 5, 6, 7]
# list_3 = [7, 8, 9, 1]
#
# all_itineraries = []
# # 将三个列表循环加入空列表
# for lst in [list_1, list_2, list_3]:
#     all_itineraries += lst
# print(all_itineraries)
#
# itineraries_list = []
# for list_element in all_itineraries:
#     print(list_element)
#     if list_element not in itineraries_list:
#         itineraries_list.append(list_element)
#
# print(itineraries_list)

# # 读取CSV文件
# df = pd.read_csv('data/pnrData_all_test.csv', usecols=[0, 10], header=None)
#
# # 使用to_dict()将数据提取到字典中
# data_dict = df.set_index(0)[10].to_dict()
#
# # 打印字典
# print(data_dict)

# 创建 A 类的实例
# a_instance = Parameter()
#
# # 调用 organize_pnr_info 方法以获取数据结构
# p_allPNRs, I, As, itineraries_list = a_instance.organize_pnr_info()
#
# priority_level = Parameter.priority_level
#
# c_t = Parameter.c_t  # 不同舱位的单位时间恢复成本/h
# c_c = Parameter.c_c  # 不同舱位的平均单张票价
# c_f = Parameter.c_f  # 航段数量变化补偿/航段
# c_cal = Parameter.c_cal  # 航班取消额外补偿/人
#
# # import ipdb; ipdb.set_trace()
#
# print(len(p_allPNRs))


# 读取dat文件
with open('./data/availability.dat', 'r', newline="") as file:
    lines = file.readlines()

# 创建一个新的dat文件来存储生成的数据
with open('data/output.dat', 'w') as output_file:
    for line in lines:
        parts = line.split(',')
        if len(parts) >= 2:
            cabin_class = parts[1]
            total_seats = 0

            if cabin_class == 'Y':
                # 生成经济舱座位数量
                total_seats = random.randint(150, 250)
            elif cabin_class == 'J':
                # 生成商务舱座位数量
                total_seats = random.randint(15, 45)
            elif cabin_class == 'F':
                # 生成头等舱座位数量
                total_seats = random.randint(5, 10)

            used_seats = random.randint(0, total_seats)

            # 更新第5和第6列的数据
            parts[4] = str(total_seats)
            parts[5] = str(used_seats)

            # 将修改后的行写入新文件
            output_line = ",".join(parts)
            print(output_line)
            output_file.write(output_line)

# 关闭文件

