import urllib2
import time
import json


class ApiTest:
    def __init__(self, ip, port):
        self.time_stamp = time.time()*1000
        self.time_stamp_formart = "%.0f" % self.time_stamp
        self.logger_pipe = None
        self.start_state = False
        self.host = "%s:%d" % (ip, port)
        self.dhcp_start_ip = "192.168.1.2"
        self.logger("smartgateway test start.....")
        self.dhcp_start_submask = "255.255.255.0"
        self.host_mac = "2c:27:d7:e9:d1:23"
        self.url = "http://%s/apitest/cmcc.cmd?timeStamp=%s" % (self.host, self.time_stamp_formart)
        self.data = "jsonCfg="
        self.get_data = self.data + "{\"CmdType\":\"EXECUTE_TEST\",\"TestItem\":{\"SubItems\":[{\"OutputParam\":{},\"\
        Name\":\"WlanQuery Test\",\"" "InputParam\":{\"ssidx\":\"1\",\"step\":\"step1\",\"hostMAC\":\"%s\
        ,58:1F:28:89:2B:90\",\"radioType\":\"2.4G\"}}],\"Method\":\"Java\",\"Name\":\"WlanQuery Test\",\"\
        SubItemName\":\"\"}}" % self.host_mac

        self.get_data_result = self.data + "{\"CmdType\":\"QUERY_TEST_RESULT\",\"ItemName\":\"WlanQuery Test\",\
        \"SubItemName\":\"WlanQuery Test\",\"SyncFlag\":\"0\",\"QueryId\":0,\"Method\":\"Java\"}"

        self.set_data = self.data + "{\"CmdType\":\"EXECUTE_TEST\",\"TestItem\":{\"SubItems\":[{\"OutputParam\":{},\"Name\
        \":\"LANIP ConfigTask Test\",\"InputParam\":{\"DHCPEndIP\":\"192.168.1.250\",\"submask\":%s,\"\
        local IP\":\"192.168.1.1\",\"DHCPStartIP\":%s}}],\"Method\":\"Java\",\"Name\":\"LANIPConfigTask \
        Test\",\"SubItemName\":\"\"}}" % (self.dhcp_start_ip, self.dhcp_start_submask)

        self.headers = {
           "Accept-Encoding": "gzip, deflate",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.\
            98 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "http://%s" % self.host,
            "Referer": "http://%s/apitest/index.htm" % self.host,
            "Connection": "keep-alive"
        }

    def post_operation(self, get_data, headers):
        req = urllib2.Request(self.url, data=get_data, headers=headers)
        ret = urllib2.urlopen(req)
        return ret

    def start_get_api(self):
        ret = self.post_operation(self.get_data, self.headers)
        ret_text = ret.read()
        ret_json = json.dumps(ret_text)
        self.logger(ret_json)
        time.sleep(20)
        ret = self.post_operation(self.get_data_result, self.headers)
        ret_text = ret.read()
        ret_json = json.dumps(ret_text)
        self.logger(ret_json)

    def start_set_api(self):
        req = urllib2.Request(self.url, data=self.set_data, headers=self.headers)
        ret = urllib2.urlopen(req)
        ret_text = ret.read()
        ret_json = json.dumps(ret_text)
        self.logger(ret_json)

    def logger(self, str):
        if self.logger_pipe is not None:
            if self.start_state:
                self.logger_pipe.send(str)
        else:
            return


def test():
    apitest = ApiTest("192.168.1.1", 8080)
    apitest.start_get_api()
    apitest.start_set_api()

if __name__ == "__main__":
    test()