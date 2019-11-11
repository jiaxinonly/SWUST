# flask框架，主程序
from flask import *
from login import login_server
import requests
from get_class import *
import threading
import time
from class_data import get_all_class_data

app = Flask(__name__)


@app.route('/')  # 获取开学时间的路由，用来效验当前时间为第几周
def begin_date():
    begin_time = "2019-8-26"  # 设置学期开始时间
    time_tuple = time.strptime(begin_time, "%Y-%m-%d")  # 转换为时间元组
    time_stamp = int(time.mktime(time_tuple))  # 转换为时间戳
    return str(time_stamp) + "000"  # 返回标准时间戳


@app.route('/login/')  # 登录一站式服务大厅的路由
def login():
    username = request.args.get('username')  # 获取学号参数
    password = request.args.get('password')  # 获取密码参数
    login_request = requests.session()  # 保持会话session
    flag = login_server(username, password, login_request)  # 一站式服务大厅系统
    if flag == '登录成功':  # 返回登录成功时
        if not seek_user(username, password):  # 查询数据库，是否有用户账户
            add_user(username, password)  # 新用户，添加并创建课表
        clear_class(username)  # 截断课表，以便重新储存数据
        test_thread = threading.Thread(target=get_test_classes, args=(username, login_request))  # 添加线程获取实验课数据
        test_thread.start()  # 启动实验课线程
        main_thread = threading.Thread(target=get_main_classes, args=(username, login_request))  # 添加线程获取理论课数据
        main_thread.start()  # 启动理论课线程
        main_thread.join()  # 等待理论课线程结束
        test_thread.join()  # 等待实验课线程结束
    return flag  # 返回结果


@app.route('/flush/')  # 刷新获取数据库课表的路由
def flush():
    username = request.args.get('username')  # 获取学号参数
    password = request.args.get('password')  # 获取密码参数
    data = get_all_class_data(username, password)  # 获取处理后的课表信息
    if data == "请先登录" or data == "数据库密码错误":  # 账号未登陆过，或者密码错误时
        return data  # 返回信息提示
    else:
        class_data = {username: data}  # 处理数据
        return class_data  # 返回数据


if __name__ == '__main__':
    app.run()
