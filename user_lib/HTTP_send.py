#coding=utf-8
import httplib
import urllib
import time
import json

class HTTP_client:
    def __init__(self):
        self.log_data = {}
        self.host = "127.0.0.1"
        self.server_port = 80
        self.requrl = ""
        self.header_data = {"Content-type": "application/x-www-form-urlencoded; charset=UTF-8","Accept-Encoding": \
            "gzip, deflate","Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8","Accept": "application/json, text/javascript,\
             */*; q=0.01","User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko\
             ) Chrome/71.0.3578.98 Safari/537.36"}
        self.conn = httplib.HTTPConnection(self.host,self.server_port)
        self.ret_str = ""
    def send_log(self):
        self.conn.request('POST', self.requrl, urllib.urlencode(self.log_data), self.header_data)
        response = self.conn.getresponse()
        res = response.read()
        ret = json.loads(res)
        if ret['result'] == '0':
            return ret['msg']
        else:
            return  ret['msg']


def main():
    http_client = HTTP_client()
    http_client.log_data = {'sn': '219801A1RGP100V86000'}
    http_client.host = "127.0.0.1"
    http_client.requrl = "http://%s/showa/route.php?op=insert_log" % http_client.host
    i = 0
    while True:
        http_client.log_data['log'] = time.ctime() + "log %d" % i
        print http_client.send_log()
        i += 1


if __name__ == '__main__':
    main()