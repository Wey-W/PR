import os
import csv
import random
import numpy as np
import scipy.stats as stats
from datetime import datetime
from pre_pnr import *

allData = {}  # 原始航班数据字典
availData = {}  # 提供旅客恢复的航班数据字典
new_PNRData_Name = "data\\pnrOutData.csv"
# orig_data = os.path.join(os.getcwd(), "data", "schedule.dat")
# avail_data = os.path.join(os.getcwd(), "data", "availability.dat")
orig_data = os.path.join(os.getcwd(), "data", "test.dat")
avail_data = os.path.join(os.getcwd(), "data", "sup_test.dat")
pnr_data = os.path.join(os.getcwd(), "data", "pnrData.csv")

""" 生成一个指定长度的随机乘客id """
def generate_random_str(randomlength):
    random_str = ''
    base_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


def generate_pnr(demand_num):
    pnrid = []  # 第1列数据
    flt_nums = []  # 尾列数据
    for i in range(demand_num):
        pnrid.append(generate_random_str(5))  # 生成随机乘客id
        flt_nums.append(random.choice([1, 2, 3, 4]))
    num_prob = get_bool_prob(pnr_data, 1, 1)
    nums = np.random.choice([key for key in num_prob.keys()], size=demand_num,
                            p=[value for value in num_prob.values()])  # 根据原始数据概率生成pnr组人数新数据  第2列数据
    norm_dist = get_fare_bound_test(pnr_data, 2, 1)  # 生成原始数据的均值与标准差
    fare = stats.truncnorm((norm_dist[0] - norm_dist[2]) / norm_dist[3], (norm_dist[1] - norm_dist[2]) / norm_dist[3],
                           loc=norm_dist[2], scale=norm_dist[3])  # 根据原始数据生成呈正态分布的指定个数的新数据（平均购票价格） 第3列数据
    fare = fare.rvs(demand_num)
    member_status = get_bool_prob(pnr_data, 3, 1)
    vip = np.random.choice([key for key in member_status.keys()], size=demand_num,
                           p=[value for value in member_status.values()])  # 根据原始数据概率生成会员乘客 第4列数据

    new_pnr_data = pd.DataFrame({'PNR_id': pnrid, 'pnr_num': nums, 'average_fare': fare, 'freqFlyer': vip, 'flt_num': flt_nums})
    return new_pnr_data


'''对航班信息进行筛选，整理在字典中'''
with open(orig_data, 'r', newline="") as csv_in_file:
    file_reader = csv.reader(csv_in_file, delimiter=',')
    for row in file_reader:
        r = dict(flt_id=row[0], act_dep_airport=row[1], act_arr_airport= row[2], flt_number=row[4],
             sch_dep_time=datetime.fromtimestamp(int(row[10])), sch_arr_time=datetime.fromtimestamp(int(row[11])),
             act_dep_time=datetime.fromtimestamp(int(row[12])), act_arr_time=datetime.fromtimestamp(int(row[13])),
             sch_dep_airport=row[23], sch_arr_airport=row[24], depCode=row[33], arrCode=row[34], status=row[39])
        allData[r['flt_id']] = r  # 同一id的航班信息会被后续信息替换，想办法不进行替换，单纯进行信息提取，更改键值对


'''将可提供恢复的航班数据从原始数据中删除，确保所有原始航班都可能出现不正常航班现象，同时整理出可提供恢复的航班关键信息'''
with open(avail_data, 'r', newline="") as csv_in_file:
    file_reader = csv.reader(csv_in_file, delimiter=',')
    avail_list = []
    for row in file_reader:
        flight = allData.get(row[0])  # 当由于舱位等级不同重复出现同一航班id时，可提供恢复航班列表会出现错误信息
        if not flight:  # 能够在两个文件中匹配的航班才是能够提供恢复的航班，将它的对应信息提取出来，并将航班从生成乘客的航班列表中删除
            continue
        d = dict(flt_id=row[0], cabin=row[1], capacity=row[4], booked=row[5],
                 avail_num=max(0, int(row[4]) - int(row[5])))
        availData[d['flt_id'] + d['cabin']] = d  # 需要确保同id航班不同舱位等级的信息被独立保存
        avail_list.append(row[0])  # 所有可提供恢复的航班id列表

avail_list = list(set(avail_list))  # 排除重复id
for i in avail_list:  # 删除可进行恢复航班
    allData.pop(i)

print(availData)  # 可提供旅客恢复的航班列表及对应舱位等级
print(avail_list)  # 提供旅客恢复的航班列表（去除重复id）
print(allData)  # 所有用于生成乘客数据的航班列表
# NEW_PNR = generate_pnr(100)
# print(NEW_PNR)
# generate_pnr(100).to_csv(new_PNRData_Name, sep=',', header=False, index=False)




