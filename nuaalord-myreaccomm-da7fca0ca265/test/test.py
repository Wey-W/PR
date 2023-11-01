import os
import csv
import random
import numpy as np
import pandas as pd
import scipy.stats as stats
from pre_pnr import *
from datetime import datetime

allData = {}  # 原始航班数据字典
test_list = [1, 2, 3, 4, 5, 6, 7, 8]

orig_data = os.path.join(os.getcwd(), "../data", "test.dat")
avail_data = os.path.join(os.getcwd(), "../data", "sup_test.dat")
file_Name = "../data/pnrData.dat"
pnr_data = os.path.join(os.getcwd(), "../data", "pnrData.csv")
schedule_data = os.path.join(os.getcwd(), "../data", "schedule.dat")
new_PNRFlights_Name = "data\\pnrFlightsOutData.csv"
# with open(orig_data, 'r', newline="") as csv_in_file:
#     file_reader = csv.reader(csv_in_file, delimiter=',')
#     for row in file_reader:
#         r = dict(flt_id=row[0], act_dep_airport=row[1], act_arr_airport= row[2], flt_number=row[4],
#              sch_dep_time=datetime.fromtimestamp(int(row[10])), sch_arr_time=datetime.fromtimestamp(int(row[11])),
#              act_dep_time=datetime.fromtimestamp(int(row[12])), act_arr_time=datetime.fromtimestamp(int(row[13])),
#              sch_dep_airport=row[23], sch_arr_airport=row[24], depCode=row[33], arrCode=row[34], status=row[39])
#         allData[r['flt_id']] = r
""" 生成一个指定长度的随机乘客id """
def generate_random_str(randomlength):
    random_str = ''
    base_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


def get_bool_prob(pnr_data, i, j):  # 计数存在问题，与数据相比少一行
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
# with open(avail_data, 'r', newline="") as csv_in_file:  # 将可提供恢复的航班数据从原始数据中删除，确保所有原始航班都可能出现不正常航班现象，同时整理出可提供恢复的航班关键信息
#     file_reader = csv.reader(csv_in_file, delimiter=',')
#     for row in file_reader:
#         d = dict(flt_id=row[0], cabin=row[1], capacity=row[4], booked=row[5],
#                  avail_num=max(0, int(row[4]) - int(row[5])))
#         print(d['flt_id'] + d['cabin'])
#         allData[d['flt_id'] + d['cabin']] = d
# print(allData)


# norm_dist = get_fare_bound(pnr_data, 2, 1)  # 生成原始数据的均值与标准差
# fare = np.random.normal(loc=norm_dist[0], scale=norm_dist[1], size=100)  # 根据原始数据生成呈正态分布的指定个数的新数据（平均购票价格） 第3列数据
# print(fare)

# norm_dist = get_fare_bound_test(pnr_data, 2, 1)  # 生成原始数据的均值与标准差
# fare = stats.truncnorm((norm_dist[0] - norm_dist[2]) / norm_dist[3], (norm_dist[1] - norm_dist[2]) / norm_dist[3], loc=norm_dist[2], scale=norm_dist[3])  # 根据原始数据生成呈正态分布的指定个数的新数据（平均购票价格） 第3列数据
# x = fare.rvs(100)
# print(x)
# pnrData = {}

# with open(pnr_data, 'r', newline="") as csv_in_file:
#     pnr_data = pd.read_csv(csv_in_file, header=None, delimiter=',')
#     pnr_data = pd.DataFrame(pnr_data)
#     print(pnr_data.iloc[:, 1].count())
#     print(pnr_data[1].value_counts())
#     min_num = pnr_data.iloc[:, 1].min()
#     print(min_num)
#     max_num = pnr_data.iloc[:, 1].max()
#     print(max_num)
# #
# for i in test_list:
#     while i == 1:
#         break
#     else:
#         print("problem")

# with open(pnr_data, 'r', newline="") as csv_in_file:
#     file_reader = csv.reader(csv_in_file, delimiter=',')
#     num = 0
#     for row in file_reader:
#         if row[1] == '0':
#             num += 1
#     print(num)
#
# pnrid = []
# for i in range(5):
#     pnrid.append(generate_random_str(5))  # 生成随机乘客id 第1列数据
# print(pnrid)
# num_prob = get_bool_prob(pnr_data, 3, 1)
# nums = np.random.choice([key for key in num_prob.keys()], size=100, p=[value for value in num_prob.values()]) # 根据原始数据概率生成新数据
# # print(len(num_prob.keys()))
# print(nums)

'''思路：
定义一个方法，用于读取与pnrid匹配的fltid，读取schedule中的fltid信息，提取到达地点和到达时间，根据航段数，随机选取fltid，判断地点与时间是否满足条件，
直到fltid数量与生成的航段数量相等，最终输出航程的全部fltid'''

# with open(schedule_data, 'r', newline="") as csv_in_file:  #
#     file_reader = csv.reader(csv_in_file, delimiter=',')

'''对航班信息进行筛选，整理在字典中'''
with open(schedule_data, 'r', newline="") as csv_in_file:
    file_reader = csv.reader(csv_in_file, delimiter=',')
    o_data = []
    for row in file_reader:
        r = dict(flt_id=row[0], act_dep_airport=row[1], act_arr_airport= row[2], flt_number=row[4],
             sch_dep_time=datetime.fromtimestamp(int(row[10])), sch_arr_time=datetime.fromtimestamp(int(row[11])),
             act_dep_time=datetime.fromtimestamp(int(row[12])), act_arr_time=datetime.fromtimestamp(int(row[13])),
             sch_dep_airport=row[23], sch_arr_airport=row[24], depCode=row[33], arrCode=row[34], status=row[39])
        o_data.append(list(r.values()))
    o_data = pd.DataFrame(o_data)
    o_data.columns = ['flt_id', 'act_dep_airport', 'act_arr_airport', 'flt_number', 'sch_dep_time', 'sch_arr_time', 'act_dep_time', 'act_arr_time', 'sch_dep_airport', 'sch_arr_airport', 'depCode', 'arrCode', 'status']
    flt_list_select = np.array(o_data.sample(n=1, random_state=None, axis=0)).tolist()  # 整理出的数据中随机选取一行，作为生成乘客数据的航班
    # flt_list = flt_list.tolist()

    # arr_airport = flt_list_select[0][2]
    # arr_time = flt_list_select[0][7]
    # avail_list = o_data[o_data['act_dep_airport'].isin([arr_airport])]  # 筛选出机场条件符合的航班数据
    # # print(avail_list)
    # avail_list = avail_list[avail_list['act_arr_time'] > arr_time]  # 筛选出时间条件符合的航班数据
    # print(avail_list)


    # print(flt_list_select[0][1])
    # flt_num = random.choice(list(flt_list.loc[:, 'flt_number']))  # 得到航班乘客数量信息，传入指定方法以生成指定的乘客数据
    # print(flt_num)

    # print(o_data)

        # r = pd.DataFrame.from_dict(r, orient='index').T
        # r = pd.DataFrame(r, index=[0])

        # print(r)


        # allData[r['flt_id']] = r  # 同一id的航班信息会被后续信息替换，想办法不进行替换，单纯进行信息提取，更改键值对


'''定义方法进行多航段航班选取'''
def get_all_flt_id(flt_pnr_list, orig_data):  # 传入原始列表值
    new_pnr_flt = []
    flt_num = flt_pnr_list[2]
    pnr_id = flt_pnr_list[1]
    new_pnr_flt.append(flt_pnr_list)

    while flt_num > len(new_pnr_flt):
        i = len(new_pnr_flt)
        prev_flt_id = new_pnr_flt[i-1][0]
        prev_flt = (orig_data.loc[orig_data['flt_id'] == str(prev_flt_id)]).values.tolist()
        prev_arr_airport = prev_flt[0][2]
        prev_arr_time = prev_flt[0][7]
        avail_list = orig_data[orig_data['act_dep_airport'].isin([prev_arr_airport])]  # 筛选出机场条件符合的航班数据
        # print(avail_list)
        avail_list = avail_list[avail_list['act_arr_time'] > prev_arr_time]  # 筛选出同时符合时间条件的航班数据
        # print(avail_list)
        latter_flt = np.array(o_data.sample(n=1, random_state=None, axis=0)).tolist()
        latter_flt = [latter_flt[0][0], pnr_id, i+1]
        new_pnr_flt.append(latter_flt)


    # arr_airport = flt_list_select[0][2]
    # arr_time = flt_list_select[0][7]
    # for p in flt_list:
    #
    #
    # new_flt_id = flt_list[0][0]
    # new_pnr_num = flt_list[0][3]
    # dep_airport = flt_list[0][1]
    # arr_airport = flt_list[0][2]
    # arr_time = flt_list[0][7]
    #
    # NEW_PNR_ALL = generate_pnr(new_pnr_num)  # 生成一个dataframe形式的新乘客数据表
    # for new_pnr in NEW_PNR_ALL.itertuples():
    #     a = [getattr(new_pnr, 'PNR_id'), getattr(new_pnr, 'flt_num')]
    #     new_pnr_flt.append(a)  # 列表信息为新pnrid与对应的航段数
    #     for p in new_pnr_flt:
    #         PNRFlt_pnr_id = p[0]
    #         PNRFlt_num = p[1]
    #         get_PNRFlt_info(PNRFlt_num, PNRFlt_pnr_id, new_flt_id)

    return new_pnr_flt




# def get_PNRFlt_info(num, pnr_id, flt_id):
#     pnrflt_info = []
#     while num == 1:
#         pnrflt_info.append([pnr_id, flt_id, num])
#     else:


from data_output import generate_pnr
flt_nums = []
pnr_flt = []

new_flt_id = flt_list_select[0][0]
new_pnr_num = flt_list_select[0][3]
# print(int(new_pnr_num))
dep_airport = flt_list_select[0][1]
arr_airport = flt_list_select[0][2]
arr_time = flt_list_select[0][7]
#
# for i in range(20):
#     flt_nums.append(random.choice([1, 2, 3, 4]))
# print(flt_nums)
pnr_info = generate_pnr(int(200))
for row in pnr_info.itertuples():
    a = [getattr(row, 'PNR_id'), getattr(row, 'flt_num')]
    flt_nums.append(a)

for p in flt_nums:
    p.insert(0, new_flt_id)
# print(flt_nums)

for p in flt_nums:
    flt_num = p[2]
    if flt_num == 1:
        pnr_flt.append(p)
    else:
        pnr_flt_multi = get_all_flt_id(p, o_data)
        for q in pnr_flt_multi:
            pnr_flt.append(q)

pnr_flt = pd.DataFrame(pnr_flt, columns=['flt_id', 'pnr_id', 'flt_num'])
print(pnr_flt)
pnr_flt.to_csv(new_PNRFlights_Name, sep=',', header=False, index=False)

'''随机选取schedule中的一趟航班，根据航班可乘人数生成乘客数据，将乘客数据中的航段数作为关键信息，
进行判断，如果为1，则直接存储pnrid， fltid， 航段数三个数据，如果不为1，则判断当前航班信息数量与
航段数量是否一致，不一致则在已有全部schedule中筛选出起始机场与起始时间满足条件的航班数据，从中选取
一架航班作为后序航班，将相关信息记录储存，直到航程数量得到满足，最终得到所有乘客组的航程航班数据。'''