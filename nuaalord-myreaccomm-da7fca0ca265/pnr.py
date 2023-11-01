from enum import Enum


class DisruptionType(Enum):  # 延误类型
    NoDisruption = 0,  # 未发生延误
    FlightCancel = 1,  # 航班取消
    StationMissConnect = 2,  # 两段航程站点发生中断
    TimeMissConnect = 3,  # 两段航程时间点发生中断
    Overbook = 4,  # 预定超额
    ExcessDelay = 5,  # 过度延迟
    Diversion = 6,  # 转移
    PaxMissFlight = 7,  # 错过航班
    NumDisruptions = 8  #

    def __str__(self):
        return self.name


class PNR:
    numPNRs = 0  # 旅客数量
    numDisruptPNRs = 0  # 受扰旅客数量
    allPNRs = {}  # 旅客信息字典

    def __init__(self, **kwargs):
        self.pnr_id = kwargs.get("pnr_id", 0)  # 获取kwargs字典中的乘客id，没有则默认值为0
        self.num_pax = kwargs.get("num_pax", 0)  # 获取kwargs字典中的乘客id，没有则默认值为0
        self.crm_index = kwargs.get("crm_index", 0)  # 获取kwargs字典中的crm（乘客优先级）指数，没有则默认值为0
        self.average_fare = kwargs.get("average_fare", 0)  # 获取kwargs字典中的平均费用，没有则默认值为0
        self.sch_start_time = None  # 行程起始时间
        self.sch_end_time = None  # 行程结束时间
        self.current_start_time = None
        self.disruption_type = DisruptionType.NoDisruption   # 默认值为0
        self.disrupt_airport = 0     # actual point of disruption  发生延误的机场
        self.current_airport = 0     # current station  现在所在的机场
        self.start_airport = 0       # origin airport of passenger  原行程的起始机场
        self.end_airport = 0         # final destination of passenger  行程的目的地机场
        self.flights = []  # 航班列表
        self.cabin = 0
        self.is_boarded = False  # 是否登机，默认值为否
        self.boarded_flights = []  # 已登机航班列表
        self.last_flight = None
        self.candidate_itineraries = []     # list of list of flights  候选航班列表
        PNR.numPNRs += 1
        PNR.allPNRs[self.pnr_id] = self  # 上述信息全部存储在allPNRs字典中，key: pnr_id (passengers.dat中的第一列内容)

    @property  # 封装后续函数，使得函数可以不加（）直接使用
    def disruption(self):  # 获取乘客延误类型
        return self.disruption_type

    @disruption.setter
    def disruption(self, d):
        self.disruption_type = d

    @staticmethod
    def read_pnr_data(_file):  # 获取乘客个人信息
        import csv
        with open(_file, 'r', newline="") as csv_in_file:
            file_reader = csv.reader(csv_in_file, delimiter=',')  # 获取文件中每行内容为一个列表，分隔符为','
            for row in file_reader:
                PNR(pnr_id=row[0], num_pax=int(row[1]), crm_index=int(row[2]), average_fare=int(row[3]))
                # 文件中每行内容依次为：乘客id，num_pax，xx指数，平均费用

    @classmethod
    def read_pnr_flights_data(cls, _file):  # 获取乘客航班信息
        import csv
        from flight import Flight, Cabin
        
        with open(_file, 'r', newline="") as csv_in_file:
            file_reader = csv.reader(csv_in_file, delimiter=',')
            for row in file_reader:
                pnr = PNR.allPNRs.get(row[0])  # 在allPNRs字典中查找pnrFlights文件中对应的pnr_id
                flight = Flight.get_flight_by_id(row[1])   # 在allFlights字典中查找pnrFlights文件中的对应flt_id
                if not pnr or not flight:  # 当上述两个id都有对应时，语句判断为假，
                    continue
                cabin = Cabin[row[2]]  # 将舱位等级转化为数值信息
                boarded = True if int(row[5]) == 1 else False  # 文件中的第六列表示登机信息，1：已登机
                pnr.flights.append(dict(flight=flight, cabin=cabin))  # 将前序的id信息以字典形式储存在flights列表中
                if boarded:
                    pnr.boarded_flights.append(flight)  # 将已登机的flt_id添加到boarded_flights列表中记录已登机航班信息
                pnr.cabin = pnr.flights[0]['cabin'].value  # 设定单一乘客组的舱位等级与第一架航班所坐舱位一致（1/2/3）
        with open(_file, 'r', newline="") as csv_in_file:
            file_reader = csv.reader(csv_in_file, delimiter=',')
            for row in file_reader:
                # import pdb; pdb.set_trace()
                pnr = PNR.allPNRs.get(row[0])  # 在allPNRs字典中查找pnrFlights文件中对应的pnr_id
                if not pnr:
                    continue
                for flt in pnr.flights:
                    tmp_keys = flt.get('flight')
                    if tmp_keys in pnr.boarded_flights:
                        continue
                    pnr.current_start_time = tmp_keys.sch_dep_time
                    pnr.current_airport = tmp_keys.sch_dep_airport
                    break

        cls.get_last_flight_for_passengers()

    @staticmethod
    def get_last_flight_for_passengers():
        from datetime import timedelta
        for _pnr in PNR.allPNRs.values():
            _pnr.start_airport = _pnr.flights[0].get("flight").sch_dep_airport  # 在allFlights字典中以某一乘客组的第一个flt_id为索引查找该乘客组的原出发机场
            _pnr.sch_start_time = _pnr.flights[0].get("flight").sch_dep_time  # 在allFlights字典中以某一乘客组的第一个flt_id为索引查找该乘客组的原出发时间
            _pnr.sch_end_time = _pnr.flights[-1].get("flight").sch_arr_time 
            prev_flt = None  # 第一个航班的前序航班默认设定为None
            con_time = timedelta(seconds=0)  # 初试时间差设置为0
            for pnr_flight in _pnr.flights:  # 每个pnr_flight中包含一个flight-flt_id，一个对应的cabin-Cabin['row[2]']
                _flt = pnr_flight.get("flight")  # flt_id赋值
                if prev_flt is None or _flt in _pnr.boarded_flights:  # 初次循环时，将首个航班设定为下一个航班的前序航班的条件语句
                    prev_flt = _flt
                    _pnr.last_flight = prev_flt  # 将每个pnr_flight中的flt_id赋值给_pnr.last_flight，定义为前序航班
                    _pnr.end_airport = prev_flt.sch_arr_airport  # 在allFlights字典中以flt_id为索引查找原到达机场并赋值给乘客组的终点机场
                    continue
                if con_time > _flt.act_dep_time - prev_flt.act_arr_time:  # 在某个乘客组中，第一次不执行该条语句；该条件判断的是当前航班与前序航班是否时间冲突
                    con_time = _flt.act_dep_time - prev_flt.act_arr_time
                    _pnr.last_flight = prev_flt
                    _pnr.end_airport = prev_flt.sch_arr_airport
                prev_flt = _flt  # 时间不存在冲突时，按顺序依次成为prev_flt，
