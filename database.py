# 存在本地数据库
import pymysql


def seek_user(username, password):  # 检查用户
    db = pymysql.connect('localhost', 'accepted', '你的密码', 'swust')  # 打开数据库连接（主机名，用户名，密码，数据库名）
    cursor = db.cursor()  # 创建游标
    sql = "select * from user where username='%s'" % username  # 从user表查询用户
    cursor.execute(sql)  # 执行
    request = cursor.fetchall()  # 获取查询结果
    if len(request) == 0:  # 没有此用户时
        db.close()  # 关闭数据库
        return False  # 返回结果
    elif len(request) == 1:  # 查询到用户时
        if request[0][1] == password:  # 检查密码
            db.close()  # 关闭数据库
            return True  # 返回结果
        else:  # 更新密码
            sql = "update user set password = '%s' where username ='%s'" % (password, username)  # 更新密码
            cursor.execute(sql)  # 执行
            db.commit()  # 提交
            db.close()  # 关闭数据库
            return True  # 返回结果


def add_user(username, password):  # 添加用户
    db = pymysql.connect('localhost', 'accepted', '你的密码', 'swust')  # 打开数据库连接（主机名，用户名，密码，数据库名）
    cursor = db.cursor()  # 创建游标
    sql_user = "insert into user (username, password) values ('%s', '%s')" % (username, password)  # 添加用户信息
    cursor.execute(sql_user)  # 执行
    sql_table = "create table t%s (begin_num int, end_num int, week int, time int, value int, class char(30), teacher char(20), place char(30), ps char(40))" % username  # 创建用户课表
    cursor.execute(sql_table)  # 执行
    db.commit()  # 提交
    db.close()  # 关闭数据库


def clear_class(username):  # 截断表
    db = pymysql.connect('localhost', 'accepted', '你的密码', 'swust')  # 打开数据库连接（主机名，用户名，密码，数据库名）
    cursor = db.cursor()  # 创建游标
    sql = "truncate table t%s" % username  # 截断表
    cursor.execute(sql)  # 执行
    db.commit()  # 提交
    db.close()  # 关闭数据库


def add_class(username, begin_num, end_num, week, time, value, class_name, teacher, place, ps):  # 添加课表信息
    db = pymysql.connect('localhost', 'accepted', '你的密码', 'swust')  # 打开数据库连接（主机名，用户名，密码，数据库名）
    cursor = db.cursor()  # 创建游标
    sql = "insert into t%s (begin_num, end_num, week, time, value, class, teacher, place, ps) values (%d, %d, %d, %d, %d, '%s', '%s', '%s', '%s')" % (
        username, begin_num, end_num, week, time, value, class_name, teacher, place, ps)  # 添加课程
    cursor.execute(sql)  # 执行
    db.commit()  # 提交
    db.close()  # 关闭数据库


def seek_class(username, password):  # 查看课表信息
    db = pymysql.connect('localhost', 'accepted', '你的密码', 'swust')  # 打开数据库连接（主机名，用户名，密码，数据库名）
    cursor = db.cursor()  # 创建游标
    seek_sql = "select * from user where username='%s'" % username  # 查询用户是否登录过
    cursor.execute(seek_sql)  # 执行
    request = cursor.fetchall()  # 获取查询结果
    if len(request) == 0:  # 未登录过，没有信息返回提示
        db.close()
        return "请先登录"
    elif len(request) == 1:  # 登录过
        if request[0][1] == password:  # 检查密码
            sql = "select * from t%s " % username  # 查询数据
            cursor.execute(sql)  # 执行
            request = cursor.fetchall()  # 获取查询结果
            db.close()  # 关闭数据库
            return request  # 返回查询结果
        else:
            return "数据库密码错误"  # 密码错误返回提示
