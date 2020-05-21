# Embedded file name: ATTVoip.py
# -*- coding: utf-8 -*-
import sys
import time
from keygoe.keygoe import Keygoe
import ConfigParser
import os
VOIP_FUN_OK = 1
VOIP_FUN_FIAL = -1

class _PHONESTATE():
    """
    """
    S_NONE = 1
    S_INIT = 2
    S_CALL_OUT_OFFHOOK = 3
    S_CHECK_CALL_IN = 5
    S_IN_CALL = 7
    S_RECV_FAX_START = 8
    S_ONHOOK = 9
    S_CLEAR_CALL = 10


class CPEPhone():

    def __init__(self, trunk_id):
        """
        CPE\xe7\x9b\xb8\xe5\x85\xb3\xe4\xbf\xa1\xe6\x81\xaf
        """
        self.trunk_id = trunk_id
        self.state = _PHONESTATE.S_NONE

    def get_trunk(self):
        return self.trunk_id

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def reset(self):
        self.state = _PHONESTATE.S_NONE


class AttToneConfig():

    def __init__(self, log):
        self.user_info = log
        self.freq_dict = {}
        self.cf = ConfigParser.ConfigParser()
        self.inifile = os.path.join(os.path.dirname(__file__), 'keygoe\\XMS_KEYGOE.INI')
        self.user_info(self.inifile)
        self.cf.read(self.inifile)
        self._read_all_freq()
        self._update_freq()
        self.user_info(u"初始化ATTToneConfig成功")

    def _read_all_freq(self):
        """
        \xe8\xaf\xbb\xe5\x8f\x96\xe9\x85\x8d\xe7\xbd\xae\xe6\x96\x87\xe4\xbb\xb6\xe8\x8e\xb7\xe5\x8f\x96\xe6\x9c\x89\xe5\x93\xaa\xe9\xa2\x91\xe7\x8e\x87
        """
        self.freq_dict.clear()
        index_freq = 0
        ss = self.cf.sections()
        for item in ss:
            if item in ('ConfigInfo', 'Freq'):
                continue
            try:
                Freq = self.cf.getint(item, 'freq')
                if Freq not in self.freq_dict.keys():
                    self.freq_dict[Freq] = index_freq
                    index_freq += 1
            except Exception as e2:
                log_info = u'\u8bfb\u53d6\u914d\u7f6e\u6587\u4ef6\u8282\u70b9%s\u5931\u8d25.' % item
                self.user_info(u"出错")
                self.user_info(log_info)
                raise RuntimeError(log_info)

    def _update_freq(self):
        """
        \xe6\x9b\xb4\xe6\x96\xb0\xe9\xa2\x91\xe7\x8e\x87\xe7\x9a\x84\xe9\x85\x8d\xe7\xbd\xae\xef\xbc\x8cupdate \xe6\x89\x80\xe6\x9c\x89\xe9\x9f\xb3\xe7\x9a\x84freqindexmask
        """
        try:
            for freq in self.freq_dict.keys():
                index = self.freq_dict.get(freq)
                self.cf.set('Freq', str(index), freq)

            freq_count = len(self.freq_dict)
            self.cf.set('ConfigInfo', 'freqcount', freq_count)
        except Exception:
            log_info = u'\u8bfb\u53d6\u9891\u7387\u914d\u7f6e\u5931\u8d25.'
            self.user_info(log_info)
            raise RuntimeError(log_info)

        ss = self.cf.sections()
        for item in ss:
            if item in ('ConfigInfo', 'Freq'):
                continue
            try:
                cur_freq = self.cf.get(item, 'freq')
                cur_index = self.freq_dict[int(cur_freq)]
                cur_freq_maxk = 2 ** cur_index
                self.cf.set(item, 'freqindexmask', cur_freq_maxk)
                self.cf.write(open(self.inifile, 'w'))
            except Exception as e2:
                log_info = u'\u4fee\u6539\u914d\u7f6e\u6587\u4ef6\u8282\u70b9%s\u5931\u8d25.' % item
                raise RuntimeError(log_info)

    def config_some_tone(self, name, freq, envelopemode, ontime1, offtime1, ontime2, offtime2, timedeviation):
        """
        \xe9\x85\x8d\xe7\xbd\xae\xe8\xa6\x81\xe6\xa3\x80\xe6\xb5\x8b\xe7\x9a\x84\xe9\x9f\xb3
        """
        skey = name
        try:
            if skey == None:
                skey = ''
                raise Exception(u'\u8981\u914d\u7f6e\u7684\u58f0\u97f3\u540d\u79f0\u4e3anone')
            self.cf.set(skey, 'Freq', freq)
            self.cf.set(skey, 'EnvelopeMode', envelopemode)
            self.cf.set(skey, 'On_Time', ontime1)
            self.cf.set(skey, 'Off_Time', offtime1)
            self.cf.set(skey, 'On_Time_Two', ontime2)
            self.cf.set(skey, 'Off_Time_Two', offtime2)
            self.cf.set(skey, 'TimeDeviation', timedeviation)
            self.cf.write(open(self.inifile, 'w'))
            index_freq = -1
            mark_freq = -1
            freq_count = len(self.freq_dict)
            self.user_info(str(self.freq_dict))
            if freq in self.freq_dict.keys():
                index_freq = self.freq_dict[freq]
                mark_freq = 2 ** index_freq
            else:
                index_freq = freq_count + 1 - 1
                if index_freq >= 16:
                    log_info = u'\u4e0d\u80fd\u914d\u7f6e\u8d85\u8fc716\u4e2a\u4e0d\u540c\u9891\u7387\uff0c\u8bf7\u65ad\u5f00\u670d\u52a1\u540e\u91cd\u65b0\u8fde\u63a5'
                    self.user_info(log_info)
                    raise RuntimeError(log_info)
                self.freq_dict[freq] = index_freq
                self.cf.set('Freq', str(index_freq), freq)
                self.cf.set('ConfigInfo', 'freqcount', index_freq + 1)
                mark_freq = 2 ** index_freq
            self.cf.set(skey, 'freqindexmask', mark_freq)
            self.cf.write(open(self.inifile, 'w'))
        except Exception as e:
            log_info = u'\u4fee\u6539\u914d\u7f6e\u6587\u4ef6\u8282\u70b9%s\u5931\u8d25. %s' % (skey, e)
            self.user_info(log_info)
            raise RuntimeError(log_info)

        log_info = u'\u5c06\u914d\u7f6e\u7684\u5f85\u68c0\u6d4b\u97f3\u4fe1\u606f\u5199\u5165\u5230\u914d\u7f6e\u6587\u4ef6\u6210\u529f'
        self.user_info(log_info)
        return True

    def config_system_param(self, serverIp, port, username, password):
        """
        \xe9\x85\x8d\xe7\xbd\xae\xe5\xba\x95\xe5\xb1\x82\xe6\xb5\x81\xe7\xa8\x8b\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x8f\x82\xe6\x95\xb0
        """
        try:
            self.cf.set('ConfigInfo', 'ipaddr', serverIp)
            self.cf.set('ConfigInfo', 'port', port)
            self.cf.set('ConfigInfo', 'username', username)
            self.cf.set('ConfigInfo', 'password', password)
            self.cf.write(open(self.inifile, 'w'))
            self.user_info(u"配置ini文件成功")
        except Exception as e:
            log_info = u'\u4fee\u6539\u914d\u7f6e\u6587\u4ef6\u4e2d\u8bed\u97f3\u5361\u6d41\u7a0b\u670d\u52a1\u914d\u7f6e\u4fe1\u606f\u5931\u8d25. %s'
            self.user_info(log_info)
            raise RuntimeError(log_info)

        return True



class ATTVoip():

    def __init__(self, log):
        self.user_info = log
        self.debug_info = log
        self.obj = Keygoe(self.user_info)
        if self.obj == None:
            log_info = u'\u8c03\u7528DLL\u5931\u8d25'
            self.user_info(log_info)
            raise RuntimeError(log_info)
        self.trunk_id_list = [1]
        self.init_keygoe_system()
        self.user_info(u"初始化keygoe系统成功")
        self.phone_dict = {}
        self._init_all_trunk()
        self.user_info(u"初始化所有的trunk成功")
        return

    def init_keygoe_system(self):
        """
        \xe5\xa7\x8b\xe5\x8c\x96\xe8\xaf\xad\xe9\x9f\xb3\xe5\x8d\xa1\xe8\xae\xbe\xe5\xa4\x87
        """
        if VOIP_FUN_OK == self.obj.init_keygoe_system():
            log_info = u'\u5f00\u59cb\u521d\u59cb\u5316\u8bed\u97f3\u5361\u8bbe\u5907...'
            self.user_info(log_info)
        else:
            log_info = u'\u542f\u52a8\u7cfb\u7edf\u521d\u59cb\u5316\u5931\u8d25'
            raise RuntimeError(log_info)
        nRet = self.obj.wait_trunk_init()
        if VOIP_FUN_FIAL == nRet:
            log_info = u'\u521d\u59cb\u5316\u6a21\u62df\u4e2d\u7ee7\u901a\u9053\u5931\u8d25'
            self.user_info("wait trunk init fail")
            self.user_info(log_info)
            raise RuntimeError(log_info)
        self.debug_info(u'\u53ef\u7528Trunk \u662f %d' % nRet)
        self.user_info(u'\u53ef\u7528Trunk \u662f %d' % nRet)
        for i in range(16):
            if nRet & 1 == 1:
                self.trunk_id_list.append(i + 1)
            nRet = nRet >> 1

        log_info = u'\u5b8c\u6210\u7cfb\u7edf\u521d\u59cb\u5316,\u53ef\u7528\u6a21\u62df\u901a\u9053\u5217\u8868\u5982\u4e0b\uff1a'
        self.user_info(log_info)
        self.user_info(self.trunk_id_list)

    def exit_keygoe_system(self):
        """
        """
        if VOIP_FUN_OK == self.obj.exit_keygoe_system():
            log_info = u'\u9000\u51fa\u7cfb\u7edf\u6210\u529f'
            self.user_info(log_info)
        else:
            log_info = u'\u9000\u51fa\u7cfb\u7edf\u5931\u8d25'
            self.user_info(log_info)
            raise RuntimeError(log_info)

    def _init_all_trunk(self):
        """
        \xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x9616\xe4\xb8\xaa\xe9\x80\x9a\xe9\x81\x93\xe7\x9a\x84\xe7\xbc\x93\xe5\xad\x98
        """
        self.phone_dict.clear()
        for i in self.trunk_id_list:
            self.phone_dict[i] = CPEPhone(i)

    def reset_trunk(self, trunk_id):
        """
        """
        phone = self._get_trunk_config_info(trunk_id)
        if VOIP_FUN_OK == self.obj.clear_keygoe_trunk(trunk_id):
            log_info = u'\u91cd\u7f6e\u6a21\u62df\u901a\u9053\u8bbe\u5907%d\u6210\u529f' % trunk_id
            self.user_info(log_info)
            phone.reset()
        else:
            log_info = u'\u91cd\u7f6e\u6a21\u62df\u901a\u9053\u8bbe\u5907%d\u5931\u8d25' % trunk_id
            self.user_info(log_info)
            raise RuntimeError(log_info)

    def reset_all_trunk(self):
        """
        """
        trunk_id_list = self.phone_dict.keys()
        for trunk_id in trunk_id_list:
            self.reset_trunk(trunk_id)

    def _get_trunk_config_info(self, trunk_id):
        """
        """
        if self.phone_dict.has_key(trunk_id):
            try:
                return self.phone_dict.get(trunk_id)
            except Exception as e:
                self.user_info(u'\u53d6\u5b57\u5178\u5931\u8d25')
                raise RuntimeError(u'\u53d6\u5b57\u5178\u5931\u8d25')

        else:
            self.user_info(u'\u8be5\u901a\u9053\u672a\u88ab\u4f7f\u7528\uff0c\u83b7\u53d6\u76f8\u5173\u4fe1\u606f\u5931\u8d25')
            raise RuntimeError(u'\u8be5\u901a\u9053\u672a\u88ab\u4f7f\u7528\uff0c\u83b7\u53d6\u76f8\u5173\u4fe1\u606f\u5931\u8d25')

    def call_out_offhook(self, trunk_id):
        """
        """
        phone = self._get_trunk_config_info(trunk_id)
        if phone.get_state() not in [_PHONESTATE.S_NONE,
         _PHONESTATE.S_INIT,
         _PHONESTATE.S_ONHOOK,
         _PHONESTATE.S_CLEAR_CALL]:
            log_info = u'\u5f53\u524d\u72b6\u6001\u4e0d\u80fd\u8fdb\u884c\u8be5\u64cd\u4f5c\uff0c\u8bf7\u68c0\u67e5\u5173\u952e\u5b57\u4f7f\u7528\u6d41\u7a0b\u662f\u5426\u6b63\u786e'
            raise RuntimeError(log_info)
        if VOIP_FUN_OK == self.obj.call_out_off_hook(trunk_id):
            log_info = u'\u6a21\u62df\u901a\u9053%d\u6458\u673a\u6210\u529f' % trunk_id
            self.user_info(log_info)
            phone.set_state(_PHONESTATE.S_CALL_OUT_OFFHOOK)
        else:
            log_info = u'\u6a21\u62df\u901a\u9053%d\u6458\u673a\u5931\u8d25' % trunk_id
            raise RuntimeError(log_info)

    def dial_by_number(self, trunk_id, number):
        """
        """
        phone_a = self._get_trunk_config_info(trunk_id)
        if phone_a.get_state() not in [_PHONESTATE.S_CALL_OUT_OFFHOOK, _PHONESTATE.S_IN_CALL]:
            log_info = u'\u5f53\u524d\u72b6\u6001\u4e0d\u80fd\u8fdb\u884c\u8be5\u64cd\u4f5c\uff0c\u8bf7\u68c0\u67e5\u5173\u952e\u5b57\u4f7f\u7528\u6d41\u7a0b\u662f\u5426\u6b63\u786e'
            raise RuntimeError(log_info)
        if VOIP_FUN_OK == self.obj.dial(trunk_id, number):
            log_info = u'\u6a21\u62df\u901a\u9053%d\u62e8\u53f7\u7ed9%s\u6210\u529f' % (trunk_id, number)
            self.user_info(log_info)
            phone_a.set_state(_PHONESTATE.S_IN_CALL)
        else:
            log_info = u'\u6a21\u62df\u901a\u9053%d\u62e8\u53f7\u7ed9%s\u5931\u8d25' % (trunk_id, number)
            raise RuntimeError(log_info)

    def send_dtmf(self, trunk_id, dtmf):
        """
        """
        phone = self._get_trunk_config_info(trunk_id)
        if phone.get_state() not in [_PHONESTATE.S_IN_CALL]:
            log_info = u'\u5f53\u524d\u72b6\u6001\u4e0d\u80fd\u8fdb\u884c\u8be5\u64cd\u4f5c\uff0c\u8bf7\u68c0\u67e5\u5173\u952e\u5b57\u4f7f\u7528\u6d41\u7a0b\u662f\u5426\u6b63\u786e'
            raise RuntimeError(log_info)
        self._clear_call_recv_data()
        if VOIP_FUN_OK == self.obj.send_data(trunk_id, dtmf):
            log_info = u'\u6a21\u62df\u901a\u9053%d\u53d1\u9001DTMF\u6570\u636e\u4e3a:%s' % (trunk_id, dtmf)
            self.user_info(log_info)
        else:
            log_info = u'\u6a21\u62df\u901a\u9053%d\u53d1\u9001DTMF\u6570\u636e\u5931\u8d25' % trunk_id
            raise RuntimeError(log_info)

    def get_recv_dtmf(self, trunk_id):
        """
        """
        phone = self._get_trunk_config_info(trunk_id)
        if phone.get_state() not in [_PHONESTATE.S_IN_CALL]:
            log_info = u'\u5f53\u524d\u72b6\u6001\u4e0d\u80fd\u8fdb\u884c\u8be5\u64cd\u4f5c\uff0c\u8bf7\u68c0\u67e5\u5173\u952e\u5b57\u4f7f\u7528\u6d41\u7a0b\u662f\u5426\u6b63\u786e'
            raise RuntimeError(log_info)
        dtmf_recv = self.obj.get_recv_data(trunk_id)
        log_info = u'\u6a21\u62df\u901a\u9053%d\u63a5\u6536\u5230\u7684DTMF\u4e3a:%s' % (trunk_id, dtmf_recv)
        self.user_info(log_info)
        return dtmf_recv

    def _clear_call_recv_data(self):
        """
        """
        for i in self.trunk_id_list:
            self.obj.clear_recv_data(i)

    def _get_fax_info(self, info):
        """
        ASCII
        """
        ls = info.split(',')
        errcode = -1
        errstep = -1
        pages = -1
        for item in ls:
            if 'EvtErrCode' in item:
                errcode = filter(lambda x: x.isdigit(), item)
            if 'ErrStep' in item:
                errstep = filter(lambda x: x.isdigit(), item)
            if 'TotalPages' in item:
                pages = filter(lambda x: x.isdigit(), item)

        return (int(errcode), int(errstep), int(pages))

    def _get_code_meaning(self, errcode, errstep):
        """
        \xe8\x8e\xb7\xe5\x8f\x96code\xe5\x80\xbc\xe5\xaf\xb9\xe5\xba\x94\xe7\x9a\x84\xe6\x84\x8f\xe4\xb9\x89
        """
        code_info = u''
        step_info = u''
        errcode_dict = {}
        errcode_dict[0] = u'T30_COMPLETE_SUCCESS'
        errcode_dict[1] = u'T30_PRESTOP_BY_REMOTE'
        errcode_dict[2] = u'T30_PRESTOP_BY_LOCAL'
        errcode_dict[3] = u'T30_NOT_FAX_TERMINAL'
        errcode_dict[4] = u'T30_NOT_COMPATIBLE_FAX_TERMINAL'
        errcode_dict[5] = u'T30_BAD_SIGNAL_CONDITION'
        errcode_dict[6] = u'T30_PROTOCOL_ERROR'
        errcode_dict[7] = u'T30_PROTOCOL_ERROR_TIMEOUT'
        errcode_dict[8] = u'T30_FLOW_REQ_CLEAN_ERROR'
        errcode_dict[9] = u'T30_NOT_RECEIVE_MEDIA_DATA'
        code_info = errcode_dict.get(errcode, u'unkown')
        step_info = {}
        step_info[0] = u'T30_INIT'
        step_info[1] = u'T30_INIT_SEND_CED'
        step_info[2] = u'T30_SEND_CED'
        step_info[3] = u'T30_INIT_SEND_DIS'
        step_info[4] = u'T30_SEND_DIS'
        step_info[5] = u'T30_INIT_RECV_DCS'
        step_info[6] = u'T30_RECV_DCS'
        step_info[7] = u'T30_INIT_RECV_TCF'
        step_info[8] = u'T30_RECV_TCF'
        step_info[9] = u'T30_INIT_SEND_CFR'
        step_info[10] = u'T30_SEND_CFR'
        step_info[11] = u'T30_INIT_SEND_FTT'
        step_info[12] = u'T30_SEND_FTT'
        step_info[13] = u'T30_INIT_RECV_PAGE'
        step_info[14] = u'T30_RECV_PAGE'
        step_info[15] = u'T30_INIT_RECV_EOP'
        step_info[16] = u'T30_RECV_EOP'
        step_info[17] = u'T30_INIT_SEND_MCF'
        step_info[18] = u'T30_SEND_MCF'
        step_info[21] = u'T30_INIT_POSTPAGE_REQ'
        step_info[22] = u'T30_POSTPAGE_REQ'
        step_info[64] = u'T30_INIT_RECV_DIS'
        step_info[65] = u'T30_RECV_DIS'
        step_info[66] = u'T30_INIT_SEND_DCS'
        step_info[67] = u'T30_SEND_DCS'
        step_info[68] = u'T30_INIT_SEND_TCF'
        step_info[69] = u'T30_SEND_TCF'
        step_info[70] = u'T30_INIT_RECV_CFR'
        step_info[71] = u'T30_RECV_CFR'
        step_info[72] = u'T30_INIT_SEND_PAGE'
        step_info[73] = u'T30_SEND_PAGE'
        step_info[74] = u'T30_INIT_SEND_EOP'
        step_info[75] = u'T30_SEND_EOP'
        step_info[76] = u'T30_INIT_SEND_MPS'
        step_info[77] = u'T30_SEND_MPS'
        step_info[78] = u'T30_INIT_SEND_EOM'
        step_info[79] = u'T30_SEND_EOM'
        step_info[80] = u'T30_INIT_RECV_MCF'
        step_info[81] = u'T30_RECV_MCF'
        step_info[82] = u'T30_INIT_PREPAGE_REQ'
        step_info[83] = u'T30_PREPAGE_REQ'
        step_info[84] = u'T30_INIT_PAGE_REQ'
        step_info[85] = u'T30_PAGE_REQ'
        step_info[86] = u'T30_INIT_SEND_CNG'
        step_info[87] = u'T30_SEND_CNG'
        step_info[88] = u'T30_RECV_MCF_CLEAN'
        step_info[89] = u'T30_INIT_RECV_PREDIS'
        step_info[106] = u'T30_RECV_PREDIS'
        step_info[107] = u'T30_TIFF_CAHANGE_COMMAND'
        step_info[108] = u'T30_TIFF_CAHANGE_FINISH'
        step_info[110] = u'T30_PRE_SEND_PAGE'
        step_info = step_info.get(errstep, u'unkown')
        return (code_info, step_info)

    def send_fax(self, trunk_id, sendfiles_list, bps_int, seconds, recordfile_send, recordfile_recv):
        """
        """
        phone = self._get_trunk_config_info(trunk_id)
        if phone.get_state() not in [_PHONESTATE.S_IN_CALL]:
            log_info = u'\u5f53\u524d\u72b6\u6001\u4e0d\u80fd\u8fdb\u884c\u8be5\u64cd\u4f5c\uff0c\u8bf7\u68c0\u67e5\u5173\u952e\u5b57\u4f7f\u7528\u6d41\u7a0b\u662f\u5426\u6b63\u786e'
            raise RuntimeError(log_info)
        if VOIP_FUN_OK != self.obj.send_fax_prepare(trunk_id):
            log_info = u'\u6a21\u62df\u901a\u9053%\u51c6\u5907\u4f20\u771f\u8bbe\u5907\u5931\u8d25' % trunk_id
            raise RuntimeError(log_info)
        firstfile = ''
        if isinstance(sendfiles_list, list):
            for index in range(len(sendfiles_list)):
                if index == 0:
                    firstfile = sendfiles_list[index]
                    log_info = u'\u6a21\u62df\u901a\u9053%d\u51c6\u5907\u53d1\u9001\u4f20\u771f\u6587\u4ef6%s, \u901f\u7387\u8bbe\u7f6e\u4e3a%d bps' % (trunk_id, firstfile, bps_int)
                    self.user_info(log_info)
                    continue
                if VOIP_FUN_OK == self.obj.set_fax_file(trunk_id, sendfiles_list[index]):
                    log_info = u'\u6dfb\u52a0\u5f85\u4f20\u7684\u4f20\u771f\u6587\u4ef6%s\u6210\u529f' % sendfiles_list[index]
                    self.user_info(log_info)
                else:
                    log_info = u'\u6dfb\u52a0\u5f85\u4f20\u7684\u4f20\u771f\u6587\u4ef6%s\u5931\u8d25' % sendfiles_list[index]
                    raise RuntimeError(log_info)

        else:
            firstfile = sendfiles_list
            log_info = u'\u6a21\u62df\u901a\u9053%d\u51c6\u5907\u53d1\u9001\u4f20\u771f\u6587\u4ef6%s\uff0c\u901f\u7387\u8bbe\u7f6e\u4e3a%d bps' % (trunk_id, firstfile, bps_int)
            self.user_info(log_info)
        state, info = self.obj.send_fax(trunk_id, firstfile, bps_int, seconds, recordfile_send, recordfile_recv)
        ierrcode, ierrstep, ipages = self._get_fax_info(info)
        if VOIP_FUN_OK == state:
            log_info = u'\u6a21\u62df\u901a\u9053%d\u53d1\u9001\u4f20\u771f\u6210\u529f,\u53d1\u9001\u9875\u6570\u4e3a%d\u3002' % (trunk_id, ipages)
            self.user_info(log_info)
        else:
            log_info = u'\u6a21\u62df\u901a\u9053%d\u53d1\u9001\u4f20\u771f\u5931\u8d25\u3002' % trunk_id
            c, s = self._get_code_meaning(ierrcode, ierrstep)
            err_info = u'\u5931\u8d25\u4fe1\u606f\uff1a%s\uff0c\u5931\u8d25\u6b65\u9aa4\uff1a%s\uff0c\u4f20\u771f\u9875\u6570\uff1a%d' % (c, s, ipages)
            log_info += err_info
            raise RuntimeError(log_info)
        return ipages

    def start_recv_fax(self, trunk_id, savefile, bps_int, recordfile_send, recordfile_recv):
        """
        """
        phone = self._get_trunk_config_info(trunk_id)
        if phone.get_state() not in [_PHONESTATE.S_IN_CALL]:
            log_info = u'\u5f53\u524d\u72b6\u6001\u4e0d\u80fd\u8fdb\u884c\u8be5\u64cd\u4f5c\uff0c\u8bf7\u68c0\u67e5\u5173\u952e\u5b57\u4f7f\u7528\u6d41\u7a0b\u662f\u5426\u6b63\u786e'
            raise RuntimeError(log_info)
        if VOIP_FUN_OK != self.obj.recv_fax_prepare(trunk_id):
            log_info = u'\u6a21\u62df\u901a\u9053%d\u51c6\u5907\u4f20\u771f\u8bbe\u5907\u5931\u8d25' % trunk_id
            raise RuntimeError(log_info)
        if VOIP_FUN_OK == self.obj.start_recv_fax(trunk_id, savefile, bps_int, recordfile_send, recordfile_recv):
            log_info = u'\u6a21\u62df\u901a\u9053%d\u51c6\u5907\u63a5\u6536\u4f20\u771f\uff0c\u901f\u7387\u8bbe\u7f6e\u4e3a%d bps, \u4f20\u771f\u6587\u4ef6\u5c06\u4fdd\u6301\u5230%s' % (trunk_id, bps_int, savefile)
            self.user_info(log_info)
            phone.set_state(_PHONESTATE.S_RECV_FAX_START)
        else:
            log_info = u'\u6a21\u62df\u901a\u9053%d\u51c6\u5907\u63a5\u6536\u4f20\u771f\u5931\u8d25' % trunk_id
            raise RuntimeError(log_info)

    def get_recv_fax_result(self, trunk_id, seconds):
        """
        """
        phone = self._get_trunk_config_info(trunk_id)
        if phone.get_state() not in [_PHONESTATE.S_RECV_FAX_START]:
            log_info = u'\u5f53\u524d\u72b6\u6001\u4e0d\u80fd\u8fdb\u884c\u8be5\u64cd\u4f5c\uff0c\u8bf7\u68c0\u67e5\u5173\u952e\u5b57\u4f7f\u7528\u6d41\u7a0b\u662f\u5426\u6b63\u786e'
            raise RuntimeError(log_info)
        state, info = self.obj.get_recv_fax_result(trunk_id, seconds)
        ierrcode, ierrstep, ipages = self._get_fax_info(info)
        if VOIP_FUN_OK == state:
            log_info = u'\u6a21\u62df\u901a\u9053%d\u63a5\u6536\u4f20\u771f\u6210\u529f\uff0c\u63a5\u6536\u9875\u6570\u4e3a%d\u3002' % (trunk_id, ipages)
            self.user_info(log_info)
            phone.set_state(_PHONESTATE.S_IN_CALL)
        else:
            phone.set_state(_PHONESTATE.S_IN_CALL)
            log_info = u'\u6a21\u62df\u901a\u9053%d\u63a5\u6536\u4f20\u771f\u5931\u8d25\u3002' % trunk_id
            c, s = self._get_code_meaning(ierrcode, ierrstep)
            err_info = u'\u5931\u8d25\u4fe1\u606f\uff1a%s\uff0c\u5931\u8d25\u6b65\u9aa4\uff1a%s\uff0c\u4f20\u771f\u9875\u6570\uff1a%d' % (c, s, ipages)
            log_info += err_info
            raise RuntimeError(log_info)
        return ipages

    def check_call_in(self, trunk_id, seconds):
        """
        """
        phone = self._get_trunk_config_info(trunk_id)
        if phone.get_state() not in [_PHONESTATE.S_NONE,
         _PHONESTATE.S_INIT,
         _PHONESTATE.S_ONHOOK,
         _PHONESTATE.S_CLEAR_CALL]:
            log_info = u'\u5f53\u524d\u72b6\u6001\u4e0d\u80fd\u8fdb\u884c\u8be5\u64cd\u4f5c\uff0c\u8bf7\u68c0\u67e5\u5173\u952e\u5b57\u4f7f\u7528\u6d41\u7a0b\u662f\u5426\u6b63\u786e'
            raise RuntimeError(log_info)
        if VOIP_FUN_OK == self.obj.check_call_in(trunk_id, seconds):
            log_info = u'\u6a21\u62df\u901a\u9053%d\u6709\u547c\u5165' % trunk_id
            self.user_info(log_info)
            phone.set_state(_PHONESTATE.S_CHECK_CALL_IN)
        else:
            log_info = u'\u6a21\u62df\u901a\u9053%d\u5728%d\u79d2\u5185\u65e0\u547c\u5165' % (trunk_id, seconds)
            self.user_info(log_info)
            raise RuntimeError(log_info)

    def call_in_offhook(self, trunk_id):
        """
        """
        phone = self._get_trunk_config_info(trunk_id)
        if phone.get_state() not in [_PHONESTATE.S_CHECK_CALL_IN]:
            log_info = u'\u5f53\u524d\u72b6\u6001\u4e0d\u80fd\u8fdb\u884c\u8be5\u64cd\u4f5c\uff0c\u8bf7\u5148\u68c0\u67e5\u662f\u5426\u6709\u7535\u8bdd\u547c\u5165'
            raise RuntimeError(log_info)
        if VOIP_FUN_OK == self.obj.call_in_off_hook(trunk_id):
            log_info = u'\u6a21\u62df\u901a\u9053%d\u6458\u673a\u6210\u529f' % trunk_id
            self.user_info(log_info)
            phone.set_state(_PHONESTATE.S_IN_CALL)
        else:
            log_info = u'\u6a21\u62df\u901a\u9053%d\u6458\u673a\u5931\u8d25' % trunk_id
            raise RuntimeError(log_info)

    def onhook(self, trunk_id):
        """
        """
        phone = self._get_trunk_config_info(trunk_id)
        if phone.get_state() in [_PHONESTATE.S_NONE,
         _PHONESTATE.S_INIT,
         _PHONESTATE.S_CHECK_CALL_IN,
         _PHONESTATE.S_ONHOOK,
         _PHONESTATE.S_CLEAR_CALL]:
            log_info = u'\u5f53\u524d\u72b6\u6001\u4e0d\u80fd\u8fdb\u884c\u8be5\u64cd\u4f5c\uff0c\u8bf7\u68c0\u67e5\u5173\u952e\u5b57\u4f7f\u7528\u6d41\u7a0b\u662f\u5426\u6b63\u786e'
            raise RuntimeError(log_info)
        if VOIP_FUN_OK == self.obj.on_hook(trunk_id):
            log_info = u'\u6a21\u62df\u901a\u9053%d\u6302\u673a\u6210\u529f' % trunk_id
            self.user_info(log_info)
            phone.set_state(_PHONESTATE.S_ONHOOK)
        else:
            log_info = u'\u6a21\u62df\u901a\u9053%d\u6302\u673a\u5931\u8d25' % trunk_id
            raise RuntimeError(log_info)

    def hook_flash(self, trunk_id):
        """
        """
        phone = self._get_trunk_config_info(trunk_id)
        if phone.get_state() not in [_PHONESTATE.S_IN_CALL]:
            log_info = u'\u5f53\u524d\u72b6\u6001\u4e0d\u80fd\u8fdb\u884c\u8be5\u64cd\u4f5c\uff0c\u8bf7\u68c0\u67e5\u5173\u952e\u5b57\u4f7f\u7528\u6d41\u7a0b\u662f\u5426\u6b63\u786e'
            raise RuntimeError(log_info)
        if VOIP_FUN_OK == self.obj.set_flash(trunk_id):
            log_info = u'\u6a21\u62df\u901a\u9053%d\u62cd\u53c9\u6210\u529f' % trunk_id
            self.user_info(log_info)
        else:
            log_info = u'\u6a21\u62df\u901a\u9053%d\u62cd\u53c9\u5931\u8d25' % trunk_id
            raise RuntimeError(log_info)

    def set_flash_time(self, times):
        """
        """
        if VOIP_FUN_OK == self.obj.set_flash_time(times):
            log_info = u'\u8bbe\u7f6e\u62cd\u53c9\u65f6\u95f4\u4e3a%d ms\u6210\u529f' % (times * 20)
            self.user_info(log_info)
        else:
            log_info = u'\u8bbe\u7f6e\u62cd\u53c9\u65f6\u95f4\u4e3a%d ms\u5931\u8d25' % (times * 20)
            raise RuntimeError(log_info)

    def wait_some_tone(self, trunk_id, tone_name, tone_key, times):
        """
        """
        phone = self._get_trunk_config_info(trunk_id)
        if VOIP_FUN_OK == self.obj.wait_some_tone(trunk_id, tone_key, times):
            log_info = u'\u6a21\u62df\u901a\u9053%d\u68c0\u6d4b\u5230%s\u97f3' % (trunk_id, tone_name)
            self.user_info(log_info)
            return True
        else:
            log_info = u'\u6a21\u62df\u901a\u9053%d\u5728%d\u79d2\u5185\u672a\u68c0\u6d4b\u5230%s\u97f3' % (trunk_id, times, tone_name)
            self.user_info(log_info)
            return False

    def update_tones_set(self):
        """
        """
        if VOIP_FUN_OK == self.obj.update_tones_set():
            log_info = u'\u66f4\u65b0\u5f85\u68c0\u6d4b\u97f3\u914d\u7f6e\u5230\u5e95\u5c42\u670d\u52a1\u6210\u529f'
            self.user_info(log_info)
        else:
            log_info = u'\u66f4\u65b0\u5f85\u68c0\u6d4b\u97f3\u914d\u7f6e\u5230\u5e95\u5c42\u670d\u52a1\u5931\u8d25'
            raise RuntimeError(log_info)

    def start_record(self, trunk_id, savefile):
        """
        """
        if VOIP_FUN_OK == self.obj.start_record(trunk_id, savefile):
            log_info = u'\u6a21\u62df\u901a\u9053%d \u542f\u52a8\u5f55\u97f3\u6210\u529f\uff0c\u4fdd\u5b58\u8def\u5f84\u4e3a %s' % (trunk_id, savefile)
            self.user_info(log_info)
        else:
            log_info = u'\u6a21\u62df\u901a\u9053%d \u542f\u52a8\u5f55\u97f3\u5931\u8d25' % trunk_id
            self.user_info(log_info)

    def stop_record(self, trunk_id):
        """
        """
        if VOIP_FUN_OK == self.obj.stop_record(trunk_id):
            log_info = u'\u6a21\u62df\u901a\u9053%d \u505c\u6b62\u5f55\u97f3\u6210\u529f' % trunk_id
            self.user_info(log_info)
        else:
            log_info = u'\u6a21\u62df\u901a\u9053%d \u505c\u6b62\u5f55\u97f3\u5931\u8d25' % trunk_id
            self.user_info(log_info)




def Test():
    v = ATTVoip(2)


if __name__ == '__main__':
    Test()