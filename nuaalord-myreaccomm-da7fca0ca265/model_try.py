from pnr import *
from flight import *
from write import *
import os


class Model:
    def __init__(self):  # 文件存储函数
        self.schedule_file = os.path.join(os.getcwd(), "data", "schedule.dat")   # 文件路径写入当前路径的子目录，得到的是data目录下的dat文件
        self.avail_file = os.path.join(os.getcwd(), "data", "availability.dat")
        self.pax_file = os.path.join(os.getcwd(), "data", "passengers.dat")
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
            _pnr.disruption = DisruptionType.NoDisruption  # 无延误
            prev_flt = None
            for pnr_flight in _pnr.flights:
                _flight = pnr_flight.get("flight")
                if _flight.status is False:
                    _pnr.disruption = DisruptionType.FlightCancel  # 航班取消
                    break
                if prev_flt is not None:  # 初次循环后执行
                    if _flight.act_dep_time - prev_flt.act_arr_time < timedelta(hours=1):
                        _pnr.disruption = DisruptionType.TimeMissConnect  # 时间差错
                    break
                if prev_flt is not None:  # 初次循环后执行
                    if _flight.act_dep_time - prev_flt.act_arr_time < timedelta(hours=1):
                        _pnr.disruption = DisruptionType.TimeMissConnect  # 时间差错
                    break
                prev_flt = _flight

    @classmethod
    def itinerary_generation(cls):  # 筛选出受到延误的乘客的可用恢复航班信息，储存在candidate_itineraries中
        for _pnr in PNR.allPNRs.values():
            if _pnr.disruption == DisruptionType.NoDisruption:
                continue
            # itineraries with one flight leg
            for flt_id, _flt in Flight.allFlights.items():
                if _flt.act_dep_airport != _pnr.start_airport:
                    continue
                if _flt.act_arr_airport != _pnr.end_airport:
                    continue
                if _flt.sch_dep_time < _pnr.sch_start_time:
                    continue
                _pnr.candidate_itineraries.append([_flt])

    def optimize(self):
        pass
