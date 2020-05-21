# -*- coding: utf-8 -*-
from chariot import Chariot
from os.path import abspath,dirname,join,exists
from pythoncom import CoInitialize
from time import sleep

class Chariot_controller():
    def __init__(self):
        self.start_state = False
        self.logger_pipe = None
        self.dict_config_items = {}
        self.chariot_ip1 = ""
        self.chariot_ip2 = ""
        self.chariot_obj = None

    def init_chariot(self):
        """
        Chariot线程，初始化Chariot后，进入Chariot测试循环
        """
        # 获取GUI信息
        chariot_protocol = self.dict_config_items.get('flow_protocol')
        chariot_tcp_script = self.dict_config_items.get('tcp_script')
        chariot_udp_script = self.dict_config_items.get('udp_script')
        chariot_num = self.dict_config_items.get('flow_count')
        chariot_time = self.dict_config_items.get('flow_time')
        mode = ['TX', 'RX', 'TX+RX']
        chariot_flow_mode = mode[self.dict_config_items.get('test_mode')]
        chariot_script_path = join(abspath(dirname(dirname(__file__))), 'resource6.70')
        self.chariot_ip1 = self.dict_config_items.get("local_endpoint")
        self.chariot_ip2 = self.dict_config_items.get("remote_endpoint")
        try:
            CoInitialize()
            self.chariot_obj = Chariot()
            ret = self.chariot_obj.init_chariot()
            self.logger(u"Chariot初始化成功")
            while self.start_state:
                self._chariot_fun_loop(chariot_flow_mode, chariot_protocol, chariot_time, chariot_num, chariot_tcp_script,
                                       chariot_udp_script)
        finally:
            self.logger(u'Chariot控制线程结束')
            del self.chariot_obj
            self.start_state = False

    def _chariot_fun_loop(self, mode, chariot_protocol, chariot_time, chariot_num, chariot_tcp_script,
                          chariot_udp_script):
        """
        Chariot测试循环，通过两层循环测试完所有用例
        """
        # 获取GUI信息
        chariot_num = int(chariot_num)
        chariot_time = int(chariot_time)
        chariot_script_path = join(abspath(dirname(dirname(__file__))),  'resource6.70')
        try:
            # 获取脚本路径
            if chariot_protocol == 'UDP':
                script_path = join(chariot_script_path, chariot_udp_script)
                self.logger(u"当前选择测试脚本为" + chariot_udp_script)
            else:
                try:
                    script_path = join(chariot_script_path, chariot_tcp_script)
                except Exception,e:
                    self.logger(e)
                self.logger(u"当前选择测试脚本为" + chariot_tcp_script)


            if mode == 'TX+RX':
                cnum = int(chariot_num) / 2
                self.chariot_obj.add_pair(self.chariot_ip1, self.chariot_ip2, script_path,
                                          chariot_protocol, cnum)
                self.chariot_obj.add_pair(self.chariot_ip2, self.chariot_ip1, script_path,
                                          chariot_protocol, cnum)
            elif mode == 'TX':
                self.chariot_obj.add_pair(self.chariot_ip1, self.chariot_ip2, script_path,
                                          chariot_protocol, chariot_num)
            else:
                self.chariot_obj.add_pair(self.chariot_ip2, self.chariot_ip1, script_path,
                                          chariot_protocol, chariot_num)
            self.chariot_obj.set_option_time(chariot_time)
            self.logger(u"建立Chariot流成功，协议%s,Pair数%d，测试时间%s" % (
                chariot_protocol, chariot_num, chariot_time))
            self.chariot_obj.set_option_time(chariot_time)
            ret = self.chariot_obj.start_chariot()
            if chariot_time != 0:
                excute_time = 0
                for tm in range(chariot_time):
                    if not self.start_state:
                        self.chariot_obj.start_chariot()
                        self.logger(u"手动结束Chariot")
                        print u"手动结束Chariot"
                        break
                    sleep(1)
                    excute_time += 1
                    self.logger(str(excute_time)+"ccccc")
            self.logger(str(excute_time)+"aaaaaaaaaaaaaaaaa")
            wait = excute_time * 2
            self.logger(str(wait))
            ret, self.current_throuput = self.chariot_obj.get_throughput_result(wait)
            # 保存Chariot结果
            self.logger(u"Chariot测试结束")
            print u"Chariot测试结束"
            chariot_path = chariot_protocol + mode + '.tst'
            print chariot_path
            self.chariot_obj.save_result(chariot_path)
            self.logger(u"Chariot测试结果保存完成")
            print u"Chariot测试结果保存完成"
            self.chariot_obj.test_delete()
        except Exception, e:
            self.logger(u"Chariot运行时出现异常:%s" % e)
            self.chariot_obj.stop_chariot()
            self.current_throuput = None

    def logger(self, str):
        if self.logger_pipe is not None:
            if self.start_state:
                self.logger_pipe.send(str)
        else:
            return