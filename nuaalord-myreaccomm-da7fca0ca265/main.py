from model import Model


if __name__ == "__main__":
    model = Model()
    model.read_input_data()         # 读取数据
    model.review_passengers()       # 判断乘客受干扰类型
    # model.show_info()
    model.itinerary_generation()    # 为每个乘客生成若干个恢复行程
    model.optimize()                # 优化模型给出恢复方案
