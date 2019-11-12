# 对密码进行RSA加密，有2种方法，一个是python直接加密，一个是使用服务大厅提供的js加密
import os


def encrypt(plaintext, public_modulus, public_exponent='10001'):
    """
    直接使用python加密
    :param plaintext: 明文密码
    :param public_modulus: 公钥m
    :param public_exponent: 公钥e，默认为10001
    :return:
    """
    public_modulus = int(public_modulus, 16)  # 将公钥m转换成10进制
    public_exponent = int(public_exponent, 16)  # 将公钥e转换成10进制
    plaintext = int(plaintext.encode('utf-8').hex(), 16)  # 将明文密码转换成utf-8编码再转换成10进制
    cipher_text = pow(plaintext, public_exponent, public_modulus)  # RSA公钥加密
    return '%x' % cipher_text  # 转换成16进制并返回


def get_password(password, pubkey_m, pubkey_e='10001'):
    """
    将获取的公钥和密码，填充在js语法的字符串中，在将字符串写入js文件，然后使用nodejs调用js
    :param password:密码
    :param pubkey_m:公钥m
    :param pubkey_e:公钥e
    :return:加密后的密码
    """
    data = ("let password = '{}'\n"  # 填充公钥
            "let code = require('./RSA_code')\n"  # 获取RSA加密文件js
            "let key = new code.RSAUtils.getKeyPair('{}', \'\', '{}')\n"  # 使用提供的RSA加密js文件的接口进行处理
            "let reversedPwd = password.split(\'\').reverse().join(\'\')\n"  # 将密码逆序
            "let encrypedPwd = code.RSAUtils.encryptedString(key, reversedPwd)\n"  # 使用提供的RSA加密js文件的接口进行加密
            "console.log(encrypedPwd)").format(password, pubkey_e, pubkey_m)  # 输出加密后的密码
    use_RSAcode = open('./static/js/use_RSAcode.js', 'w')  # 打开文件
    use_RSAcode.write(data)  # 写入js
    use_RSAcode.close()  # 关闭文件
    node = os.popen('node ./static/js/use_RSAcode.js')  # 使用node命令调用js
    password_data = node.read()  # 获取输出结果
    node.close()  # 关闭node
    password_data = password_data.replace('\n', '')  # 去掉多余字符
    return password_data  # 返回加密后的密码
