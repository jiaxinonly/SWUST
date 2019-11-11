# 登录一站式服务大厅
import requests
from RSA_password import get_password
import re
from url_data import *
from lxml import etree
from code_OCR import get_code


def login_server(username, password, login):  # 登录服务大厅
    requests.packages.urllib3.disable_warnings()  # 忽略不安全连接警告
    flag = ''  # 储存登录情况
    while True:
        try:
            response_index = login.get(login_url, timeout=15)  # 获取一站式服务大厅cookie
            # print('获取主页')
            html = etree.HTML(response_index.text)  # 解析主页html
            execution = html.xpath('//*[@id="fm1"]/ul/li[1]/input[1]/@value')  # 获取参数
            if execution:  # 获取成功时
                execution = execution[0]
                # print(execution)
            else:  # 获取失败，重新开始
                continue
            response_code = login.get(code_url, timeout=5)  # 请求验证码图片
            # print('获取验证码')
            img = response_code.content  # 获取验证码图片
            file = open('./code_img/' + username + '.png', 'wb')  # 创建验证码图片文件
            file.write(img)  # 写入验证码
            file.close()  # 关闭文件
            # print('识别验证码')
            code = get_code(username)  # 识别验证码
            if code == 'false':  # 识别失败，重新开始
                # print('识别失败，重新尝试')
                continue
            # print('识别成功')
            response_key = login.get(key_url, timeout=5)  # 获取RSA公钥
            # print('获取密钥')
            key = re.search('[0-9a-zA-Z]{256}', response_key.text).group()  # 正则匹配公钥
            # print('加密中')
            rsa_password = get_password(password, key)  # 使用公钥加密密码
            # print('加密成功')
            rsa_password = rsa_password.replace('\n', '')  # 去掉多余字符
            data = {
                'execution': execution,
                '_eventId': 'submit',
                'geolocation': '',
                'username': username,
                'password': rsa_password,
                'captcha': code
            }  # 登录参数
            # print('登录中')
            response_login = login.post(login_url, data=data, timeout=15)  # 尝试登录
            html = etree.HTML(response_login.text)  # 解析返回的html
            error = html.xpath('//*[@id="fm1"]/ul/li[4]/p/b/text()')  # 获取提示
            if not error:  # 如果获取提示为空则登录成功
                flag = '登录成功'
                # print('登录成功')
                break
            else:  # 获取提示不为空时，则登录失败了
                if error[0] == 'authenticationFailure.CaptchaFailException':  # 提示验证码错误
                    # print('验证码错误，重新尝试')
                    continue  # 重新尝试
                elif error[0] == 'Invalid credentials.':  # 提示用户或密码错误
                    flag = '用户名或密码错误'
                    # print('用户名或密码错误')
                    break  # 退出循环
        except TimeoutError:  # 请求超时，一般为服务大厅奔溃
            flag = '登录请求超时'
            # print('登录请求超时')
            break
    return flag  # 返回提示
