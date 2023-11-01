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

list_0 = []
list_1 = ['23494930', 'CZKFX', 4]
list_2 = ['23494930', 'ZMCIS', 1]

list_0.append(list_1)
list_0.append(list_2)
print(list_0)
print(len(list_0))
print(list_1[2])


'''定义方法进行多航段航班选取'''
def get_all_flt_id(flt_pnr_list, orig_data, select_flt):  # 传入原始列表值
    new_pnr_flt = []
    flt_num = flt_pnr_list[2]
    pnr_id = flt_pnr_list[1]
    new_pnr_flt.append(flt_pnr_list)
    i = len(new_pnr_flt)
    while flt_num > i:
        prev_flt_id = new_pnr_flt[i-1][0]
        prev_flt = (orig_data.loc[orig_data['flt_id'] == prev_flt_id]).values.tolist()
        prev_arr_airport = prev_flt[0][2]
        prev_arr_time = prev_flt[0][7]
        avail_list = orig_data[orig_data['act_dep_airport'].isin([prev_arr_airport])]  # 筛选出机场条件符合的航班数据
        # print(avail_list)
        avail_list = avail_list[avail_list['act_arr_time'] > prev_arr_time]  # 筛选出同时符合时间条件的航班数据
        # print(avail_list)
        latter_flt = np.array(o_data.sample(n=1, random_state=None, axis=0)).tolist()
        latter_flt = [latter_flt[0], pnr_id, i+1]
        new_pnr_flt.append(latter_flt)


'''对航班信息进行筛选，整理在字典中'''
with open(schedule_data, 'r', newline="") as csv_in_file:
    file_reader = csv.reader(csv_in_file, delimiter=',')
    o_data = []
    for row in file_reader:
        r = dict(flt_id=row[0], act_dep_airport=row[1], act_arr_airport=row[2], flt_number=row[4],
                 sch_dep_time=datetime.fromtimestamp(int(row[10])), sch_arr_time=datetime.fromtimestamp(int(row[11])),
                 act_dep_time=datetime.fromtimestamp(int(row[12])), act_arr_time=datetime.fromtimestamp(int(row[13])),
                 sch_dep_airport=row[23], sch_arr_airport=row[24], depCode=row[33], arrCode=row[34], status=row[39])
        o_data.append(list(r.values()))
    o_data = pd.DataFrame(o_data)
    o_data.columns = ['flt_id', 'act_dep_airport', 'act_arr_airport', 'flt_number', 'sch_dep_time', 'sch_arr_time',
                      'act_dep_time', 'act_arr_time', 'sch_dep_airport', 'sch_arr_airport', 'depCode', 'arrCode',
                      'status']

    prev_flt_id = list_0[0][0]
    print(prev_flt_id)
    latter_flt = (o_data.loc[o_data['flt_id'] == str(prev_flt_id)]).values.tolist()
    print(latter_flt[0][2])
