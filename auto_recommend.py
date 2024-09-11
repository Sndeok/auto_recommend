# # -*- coding: utf-8 -*-
# import xlrd
# import os
#
#
# def auto_recommend(current_number, car_data):
#     detail_sheet = car_data.sheet_by_index(4)  # 第5个子表:车型详细
#     current_car = []
#
#     for row in range(1, detail_sheet.nrows):
#         if detail_sheet.row_values(row)[2] == current_number:
#             current_car = detail_sheet.row_values(row)  # 当前车型
#             break
#
#     if not current_car:
#         print("未找到匹配的车型")
#         return []
#
#     diff_dict = {}  # 差异总值字典
#     diff_martix = []  # 差异细节矩阵
#
#     whell_diff = []  # 轴距差异列表
#     displacement_diff = []  # 排量差异列表
#     price_diff = []  # 价格差异列表
#
#     for row in range(1, detail_sheet.nrows):
#         row_values = detail_sheet.row_values(row)
#         if len(row_values) < 27:  # 确保行数据足够长
#             continue
#
#         diff_value = []
#
#         # 检查品牌
#         if row_values[0] == current_car[0]:
#             diff_value.append(2)
#         else:
#             diff_value.append(1)
#
#         # 检查车身结构
#         if row_values[10] == current_car[10]:
#             diff_value.append(0)
#         else:
#             diff_value.append(1)
#
#         # 轴距
#         if row_values[9] != '-':
#             term = abs(float(current_car[9]) - float(row_values[9]))
#             diff_value.append(term)
#             whell_diff.append(term)
#         else:
#             diff_value.append(-1)
#
#         # 排量
#         if row_values[14] != '-':
#             term = abs(float(current_car[14]) - float(row_values[14]))
#             diff_value.append(term)
#             displacement_diff.append(term)
#         else:
#             diff_value.append(-1)
#
#         # 指导价
#         if isinstance(row_values[26], float) and row_values[26] > 0:
#             term = abs(float(current_car[26]) - float(row_values[26]))
#             diff_value.append(term)
#             price_diff.append(term)
#         else:
#             diff_value.append(-1)
#
#         diff_martix.append(diff_value)
#
#     # 归一化
#     ave_whell = sum(whell_diff) / len(whell_diff) if whell_diff else 0
#     ave_displacement = sum(displacement_diff) / len(displacement_diff) if displacement_diff else 0
#     ave_price = sum(price_diff) / len(price_diff) if price_diff else 0
#     max_whell = max(whell_diff) if whell_diff else 0
#     min_whell = min(whell_diff) if whell_diff else 0
#     max_displacement = max(displacement_diff) if displacement_diff else 0
#     min_displacement = min(displacement_diff) if displacement_diff else 0
#     max_price = max(price_diff) if price_diff else 0
#     min_price = min(price_diff) if price_diff else 0
#
#     for i in range(len(diff_martix)):
#         if diff_martix[i][2] == -1:
#             diff_martix[i][2] = ave_whell
#         if diff_martix[i][3] == -1:
#             diff_martix[i][3] = ave_displacement
#         if diff_martix[i][4] == -1:
#             diff_martix[i][4] = ave_price
#
#         diff_martix[i][2] = (diff_martix[i][2] - min_whell) / (max_whell - min_whell) if max_whell != min_whell else 0
#         diff_martix[i][3] = (diff_martix[i][3] - min_displacement) / (
#                     max_displacement - min_displacement) if max_displacement != min_displacement else 0
#         diff_martix[i][4] = (diff_martix[i][4] - min_price) / (max_price - min_price) if max_price != min_price else 0
#
#         diff_dict[detail_sheet.row_values(i + 1)[2]] = sum(diff_martix[i])
#
#     selected_dict = sorted(diff_dict.items(), key=lambda d: d[1], reverse=False)[1:5]
#     return selected_dict
#
#
# def find_detail(current_number,car_data):
#
#     brand_id=0
#     price=0.0
#     brand_name='404'
#     car_name='404'
#     grade_id=0
#     grade_name='404'
#     series_id=0
#     series_name='404'
#
#     brand_sheet=car_data.sheet_by_index(0) #第一个子表：品牌
#     series_sheet=car_data.sheet_by_index(1)#第二个子表：车系
#     type_sheet=car_data.sheet_by_index(2)  #第三个子表：车型
#     grade_sheet=car_data.sheet_by_index(3)  #第四个子表：级别
#     detail_sheet = car_data.sheet_by_index(4)  #第5个子表:车型详细
#
#     for row in range(1, detail_sheet.nrows):                      #找厂商id号,车系id号以及价格
#         if current_number==detail_sheet.row_values(row)[2]:
#             brand_id=int(detail_sheet.row_values(row)[0])
#             price=detail_sheet.row_values(row)[26]
#             series_id=detail_sheet.row_values(row)[1]
#             break
#
#
#     for row in range(1, brand_sheet.nrows):                       #找厂商名字
#         if brand_id == int(brand_sheet.row_values(row)[0]):
#             brand_name=brand_sheet.row_values(row)[2]
#             break
#
#     for row in range(1,type_sheet.nrows):                        #找车名以及级别id
#         if current_number == type_sheet.row_values(row)[2]:
#             car_name=type_sheet.row_values(row)[3]
#             grade_id=type_sheet.row_values(row)[4]+100
#             break
#
#     for row in range(1, grade_sheet.nrows):                       #找级别名称
#         if grade_id==grade_sheet.row_values(row)[0]:
#             grade_name=grade_sheet.row_values(row)[1]
#             break
#
#     for row in range(1, series_sheet.nrows):                        #找车系
#         if series_id==series_sheet.row_values(row)[2]:
#             series_name=series_sheet.row_values(row)[1]
#
#     if brand_name=='404'or series_name=='404'or grade_name=='404'or car_name=='404':
#         return 'nothing'
#     else:
#         current_detail=[brand_name,series_name,grade_name,car_name,price]
#         return current_detail
#
#
# def recommend(current_id):
#     car_data = xlrd.open_workbook("car_data2.xls")  #读取excell表
#     selected_car=auto_recommend(current_id,car_data)           #筛选出最相近的前四辆汽车
#     recommend_car=[]
#     for car in selected_car:                             #对每一辆汽车寻找其五个指标
#         car_detail=find_detail(car[0],car_data)
#         if car_detail!='nothing':
#             recommend_car.append(car_detail)
#     return (recommend_car)                              #最终返回的推荐车及其指标，按序排列
#
#
#
# -*- coding: utf-8 -*-
import xlrd
import os

# 计算归一化函数
def normalize(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value) if max_value != min_value else 0

# 增加属性加权和用户行为数据处理
def auto_recommend(current_number, car_data, user_data):
    detail_sheet = car_data.sheet_by_index(4)  # 第5个子表:车型详细
    current_car = []

    for row in range(1, detail_sheet.nrows):
        # print(current_number)
        print(detail_sheet.row_values(row)[2])
        print("=============")
        # if detail_sheet.row_values(row)[2] == current_number:
        # 改为差值在 2000 以内
        car_number = int(float(detail_sheet.row_values(row)[2]))  # 先转为浮点，再转为整数
        if abs(car_number  - current_number) <= 1000:

            # print("aa")
            current_car = detail_sheet.row_values(row)  # 当前车型
            # print(current_car)
            # print("ee")
            break

    if not current_car:
        print("未找到匹配的车型")
        return []

    diff_dict = {}  # 差异总值字典
    diff_martix = []  # 差异细节矩阵

    whell_diff = []  # 轴距差异列表
    displacement_diff = []  # 排量差异列表
    price_diff = []  # 价格差异列表

    # 权重定义：可以根据需求调整
    brand_weight = 0.2
    structure_weight = 0.1
    whell_weight = 0.25
    displacement_weight = 0.25
    price_weight = 0.2

    # 获取用户行为数据，比如点击量和浏览时间
    user_clicks = user_data.get('clicks', {})
    user_view_time = user_data.get('view_time', {})

    for row in range(1, detail_sheet.nrows):
        row_values = detail_sheet.row_values(row)
        if len(row_values) < 27:  # 确保行数据足够长
            continue

        diff_value = []

        # 检查品牌
        if row_values[0] == current_car[0]:
            diff_value.append(brand_weight * 2)
        else:
            diff_value.append(brand_weight * 1)

        # 检查车身结构
        if row_values[10] == current_car[10]:
            diff_value.append(structure_weight * 0)
        else:
            diff_value.append(structure_weight * 1)

        # 轴距
        if row_values[9] != '-':
            term = abs(float(current_car[9]) - float(row_values[9]))
            diff_value.append(term * whell_weight)
            whell_diff.append(term)
        else:
            diff_value.append(-1)

        # 排量
        if row_values[14] != '-':
            term = abs(float(current_car[14]) - float(row_values[14]))
            diff_value.append(term * displacement_weight)
            displacement_diff.append(term)
        else:
            diff_value.append(-1)

        # 价格
        if isinstance(row_values[26], float) and row_values[26] > 0:
            term = abs(float(current_car[26]) - float(row_values[26]))
            diff_value.append(term * price_weight)
            price_diff.append(term)
        else:
            diff_value.append(-1)

        diff_martix.append(diff_value)

    # 归一化处理
    max_whell = max(whell_diff) if whell_diff else 0
    min_whell = min(whell_diff) if whell_diff else 0
    max_displacement = max(displacement_diff) if displacement_diff else 0
    min_displacement = min(displacement_diff) if displacement_diff else 0
    max_price = max(price_diff) if price_diff else 0
    min_price = min(price_diff) if price_diff else 0

    for i in range(len(diff_martix)):
        if diff_martix[i][2] == -1:
            diff_martix[i][2] = normalize(sum(whell_diff) / len(whell_diff), min_whell, max_whell) * whell_weight
        if diff_martix[i][3] == -1:
            diff_martix[i][3] = normalize(sum(displacement_diff) / len(displacement_diff), min_displacement, max_displacement) * displacement_weight
        if diff_martix[i][4] == -1:
            diff_martix[i][4] = normalize(sum(price_diff) / len(price_diff), min_price, max_price) * price_weight

        # 根据用户点击量和浏览时间进行加权推荐
        car_id = detail_sheet.row_values(i + 1)[2]
        clicks_weight = user_clicks.get(car_id, 1)
        view_time_weight = user_view_time.get(car_id, 1)

        diff_dict[car_id] = (sum(diff_martix[i]) * clicks_weight * view_time_weight)

    # 按差异值排序并选择最相近的车辆
    selected_dict = sorted(diff_dict.items(), key=lambda d: d[1], reverse=False)[1:5]
    return selected_dict


def find_detail(current_number,car_data):

    brand_id=0
    price=0.0
    brand_name='404'
    car_name='404'
    grade_id=0
    grade_name='404'
    series_id=0
    series_name='404'

    brand_sheet=car_data.sheet_by_index(0) #第一个子表：品牌
    series_sheet=car_data.sheet_by_index(1)#第二个子表：车系
    type_sheet=car_data.sheet_by_index(2)  #第三个子表：车型
    grade_sheet=car_data.sheet_by_index(3)  #第四个子表：级别
    detail_sheet = car_data.sheet_by_index(4)  #第5个子表:车型详细

    for row in range(1, detail_sheet.nrows):                      #找厂商id号,车系id号以及价格
        if current_number==detail_sheet.row_values(row)[2]:
            brand_id=int(detail_sheet.row_values(row)[0])
            price=detail_sheet.row_values(row)[26]
            series_id=detail_sheet.row_values(row)[1]
            break


    for row in range(1, brand_sheet.nrows):                       #找厂商名字
        if brand_id == int(brand_sheet.row_values(row)[0]):
            brand_name=brand_sheet.row_values(row)[2]
            break

    for row in range(1,type_sheet.nrows):                        #找车名以及级别id
        if current_number == type_sheet.row_values(row)[2]:
            car_name=type_sheet.row_values(row)[3]
            grade_id=type_sheet.row_values(row)[4]+100
            break

    for row in range(1, grade_sheet.nrows):                       #找级别名称
        if grade_id==grade_sheet.row_values(row)[0]:
            grade_name=grade_sheet.row_values(row)[1]
            break

    for row in range(1, series_sheet.nrows):                        #找车系
        if series_id==series_sheet.row_values(row)[2]:
            series_name=series_sheet.row_values(row)[1]

    if brand_name=='404'or series_name=='404'or grade_name=='404'or car_name=='404':
        return 'nothing'
    else:
        current_detail=[brand_name,series_name,grade_name,car_name,price]
        return current_detail
def recommend(current_id):
    car_data = xlrd.open_workbook("car_data2.xls")  # 读取excel表
    user_data = {  # 模拟的用户数据
        'clicks': {
            'car_1': 2,  # 用户点击次数
            'car_2': 3,
        },
        'view_time': {
            'car_1': 150,  # 浏览时间（秒）
            'car_2': 300,
        }
    }
    selected_car = auto_recommend(current_id, car_data, user_data)  # 筛选出最相近的前四辆汽车
    recommend_car = []
    for car in selected_car:  # 对每一辆汽车寻找其五个指标
        car_detail = find_detail(car[0], car_data)
        if car_detail != 'nothing':
            recommend_car.append(car_detail)
    return recommend_car  # 最终返回的推荐车及其指标，按序排列
