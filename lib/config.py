# -*- coding: utf-8 -*-
from os import path

TESTCFG_SUC = 0
TESTCFG_FAIL = -1

class Config(object):
    """
    load and save radiofrequency test configuration
    """
    
    def __init__(self):
        """
        initial
        """
        
        self.dict_config_items = None
        self.config_file = "config.json"
        self.dut_config_file = "dut_config.json"
        self.chariot_config_file = "chariot_config.json"
        self.keygoe_config_file = "keygoe_config.json"
        self.dut_dict_config_items = None
        self.chariot_dict_config_items = None
        self.keygoe_dict_config_items = None

    def load_cfg(self):
        """
        load test configuration from .ini file
        """
        n_ret = TESTCFG_SUC    # 执行结果：SUC or FAIL
        str_ret = ""                         # 执行结果信息
        
        try:
            test_cfg_path = path.join(path.dirname(__file__), self.config_file)
            test_cfg_file = open(test_cfg_path, "rb+")
            cfg_info = test_cfg_file.read()
            dict_test_cfg = eval(cfg_info)    
            test_cfg_file.close()
            
            self.dict_config_items = dict_test_cfg
            
        except Exception, e:
            n_ret = TESTCFG_FAIL
            str_ret = u"从配置文件中加载配置信息发生异常，错误信息为：%s" % e
            
        return n_ret, str_ret

    def load_dut_cfg(self):
        """
        load test configuration from .ini file
        """
        n_ret = TESTCFG_SUC  # 执行结果：SUC or FAIL
        str_ret = ""  # 执行结果信息

        try:
            test_cfg_path = path.join(path.dirname(__file__), self.dut_config_file)
            test_cfg_file = open(test_cfg_path, "rb+")
            cfg_info = test_cfg_file.read()
            dict_test_cfg = eval(cfg_info)
            test_cfg_file.close()

            self.dut_dict_config_items = dict_test_cfg

        except Exception, e:
            n_ret = TESTCFG_FAIL
            str_ret = u"从配置文件中加载配置信息发生异常，错误信息为：%s" % e

        return n_ret, str_ret

    def load_keygoe_cfg(self):
        """
        load test configuration from .ini file
        """
        n_ret = TESTCFG_SUC  # 执行结果：SUC or FAIL
        str_ret = ""  # 执行结果信息

        try:
            test_cfg_path = path.join(path.dirname(__file__), self.keygoe_config_file)
            test_cfg_file = open(test_cfg_path, "rb+")
            cfg_info = test_cfg_file.read()
            dict_test_cfg = eval(cfg_info)
            test_cfg_file.close()

            self.keygoe_dict_config_items = dict_test_cfg

        except Exception, e:
            n_ret = TESTCFG_FAIL
            str_ret = u"从Keygoe配置文件中加载配置信息发生异常，错误信息为：%s" % e

        return n_ret, str_ret

    def load_chariot_cfg(self):
        """
        load test configuration from .ini file
        """
        n_ret = TESTCFG_SUC  # 执行结果：SUC or FAIL
        str_ret = ""  # 执行结果信息

        try:
            test_cfg_path = path.join(path.dirname(__file__), self.chariot_config_file)
            test_cfg_file = open(test_cfg_path, "rb+")
            cfg_info = test_cfg_file.read()
            dict_test_cfg = eval(cfg_info)
            test_cfg_file.close()

            self.chariot_dict_config_items = dict_test_cfg

        except Exception, e:
            n_ret = TESTCFG_FAIL
            str_ret = u"从配置文件中加载配置信息发生异常，错误信息为：%s" % e

        return n_ret, str_ret

    def save_cfg(self, dict_cfg):
        """
        save test configuration to .ini file
        """
        
        n_ret = TESTCFG_SUC    # 执行结果：SUC or FAIL
        str_ret = ""                         # 执行结果信息
        try:
            # update dict
            test_cfg_path = path.join(path.dirname(__file__), self.config_file)
            test_cfg_file = open(test_cfg_path, "rb+")
            cfg_info = test_cfg_file.read()
            test_cfg_file.close()
            try:
                dict_test_cfg = eval(cfg_info)
            except Exception, e:
                dict_test_cfg = {}
            dict_test_cfg.update(dict_cfg)
        except Exception, e:
            n_ret = TESTCFG_FAIL
            str_ret = u"更新配置信息发生异常，错误信息为：%s" % e
        
        try:
            # save to file
            test_cfg_file = open(test_cfg_path, "wb+")
            cfg_info = str(dict_test_cfg)
            test_cfg_file.write(cfg_info)
            test_cfg_file.close()
        except Exception, e:
            n_ret = TESTCFG_FAIL
            str_ret = u"保存配置信息到配置文件发生异常，错误信息为：%s" % e
        return n_ret, str_ret

    def save_dut_cfg(self, dict_cfg):
        """
        save test configuration to .ini file
        """

        n_ret = TESTCFG_SUC  # 执行结果：SUC or FAIL
        str_ret = ""  # 执行结果信息
        try:
            # update dict
            test_cfg_path = path.join(path.dirname(__file__), self.dut_config_file)
            test_cfg_file = open(test_cfg_path, "rb+")
            cfg_info = test_cfg_file.read()
            test_cfg_file.close()
            try:
                dict_test_cfg = eval(cfg_info)
            except Exception, e:
                dict_test_cfg = {}
            dict_test_cfg.update(dict_cfg)
        except Exception, e:
            n_ret = TESTCFG_FAIL
            str_ret = u"更新DUT配置信息发生异常，错误信息为：%s" % e

        try:
            # save to file
            test_cfg_file = open(test_cfg_path, "wb+")
            cfg_info = str(dict_test_cfg)
            test_cfg_file.write(cfg_info)
            test_cfg_file.close()
        except Exception, e:
            n_ret = TESTCFG_FAIL
            str_ret = u"保存DUT配置信息到配置文件发生异常，错误信息为：%s" % e
        return n_ret, str_ret

    def save_chariot_cfg(self, dict_cfg):
        """
        save test configuration to .ini file
        """

        n_ret = TESTCFG_SUC  # 执行结果：SUC or FAIL
        str_ret = ""  # 执行结果信息
        try:
            # update dict
            test_cfg_path = path.join(path.dirname(__file__), self.chariot_config_file)
            test_cfg_file = open(test_cfg_path, "rb+")
            cfg_info = test_cfg_file.read()
            test_cfg_file.close()
            try:
                dict_test_cfg = eval(cfg_info)
            except Exception, e:
                dict_test_cfg = {}
            dict_test_cfg.update(dict_cfg)
        except Exception, e:
            n_ret = TESTCFG_FAIL
            str_ret = u"更新Chariot配置信息发生异常，错误信息为：%s" % e

        try:
            # save to file
            test_cfg_file = open(test_cfg_path, "wb+")
            cfg_info = str(dict_test_cfg)
            test_cfg_file.write(cfg_info)
            test_cfg_file.close()
        except Exception, e:
            n_ret = TESTCFG_FAIL
            str_ret = u"保存DUT配置信息到配置文件发生异常，错误信息为：%s" % e
        return n_ret, str_ret

    def save_keygoe_cfg(self, dict_cfg):
        """
        save test configuration to .ini file
        """

        n_ret = TESTCFG_SUC  # 执行结果：SUC or FAIL
        str_ret = ""  # 执行结果信息
        try:
            # update dict
            test_cfg_path = path.join(path.dirname(__file__), self.keygoe_config_file)
            test_cfg_file = open(test_cfg_path, "rb+")
            cfg_info = test_cfg_file.read()
            test_cfg_file.close()
            try:
                dict_test_cfg = eval(cfg_info)
            except Exception, e:
                dict_test_cfg = {}
            dict_test_cfg.update(dict_cfg)
        except Exception, e:
            n_ret = TESTCFG_FAIL
            str_ret = u"更新Keygoe配置信息发生异常，错误信息为：%s" % e

        try:
            # save to file
            test_cfg_file = open(test_cfg_path, "wb+")
            cfg_info = str(dict_test_cfg)
            test_cfg_file.write(cfg_info)
            test_cfg_file.close()
        except Exception, e:
            n_ret = TESTCFG_FAIL
            str_ret = u"保存Keygoe配置信息到配置文件发生异常，错误信息为：%s" % e
        return n_ret, str_ret

if __name__ == '__main__':
    print "test start..."
    obj=Config()
    obj.load_cfg()
    print obj.dict_config_items
    obj.save_cfg({"${g_RF_CFG_TELNET_IP}":u"192.168.0.1"})
    obj.load_cfg()
    print obj.dict_config_items
    print "test end"
