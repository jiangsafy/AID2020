#class   encode-生成会员卡  decode-解析会员卡
import json
import base64
import time
import hmac
import copy

class Jwt():

    def __init__(self):
        pass

    @staticmethod
    def encode(body, key, exp=300):
        #body {'username':'guoxiaonao'}
        #key - hmac sha256 要用到的key
        #exp - 会员卡的有效期 默认是s

        # init header
        header = {'typ': 'JWT', 'alg':'HS256'}
        #separators: 分割符, 类型为元组（1,2）;元组内的第一个参数为每个键值对之间用什么分隔；第二个参数为每个key和value之间用什么分隔
        #sort_keys 是否排序json字符串
        header_json = json.dumps(header, separators=(',',':'),sort_keys=True)
        header_bs =  Jwt.b64encode(header_json.encode())

        #init payload
        payload = copy.deepcopy(body)
        payload['exp'] = time.time() + int(exp)
        payload_json = json.dumps(payload, separators=(',',':'),sort_keys=True)
        payload_bs  = Jwt.b64encode(payload_json.encode())

        #签名，规则为 前两部分b64串用 . 相连，用hmac-sha256进行计算
        hm = hmac.new(key.encode(), header_bs + b'.' + payload_bs, digestmod='SHA256')
        hm_bs = Jwt.b64encode(hm.digest())

        return header_bs + b'.' + payload_bs + b'.' + hm_bs

    @staticmethod
    def b64encode(j_s):
        return base64.urlsafe_b64encode(j_s).replace(b'=',b'')

    @staticmethod
    def b64decode(b_s):
        #abc def g
        # 标准长度32  删掉一个等号31 31%4
        rem = len(b_s) % 4
        if rem > 0:
            b_s += b'=' * (4-rem)
        return base64.urlsafe_b64decode(b_s)


def decode(token, key):
    # 删掉的=?
    # 校验一下当前token 是不是真的是我们签发
    # 检查一下 是否还在有效期
    # 取出username or uid
    header_b, payload_b, sign = token.split(b'.')
    hm = hmac.new(key.encode(), header_b + b'.' + payload_b, digestmod='SHA256')
    if sign != Jwt.b64encode(hm.digest()):
        raise()

    payload_j = Jwt.b64decode(payload_b)
    payload = json.loads(payload_j)

    if 'exp' in payload:
        now = time.time()
        if int(now) > int(payload['exp']):
            print('---The token expire')
            raise()

    return payload


if __name__ == '__main__':

    s = Jwt.encode({'username':'guoxiaonao'}, 'abcdef', 3)
    print(s)
    #b'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1ODEzMDUwNjcuMzY2NzksInVzZXJuYW1lIjoiZ3VveGlhb25hbyJ9.iKxB1U55qY2aqV2060rSzijk3JyV9QET342MKQONERM'
    #time.sleep(5)
    print(Jwt.decode(s, 'abcdef'))



















