from pnr import *
from flight import *
import pandas as pd


class Parameter:
    # 直接设定的前置参数
    c_t = {1: 25, 2: 50, 3: 100}  # 不同舱位的单位时间恢复成本/h
    c_c = {1: 300, 2: 800, 3: 1200}  # 不同舱位的平均单张票价
    c_f = 100  # 航段数量变化补偿/航段
    c_cal = 50  # 航班取消额外补偿/人

    # 读取文件后将乘客优先级数据提取到字典中（键值对pnr_id - priority_index）
    df = pd.read_csv('./data/pnrData_all_test.csv', usecols=[0, 10], header=None)
    priority_level = df.set_index(0)[10].to_dict()

    # 整理归纳后便于求解的部分参数

    def organize_pnr_info(self):
        from pnr import PNR

        p_allPNRs = {}  # 所有遭遇不正常航班现象的乘客组（键值对：pnr_id - pnr_info）
        for pnr_id, pnr_info in PNR.allPNRs.items():
            if pnr_info.disruption == DisruptionType.NoDisruption:
                continue
            temp = pnr_id
            p_allPNRs[temp] = pnr_info

        I = {}  # 所有遭遇不正常航班现象的乘客组的可用恢复航班（键值对：pnr_id - flt_id）
        for p, i in p_allPNRs.items():
            I[p] = i.candidate_itineraries

        # 所有乘客组的可用航班信息汇总
        all_itineraries = []  # 存在重复flt_id的航班汇总
        for _pnr in p_allPNRs.values():
            all_itineraries += _pnr.candidate_itineraries
            # print(all_itineraries)
        itineraries_list = []  # 去重后的全部航班flt_id信息
        for list_element in all_itineraries:
            if list_element not in itineraries_list:
                itineraries_list.append(list_element)

        # Availability_seats 所有用于恢复的航班的可用座位数量信息
        # import ipdb; ipdb.set_trace()
        As = {(i, j.value): Flight.allFlights[i].availability[j.value] for i in itineraries_list for j in Cabin}

        return p_allPNRs, I, As, itineraries_list
