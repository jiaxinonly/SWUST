# 爬取课表信息并解析
from lxml import etree
from url_data import *
import threading
from time import sleep
from save_data import *


def get_main_classes(username, login):  # 登录教务处
    login.get(login_main_url, verify=False, timeout=10)  # 通过一站式服务大厅登录教务处
    response = login.get(get_main_url)  # 获取返回结果
    html = etree.HTML(response.text)  # 解析html
    num = [3, 2, 3, 2, 3, 2]  # 用来设置解析的下标
    all_data = []  # 储存课程信息
    for i in range(7):  # 从星期一开始到星期天
        for j in range(6):  # 从第一讲到第六讲
            for k in range(1, 10, 2):  # 循环遍历这个课表框，将重课的都获解析出来，如果没有重课只进行一次，最多处理一讲课5个重课
                class_name = html.xpath(
                    '//*[@id="choosenCourseTable"]/table/tbody/tr[' + str(j + 1) + ']/td[' + str(
                        num[j]) + ']/div[' + str(k) + ']/span[1]/text()')  # 使用xpath获取课程名
                teacher = html.xpath('//*[@id="choosenCourseTable"]/table/tbody/tr[' + str(j + 1) + ']/td[' + str(
                    num[j]) + ']/div[' + str(k) + ']/span[3]/text()')  # 使用xpath获取课老师姓名
                week = html.xpath('//*[@id="choosenCourseTable"]/table/tbody/tr[' + str(j + 1) + ']/td[' + str(
                    num[j]) + ']/div[' + str(k) + ']/span[4]/text()')  # 使用xpath获取第几周到第几周
                place = html.xpath('//*[@id="choosenCourseTable"]/table/tbody/tr[' + str(j + 1) + ']/td[' + str(
                    num[j]) + ']/div[' + str(k) + ']/span[5]/text()')  # 使用xpath获取地点
                if class_name:  # 如果不为空，就储存
                    data = class_name + teacher + week + place
                    data.insert(0, j + 1)  # 插入第几讲的值
                    data.insert(0, i + 1)  # 插入星期几的值
                    all_data.append(data)  # 储存
                else:  # 如果为空了，就没有必要继续遍历了，直接break
                    break
            num[j] += 1  # 下标+1
    save_main_class(username, all_data)  # 保存在数据库


def get_test_classes(username, login):  # 登录实验系统
    response_id = login.get(test_id_url, timeout=10)  # 获取登录实验系统的cookie
    url_id = re.search("/StuExpbook/API/sso.jsp\?no=[0-9]*&timestamp=[0-9]*&verify=[0-9a-z]*",
                       response_id.text).group()  # 正则匹配获取cookie
    login.get(login_test_url + url_id, timeout=10)  # 使用cookie登录实验系统
    response_date = login.get(test_index_url, timeout=10)  # 进入使用系统首页
    html_main = etree.HTML(response_date.text)  # 解析html
    date = html_main.xpath('//*[@id="nav-secondary"]/li[2]/a/text()')[0]  # 使用xpath获取学期参数
    date_list = re.findall('[0-9]+', date)  # 正则匹配出数字
    currYearterm = date_list[0] + '-' + date_list[1] + '-' + date_list[2]  # 拼接学期参数
    all_data = []  # 用来储存获取到的实验课数据
    finish = False  # 标记是否将所有数据爬取完成

    def get_page(page):  # 获取page页是实验课数据
        nonlocal finish  # 申明非局部变量
        if not finish:  # 如果未完成爬取时

            params = {'currYearterm': currYearterm,
                      'currTeachCourseCode': '%',
                      'page': page}  # 请求参数
            response_class = login.get(get_test_url, params=params)  # 提交请求，获取html数据
            html_class = etree.HTML(response_class.text)  # 解析html
            for j in range(2, 12):  # 获取这一页的十条实验课程信息
                class_name = html_class.xpath(
                    '//*[@id="content"]/table/tbody/tr[' + str(j) + ']/td[1]/strong/text()')  # 使用xpath获取课程名
                ps = html_class.xpath('//*[@id="content"]/table/tbody/tr[' + str(j) + ']/td[2]/text()')  # 使用xpath获取备注
                time = html_class.xpath(
                    '//*[@id="content"]/table/tbody/tr[' + str(j) + ']/td[3]/text()')  # 使用xpath获取上课时间
                if time and time[0] == '\r\n':  # 处理特殊的带链接的实验课时间
                    time = html_class.xpath('//*[@id="content"]/table/tbody/tr[' + str(j) + ']/td[3]/a/text()')
                place = html_class.xpath(
                    '//*[@id="content"]/table/tbody/tr[' + str(j) + ']/td[4]/text()')  # 使用xpath获取地点
                teacher = html_class.xpath(
                    '//*[@id="content"]/table/tbody/tr[' + str(j) + ']/td[5]/text()')  # 使用xpath获取老师姓名
                if class_name:  # 储存数据
                    data = time + class_name + teacher + place + ps
                    nonlocal all_data  # 申明非局部变量
                    mutex.acquire()  # 使用互斥锁
                    all_data.append(data)  # 储存数据
                    mutex.release()  # 解锁
                else:  # 如果为空，说明已经将数据全部爬完，更改标记
                    mutex.acquire()  # 使用互斥锁
                    finish = True  # 改变标记
                    mutex.release()  # 解锁
                    break

    page = 0  # 页号
    mutex = threading.Lock()  # 使用互斥锁
    threads = []  # 储存线程
    while True:  # 一页一个线程，同时爬取，提高速度
        if not finish:  # 如果还未爬取完成，继续创建线程
            threads.append(threading.Thread(target=get_page, args=(page + 1,)))  # 创建线程并添加到线程列表中
            threads[page].start()  # 启动线程
            page += 1  # 页号加1
        elif finish:  # 如果完成，等待所以线程结束
            for i in threads:  # 等待线程
                i.join()
            break
        if page % 5 == 0:  # 每启动5个线程，等待1秒，避免创建线程太多，减少服务器开销
            sleep(1)
    save_test_class(username, all_data)  # 保存数据到数据库
