from pnr import PNR


class Write:
    @staticmethod
    def show_passenger_itineraries():
        print("PNR\t\tPNR_Num\t\tAverage Fare\t\tFirst(arp,status)\tLast(arp,status)\tDisruption\tS-D\tTime-Dep\tTime-Arr\tFlight_Num")
        for _pnr in PNR.allPNRs.values():
            first_flt = _pnr.flights[0].get("flight")  # flt_id
            last_flt = _pnr.last_flight  # 根据pnr.py中的get_last_flight_for_passengers()函数获取，结果是flt_id或None
            canceled_flt = "na"
            flights_num = len(_pnr.flights)
            for pnr_flight in _pnr.flights:
                _flt = pnr_flight.get("flight")  # flt_id
                if _flt.status is False:  # 从allFlights字典中查询得到的status值
                    canceled_flt = _flt.flt_number  # 从allFlights字典中查询得到的flt_number值
                    break
            print("{0}\t{1}\t{2}\t{3}({4},{5})\t{6}({7},{8})\t{9}\t{10}-{11}\t{12}\t{13}".format(
                _pnr.pnr_id, _pnr.num_pax, _pnr.average_fare, first_flt.flt_number, first_flt.sch_dep_airport, first_flt.depCode,
                last_flt.flt_number, last_flt.sch_arr_airport, last_flt.arrCode, _pnr.disruption, _pnr.start_airport,
                _pnr.end_airport, first_flt.sch_dep_time, last_flt.sch_arr_time))


