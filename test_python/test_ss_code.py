# encoding: utf-8

import base64
import qrcode

method = 'aes-256-cfb'
hostname = '95.179.180.206'
port = 50001
password = 'wintertrump_2017@check'
'''
method = 'bf-cfb'
hostname = '192.168.100.1'
port = 8888
password = 'test'
'''
string = '{}-auth:{}@{}:{}'.format(method, password, hostname, port)
string_64 = base64.urlsafe_b64encode(string)
ss_url = 'ss://' + string_64.strip('=')
print(ss_url)

img = qrcode.make(ss_url)
img.save("test_qrcode.png")


