# Embedded file name: keygoe\keygoe.py
# -*- coding: utf-8 -*-
import os
import sys
from ctypes import *
import time
#import attlog as log
VOIP_PRINT_LOG = False

class Keygoe():
    """
    Keygoe \xe7\xb3\xbb\xe7\xbb\x9f\xe7\x9a\x84\xe8\xaf\xad\xe9\x9f\xb3\xe5\x8d\xa1
    """

    def __init__(self, log):
        """
        \xe6\xa3\x80\xe6\x9f\xa5\xe6\x98\xaf\xe5\x90\xa6\xe5\x87\x86\xe5\xa4\x87OK
        """
        self.h_voip = CDLL(os.path.join(os.path.dirname(__file__), 'VoipKeygoe.dll'))
        self.logger = log

    def init_keygoe_system(self):
        """
        \xe5\x87\x86\xe5\xa4\x87\xe6\x98\xaf\xe5\x90\xa6OK \xe7\x8a\xb6\xe6\x80\x81Free
        """
        configfile = os.path.join(os.path.dirname(__file__), '')
        n_ret = self.h_voip.InitKeygoeSystem(c_char_p(configfile))
        self.logger(str(n_ret))
        if n_ret == -2:
            log_info = u'\u8bfb\u53d6\u914d\u7f6e\u6587\u4ef6XMS_KEYGOE.INI\u5931\u8d25\u3002\u8bf7\u786e\u8ba4\u914d\u7f6e\u6587\u4ef6\u5185\u5bb9\u662f\u5426\u6b63\u786e\u3002'
            self.logger(log_info)
            #log.user_info(log_info)
        elif n_ret == -3:
            log_info = u'\u8fde\u63a5keygoe\u6d41\u7a0b\u6a21\u5757\u5931\u8d25\u3002\u8bf7\u786e\u8ba4IP\u5730\u5740\uff0c\u7aef\u53e3\u53f7\uff0c\u8d26\u53f7\u3001\u5bc6\u7801\u7b49\u4fe1\u606f\u8f93\u5165\u662f\u5426\u6b63\u786e\u3002\n\u6ce8\u610fIP\u5730\u5740\u3001\u7aef\u53e3\u53f7\u662f\u6307\u6d41\u7a0b\u6a21\u5757\u7684\u914d\u7f6e\u3002'
            self.logger(log_info)
            #log.user_info(log_info)
        return n_ret

    def clear_keygoe_trunk(self, trunk_id):
        """
        \xe9\x87\x8d\xe7\xbd\xaeTrunk\xe7\x9a\x84\xe7\x8a\xb6\xe6\x80\x81\xe5\x88\xb0Free
        """
        trunk_id -= 1
        try:
            n_ret = self.h_voip.ClearCall(c_int(trunk_id))
        except Exception as e:
            raise RuntimeError(u'\u8c03\u7528DLL\u4e2d\u7684\u65b9\u6cd5\u5931\u8d25')

        time.sleep(3)
        return n_ret

    def exit_keygoe_system(self):
        """
        \xe5\x87\x86\xe5\xa4\x87\xe6\x98\xaf\xe5\x90\xa6OK \xe7\x8a\xb6\xe6\x80\x81Free
        """
        n_ret = self.h_voip.ExitKeygoeSystem()
        del self.h_voip
        self.h_voip = None
        return n_ret

    def wait_trunk_init(self):
        """
        \xe5\x87\x86\xe5\xa4\x87\xe6\x98\xaf\xe5\x90\xa6OK \xe7\x8a\xb6\xe6\x80\x81Free
        """
        self.logger(u"等待通道准备好中....")
        n_ret = self.h_voip.WaitTrunkReady()
        self.logger(str(n_ret))
        if n_ret == -1:
            log_info = u'\u672a\u63a5\u6536\u5230keygoe\u6d41\u7a0b\u8fd4\u56de\u7684\u4e8b\u4ef6\u3002\u8bf7\u786e\u8ba4\u4ee5\u4e0b\u4fe1\u606f\uff1a\n1\u3001\u8f93\u5165\u53c2\u6570\u662f\u5426\u4e0ekeygoe\u7cfb\u7edf\u6d41\u7a0b\u6a21\u5757\u7684\u914d\u7f6e\u4e00\u81f4\u3002\n2\u3001keygoe\u670d\u52a1\u662f\u5426\u6b63\u5e38\u8fd0\u884c\u3002\u8bf7\u91cd\u542fkeygoe\u670d\u52a1\uff0c\u91cd\u65b0\u8fde\u63a5\u3002\n\u91cd\u542f\u65b9\u6cd5\uff1a\u5148\u8fd0\u884cC:\\DJKeygoe\\Bin\\Remove server.bat\uff0c\u518d\u8fd0\u884cC:\\DJKeygoe\\Bin\\start server.bat\u3002'
            #log_info = u"等待通道准备好时发生异常，请确保Keygoe线缆正确连接到了待测设备，确保待测设备有馈电产生"
            self.logger(log_info)
            #log.user_info(log_info)
        return n_ret

    def call_out_off_hook(self, trunk_id):
        """
        """
        trunk_id -= 1
        try:
            n_ret = self.h_voip.CallOutOffHook(c_int(trunk_id))
        except Exception:
            raise RuntimeError(u'\u8c03\u7528DLL\u4e2d\u7684\u65b9\u6cd5\u5931\u8d25')

        if VOIP_PRINT_LOG:
            self.get_trunk_state(trunk_id)
            self.get_trunk_link_state(trunk_id)
        return n_ret

    def dial(self, trunk_id, number):
        """
        """
        trunk_id -= 1
        if isinstance(number, unicode):
            str_number = number.encode('ASCII')
        else:
            str_number = number
        n_ret = self.h_voip.Dial(c_int(trunk_id), c_int(len(str_number)), c_char_p(str_number))
        if VOIP_PRINT_LOG:
            self.get_trunk_state(trunk_id)
            self.get_trunk_link_state(trunk_id)
        return n_ret

    def send_data(self, trunk_id, data):
        """
        """
        trunk_id -= 1
        if isinstance(data, unicode):
            str_data = data.encode('ASCII')
        else:
            str_data = data
        n_ret = self.h_voip.SendData(c_int(trunk_id), c_char_p(str_data))
        if VOIP_PRINT_LOG:
            self.get_trunk_state(trunk_id)
            self.get_trunk_link_state(trunk_id)
        return n_ret

    def get_recv_data(self, trunk_id, iLen = 0, seconds = 3):
        """
        """
        trunk_id -= 1
        self.h_voip.GetRecvData.restype = c_char_p
        n_ret = self.h_voip.GetRecvData(c_int(trunk_id), c_int(iLen), c_int(seconds))
        if VOIP_PRINT_LOG:
            self.get_trunk_state(trunk_id)
            self.get_trunk_link_state(trunk_id)
        return n_ret

    def clear_recv_data(self, trunk_id):
        """
        """
        trunk_id -= 1
        n_ret = self.h_voip.ClearRecvData(c_int(trunk_id))
        if VOIP_PRINT_LOG:
            self.get_trunk_state(trunk_id)
            self.get_trunk_link_state(trunk_id)
        return n_ret

    def send_fax_prepare(self, trunk_id):
        """
        """
        trunk_id -= 1
        n_ret = self.h_voip.SendFax_prepare(c_int(trunk_id))
        if VOIP_PRINT_LOG:
            self.get_trunk_state(trunk_id)
            self.get_trunk_link_state(trunk_id)
        return n_ret

    def send_fax(self, trunk_id, sendfile, bps_int, seconds, recordfile_send, recordfile_recv):
        """
        SendFax \xe5\xbf\x85\xe9\xa1\xbb\xe5\x85\x88\xe8\xb0\x83\xe7\x94\xa8send_fax_prepare
        """
        trunk_id -= 1
        if isinstance(sendfile, unicode):
            str_sendfile = sendfile.encode('ASCII')
        else:
            str_sendfile = sendfile
        iRecord = 0
        str_recordfile_send = ''
        str_recordfile_recv = ''
        if len(recordfile_send) < len('wav'):
            iRecord = 0
        else:
            iRecord = 1
            if isinstance(recordfile_send, unicode):
                str_recordfile_send = recordfile_send.encode('ASCII')
            else:
                str_recordfile_send = recordfile_send
            if isinstance(recordfile_recv, unicode):
                str_recordfile_recv = recordfile_recv.encode('ASCII')
            else:
                str_recordfile_recv = recordfile_recv
        info_c = c_char_p()
        n_ret = self.h_voip.SendFax(c_int(trunk_id), c_int(bps_int), c_char_p(str_sendfile), c_int(seconds), byref(info_c), c_int(iRecord), c_char_p(str_recordfile_send), c_char_p(str_recordfile_recv))
        if VOIP_PRINT_LOG:
            self.get_trunk_state(trunk_id)
            self.get_trunk_link_state(trunk_id)
            log_info = u'%s' % info_c.value
            self.user_info(log_info)
        return (n_ret, info_c.value)

    def recv_fax_prepare(self, trunk_id):
        """
        """
        trunk_id -= 1
        n_ret = self.h_voip.RecvFax_prepare(c_int(trunk_id))
        if VOIP_PRINT_LOG:
            self.get_trunk_state(trunk_id)
            self.get_trunk_link_state(trunk_id)
        return n_ret

    def start_recv_fax(self, trunk_id, savefile, bps_int, recordfile_send, recordfile_recv):
        """
        \xe5\xbf\x85\xe9\xa1\xbb\xe5\x85\x88\xe8\xb0\x83\xe7\x94\xa8 recv_fax_prepare
        """
        trunk_id -= 1
        if isinstance(savefile, unicode):
            str_savefile = savefile.encode('ASCII')
        else:
            str_savefile = savefile
        iRecord = 0
        str_recordfile_send = ''
        str_recordfile_recv = ''
        if len(recordfile_send) < len('wav'):
            iRecord = 0
        else:
            iRecord = 1
            if isinstance(recordfile_send, unicode):
                str_recordfile_send = recordfile_send.encode('ASCII')
            else:
                str_recordfile_send = recordfile_send
            if isinstance(recordfile_recv, unicode):
                str_recordfile_recv = recordfile_recv.encode('ASCII')
            else:
                str_recordfile_recv = recordfile_recv
        n_ret = self.h_voip.StartRecvFax(c_int(trunk_id), c_int(bps_int), c_char_p(str_savefile), c_int(iRecord), c_char_p(str_recordfile_send), c_char_p(str_recordfile_recv))
        if VOIP_PRINT_LOG:
            self.get_trunk_state(trunk_id)
            self.get_trunk_link_state(trunk_id)
        return n_ret

    def get_recv_fax_result(self, trunk_id, seconds):
        """
        """
        trunk_id -= 1
        info_c = c_char_p()
        n_ret = self.h_voip.GetRecvFaxResult(c_int(trunk_id), c_int(seconds), byref(info_c))
        if VOIP_PRINT_LOG:
            self.get_trunk_state(trunk_id)
            self.get_trunk_link_state(trunk_id)
            log_info = u'%s' % info_c.value
            self.logger(log_info)
            #log.user_info(log_info)
        return (n_ret, info_c.value)

    def check_call_in(self, trunk_id, seconds):
        """
        """
        trunk_id -= 1
        n_ret = self.h_voip.CheckCallIn(c_int(trunk_id), c_int(seconds))
        if VOIP_PRINT_LOG:
            self.get_trunk_state(trunk_id)
            self.get_trunk_link_state(trunk_id)
        return n_ret

    def call_in_off_hook(self, trunk_id):
        """
        """
        trunk_id -= 1
        n_ret = self.h_voip.CallInOffHook(c_int(trunk_id))
        if VOIP_PRINT_LOG:
            self.get_trunk_state(trunk_id)
            self.get_trunk_link_state(trunk_id)
        return n_ret

    def on_hook(self, trunk_id):
        """
        """
        trunk_id -= 1
        n_ret = self.h_voip.ClearCall(c_int(trunk_id))
        if VOIP_PRINT_LOG:
            self.get_trunk_state(trunk_id)
            self.get_trunk_link_state(trunk_id)
        return n_ret

    def get_trunk_state(self, trunk_id):
        """
        """
        trunk_id -= 1
        n_ret = self.h_voip.GetTrunkState(c_int(trunk_id))
        log_info = u'TrunkState is %d' % n_ret
        self.logger(log_info)
        #log.user_info(log_info)
        return n_ret

    def get_trunk_link_state(self, trunk_id):
        """
        """
        trunk_id -= 1
        n_ret = self.h_voip.GetTrunkLinkState(c_int(trunk_id))
        log_info = u'TrunkLinkState is %d' % n_ret
        self.logger(log_info)
        #log.user_info(log_info)
        return n_ret

    def set_flash(self, trunk_id):
        """
        """
        trunk_id -= 1
        n_ret = self.h_voip.SetFlash(c_int(trunk_id))
        if VOIP_PRINT_LOG:
            self.get_trunk_state(trunk_id)
            self.get_trunk_link_state(trunk_id)
        return n_ret

    def set_flash_time(self, iTimes):
        """
        """
        n_ret = self.h_voip.SetFlashTime(c_int(iTimes))
        return n_ret

    def set_fax_file(self, trunk_id, sendfile):
        """
        \xe5\xbf\x85\xe9\xa1\xbb\xe5\x9c\xa8prepare\xe4\xb9\x8b\xe5\x90\x8e\xe8\xb0\x83\xe7\x94\xa8\xef\xbc\x8c \xe6\xb7\xbb\xe5\x8a\xa0\xe4\xbc\xa0\xe7\x9c\x9f\xe6\x96\x87\xe4\xbb\xb6
        """
        trunk_id -= 1
        if isinstance(sendfile, unicode):
            str_sendfile = sendfile.encode('ASCII')
        else:
            str_sendfile = sendfile
        n_ret = self.h_voip.SetFaxFile(c_int(trunk_id), c_char_p(str_sendfile))
        if VOIP_PRINT_LOG:
            self.get_trunk_state(trunk_id)
            self.get_trunk_link_state(trunk_id)
        return n_ret

    def wait_some_tone(self, trunk_id, sTone, milliseconds):
        """
        \xe6\xa3\x80\xe6\xb5\x8b\xe9\x9f\xb3\xef\xbc\x8c\xe9\x9f\xb3\xe7\x94\xa8"G" -"L"\xe8\xa1\xa8\xe7\xa4\xba
        """
        trunk_id -= 1
        milliseconds = 1000 * milliseconds
        if isinstance(sTone, unicode):
            str_sTone = sTone.encode('ASCII')
        else:
            str_sTone = sTone
        n_ret = self.h_voip.WaitSomeTone(c_int(trunk_id), c_char_p(str_sTone), c_int(milliseconds))
        if VOIP_PRINT_LOG:
            self.get_trunk_state(trunk_id)
            self.get_trunk_link_state(trunk_id)
        return n_ret

    def update_tones_set(self):
        """
        """
        n_ret = self.h_voip.UpdateTones()
        return n_ret

    def start_record(self, trunk_id, savefile):
        """
        """
        trunk_id -= 1
        if isinstance(savefile, unicode):
            str_savefile = savefile.encode('ASCII')
        else:
            str_savefile = savefile
        n_ret = self.h_voip.StartRecord(c_int(trunk_id), c_char_p(str_savefile))
        if VOIP_PRINT_LOG:
            self.get_trunk_state(trunk_id)
            self.get_trunk_link_state(trunk_id)
        return n_ret

    def stop_record(self, trunk_id):
        """
        """
        trunk_id -= 1
        n_ret = self.h_voip.StopRecord(c_int(trunk_id))
        if VOIP_PRINT_LOG:
            self.get_trunk_state(trunk_id)
            self.get_trunk_link_state(trunk_id)
        return n_ret


def Test():
    from time import ctime, sleep
    print u'start test...'


if __name__ == '__main__':
    Test()
    print 'Test end...'