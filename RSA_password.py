# 使用一站式服务大厅提供的js加密文件加密
import os


def get_password(password, pubkey):
    """
    将获取的公钥和密码，填充在js语法的字符串中，在将字符串写入js文件，然后使用nodejs调用js
    :param password:密码
    :param pubkey:公钥
    :return:加密后的密码
    """
    data = ("let password = '{}'\n"  # 填充公钥
            "let code = require('./RSA_code')\n"  # 获取RSA加密文件js
            "let key = new code.RSAUtils.getKeyPair('10001', \'\', '{}')\n"  # 使用提供的RSA加密js文件的接口进行处理
            "let reversedPwd = password.split(\'\').reverse().join(\'\')\n"  # 将密码逆序
            "let encrypedPwd = code.RSAUtils.encryptedString(key, reversedPwd)\n"  # 使用提供的RSA加密js文件的接口进行加密
            "console.log(encrypedPwd)").format(password, pubkey)  # 输出加密后的密码
    use_RSAcode = open('./static/js/use_RSAcode.js', 'w')  # 打开文件
    use_RSAcode.write(data)  # 写入js
    use_RSAcode.close()  # 关闭文件
    node = os.popen('node ./static/js/use_RSAcode.js')  # 使用node命令调用js
    password_data = node.read()  # 获取输出结果
    node.close()  # 关闭node
    return password_data  # 返回加密后的密码
