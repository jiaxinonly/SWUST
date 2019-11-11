# 自动识别验证码，针对服务大厅验证码进行处理在识别
from PIL import Image
from pytesseract import *
import cv2

table = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
         'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
         'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
         'z']  # 验证码字符表

dataset = set('')  # 收集字符边边以外的干扰线的RGB


def clean_color(file_dir, img_name):  # 去除字符四周的干扰线
    img = Image.open(file_dir + '/' + img_name)  # 打开验证码图片
    pix_data = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b = pix_data[x, y]
            if r == g == b or r < 35 and g < 35 and b < 35:
                pix_data[x, y] = 255, 255, 255
            if y < 7 or y > 28 or x < 19 or x > 94:
                dataset.add('(' + str(r) + ',' + str(g) + ',' + str(b) + ')')  # 收集去除的干扰线的RGB
                pix_data[x, y] = 255, 255, 255
    for y in range(h):
        for x in range(w):
            r, g, b = pix_data[x, y]
            string = '(' + str(r) + ',' + str(g) + ',' + str(b) + ')'
            if string in dataset:  # 去除跟干扰线相同的RGB为
                pix_data[x, y] = 255, 255, 255
    img.save(file_dir + '/' + img_name)  # 保存处理后的图片
    return img


def binary_image(file_dir, img_name):  # 二值化，即灰度化，将验证码变成黑白，以提高识别率
    im = cv2.imread(file_dir + '/' + img_name)  # 打开图片
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  # 二值化
    h, w = im.shape[:2]
    for y in range(1, w - 1):
        for x in range(1, h - 1):
            if im[x, y] > 220:  # 将较浅的灰色去掉
                im[x, y] = 255
            else:  # 将其它灰色加深为黑色
                im[x, y] = 0
    cv2.imwrite(file_dir + '/' + img_name, im)  # 保存处理好的图片
    return im


def get_code(username):  # 识别验证码主函数
    file_dir = './code_img'  # 验证码保存的目录

    img_name = username + '.png'  # 获取要识别的验证码

    img = clean_color(file_dir, img_name)  # 去除杂色

    img = binary_image(file_dir, img_name)  # 二值化

    data = image_to_string(img, lang='eng')  # 识别验证码
    code_data = ''  # 储存识别后的验证码字符
    for x in data:
        if x in table:  # 识别出的字符必须在验证码表中
            code_data += x
    if len(code_data) == 4:  # 如果识别出来的字符正好是4个
        return code_data.upper()
    else:  # 否则识别失败
        return 'false'
