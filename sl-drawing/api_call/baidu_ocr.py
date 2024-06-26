# coding=utf-8

import sys
import json
import base64

# 保证兼容python2以及python3
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus

# 防止https证书校验不正确
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# API_KEY = 'lyuUDvHD3VcjO0L8EAFRD40n'
API_KEY = 'GMIWtKsFv8PYKOBtkvnlBPfP'

# SECRET_KEY = 'eAK7S5MkBVYh3iNfWQDNX0FDFTE1x9WT'
SECRET_KEY = 'HkGI88mDhh215v2w3B9lp5I2KiUXNBDq'

# OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
# OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/general"

"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'

"""
    获取token
"""


def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    if (IS_PY3):
        result_str = result_str.decode()

    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print('please overwrite the correct API_KEY and SECRET_KEY')
        exit()


"""
    读取文件
"""


def read_file(image_path):
    f = None
    try:
        f = open(image_path, 'rb')
        return f.read()
    except:
        print('read image file fail')
        return None
    finally:
        if f:
            f.close()


"""
    调用远程服务
"""


def request(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        if (IS_PY3):
            result_str = result_str.decode()
        return result_str
    except URLError as err:
        print('request error.....')
        print(err)


def ocr(token, img):
    texts = []
    probabilities = []
    locations = []
    # 获取access token
    # token = fetch_token()

    # 拼接通用文字识别高精度url
    image_url = OCR_URL + "?access_token=" + token

    # 读取测试图片
    file_content = read_file(img)
    try:
        # 调用文字识别服务
        result = request(image_url, urlencode({'image': base64.b64encode(file_content),
                                               'probability': 'true'}))
        # print(result)

        # 解析返回结果
        result_json = json.loads(result)
        # print(result_json)

        for words_result in result_json["words_result"]:
            texts.append(words_result["words"])
            probabilities.append(words_result["probability"]["average"])
            # locations.append(words_result["location"])

        return texts, probabilities

    except Exception as e:
        import traceback
        traceback.print_stack()
        print('ocr error.........')
        print(e)
        return None

