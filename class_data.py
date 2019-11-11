# 处理从数据库获取的课表数据，返回给前端，主要是重课的处理
from database import *


def get_all_class_data(username, password):  # 获取数据库数据
    class_data = seek_class(username, password)  # 检查账号密码是否正确
    if class_data == "请先登录" or class_data == "数据库密码错误":  # 如果未登陆过，或者密码错误时
        return class_data  # 直接返回提示
    else:  # 账号密码正确时
        result_data = {}  # 用来储存处理好的数据
        for num in range(1, 25):  # 循环周次，从第1周到第24周
            for week in range(1, 8):  # 循环星期，从星期一到星期天
                for time in range(1, 7):  # 循环讲次，从第一讲到第六讲
                    all_class_list = []  # 用来储存第num周，星期week，第time讲的课，主要是处理重课信息！
                    value = 0  # 讲值，用来记录此课有几讲，比如2讲一起的实验课
                    for data in class_data:  # 遍历从数据库获取的数据
                        if data[0] <= num <= data[1]:  # 如果是当前遍历的周
                            if data[2] == week and data[3] == time:  # 并且是当前遍历的星期并且是当前遍历的讲次
                                if data[4] > value:  # 获取讲值
                                    value = data[4]
                                class_dict = {'class_name': data[5], 'teacher': data[6], 'place': data[7],
                                              'ps': data[8]}  # 储存当前遍历周，当前遍历星期，当前遍历讲课的课程名，老师，地点，备注
                                all_class_list.append(class_dict)  # 添加到第num周，星期week，第time讲的列表，这样就将重课的数据储存在一起了
                    if value != 0:  # 将第num周，星期week，第time讲的课表数据储存在总的列表中
                        result_data[str(num) + '-' + str(week) + '-' + str(time) + '-' + str(
                            value)] = all_class_list  # 用num-week-time为键储存数据，便于前端处理
        return result_data  # 返回处理好的数据
