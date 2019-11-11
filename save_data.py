# 保存数据到数据库
from database import *
import re


def save_main_class(username, main_data):  # 保存理论课数据
    for data in main_data:  # 遍历处理获取的数据
        min_week = int(data[4][0:2])  # 提出开始周的数字
        max_week = int(data[4][3:5])  # 提出结束周的数字
        add_class(username, min_week, max_week, data[0], data[1], 1, data[2], data[3], data[5], '')  # 保存到数据库


def save_test_class(username, test_data):  # 保存实验课数据
    week_code = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '日': 7}  # 用来处理星期
    for data in test_data:  # 遍历处理获取的数据
        text = data[0]  # 获取上课时间，如：4周星期三5-6节
        num = int(re.search('[0-9]{1,2}', text).group())  # 正则匹配出上课的周次，如：4
        week = week_code[re.search('[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u65e5]', text).group()]  # 正则匹配出星期几，如：三
        time_text = re.search('[0-9]{1,2}-[0-9]{1,2}', text).group().split('-')  # 正则匹配出节数，如5-6
        time = (int(time_text[0]) + 1) // 2  # 计算出第几讲，如第5节，则是第3讲
        value = (int(time_text[1]) - int(time_text[0]) + 1) // 2  # 计算出讲值，如5-6，即1讲
        add_class(username, num, num, week, time, value, data[1], data[2], data[3], data[4])  # 保存到数据库
