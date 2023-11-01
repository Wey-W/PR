import numpy as np
import pandas as pd
import flight

'''读取原始pnrData文件，添加两列乘客类型信息便于后续乘客优先级指数计算'''
# # 读取原始pnrData文件
# df = pd.read_csv(r'D:\研究生\论文写作\PR_TEST\nuaalord-myreaccomm-da7fca0ca265\data\pnrData.csv', header=None)
#
# # 插入新列，用于存储“是否是普通乘客”的信息
# df.insert(4, 'Common_Passenger', 0)
#
# # 在文件最后添加新列，用于存储“是否为特殊人士”的信息
# df['Special_Person'] = 0
#
# # 设置随机种子以保证可复现性
# np.random.seed(0)
#
# # 按照设定的比例随机生成“是否为特殊人士”列的值
# special_ratio = 0.02  # 设置特殊人士占比为2%
# total_rows = len(df)
# special_count = int(total_rows * special_ratio)  # 特殊人士数量
# special_indices = np.random.choice(total_rows, special_count, replace=False)  # 随机选取部分行作为特殊人士填充
# df.loc[special_indices, 'Special_Person'] = 1
#
# # 修正“是否是普通乘客”列的值，确保每一行乘客类型代表数字之和为1
# df.iloc[:, 4] = 1 - (df.iloc[:, -2] + df.iloc[:, -3] + df['Special_Person'])
#
# # 保存修改后的DataFrame到pnrData_all.csv文件，没有列名
# df.to_csv(r'D:\研究生\论文写作\PR_TEST\nuaalord-myreaccomm-da7fca0ca265\data\pnrData_all.csv', index=False, header=False)

'''读取pnrData文件，根据pnrFlights文件进行id匹配添加乘客舱位信息，默认同一乘客组的全航程舱位不变'''
# # 读取pnrData_all.csv文件
# csv_df = pd.read_csv(r'D:\研究生\论文写作\PR_TEST\nuaalord-myreaccomm-da7fca0ca265\data\pnrData_all.csv', header=None)
# csv_df.columns = ['id', 'num', 'a_f', 'level', 'common', 'staff', 'minor', 'special']  # 根据您的文件设置列名
#
# # 读取pnrFlights.dat文件[]
# dat_df = pd.read_csv(r'D:\研究生\论文写作\PR_TEST\nuaalord-myreaccomm-da7fca0ca265\data\pnrFlights.dat', header=None)  # 根据您的文件更改路径和header选项
# dat_df.columns = ['id', 'flt_id', 'cabin', 'other_info1', 'other_info2', 'other_info3', 'other_info4', 'other_info5']  # 根据您的文件设置列名
#
# # 删除DAT文件中的重复ID，仅保留一个（因为第三列信息一致）
# dat_df.drop_duplicates(subset='id', keep='first', inplace=True)
#
# # 合并两个DataFrame
# merged_df = pd.merge(csv_df, dat_df[['id', 'cabin']], on='id', how='left')
#
# # 重新排列列的顺序以将'cabin'放在第三列
# column_order = ['id', 'num', 'cabin', 'a_f', 'level', 'common', 'staff', 'minor', 'special']
# merged_df = merged_df[column_order]
#
# # 将合并后的DataFrame保存为新的CSV文件
# merged_df.to_csv(r'D:\研究生\论文写作\PR_TEST\nuaalord-myreaccomm-da7fca0ca265\data\pnrData_all_test.csv', index=False, header=False)

'''将pnrData文件中舱位等级信息变更为对应数值'''
# # 根据flight中的Cabin字典创建一个舱位信息替换规则的字典
# replace_rules = {cabin.name: cabin.value for cabin in flight.Cabin}
#
# # 读取CSV文件
# csv_df = pd.read_csv(r'D:\研究生\论文写作\PR_TEST\nuaalord-myreaccomm-da7fca0ca265\data\pnrData_all_test.csv', header=None)
#
# # 应用替换规则到第三列（索引为2）
# csv_df.iloc[:, 2] = csv_df.iloc[:, 2].replace(replace_rules)
#
# # 保存修改后的CSV文件
# csv_df.to_csv(r'D:\研究生\论文写作\PR_TEST\nuaalord-myreaccomm-da7fca0ca265\data\pnrData_all_test.csv', index=False, header=False)

'''根据各级判断矩阵得到各项指标所占权重'''
# # 计算各级指标权重的函数
# def get_weights(matrix):
#     eigvalues, eigvectors = np.linalg.eig(matrix)
#     max_eigvalue_index = np.argmax(eigvalues.real)
#     max_eigvector = eigvectors[:, max_eigvalue_index].real
#     return max_eigvector / np.sum(max_eigvector)
#
#
# # 构建一级指标判断矩阵
# top_matrix = np.array([
#     [1, 3, 7, 5],
#     [1/3, 1, 6, 4],
#     [1/7, 1/6, 1, 1/4],
#     [1/5, 1/4, 4, 1]
# ])
#
# # 构建各二级指标的判断矩阵
# # 例如，舱位等级有三个二级指标：头等舱、经济舱和商务舱
# cabin_matrix = np.array([
#     [1, 4, 8],
#     [1/4, 1, 6],
#     [1/8, 1/6, 1]
# ])
#
# # 乘客类型有四个二级指标：普通、儿童、职员、其他
# passenger_matrix = np.array([
#     [1, 1 / 7, 1 / 5, 1 / 3],
#     [7, 1, 5, 3],
#     [5, 1 / 5, 1, 1 / 2],
#     [3, 1 / 3, 2, 1]
# ])
#
# # 会员等级有三个二级指标：普通会员、VIP1、VIP2
# member_matrix = np.array([
#     [1, 1/2, 1/7],
#     [2, 1, 1/3],
#     [7, 3, 1]
# ])
#
# # 获取各级权重
# weights_top = get_weights(top_matrix)
# weights_cabin = get_weights(cabin_matrix)
# weights_passenger = get_weights(passenger_matrix)
# weights_member = get_weights(member_matrix)
#
# # 标准化处理的"票价"假定权重为0.05（或根据您的具体情况来设定）
# weights_price = 0.05
#
# # 汇总各一级指标下的二级指标权重
# second_level_weights = {
#     'Cabin_Level': weights_cabin,
#     'Passenger_Type': weights_passenger,
#     'Member_Level': weights_member,
#     'Ticket_Price': np.array([weights_price])
# }
#
# # 综合各级权重得到最终权重
# final_weights = {}
# for i, top_indicator in enumerate(['Cabin_Level', 'Passenger_Type', 'Member_Level', 'Ticket_Price']):
#     final_weights[top_indicator] = weights_top[i] * second_level_weights[top_indicator]
#
# print(
#     "Top_Weights", weights_top,
#     "Weights：", final_weights)

'''根据已有的各指标权重计算各乘客组的优先级指标指数'''
# 读取CSV文件
df = pd.read_csv('./data/pnrData_all_test.csv', header=None)

# 定义权重字典

final_weights = {
    'Cabin_Level': {3: 0.37915644, 2: 0.13670955, 1: 0.03286155},
    'Passenger_Type': np.array([0.01654936, 0.16462682, 0.04564394, 0.06111945]),
    'Member_Level': {0: 0.00491544, 1: 0.01034923, 2: 0.03268474},
    'Ticket_Price': np.array([0.00576917])
}

# 创建一个新的列用于存放优先指数
df['Priority_Index'] = 0

# 逐行读取DataFrame并计算优先指数
for index, row in df.iterrows():
    cabin_level = row[2]  # 第3列是舱位等级
    ticket_price = row[3]  # 第4列是票价
    member_level = row[4]  # 第5列是会员等级
    passenger_common = row[5]  # 乘客类型
    passenger_minor = row[6]  # 乘客类型
    passenger_staff = row[7]  # 乘客类型
    passenger_special = row[8]  # 乘客类型

    priority_index = (
            final_weights['Cabin_Level'].get(cabin_level, 0) +
            ticket_price * final_weights['Ticket_Price'][0] +
            final_weights['Member_Level'].get(member_level, 0) +
            passenger_common * final_weights['Passenger_Type'][0] +
            passenger_minor * final_weights['Passenger_Type'][1] +
            passenger_staff * final_weights['Passenger_Type'][2] +
            passenger_special * final_weights['Passenger_Type'][3]
    )

    # 将计算出的优先指数存储回DataFrame
    df.at[index, 'Priority_Index'] = priority_index

# 保存结果到新的CSV文件
df.to_csv('./data/pnrData_all_test.csv', index=False, header=False)
