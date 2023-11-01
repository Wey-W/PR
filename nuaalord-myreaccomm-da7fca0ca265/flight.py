from enum import Enum


class Airport:  # 机场类
    allAirports = []  # 机场列表
    numAirports = 0  # 机场数量

    def __init__(self, _code):
        self.id = Airport.numAirports  # 赋予机场id，从0开始，依次加一
        self.code = _code
        Airport.numAirports += 1
        Airport.allAirports.append(self)  # 新机场添加到allAirports列表中

    @classmethod
    def get_or_create_airport(cls, _code):  # 判断新传入的机场实例与现有机场是否重复，进行添加
        for a in cls.allAirports:
            if a.code == _code:
                return a
        return Airport(_code)

    def __str__(self):  # 引用Airport类后，如有输出，则输出机场对应的code
        return self.code


class Cabin(Enum):  # 舱位等级
    Y = 1  # 经济舱  Economy
    J = 2  # 商务舱  Business
    F = 3  # 头等舱  First


class DepArrCode(Enum):
    Unknown = 0
    ETD = 1
    ETA = 2
    AIR = 3
    OFF = 4
    OUT = 5
    IN = 6
    ON = 7
    SCH = 8
    EST = 9

    @staticmethod
    def get_dep_arr_code(str_code):
        for c in DepArrCode:
            if c.name == str_code:
                return c
        return DepArrCode.Unknown

    def __str__(self):
        return self.name


class Flight:
    allFlights = {}  # 航班字典
    numFlights = 0  # 航班数量

    def __init__(self, **kwargs):
        self.flt_id = kwargs.get("flt_id")  # 航班id
        self.flt_number = kwargs.get("flt_number")  # 航班数量（？）
        self.average_fare = kwargs.get("average_fare")  # 平均费用
        self.ac_id = kwargs.get("ac_id")
        self.sch_dep_airport = kwargs.get("sch_dep_airport")  # 原时刻表出发机场
        self.sch_dep_time = kwargs.get("sch_dep_time")  # 原时刻表出发时间
        self.sch_arr_airport = kwargs.get("sch_arr_airport")  # 原时刻表到达机场
        self.sch_arr_time = kwargs.get("sch_arr_time")  # 原时刻表到达时间
        self.act_dep_airport = kwargs.get("act_dep_airport")  # 实际出发机场
        self.act_dep_time = kwargs.get("act_dep_time")  # 实际出发时间
        self.act_arr_airport = kwargs.get("act_arr_airport")  # 实际到达机场
        self.act_arr_time = kwargs.get("act_arr_time")  # 实际到达时间
        self.status = True if int(kwargs.get("status")) > 0 else False  # 航班状态
        self.depCode = DepArrCode.get_dep_arr_code(kwargs.get("depCode"))
        self.arrCode = DepArrCode.get_dep_arr_code(kwargs.get("arrCode"))
        self.availability = {}
        Flight.allFlights[self.flt_id] = self  # 将实例对象加入到航班字典中并赋予key值为航班id
        Flight.numFlights += 1

    def get_status(self):  # 获取航班状态
        return self.status

    def set_availability(self, cabin, a):
        self.availability[Cabin[cabin].value] = a

    @staticmethod
    def get_flight_by_id(flt_id):  # 通过航班id从航班字典中得到对应航班信息
        return Flight.allFlights.get(flt_id)

    @staticmethod
    def read_flight_data(_file):
        import csv
        from datetime import datetime
        with open(_file, 'r', newline="") as csv_in_file:
            file_reader = csv.reader(csv_in_file, delimiter=',')
            for row in file_reader:
                Flight(flt_id=row[0], act_dep_airport=Airport.get_or_create_airport(row[1]),
                       act_arr_airport=Airport.get_or_create_airport(row[2]),
                       flt_number=row[4], sch_dep_time=datetime.fromtimestamp(int(row[10])),
                       sch_arr_time=datetime.fromtimestamp(int(row[11])),
                       act_dep_time=datetime.fromtimestamp(int(row[12])),
                       act_arr_time=datetime.fromtimestamp(int(row[13])),
                       sch_dep_airport=Airport.get_or_create_airport(row[23]),
                       sch_arr_airport=Airport.get_or_create_airport(row[24]),
                       depCode=row[33], arrCode=row[34],
                       status=row[39])
                # 从航班信息文件的每一行中获取需要加入到航班字典中的航班相关信息：是一个筛选过程

    @staticmethod
    def read_availability_data(_file):
        import csv
        with open(_file, 'r', newline="") as csv_in_file:
            file_reader = csv.reader(csv_in_file, delimiter=',')
            for row in file_reader:
                flight = Flight.get_flight_by_id(row[0])
                if not flight:  # 在availability中的航班与schedule中的航班不能匹配时（找不到flight值时），进入下一个循环
                    continue
                capacity = int(row[4])  # 航班某种舱位的总可载客量
                booked = int(row[5])  # 航班某种舱位的已预订量
                flight.set_availability(row[1], max(0, capacity - booked))  # 得到航班的舱位等级以及对应的剩余可载客量

    def is_departed(self):
        return self.depCode == DepArrCode.OFF or self.depCode == DepArrCode.OUT

    def is_arrived(self):
        return self.arrCode == DepArrCode.ON or self.arrCode == DepArrCode.IN

    def is_actual(self):
        return self.is_departed() or self.is_arrived()
