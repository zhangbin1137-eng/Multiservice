# -*- coding: utf-8 -*-
from ctypes import *
from os import path
import time
#environ['path'] += ';C:\\Program Files\\Ixia\\IxChariot\\'



#
class Chariot():
    def __init__(self):
        self.testHandle=c_ulong
        self.pairHandle=c_ulong
        self.m_h_chariot=None
        self.init_chariot()

    def init_chariot(self):
        """
        初始化Chariot环境
        """
        current_path=path.dirname(__file__)
        dll_path=path.join(current_path, "ctdll.dll")
        self.m_h_chariot = cdll.LoadLibrary(dll_path)
        CHRapiinitialize = self.m_h_chariot.api_initialize
        CHRapiinitialize.restypes =[c_int]
        ret = CHRapiinitialize()
        return ret

    def add_pair(self,e1="172.16.30.23",e2="172.16.30.36",
                       script="c:/Program Files/Ixia/IxChariot/Scripts/Throughput.scr",
                       protocol='TCP',pairCount=4):
        """
        添加pair
        """
        CHRadd_pair = self.m_h_chariot.add_pair
        CHRadd_pair.argtypes =(c_char_p,c_char_p,c_char_p,c_int,c_int)
        CHRadd_pair.restypes =[c_int]
        if protocol=='TCP':
            pro=2
        else:
            pro=5
        ret=CHRadd_pair(e1,e2,script,pro,pairCount)
        return ret

    def set_option_time(self,time=10):
        """
        设置测试时间
        """
        CHRset_option_time=self.m_h_chariot.set_option_time
        CHRset_option_time.argtypes =[c_ulong]
        CHRset_option_time.restypes =(c_int)
        ret=CHRset_option_time(time)
        return ret
    def execute_chariot_throughtput(self,time=120):
        """
        执行Chariot测试，并在指定时间范围内等待获取结果
        """
        avg=c_double()
        CHRexecute_chariot_throughtput=self.m_h_chariot.execute_chariot_throughtput
        CHRexecute_chariot_throughtput.argtypes = (POINTER(c_double),c_ulong)
        CHRexecute_chariot_throughtput.restypes =(c_int)
        ret=CHRexecute_chariot_throughtput(byref(avg),time)
        avg="%.2f" %(avg.value)
        return ret,avg
    def save_result(self,dd="D:/lbtest.tst"):
        """
        保存测试结果
        """
        CHRsave_result=self.m_h_chariot.save_resule_file
        CHRsave_result.argtypes = [c_char_p]
        CHRsave_result.restypes =(c_int)
        ret=CHRsave_result(dd)
        return ret
    def test_delete(self):
        """
        删除测试对象
        """
        CHRtest_delete=self.m_h_chariot.test_delete
        CHRtest_delete.restypes =[c_int]
        ret=CHRtest_delete()
        return ret
    def pari_delete(self):
        """
        删除测试对象中的所有pair
        """
        CHRpari_delete=self.m_h_chariot.pair_delete
        CHRpari_delete.restypes =[c_int]
        ret=CHRpari_delete()
        return ret
    def start_chariot(self, ):
        """
        开始Chariot测试
        """
        CHRstart_chariot=self.m_h_chariot.start_chariot
        CHRstart_chariot.restypes =[c_int]
        ret=CHRstart_chariot()
        return ret
    def stop_chariot(self):
        """
        中断Chariot测试
        """
        CHRstop_chariot=self.m_h_chariot.stop_chariot
        CHRstop_chariot.restypes =[c_int]
        ret=CHRstop_chariot()
        return ret
    def abandon_chariot(self):
        """
        停止Chariot测试，在stop_chariot之后用
        """
        CHRabandon_chariot=self.m_h_chariot.abandon_chariot
        CHRabandon_chariot.restypes =[c_int]
        ret=CHRabandon_chariot()
        return ret
    def get_throughput_result(self,time=120):
        """
        在指定时间范围内获取测试结果
        """
        avg=c_double()
        CHRget_throughput_result=self.m_h_chariot.get_throughput_result
        CHRget_throughput_result.argtypes =[POINTER(c_double),c_ulong]
        CHRget_throughput_result.restypes =[c_int]
        ret=CHRget_throughput_result(byref(avg),time)
        avg="%.2f" %(avg.value)
        return ret,avg
    
    
        

def tests1():
    C1=Chariot()
    
    C1.pari_delete()
    C1.add_pair(e1="192.168.0.20",e2="192.168.0.30",pairCount=8,protocol='TCP',script='c:/Program Files/Ixia/IxChariot/Scripts/High_Performance_Throughput.scr')
    C1.set_option_time(20)
    C1.start_chariot()
    time.sleep(20)
    a,b=C1.get_throughput_result()
    print a,b
    C1.stop_chariot()
    a,b=C1.get_throughput_result()
    print a,b
    #C1.add_pair('11.11.11.36','11.11.11.36',protocol="UDP",pairCount=2)
    #a=C1.execute_chariot_throughtput(time=120)
    print a
    C1.save_result()
    #C1.pari_delete()
    #C1.add_pair(pairCount=4)
    #C1.execute_chariot_throughtput()
    #C1.pari_delete()
    C1.test_delete()
    C1.add_pair(e1="192.168.0.20",e2="192.168.0.30",pairCount=8,protocol='TCP',script='c:/Program Files/Ixia/IxChariot/Scripts/High_Performance_Throughput.scr')
    C1.set_option_time(20)
    C1.start_chariot()
    time.sleep(20)
    a,b=C1.get_throughput_result()
    C1.save_result("D:/lbtest2.tst")
    print a,b
    
    
if __name__ == '__main__':
    tests1()
    #C1=Chariot()

    
    

    