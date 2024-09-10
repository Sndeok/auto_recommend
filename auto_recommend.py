# -*- coding: utf-8 -*-
import xlrd
import os

def auto_recommend(current_number,car_data):

    detail_sheet=car_data.sheet_by_index(4)   #第5个子表:车型详细
    current_car=[]


    for row in range(1,detail_sheet.nrows):

        if  detail_sheet.row_values(row)[2] == current_number:
            current_car=detail_sheet.row_values(row)    #当前车型
            break


    diff_dict={}     #差异总值字典
    diff_martix=[]   #差异细节矩阵


    whell_diff=[]         #轴距差异列表
    displacement_diff=[]    #排量差异列表
    price_diff=[]         #价格差异列表


    for row in range(1,detail_sheet.nrows):
        diff_value=[]

        if detail_sheet.row_values(row)[0]==current_car[0]:   #品牌
            diff_value.append(2)
        else:
            diff_value.append(1)

        if detail_sheet.row_values(row)[10]==current_car[10]:  #车身结构
            diff_value.append(0)
        else:
            diff_value.append(1)

        if detail_sheet.row_values(row)[9]!='-':     #轴距
            term=abs(float(current_car[9])-float(detail_sheet.row_values(row)[9]))
            diff_value.append(term)
            whell_diff.append(term)
        else:
            diff_value.append(-1)


        if detail_sheet.row_values(row)[14]!='-':    #排量
            term=abs(float(current_car[14])-float(detail_sheet.row_values(row)[14]))
            diff_value.append(term)
            displacement_diff.append(term)
        else:
            diff_value.append(-1)



        if isinstance(detail_sheet.row_values(row)[26],float) and detail_sheet.row_values(row)[26]>0:    #指导价
            term=abs(float(current_car[26])-float(detail_sheet.row_values(row)[26]))
            diff_value.append(term)
            price_diff.append(term)
        else:
            diff_value.append(-1)


        diff_martix.append(diff_value)


    #归一化
    ave_whell=sum(whell_diff) / len(whell_diff)
    ave_displacement=sum(displacement_diff) / len(displacement_diff)
    ave_price=sum(price_diff) / len(price_diff)
    max_whell=max(whell_diff)
    min_whell=min(whell_diff)
    max_displacement=max(displacement_diff)
    min_displacement=min(displacement_diff)
    max_price=max(price_diff)
    min_price=min(price_diff)
    for i in range(len(diff_martix)):

        if(diff_martix[i][2]==-1):                          #如果该款车型没有轴距数据
            diff_martix[i][2] = ave_whell

        if(diff_martix[i][3]==-1):                          #如果该款车型没有排量数据
            diff_martix[i][3] = ave_displacement

        if(diff_martix[i][4]==-1):                        #如果该款车型没有价格数据
            diff_martix[i][4] = ave_price

        diff_martix[i][2] = (diff_martix[i][2] - min_whell) / (max_whell - min_whell)
        diff_martix[i][3] = (diff_martix[i][3] - min_displacement) / (max_displacement - min_displacement)
        diff_martix[i][4] = (diff_martix[i][4] - min_price) / (max_price - min_price)

        diff_dict[detail_sheet.row_values(i+1)[2]]=sum(diff_martix[i])    #每一辆车和当前车的总差距

    selected_dict= sorted(diff_dict.items(), key=lambda d:d[1], reverse = False)[1:5]
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
    car_data = xlrd.open_workbook("car_data1.xls")  #读取excell表
    selected_car=auto_recommend(current_id,car_data)           #筛选出最相近的前四辆汽车
    recommend_car=[]
    for car in selected_car:                             #对每一辆汽车寻找其五个指标
        car_detail=find_detail(car[0],car_data)
        if car_detail!='nothing':
            recommend_car.append(car_detail)
    return (recommend_car)                              #最终返回的推荐车及其指标，按序排列


