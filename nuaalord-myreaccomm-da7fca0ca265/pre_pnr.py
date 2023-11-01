
import os
import csv
import numpy as np
import pandas as pd

file_Name = "data\\pnrData.csv"
pnr_data = os.path.join(os.getcwd(), "data", "passengers.dat")
pnrData = os.path.join(os.getcwd(), "data", "pnrData_pre.csv")
schedule_data = os.path.join(os.getcwd(), "data", "schedule.dat")


def get_fare_bound(pnr_data, i, j):  # 分别传入数据文件、目标列指数、人数信息列指数
    with open(pnr_data, 'r', newline="") as csv_in_file:
        pnr_data = pd.read_csv(csv_in_file, header=None, delimiter=',')
        pnr_data = pd.DataFrame(pnr_data)
        mean_fare = pnr_data.iloc[:, i].mean()  # 计算均值
        standard_dif = (pnr_data.iloc[:, i].max() - mean_fare)/3  # 计算标准差
        return [mean_fare, standard_dif]


def get_bool_prob(pnr_data, i, j):  #
    num_prob = {}
    with open(pnr_data, 'r', newline="") as csv_in_file:
        pnr_data = pd.read_csv(csv_in_file, header=None, delimiter=',')
        pnr_data = pd.DataFrame(pnr_data)
        pnr_num = pnr_data.iloc[:, i].count()
        min_num = pnr_data.iloc[:, i].min()
        max_num = pnr_data.iloc[:, i].max()
        for num in range(min_num, max_num+1):
            num_prob[num] = float(list(pnr_data[i]).count(num) / pnr_num)
        return num_prob


'''数据预处理，读取原文件后经过筛选生成关键数据文件'''  # pnr数据
with open(pnr_data, 'r', newline="") as csv_in_file:
    pnr_data = pd.read_csv(csv_in_file, header=None, delimiter=',')
    pnr_data = pd.DataFrame(pnr_data)
    pnr_use_data = pnr_data.drop(columns=[2, 5, 6, 8, 9, 10, 11, 12, 13], axis=1, inplace=False)  # 对数据进行筛选，提取所需的关键数据信息，不改变原数据文件
    pnr_use_data.columns = ['PNR_id', 'pnr_num', 'average_fare', 'freqFlyer', 'minor', 'staff']
    pnr_use_data['freqFlyer'] = pnr_use_data['freqFlyer'].str.replace('TrueBlue', '1')  # 替换会员文字信息为数值信息  1
    pnr_use_data['freqFlyer'] = pnr_use_data['freqFlyer'].str.replace('Mosaic', '2')  # 替换会员文字信息为数值信息  1
    pnr_use_data = pnr_use_data.fillna({'freqFlyer': 0})  # 替换会员文字信息缺失值  0
    pnr_use_data.to_csv(file_Name, sep=',', header=False, index=False)
    # print(pnr_use_data)


'''数据预处理，读取原文件后经过筛选生成关键数据文件'''  # schedule数据
# with open(schedule_data, 'r', newline="") as csv_in_file:
#     schedule_data = pd.read_csv(csv_in_file, header=None, delimiter=',')
#     schedule_data = pd.DataFrame(schedule_data)
#     pnr_use_data = pnr_data.drop(columns=[2, 5, 6, 8, 9, 10, 11, 12, 13], axis=1, inplace=False)  # 对数据进行筛选，提取所需的关键数据信息，不改变原数据文件
#     pnr_use_data.columns = ['PNR_id', 'pnr_num', 'average_fare', 'freqFlyer', 'minor', 'staff']
#     pnr_use_data['freqFlyer'] = pnr_use_data['freqFlyer'].str.replace('TrueBlue', '1')  # 替换会员文字信息为数值信息  1
#     pnr_use_data['freqFlyer'] = pnr_use_data['freqFlyer'].str.replace('Mosaic', '2')  # 替换会员文字信息为数值信息  1
#     pnr_use_data = pnr_use_data.fillna({'freqFlyer': 0})  # 替换会员文字信息缺失值  0
#     pnr_use_data.to_csv(file_Name, sep=',', header=False, index=False)
#     # print(pnr_use_data)

def get_fare_bound_test(pnr_data, i, j):  # 分别传入数据文件、目标列指数、人数信息列指数
    with open(pnr_data, 'r', newline="") as csv_in_file:
        pnr_data = pd.read_csv(csv_in_file, header=None, delimiter=',')
        pnr_data = pd.DataFrame(pnr_data)
        data_min = pnr_data.iloc[:, i].min()
        data_max = pnr_data.iloc[:, i].max()
        mean_fare = pnr_data.iloc[:, i].mean()  # 计算均值
        standard_dif = pnr_data.iloc[:, i].std()  # 计算标准差
        return [data_min, data_max, mean_fare, standard_dif]



    # for row in file_reader:
    #     p = dict(pnr_id=row[0], num_pax=int(row[1]), crm_index=int(row[2]), average_fare=int(row[3]))
    # with open(file_Name, "a", newline="") as csv_file:  # 将筛选出的乘客信息写入新文件，但要考虑如何进行全部替换同时避免覆盖
    #     writer = csv.writer(csv_file)
    #         for value in p.items():
    #             writer.writerow([value])
    #     pnrData[p['pnr_id']] = p


# print(get_fare_bound(pnrData, 2, 1))
# print(get_bool_prob(pnrData, 1, 1))
# print(get_bool_prob(pnrData, 1, 1).keys())
# print(get_bool_prob(pnrData, 1, 1).values())

