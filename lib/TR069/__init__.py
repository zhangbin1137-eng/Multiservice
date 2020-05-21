# Embedded file name: .\__init__.py
import time
from time import sleep
import re
import sys
import os
from cStringIO import StringIO
import pickle
import random
DEBUG_UNIT = False
tr069_pro_dir = os.path.dirname(os.path.dirname(__file__))
methodagent_pro_path = os.path.join(tr069_pro_dir, 'lib', 'methodagent')
REQUEST_ROM_METHOD_AGENT = False
if os.path.exists(methodagent_pro_path):
    DEBUG_UNIT = True
    REQUEST_ROM_METHOD_AGENT = True
if DEBUG_UNIT:
    from robot_lib_utils.connectioncache import _NoConnection, ConnectionCache
else:
    from robot.utils.connectioncache import _NoConnection, ConnectionCache
# if DEBUG_UNIT:
#     rf_common = 'initapp\\common'
#     for i in sys.path:
#         len1 = len(rf_common)
#         if i[-len1:] == rf_common:
#             sys.path.remove(i)
# 
#     g_prj_dir = os.path.dirname(__file__)
#     parent1 = os.path.dirname(g_prj_dir)
#     parent2 = os.path.dirname(parent1)
#     sys.path.insert(0, parent2)
#     import TR069.lib.common.logs.log as log
#     if not REQUEST_ROM_METHOD_AGENT:
#         log_dir = os.path.join(parent1, 'log')
#         log.start(name='nwf', directory=log_dir, level='DebugWarn')
#         log.set_file_id(testcase_name='tr069')
# else:
#     import attlog as log
import TR069.lib.users.user as user
from TR069.lib.common.event import *
from TR069.lib.common.error import *
from TR069.lib.common.function import *
VERSION = '2.1.1'

class TR069(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self):
        """
        """
        self._cache = ConnectionCache()
        self.log_obj = None
    
    def _user_info(self, str):
        if self.log_obj != None:
            self.log_obj(str)
        else:
            raise RuntimeError(u"请先传入log_obj函数")

    def switch_cpe(self, sn):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9aoui-sn\xe4\xb8\x8d\xe5\xad\x98\xe5\x9c\xa8\xe5\x88\x99\xe5\x88\x9b\xe5\xbb\xbaCPE(oui-sn)\xef\xbc\x8c\xe5\xad\x98\xe5\x9c\xa8\xe5\x88\x99\xe5\x88\x87\xe6\x8d\xa2\xe5\x88\xb0CPE(oui-sn)  
                  
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9asn:  oui-sn 
              
        Example:
        | Switch Cpe | 02018-001CF00865300  |
        
        \xe6\xb3\xa8\xe6\x84\x8f\xef\xbc\x9a\xe8\xaf\x86\xe5\x88\xabCPE\xe6\x98\xaf\xe9\x80\x9a\xe8\xbf\x87oui-sn\xe6\x9d\xa5\xe7\xa1\xae\xe5\xae\x9a\xe5\x85\xa8\xe5\xb1\x80\xe5\x94\xaf\xe4\xb8\x80\xe6\x80\xa7\xe7\x9a\x84
        """
        self._cache.register(sn, sn)
        desc = 'switch cpe(sn=%s) successfully.' % sn
        self._user_info(desc)
        return None

    def config_remote_server_addr(self, ip, port = 50000):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe9\x85\x8d\xe7\xbd\xae\xe8\xbf\x9c\xe7\xab\xaf\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe5\x9c\xb0\xe5\x9d\x80\xef\xbc\x9aIP\xe5\x92\x8c\xe7\xab\xaf\xe5\x8f\xa3\xe5\x8f\xb7
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9aip: \xe8\xbf\x9c\xe7\xab\xaf\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8ip\xe5\x9c\xb0\xe5\x9d\x80;
            port: \xe8\xbf\x9c\xe7\xab\xaf\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe7\xab\xaf\xe5\x8f\xa3\xe5\x8f\xb7\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba50000
             
        Example:
        | Config Remote Server Addr  | 10.10.10.10 | 50000 |
        
        """
        ret_api = None
        ret_data = None
        if 0 and not check_ipaddr_validity(ip):
            desc = u'\u5173\u952e\u5b57\u6267\u884c\u5931\u8d25\uff0cIP\u5730\u5740\u4e3a\u975e\u6cd5\u5730\u5740\uff01'
            raise RuntimeError(desc)
        ret_api, ret_data = user.config_remote_address(ip, port)
        if ret_api == ERR_SUCCESS:
            log_info = u'\u914d\u7f6e\u8fdc\u7aef\u670d\u52a1\u5668\u6210\u529f\u3002'
            self._user_info(log_info)
        else:
            desc = u'\u914d\u7f6e\u8fdc\u7aef\u670d\u52a1\u5668\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return

    def _get_sn(self):
        """
        if sn is not register, sn = ""(should not be obj(pickle not support) send to agent)
        """
        sn = self._cache.current
        if isinstance(sn, _NoConnection):
            sn = ''
            self._user_info('warnning:SN is empty')
        return sn

    def add_object(self, object_name, parameter_key = ''):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe7\xbb\x99\xe5\xa4\x9a\xe5\xae\x9e\xe4\xbe\x8b\xe5\xaf\xb9\xe8\xb1\xa1\xe5\x88\x9b\xe5\xbb\xba\xe4\xb8\x80\xe4\xb8\xaa\xe5\xae\x9e\xe4\xbe\x8b
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9aobject_name: \xe8\xa1\xa8\xe7\xa4\xbaObjectName\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe5\x88\x9b\xe5\xbb\xba\xe5\xae\x9e\xe4\xbe\x8b\xe7\x9a\x84\xe8\xb7\xaf\xe5\xbe\x84\xe5\x90\x8d\xef\xbc\x8c\xe5\xbf\x85\xe9\xa1\xbb\xe4\xbb\xa5\xe7\x82\xb9\xe7\xbb\x93\xe5\xb0\xbe;
              parameter_key: \xe8\xa1\xa8\xe7\xa4\xbaParameterKey\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba\xe7\xa9\xba\xe3\x80\x82
              
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e [\xe6\x96\xb0\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe5\xae\x9e\xe4\xbe\x8b\xe5\x8f\xb7,CPE\xe8\xbf\x94\xe5\x9b\x9e\xe7\x9a\x84\xe4\xbf\xae\xe6\x94\xb9\xe7\x8a\xb6\xe6\x80\x81status];
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${ret_list} | Add Object | InternetGatewayDevice.WANDevice.1.WANConnectionDevice. |          |
        | ${ret_list} | Add Object | InternetGatewayDevice.WANDevice.1.WANConnectionDevice. | some_key |
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        list_ret = []
        ret_api, ret_data = user1.add_object(ObjectName=object_name, ParameterKey=parameter_key)
        if ret_api == ERR_SUCCESS:
            desc = u'\u5efa\u7acb\u65b0\u5b9e\u4f8b\u6210\u529f\u3002'
            self._user_info(desc)
            if 'Status' in ret_data and 'InstanceNumber' in ret_data:
                list_ret.append(ret_data['InstanceNumber'])
                list_ret.append(ret_data['Status'])
                ret_out = list_ret
            else:
                desc = u'\u5efa\u7acb\u65b0\u5b9e\u4f8b\u5931\u8d25(\u89e3\u6790\u5931\u8d25)\u3002'
                raise RuntimeError(desc)
        else:
            desc = u'\u5efa\u7acb\u65b0\u5b9e\u4f8b\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def delete_object(self, object_name, parameter_key = ''):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe5\x88\xa0\xe9\x99\xa4\xe5\xaf\xb9\xe8\xb1\xa1\xe7\x9a\x84\xe4\xb8\x80\xe4\xb8\xaa\xe7\x89\xb9\xe5\xae\x9a\xe5\xae\x9e\xe4\xbe\x8b
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9aobject_name: \xe8\xa1\xa8\xe7\xa4\xbaObjectName\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe8\xa6\x81\xe5\x88\xa0\xe9\x99\xa4\xe7\x9a\x84\xe5\xae\x9e\xe4\xbe\x8b\xe5\xaf\xb9\xe8\xb1\xa1\xe7\x9a\x84\xe8\xb7\xaf\xe5\xbe\x84\xe5\x90\x8d\xef\xbc\x8c\xe5\xbf\x85\xe9\xa1\xbb\xe4\xbb\xa5\xe7\x82\xb9\xe7\xbb\x93\xe5\xb0\xbe;  
              parameter_key: \xe8\xa1\xa8\xe7\xa4\xbaParameterKey\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba\xe7\xa9\xba\xe3\x80\x82
              
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e CPE\xe8\xbf\x94\xe5\x9b\x9e\xe7\x9a\x84\xe4\xbf\xae\xe6\x94\xb9\xe7\x8a\xb6\xe6\x80\x81status;
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${status} | Delete Object | InternetGatewayDevice.WANDevice.1.WANConnectionDevice.3 |
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        ret_api, ret_data = user1.delete_object(ObjectName=object_name, ParameterKey=parameter_key)
        if ret_api == ERR_SUCCESS:
            desc = u'\u5220\u9664\u4e00\u4e2a\u5bf9\u8c61\u7684\u7279\u5b9a\u5b9e\u4f8b\u6210\u529f\u3002'
            self._user_info(desc)
            if 'Status' in ret_data:
                ret_out = ret_data['Status']
            else:
                desc = u'\u5220\u9664\u4e00\u4e2a\u5bf9\u8c61\u7684\u7279\u5b9a\u5b9e\u4f8b\u5931\u8d25(\u89e3\u6790\u5931\u8d25)\u3002'
                raise RuntimeError(desc)
        else:
            desc = u'\u5220\u9664\u4e00\u4e2a\u5bf9\u8c61\u7684\u7279\u5b9a\u5b9e\u4f8b\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def cancel_transfer(self, command_key = ''):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe5\x8f\x96\xe6\xb6\x88\xe4\xbc\xa0\xe8\xbe\x93
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9acommand_key: \xe8\xa1\xa8\xe7\xa4\xbaCommandKey\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba\xe7\xa9\xba\xe3\x80\x82
         
        Example:
        | Cancel Transfer  |  |
        | Cancel Transfer  | some_key  |
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        ret_api, ret_data = user1.cancel_transfer(CommandKey=command_key)
        if ret_api == ERR_SUCCESS:
            desc = u'\u53d6\u6d88\u4f20\u8f93\u6210\u529f\u3002'
            self._user_info(desc)
            ret_out = ret_data
        else:
            desc = u'\u53d6\u6d88\u4f20\u8f93\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def change_du_state(self, install_op_struct = [], update_op_struct = [], uninstall_op_struct = [], command_key = 'AUTO'):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\xa7\xa6\xe5\x8f\x91Deployment Unit\xef\xbc\x88DU\xef\xbc\x89\xe7\x9a\x84Install\xef\xbc\x8cUpdate\xe5\x92\x8cUninstall\xe7\x8a\xb6\xe6\x80\x81\xe5\x8f\x98\xe8\xbf\x81\xe3\x80\x82
                  \xe4\xbe\x8b\xe5\xa6\x82\xef\xbc\x9ainstalling a new DU, updating an existing DU\xef\xbc\x8cor uninstalling an existing DU.
                  
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9ainstall_op_struct: \xe8\xa1\xa8\xe7\xa4\xba\xe7\x94\xb1InstallOpStruct\xe7\xbb\x84\xe6\x88\x90\xe7\x9a\x84list\xef\xbc\x8c\xe6\xa0\xbc\xe5\xbc\x8f\xe4\xb8\xba[URL,UUID,Username,Password,ExecutionEnvRef]
                                  \xe6\x88\x96\xe8\x80\x85[[URL,...],[URL,...],...];
              update_op_struct: \xe8\xa1\xa8\xe7\xa4\xba\xe7\x94\xb1UpdateOpStruct\xe7\xbb\x84\xe6\x88\x90\xe7\x9a\x84list\xef\xbc\x8c\xe6\xa0\xbc\xe5\xbc\x8f\xe4\xb8\xba[UUID,Version,URL,Username,Password]
                                  \xe6\x88\x96\xe8\x80\x85[[UUID,...],[UUID,...],...];
              uninstall_op_struct: \xe8\xa1\xa8\xe7\xa4\xba\xe7\x94\xb1UninstallOpStruct\xe7\xbb\x84\xe6\x88\x90\xe7\x9a\x84list\xef\xbc\x8c\xe6\xa0\xbc\xe5\xbc\x8f\xe4\xb8\xba[UUID,Version,ExecutionEnvRef]
                                  \xe6\x88\x96\xe8\x80\x85[[UUID,...],[UUID,...],...];
              command_key: \xe8\xa1\xa8\xe7\xa4\xbaCommandKey\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba"AUTO"(\xe7\x94\xb1\xe7\xb3\xbb\xe7\xbb\x9f\xe8\x87\xaa\xe5\x8a\xa8\xe7\x94\x9f\xe6\x88\x90\xe9\x9a\x8f\xe6\x9c\xba\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2)
               
        Example:
        | ${install_list}   | Create List     | url             | uuid              |
        | ...               | username        | password        | ExecutionEnvRef   |
        | ${update_list}    | Create List     | uuid            | version           |
        | ...               | url             | username        | password          |
        | ${uninstall_list} | Create List     | uuid            | version           |
        | ...               | ExecutionEnvRef |                 |                   |
        | Change Du State   | ${install_list} | ${update_list}  | ${uninstall_list} |
        
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        tmp_install_list = []
        tmp_update_list = []
        tmp_uninstall_list = []
        tmp_operations = []
        if install_op_struct == []:
            tmp_install_list = install_op_struct
        elif type(install_op_struct[0]) is not list:
            tmp_install_list.append(install_op_struct)
        else:
            tmp_install_list = install_op_struct
        if update_op_struct == []:
            tmp_update_list = update_op_struct
        elif type(update_op_struct[0]) is not list:
            tmp_update_list.append(update_op_struct)
        else:
            tmp_update_list = update_op_struct
        if uninstall_op_struct == []:
            tmp_uninstall_list = uninstall_op_struct
        elif type(uninstall_op_struct[0]) is not list:
            tmp_uninstall_list.append(uninstall_op_struct)
        else:
            tmp_uninstall_list = uninstall_op_struct
        for item in tmp_install_list:
            if len(item) == 5:
                dict_op_struct = {}
                dict_op_struct['URL'] = item[0]
                dict_op_struct['UUID'] = item[1]
                dict_op_struct['Username'] = item[2]
                dict_op_struct['Password'] = item[3]
                dict_op_struct['ExecutionEnvRef'] = item[4]
                tmp_operations.append({'InstallOpStruct': dict_op_struct})
            else:
                raise RuntimeError(u'\u8f93\u5165\u7684\u53c2\u6570(install_op_struct)\u683c\u5f0f\u6709\u8bef')

        for item in tmp_update_list:
            if len(item) == 5:
                dict_op_struct = {}
                dict_op_struct['UUID'] = item[0]
                dict_op_struct['Version'] = item[1]
                dict_op_struct['URL'] = item[2]
                dict_op_struct['Username'] = item[3]
                dict_op_struct['Password'] = item[4]
                tmp_operations.append({'UpdateOpStruct': dict_op_struct})
            else:
                raise RuntimeError(u'\u8f93\u5165\u7684\u53c2\u6570(update_op_struct)\u683c\u5f0f\u6709\u8bef')

        for item in tmp_uninstall_list:
            if len(item) == 3:
                dict_op_struct = {}
                dict_op_struct['UUID'] = item[0]
                dict_op_struct['Version'] = item[1]
                dict_op_struct['ExecutionEnvRef'] = item[2]
                tmp_operations.append({'UninstallOpStruct': dict_op_struct})
            else:
                raise RuntimeError(u'\u8f93\u5165\u7684\u53c2\u6570(uninstall_op_struct)\u683c\u5f0f\u6709\u8bef')

        if command_key == 'AUTO':
            command_key = self._get_random_command_key()
        ret_api, ret_data = user1.change_du_state(Operations=tmp_operations, CommandKey=command_key)
        if ret_api == ERR_SUCCESS:
            desc = u'\u89e6\u53d1Deployment Unit\uff08DU\uff09\u7684\u72b6\u6001\u53d8\u8fc1\u6210\u529f\u3002'
            self._user_info(desc)
            ret_out = ret_data
        else:
            desc = u'\u89e6\u53d1Deployment Unit\uff08DU\uff09\u7684\u72b6\u6001\u53d8\u8fc1\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def download(self, file_type, url, user_name = '', password = '', file_size = 0, target_file_name = '', delay_seconds = 0, success_url = '', failure_url = '', command_key = 'AUTO'):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\xae\xa9CPE\xe5\x8e\xbb\xe6\x9f\x90\xe4\xb8\x80\xe6\x8c\x87\xe5\xae\x9a\xe8\xb7\xaf\xe5\xbe\x84\xe4\xb8\x8b\xe8\xbd\xbd\xe6\x9f\x90\xe4\xb8\x80\xe6\x8c\x87\xe5\xae\x9a\xe6\x96\x87\xe4\xbb\xb6
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9afile_type: \xe8\xa1\xa8\xe7\xa4\xbaFileType\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe4\xb8\x80\xe4\xb8\xaa\xe6\x95\xb4\xe6\x95\xb0\xe5\x8a\xa0\xe4\xb8\x80\xe4\xb8\xaa\xe7\xa9\xba\xe6\xa0\xbc\xe5\x8a\xa0\xe6\x96\x87\xe4\xbb\xb6\xe7\xb1\xbb\xe5\x9e\x8b\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x8c\xe7\x9b\xae\xe5\x89\x8d\xe6\x94\xaf\xe6\x8c\x81\xe4\xbb\xa5\xe4\xb8\x8b\xe5\x87\xa0\xe7\xa7\x8d\xef\xbc\x9a
                          "1 Firmware Upgrade Image"
                          "2 Web Content"
                          "3 Vendor Configuration File"
                          "4 Tone File"(new in cwmp-1-2)
                          "5 Ringer File"(new in cwmp-1-2)
                          "X<VENDOR><Vendor-specific-identifier>"
                          "X CU 4 User-Selective Firmware Upgrade Image"(\xe8\x81\x94\xe9\x80\x9a)
                          
              url: \xe8\xa1\xa8\xe7\xa4\xbaURL\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe6\xba\x90\xe6\x96\x87\xe4\xbb\xb6\xe8\xb7\xaf\xe5\xbe\x84;
              
              user_name: \xe8\xa1\xa8\xe7\xa4\xbaUsername\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe6\x96\x87\xe4\xbb\xb6\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe8\xae\xa4\xe8\xaf\x81\xe7\x9a\x84\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba\xe7\xa9\xba;
              
              password: \xe8\xa1\xa8\xe7\xa4\xbaPassword\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe6\x96\x87\xe4\xbb\xb6\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe8\xae\xa4\xe8\xaf\x81\xe7\x9a\x84\xe5\xaf\x86\xe7\xa0\x81\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba\xe7\xa9\xba;
              
              file_size: \xe8\xa1\xa8\xe7\xa4\xbaFileSize\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe4\xb8\x8b\xe8\xbd\xbd\xe6\x96\x87\xe4\xbb\xb6\xe7\x9a\x84\xe5\xa4\xa7\xe5\xb0\x8f\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba0\xef\xbc\x8c\xe8\xa1\xa8\xe7\xa4\xba\xe4\xb8\x8d\xe6\x8f\x90\xe4\xbe\x9b\xe6\x96\x87\xe4\xbb\xb6\xe9\x95\xbf\xe5\xba\xa6\xe7\x9a\x84\xe4\xbf\xa1\xe6\x81\xaf;
              
              target_file_name: \xe8\xa1\xa8\xe7\xa4\xbaTargetFileName\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe7\x94\xa8\xe4\xba\x8e\xe7\x9b\xae\xe6\xa0\x87\xe6\x96\x87\xe4\xbb\xb6\xe7\xb3\xbb\xe7\xbb\x9f\xe7\x9a\x84\xe6\x96\x87\xe4\xbb\xb6\xe5\x90\x8d\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba\xe7\xa9\xba;
              
              delay_seconds: \xe8\xa1\xa8\xe7\xa4\xbaDelaySeconds\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba0;
              
              success_url\xef\xbc\x9a\xe8\xa1\xa8\xe7\xa4\xbaSuccessURL\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe4\xb8\x8b\xe8\xbd\xbd\xe6\x88\x90\xe5\x8a\x9f\xe5\x90\x8e\xef\xbc\x8cCPE\xe5\xb0\x86\xe7\x94\xa8\xe6\x88\xb7\xe6\xb5\x8f\xe8\xa7\x88\xe5\x99\xa8\xe9\x87\x8d\xe5\xae\x9a\xe4\xbd\x8d\xe5\x88\xb0\xe8\xaf\xa5URL\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba\xe7\xa9\xba;
              
              failure_url\xef\xbc\x9a\xe8\xa1\xa8\xe7\xa4\xbaFailureURL\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe4\xb8\x8b\xe8\xbd\xbd\xe5\xa4\xb1\xe8\xb4\xa5\xe5\x90\x8e\xef\xbc\x8cCPE\xe5\xb0\x86\xe7\x94\xa8\xe6\x88\xb7\xe6\xb5\x8f\xe8\xa7\x88\xe5\x99\xa8\xe9\x87\x8d\xe5\xae\x9a\xe4\xbd\x8d\xe5\x88\xb0\xe8\xaf\xa5URL\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba\xe7\xa9\xba;
              
              command_key: \xe8\xa1\xa8\xe7\xa4\xbaCommandKey\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba"AUTO"(\xe7\x94\xb1\xe7\xb3\xbb\xe7\xbb\x9f\xe8\x87\xaa\xe5\x8a\xa8\xe7\x94\x9f\xe6\x88\x90\xe9\x9a\x8f\xe6\x9c\xba\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2)
              
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e [CPE\xe8\xbf\x94\xe5\x9b\x9e\xe7\x9a\x84\xe4\xbf\xae\xe6\x94\xb9\xe7\x8a\xb6\xe6\x80\x81status, StartTime,CompleteTime];
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${ret_list} | Download  | 3 Vendor Configuration File | http://172.24.35.35/001CF0001CF0865300.CFG |
        | ${ret_list} | Download  | 3 Vendor Configuration File | http://172.24.35.35/001CF0001CF0865300.CFG |
        | ...         | username  | password                    |                                            |
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        tmp_list = []
        if command_key == 'AUTO':
            command_key = self._get_random_command_key()
        desc = 'file_type=%s, url=%s, user_name=%s,password=%s, file_size=%s,  target_file_name=%s, delay_seconds=%s, success_url=%s,  failure_url=%s, command_key=%s' % (file_type,
         url,
         user_name,
         password,
         file_size,
         target_file_name,
         delay_seconds,
         success_url,
         failure_url,
         command_key)
        self._user_info(desc)
        ret_api, ret_data = user1.download(CommandKey=command_key, FileType=file_type, URL=url, Username=user_name, Password=password, FileSize=file_size, TargetFileName=target_file_name, DelaySeconds=delay_seconds, SuccessURL=success_url, FailureURL=failure_url)
        if ret_api == ERR_SUCCESS:
            desc = u'\u4e0b\u8f7d\u6210\u529f\u3002'
            self._user_info(desc)
            if 'Status' in ret_data and 'StartTime' in ret_data and 'CompleteTime' in ret_data:
                tmp_list.append(ret_data['Status'])
                tmp_list.append(ret_data['StartTime'])
                tmp_list.append(ret_data['CompleteTime'])
                ret_out = tmp_list
            else:
                desc = u'\u4e0b\u8f7d\u5931\u8d25(\u89e3\u6790\u5931\u8d25)\u3002'
                raise RuntimeError(desc)
        else:
            desc = u'\u4e0b\u8f7d\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def schedule_download(self, file_type, url, time_window_list, user_name = '', password = '', file_size = 0, target_file_name = '', command_key = 'AUTO'):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\xae\xa9CPE\xe5\x9c\xa8\xe4\xb8\x80\xe4\xb8\xaa\xe6\x88\x96\xe4\xb8\xa4\xe4\xb8\xaa\xe6\x8c\x87\xe5\xae\x9a\xe6\x97\xb6\xe9\x97\xb4\xe7\xaa\x97\xe5\x86\x85\xe5\x88\xb0\xe6\x8c\x87\xe5\xae\x9a\xe8\xb7\xaf\xe5\xbe\x84\xe4\xb8\x8b\xe8\xbd\xbd\xe7\x89\xb9\xe5\xae\x9a\xe6\x96\x87\xe4\xbb\xb6\xe5\xb9\xb6\xe5\xba\x94\xe7\x94\xa8
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9afile_type: \xe8\xa1\xa8\xe7\xa4\xbaFileType\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe4\xb8\x80\xe4\xb8\xaa\xe6\x95\xb4\xe6\x95\xb0\xe5\x8a\xa0\xe4\xb8\x80\xe4\xb8\xaa\xe7\xa9\xba\xe6\xa0\xbc\xe5\x8a\xa0\xe6\x96\x87\xe4\xbb\xb6\xe7\xb1\xbb\xe5\x9e\x8b\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x8c\xe7\x9b\xae\xe5\x89\x8d\xe6\x94\xaf\xe6\x8c\x81\xe4\xbb\xa5\xe4\xb8\x8b\xe5\x87\xa0\xe7\xa7\x8d\xef\xbc\x9a
                          "1 Firmware Upgrade Image"
                          "2 Web Content"
                          "3 Vendor Configuration File"
                          "4 Tone File"(new in cwmp-1-2)
                          "5 Ringer File"(new in cwmp-1-2)
                          
                          "X<VENDOR><Vendor-specific-identifier>";
                          
              url: \xe8\xa1\xa8\xe7\xa4\xbaURL\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe6\xba\x90\xe6\x96\x87\xe4\xbb\xb6\xe8\xb7\xaf\xe5\xbe\x84;
              
              user_name: \xe8\xa1\xa8\xe7\xa4\xbaUsername\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe6\x96\x87\xe4\xbb\xb6\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe8\xae\xa4\xe8\xaf\x81\xe7\x9a\x84\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba\xe7\xa9\xba;
              
              password: \xe8\xa1\xa8\xe7\xa4\xbaPassword\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe6\x96\x87\xe4\xbb\xb6\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe8\xae\xa4\xe8\xaf\x81\xe7\x9a\x84\xe5\xaf\x86\xe7\xa0\x81\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba\xe7\xa9\xba;
              
              file_size: \xe8\xa1\xa8\xe7\xa4\xbaFileSize\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe4\xb8\x8b\xe8\xbd\xbd\xe6\x96\x87\xe4\xbb\xb6\xe7\x9a\x84\xe5\xa4\xa7\xe5\xb0\x8f\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba0\xef\xbc\x8c\xe8\xa1\xa8\xe7\xa4\xba\xe4\xb8\x8d\xe6\x8f\x90\xe4\xbe\x9b\xe6\x96\x87\xe4\xbb\xb6\xe9\x95\xbf\xe5\xba\xa6\xe7\x9a\x84\xe4\xbf\xa1\xe6\x81\xaf;
              
              target_file_name: \xe8\xa1\xa8\xe7\xa4\xbaTargetFileName\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe7\x94\xa8\xe4\xba\x8e\xe7\x9b\xae\xe6\xa0\x87\xe6\x96\x87\xe4\xbb\xb6\xe7\xb3\xbb\xe7\xbb\x9f\xe7\x9a\x84\xe6\x96\x87\xe4\xbb\xb6\xe5\x90\x8d\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba\xe7\xa9\xba;
              
              time_window_list: \xe8\xa1\xa8\xe7\xa4\xbaTimeWindowList\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe7\x94\xb1\xe4\xb8\x80\xe4\xb8\xaa\xe6\x88\x96\xe4\xb8\xa4\xe4\xb8\xaa\xe6\x97\xb6\xe9\x97\xb4\xe7\xaa\x97\xe7\x9a\x84\xe7\xbb\x93\xe6\x9e\x84\xe4\xbd\x93\xe7\xbb\x84\xe6\x88\x90\xe7\x9a\x84list\xef\xbc\x8c\xe4\xb8\xa4\xe4\xb8\xaa\xe6\x97\xb6\xe9\x97\xb4\xe7\xaa\x97\xe4\xb8\x8d\xe8\x83\xbd\xe9\x87\x8d\xe5\x8f\xa0
                                \xe6\x97\xb6\xe9\x97\xb4\xe7\xaa\x97\xe7\x9a\x84\xe7\xbb\x93\xe6\x9e\x84\xe4\xbd\x93\xe4\xb8\xba\xef\xbc\x9a
                                WindowStart: \xe4\xbb\x8e\xe6\x8e\xa5\xe5\x8f\x97\xe5\x88\xb0\xe8\xaf\xb7\xe6\xb1\x82\xe5\x88\xb0\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4\xe7\xaa\x97\xe7\x9a\x84\xe5\x81\x8f\xe7\xa7\xbb\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x88in seconds\xef\xbc\x89
                                WindowEnd: \xe4\xbb\x8e\xe6\x8e\xa5\xe5\x8f\x97\xe5\x88\xb0\xe8\xaf\xb7\xe6\xb1\x82\xe5\x88\xb0\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4\xe7\xaa\x97\xe7\x9a\x84\xe5\x81\x8f\xe7\xa7\xbb\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x88in seconds\xef\xbc\x89
                                WindowMode: \xe8\xa1\xa8\xe7\xa4\xba\xe5\x9c\xa8\xe6\x97\xb6\xe9\x97\xb4\xe7\xaa\x97\xe5\x86\x85\xef\xbc\x8cCPE\xe5\xa6\x82\xe4\xbd\x95perform\xe5\x92\x8capply the download,\xe7\x9b\xae\xe5\x89\x8d\xe5\xae\x9a\xe4\xb9\x89\xe4\xba\x86\xe4\xbb\xa5\xe4\xb8\x8b\xe5\x87\xa0\xe7\xa7\x8d\xef\xbc\x9a
                                                        "1 At Any Time"
                                                        "2 Immediately"
                                                        "3 When Idle"
                                                        "4 Confirmation Needed"
                                                        "X <VENDOR> <Vendor specific identifier>"
                                UserMessage: \xe7\xbb\x99CPE\xe7\x94\xa8\xe6\x88\xb7\xe7\x9a\x84\xe6\xb6\x88\xe6\x81\xaf\xef\xbc\x8c\xe9\x80\x9a\xe7\x9f\xa5\xe4\xbb\x96\xe5\x85\xb3\xe4\xba\x8edownload\xe8\xaf\xb7\xe6\xb1\x82\xe3\x80\x82\xe5\xbd\x93WindowMode\xe6\x98\xaf"4 Confirmation Needed"\xe6\x97\xb6\xef\xbc\x8cCPE\xe5\x8f\xaf\xe4\xbb\xa5\xe7\x94\xa8\xe5\xae\x83\xe5\x90\x91\xe7\x94\xa8\xe6\x88\xb7\xe7\xa1\xae\xe8\xae\xa4\xe3\x80\x82\xe5\xa6\x82\xe6\x9e\x9c\xe4\xb8\x8d\xe9\x9c\x80\xe8\xa6\x81\xef\xbc\x8c\xe8\xaf\xa5\xe5\x8f\x82\xe6\x95\xb0\xe5\x8f\xaf\xe4\xbb\xa5\xe4\xb8\xba\xe7\xa9\xba\xe3\x80\x82
                                MaxRetries: \xe5\x9c\xa8\xe7\xa1\xae\xe5\xae\x9a\xe5\xa4\xb1\xe8\xb4\xa5\xe4\xb9\x8b\xe5\x89\x8d\xef\xbc\x8c\xe4\xb8\x8b\xe8\xbd\xbd\xe5\x92\x8c\xe5\xba\x94\xe7\x94\xa8\xe5\xb0\x9d\xe8\xaf\x95\xe7\x9a\x84\xe6\x9c\x80\xe5\xa4\xa7\xe6\xac\xa1\xe6\x95\xb0\xef\xbc\x8c\xe4\xb8\xba0\xe8\xa1\xa8\xe7\xa4\xba\xe4\xb8\x8d\xe5\x85\x81\xe8\xae\xb8\xe9\x87\x8d\xe8\xaf\x95\xef\xbc\x8c\xe4\xb8\xba-1\xe8\xa1\xa8\xe7\xa4\xba\xe7\x94\xb1CPE\xe5\x86\xb3\xe5\xae\x9a\xe9\x87\x8d\xe8\xaf\x95\xe5\xa4\x9a\xe5\xb0\x91\xe6\xac\xa1\xe3\x80\x82
                                time_window_list\xe7\x9a\x84\xe5\x8f\x82\xe6\x95\xb0\xe6\xa0\xbc\xe5\xbc\x8f\xe4\xb8\xba\xef\xbc\x9a
                                \xe5\xa6\x82\xe6\x9e\x9c\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe6\x97\xb6\xe9\x97\xb4\xe7\xaa\x97\xe7\xbb\x93\xe6\x9e\x84\xe4\xbd\x93\xef\xbc\x9a[WindowStart, WindowEnd, WindowMode, UserMessage, MaxRetries]
                                \xe5\xa6\x82\xe6\x9e\x9c\xe6\x98\xaf\xe4\xb8\xa4\xe4\xb8\xaa\xe6\x97\xb6\xe9\x97\xb4\xe7\xaa\x97\xe7\xbb\x93\xe6\x9e\x84\xe4\xbd\x93\xef\xbc\x9a[[WindowStart,...],[WindowStart,...]]
                                
              command_key: \xe8\xa1\xa8\xe7\xa4\xbaCommandKey\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba"AUTO"(\xe7\x94\xb1\xe7\xb3\xbb\xe7\xbb\x9f\xe8\x87\xaa\xe5\x8a\xa8\xe7\x94\x9f\xe6\x88\x90\xe9\x9a\x8f\xe6\x9c\xba\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2)
                
        Example:
        | ${one_time_window}  | Create List           | 10                      |       100           |
        | ...                 | 1 At Any Time         | ${EMPTY}                |       -1            |
        | ${two_time_window}  | Create List           | 110                     |      200            |
        | ...                 | 4 Confirmation Needed | "Begin to download now" |       -1            |
        | ${time_window_list} | Create List           | ${one_time_window}      | ${two_time_window}  |
        | Schedule Download   | 2 Web Content         | http://register/web/tt  | ${time_window_list} |
        | Schedule Download   | 2 Web Content         | http://register/web/tt  | ${one_time_window}  |
        
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        tmp_time_window_list = []
        tmp_list = []
        if type(time_window_list[0]) is not list:
            tmp_list.append(time_window_list)
        else:
            tmp_list = time_window_list
        for item in tmp_list:
            if len(item) == 5:
                dict_time_window = {}
                dict_time_window['WindowStart'] = item[0]
                dict_time_window['WindowEnd'] = item[1]
                dict_time_window['WindowMode'] = item[2]
                dict_time_window['UserMessage'] = item[3]
                dict_time_window['MaxRetries'] = item[4]
                tmp_time_window_list.append(dict_time_window)
            else:
                raise RuntimeError(u'\u8f93\u5165\u7684\u53c2\u6570(time_window_list)\u683c\u5f0f\u6709\u8bef')

        if command_key == 'AUTO':
            command_key = self._get_random_command_key()
        ret_api, ret_data = user1.schedule_download(CommandKey=command_key, FileType=file_type, URL=url, Username=user_name, Password=password, FileSize=file_size, TargetFileName=target_file_name, TimeWindowList=tmp_time_window_list)
        if ret_api == ERR_SUCCESS:
            desc = u'\u8ba1\u5212\u4e0b\u8f7d\u6210\u529f\u3002'
            self._user_info(desc)
            ret_out = ret_data
        else:
            desc = u'\u8ba1\u5212\u4e0b\u8f7d\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def factory_reset(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\xae\xa9CPE\xe6\x81\xa2\xe5\xa4\x8d\xe5\x87\xba\xe5\x8e\x82\xe9\xbb\x98\xe8\xae\xa4\xe8\xae\xbe\xe7\xbd\xae
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a\xe6\x97\xa0
           
        Example:
        | Factory Reset  |       |
        
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        ret_api, ret_data = user1.factory_reset()
        if ret_api == ERR_SUCCESS:
            desc = u'\u6062\u590d\u51fa\u5382\u8bbe\u7f6e\u6210\u529f\u3002'
            self._user_info(desc)
            ret_out = ret_data
        else:
            desc = u'\u6062\u590d\u51fa\u5382\u8bbe\u7f6e\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def get_all_queued_transfers(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\x8e\xb7\xe5\x8f\x96\xe6\x89\x80\xe6\x9c\x89\xe4\xb8\x8a\xe4\xbc\xa0\xef\xbc\x8c\xe4\xb8\x8b\xe8\xbd\xbd\xef\xbc\x8c\xe5\x8c\x85\xe6\x8b\xac\xe4\xb8\x8d\xe6\x98\xafACS\xe6\x8c\x87\xe5\xae\x9a\xe7\x9a\x84\xe8\xaf\xb7\xe6\xb1\x82\xe7\x9a\x84transfer\xe7\x9a\x84\xe7\x8a\xb6\xe6\x80\x81
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a\xe6\x97\xa0
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e \xe7\x94\xb1[CommandKey,State,IsDownload,FileType,FileSize,TargetFileName]\xe7\xbb\x84\xe6\x88\x90\xe7\x9a\x84\xe5\x88\x97\xe8\xa1\xa8;
               \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
               
        Example:
        | ${ret_list} | Get All Queued Transfers  |       |
        
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        tmp_list = []
        ret_api, ret_data = user1.get_all_queued_transfers()
        if ret_api == ERR_SUCCESS:
            desc = u'\u786e\u5b9a\u524d\u9762\u7684\u4e0b\u8f7d\u6216\u4e0a\u8f7d\u8bf7\u6c42\u7684\u72b6\u6001\u6210\u529f\u3002'
            self._user_info(desc)
            if 'TransferList' in ret_data:
                for item in ret_data['TransferList']:
                    tmp_sub_list = []
                    tmp_sub_list.append(item.get('CommandKey'))
                    tmp_sub_list.append(item.get('State'))
                    tmp_sub_list.append(item.get('IsDownload'))
                    tmp_sub_list.append(item.get('FileType'))
                    tmp_sub_list.append(item.get('FileSize'))
                    tmp_sub_list.append(item.get('TargetFileName'))
                    tmp_list.append(tmp_sub_list)

                ret_out = tmp_list
            else:
                desc = u'\u786e\u5b9a\u524d\u9762\u7684\u4e0b\u8f7d\u6216\u4e0a\u4f20\u8bf7\u6c42\u7684\u72b6\u6001\u5931\u8d25(\u89e3\u6790\u5931\u8d25)\u3002'
                raise RuntimeError(desc)
        else:
            desc = u'\u786e\u5b9a\u524d\u9762\u7684\u4e0b\u8f7d\u6216\u4e0a\u4f20\u8bf7\u6c42\u7684\u72b6\u6001\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def get_options(self, option_name = ''):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\x8e\xb7\xe5\x8f\x96\xe5\xbd\x93\xe5\x89\x8dCPE\xe7\x9a\x84\xe9\x80\x89\xe9\xa1\xb9\xe8\xae\xbe\xe7\xbd\xae\xe3\x80\x82\xe4\xbb\xa5\xe5\x8f\x8a\xe5\xae\x83\xe4\xbb\xac\xe7\x9b\xb8\xe5\xba\x94\xe7\x9a\x84\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xa1\xe6\x81\xaf
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9aoption_name: \xe8\xa1\xa8\xe7\xa4\xbaOptionName\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe8\xaf\xa5\xe5\x8f\x82\xe6\x95\xb0\xe8\xa1\xa8\xe7\xa4\xba\xe4\xb8\x80\xe4\xb8\xaa\xe7\x89\xb9\xe5\xae\x9aoption\xe7\x9a\x84\xe5\x90\x8d\xe5\xad\x97;
                            \xe5\xa6\x82\xe6\x9e\x9c\xe4\xb8\xba\xe7\xa9\xba\xef\xbc\x8c\xe8\xa1\xa8\xe7\xa4\xba\xe9\x9c\x80\xe8\xa6\x81\xe8\xbf\x94\xe5\x9b\x9e\xe6\x89\x80\xe6\x9c\x89CPE\xe6\x94\xaf\xe6\x8c\x81\xe7\x9a\x84Options\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba\xe7\xa9\xba
                            
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e \xe7\x94\xb1[OptionName,VoucherSN,State,Mode,StartDate,ExpirationDate,IsTransferable]\xe7\xbb\x84\xe6\x88\x90\xe7\x9a\x84\xe5\x88\x97\xe8\xa1\xa8;
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${ret_list} | Get Options  | some_option_name  |
        
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        tmp_list = []
        ret_api, ret_data = user1.get_options(OptionName=option_name)
        if ret_api == ERR_SUCCESS:
            desc = u'\u83b7\u53d6\u5f53\u524dCPE\u7684\u9009\u9879\u8bbe\u7f6e\u6210\u529f\u3002'
            self._user_info(desc)
            if 'OptionList' in ret_data:
                for item in ret_data['OptionList']:
                    tmp_sub_list = []
                    tmp_sub_list.append(item.get('OptionName'))
                    tmp_sub_list.append(item.get('VoucherSN'))
                    tmp_sub_list.append(item.get('State'))
                    tmp_sub_list.append(item.get('Mode'))
                    tmp_sub_list.append(item.get('StartDate'))
                    tmp_sub_list.append(item.get('ExpirationDate'))
                    tmp_sub_list.append(item.get('IsTransferable'))
                    tmp_list.append(tmp_sub_list)

                ret_out = tmp_list
            else:
                desc = u'\u83b7\u53d6\u5f53\u524dCPE\u7684\u9009\u9879\u8bbe\u7f6e\u5931\u8d25(\u89e3\u6790\u5931\u8d25)\u3002'
                raise RuntimeError(desc)
        else:
            desc = u'\u83b7\u53d6\u5f53\u524dCPE\u7684\u9009\u9879\u8bbe\u7f6e\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def get_rpc_methods(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\x8e\xb7\xe5\x8f\x96CPE\xe6\x89\x80\xe6\x94\xaf\xe6\x8c\x81\xe7\x9a\x84RPC\xe6\x96\xb9\xe6\xb3\x95
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a\xe6\x97\xa0
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e CPE\xe6\x94\xaf\xe6\x8c\x81\xe7\x9a\x84RPC\xe6\x96\xb9\xe6\xb3\x95\xe5\x88\x97\xe8\xa1\xa8;
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${method_list}  | Get Rpc Methods  |
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        ret_api, ret_data = user1.get_rpc_methods()
        if ret_api == ERR_SUCCESS:
            desc = u'\u83b7\u53d6CPE\u652f\u6301\u7684RPC\u65b9\u6cd5\u5217\u8868\u6210\u529f\u3002'
            self._user_info(desc)
            if 'MethodsList' in ret_data:
                ret_data = ret_data.get('MethodsList')
                ret_out = ret_data
            else:
                desc = u'\u83b7\u53d6CPE\u652f\u6301\u7684RPC\u65b9\u6cd5\u5217\u8868\u5931\u8d25(\u89e3\u6790\u5931\u8d25)\u3002'
                raise RuntimeError(desc)
        else:
            desc = u'\u53d6CPE\u652f\u6301\u7684RPC\u65b9\u6cd5\u5217\u8868\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def set_parameter_values(self, parameter_list, parameter_key = ''):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe4\xbf\xae\xe6\x94\xb9CPE\xe7\x9a\x84\xe4\xb8\x80\xe4\xb8\xaa\xe6\x88\x96\xe5\xa4\x9a\xe4\xb8\xaa\xe5\x8f\x82\xe6\x95\xb0\xe5\x80\xbc
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9aparameter_list: \xe8\xa1\xa8\xe7\xa4\xbaParameterList\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe7\x94\xb1[name,vlaue]\xe5\x80\xbc\xe5\xaf\xb9\xe4\xbd\x9c\xe4\xb8\xba\xe5\x85\x83\xe7\xb4\xa0\xe7\xbb\x84\xe6\x88\x90\xe7\x9a\x84\xe5\x88\x97\xe8\xa1\xa8\xef\xbc\x8c
                              name\xe8\xa1\xa8\xe7\xa4\xba\xe8\xa6\x81\xe4\xbf\xae\xe6\x94\xb9\xe7\x9a\x84\xe5\x8f\x82\xe6\x95\xb0\xe5\x90\x8d\xef\xbc\x8cvalue\xe8\xa1\xa8\xe7\xa4\xba\xe8\xa6\x81\xe4\xbf\xae\xe6\x94\xb9\xe7\x9a\x84\xe5\x8f\x82\xe6\x95\xb0\xe5\x80\xbc\xe3\x80\x82
                              \xe5\xa6\x82\xe6\x9e\x9c\xe5\x8f\xaa\xe4\xbf\xae\xe6\x94\xb9\xe4\xb8\x80\xe4\xb8\xaa\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe5\x8f\x82\xe6\x95\xb0\xe6\xa0\xbc\xe5\xbc\x8f\xe4\xb8\xba\xef\xbc\x9a[name,value]\xe6\x88\x96\xe8\x80\x85[[name,value]]
                              \xe5\xa6\x82\xe6\x9e\x9c\xe4\xbf\xae\xe6\x94\xb9\xe5\xa4\x9a\xe4\xb8\xaa\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe5\x8f\x82\xe6\x95\xb0\xe6\xa0\xbc\xe5\xbc\x8f\xe4\xb8\xba\xef\xbc\x9a[[name1,value1],[name2,value2],...]
                              
              parameter_key: \xe8\xa1\xa8\xe7\xa4\xbaParameterKey\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba\xe7\xa9\xba\xe3\x80\x82
              
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e CPE\xe8\xbf\x94\xe5\x9b\x9e\xe7\x9a\x84\xe4\xbf\xae\xe6\x94\xb9\xe7\x8a\xb6\xe6\x80\x81status;
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${name}       | Set Variable         | InternetGatewayDevice.DeviceInfo.ManufacturerOUI  |               |
        | ${value}      | Set Variable         | 0F34PT                                            |               |
        | ${para_list}  | Create List          | ${name}                                           | ${value}      |
        | ${status}     | Set Parameter Values | ${para_list}                                      | some_key      |
        | ${one_list}   | Create List          | InternetGatewayDevice.DeviceInfo.ManufacturerOUI  | 0F34PT        |
        | ${two_list}   | Create List          | InternetGatewayDevice.DeviceInfo.ProvisioningCode |  111          |
        | ${para_lists} | Create List          | ${one_list}                                       | ${two_list}   |
        | ${status}     | Set Parameter Values | ${para_lists}                                     | some_key      |
        
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        tmp_list = []
        tmp_parameter_list = []
        if type(parameter_list[0]) is not list:
            tmp_list.append(parameter_list)
        else:
            tmp_list = parameter_list
        for item in tmp_list:
            len1 = len(item)
            dict_parameters = {}
            if len1 < 2:
                raise RuntimeError(u'\u8f93\u5165\u7684\u53c2\u6570(parameter_list)\u683c\u5f0f\u6709\u8bef')
            if len1 >= 2:
                dict_parameters['Name'] = item[0]
                dict_parameters['Value'] = item[1]
            if len1 >= 3:
                dict_parameters['Type'] = item[2]
            tmp_parameter_list.append(dict_parameters)

        ret_api, ret_data = user1.set_parameter_values(ParameterList=tmp_parameter_list, ParameterKey=parameter_key)
        if ret_api == ERR_SUCCESS:
            desc = u'\u4fee\u6539CPE\u53c2\u6570\u6210\u529f\u3002'
            self._user_info(desc)
            if 'Status' in ret_data:
                ret_data = ret_data['Status']
                ret_out = ret_data
            else:
                desc = u'\u4fee\u6539CPE\u53c2\u6570\u5931\u8d25(\u89e3\u6790\u5931\u8d25)\u3002'
                raise RuntimeError(desc)
        else:
            desc = u'\u4fee\u6539CPE\u53c2\u6570\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def get_parameter_values(self, parameter_names = []):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\x8e\xb7\xe5\x8f\x96CPE\xe7\x9a\x84\xe4\xb8\x80\xe4\xb8\xaa\xe6\x88\x96\xe5\xa4\x9a\xe4\xb8\xaa\xe5\x8f\x82\xe6\x95\xb0\xe5\x80\xbc
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9aparameter_names: \xe8\xa1\xa8\xe7\xa4\xbaParameterNames\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe7\x94\xb1\xe5\x8f\x82\xe6\x95\xb0\xe5\x90\x8d\xe7\xbb\x84\xe6\x88\x90\xe7\x9a\x84\xe5\x88\x97\xe8\xa1\xa8\xef\xbc\x8c
                               \xe5\xa6\x82\xe6\x9e\x9c\xe5\x8f\xaa\xe8\x8e\xb7\xe5\x8f\x96\xe4\xb8\x80\xe4\xb8\xaa\xe5\x8f\x82\xe6\x95\xb0\xe5\x80\xbc\xef\xbc\x8c\xe5\x8f\x82\xe6\x95\xb0\xe6\xa0\xbc\xe5\xbc\x8f\xe4\xb8\xba\xef\xbc\x9aname \xe6\x88\x96\xe8\x80\x85[name]
                               \xe5\xa6\x82\xe6\x9e\x9c\xe8\xa6\x81\xe8\x8e\xb7\xe5\x8f\x96\xe5\xa4\x9a\xe4\xb8\xaa\xe5\x8f\x82\xe6\x95\xb0\xe5\x80\xbc\xef\xbc\x8c\xe5\x8f\x82\xe6\x95\xb0\xe6\xa0\xbc\xe5\xbc\x8f\xe4\xb8\xba\xef\xbc\x9a[name1,name2,...]
                               \xe5\xa6\x82\xe6\x9e\x9c\xe5\x8f\x82\xe6\x95\xb0\xe5\x90\x8d\xe4\xb8\x8d\xe6\x98\xaf\xe5\xae\x8c\xe6\x95\xb4\xe8\xb7\xaf\xe5\xbe\x84\xef\xbc\x8c\xe4\xbb\xa5\xe7\x82\xb9\xe7\xbb\x93\xe5\xb0\xbe\xef\xbc\x8c\xe8\xa1\xa8\xe7\xa4\xba\xe8\x8e\xb7\xe5\x8f\x96\xe8\xaf\xa5\xe8\xb7\xaf\xe5\xbe\x84\xe4\xb8\x8b\xe6\x89\x80\xe6\x9c\x89\xe7\x9a\x84\xe5\x8f\x82\xe6\x95\xb0\xe5\x80\xbc
                               \xe5\xa6\x82\xe6\x9e\x9c\xe5\x8f\x82\xe6\x95\xb0\xe5\x90\x8d\xe4\xb8\xba\xe7\xa9\xba\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2\xef\xbc\x8c\xe8\xa1\xa8\xe7\xa4\xba\xe9\xa1\xb6\xe7\xba\xa7\xe5\x8f\x82\xe6\x95\xb0\xe5\x90\x8d\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba\xe7\xa9\xba
                               
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e \xe7\x94\xb1[Name, Value]\xe7\xbb\x84\xe6\x88\x90\xe7\x9a\x84\xe5\x88\x97\xe8\xa1\xa8;
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${name1}     | Set Variable           | InternetGatewayDevice.DeviceInfo.ManufacturerOUI  |          |
        | ${name2}     | Set Variable           | InternetGatewayDevice.DeviceInfo.ProvisioningCode |          |                                   |
        | ${para_list} | Create List            | ${name1}                                          | ${name2} |
        | ${ret_list}  | Get Parameter Values   | ${para_list}                                      |          |
        | ${ret_list}  | Get Parameter Values   | ${name1}                                          |          |
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        tmp_parameter_names = []
        ret_list = []
        if type(parameter_names) is not list:
            tmp_parameter_names.append(parameter_names)
        else:
            tmp_parameter_names = parameter_names
        ret_api, ret_data = user1.get_parameter_values(ParameterNames=tmp_parameter_names)
        if ret_api == ERR_SUCCESS:
            desc = u'\u83b7\u53d6CPE\u53c2\u6570\u503c\u6210\u529f\u3002'
            self._user_info(desc)
            if 'ParameterList' in ret_data:
                tmp_ret_list = ret_data['ParameterList']
                for item in tmp_ret_list:
                    ret_list.append([item['Name'], item['Value']])

                ret_out = ret_list
            else:
                desc = u'\u83b7\u53d6CPE\u53c2\u6570\u503c\u5931\u8d25(\u89e3\u6790\u5931\u8d25)\u3002'
                raise RuntimeError(desc)
        else:
            desc = u'\u83b7\u53d6CPE\u53c2\u6570\u503c\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def get_parameter_names(self, parameter_path = '', next_level = False):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\x8e\xb7\xe5\x8f\x96CPE\xe4\xb8\x8a\xe5\x8f\xaf\xe4\xbb\xa5\xe8\xae\xbf\xe9\x97\xae\xe7\x9a\x84\xe5\x8f\x82\xe6\x95\xb0
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9aparameter_path:  \xe8\xa1\xa8\xe7\xa4\xbaParameterPath\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe5\x8f\xaf\xe4\xbb\xa5\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe5\x85\xa8\xe8\xb7\xaf\xe5\xbe\x84\xe6\x88\x96\xe8\x80\x85\xe9\x83\xa8\xe5\x88\x86\xe8\xb7\xaf\xe5\xbe\x84\xef\xbc\x8c
                               \xe5\xa6\x82\xe6\x9e\x9c\xe6\x98\xaf\xe9\x83\xa8\xe5\x88\x86\xe8\xb7\xaf\xe5\xbe\x84\xe5\xbf\x85\xe9\xa1\xbb\xe4\xbb\xa5\xe7\x82\xb9\xe7\xbb\x93\xe5\xb0\xbe\xef\xbc\x8c
                               \xe5\xa6\x82\xe6\x9e\x9c\xe6\x98\xaf\xe7\xa9\xba\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2\xe8\xa1\xa8\xe7\xa4\xba\xe9\xa1\xb6\xe7\xba\xa7\xe5\x8f\x82\xe6\x95\xb0\xe5\x90\x8d\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba\xe7\xa9\xba\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2;
                               
              next_level: \xe8\xa1\xa8\xe7\xa4\xbaNextLevel\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe4\xb8\xbaFalse\xe8\xa1\xa8\xe7\xa4\xba\xe8\xbf\x94\xe5\x9b\x9e\xe4\xb8\x8e\xe5\x8f\x82\xe6\x95\xb0\xe8\xb7\xaf\xe5\xbe\x84\xe5\xae\x8c\xe5\x85\xa8\xe5\x8c\xb9\xe9\x85\x8d\xe7\x9a\x84\xe8\x8a\x82\xe7\x82\xb9\xe5\x8f\x82\xe6\x95\xb0
                          \xe4\xbb\xa5\xe5\x8f\x8a\xe8\xaf\xa5\xe8\xb7\xaf\xe5\xbe\x84\xe4\xb8\x8b\xe9\x9d\xa2\xe6\x89\x80\xe6\x9c\x89\xe7\x9a\x84\xe5\xad\x90\xe8\x8a\x82\xe7\x82\xb9\xe5\x8f\x82\xe6\x95\xb0\xe3\x80\x82\xe4\xb8\xbaTrue\xef\xbc\x8c\xe5\x8f\xaa\xe8\xbf\x94\xe5\x9b\x9e\xe5\x8c\xb9\xe9\x85\x8d\xe8\xb7\xaf\xe5\xbe\x84\xe4\xb8\x8b\xe4\xb8\x80\xe7\xba\xa7\xe7\x9a\x84\xe8\x8a\x82\xe7\x82\xb9\xe5\x8f\x82\xe6\x95\xb0
                          \xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xbaFalse
                          
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e \xe7\x94\xb1[Name, Writalbe]\xe7\xbb\x84\xe6\x88\x90\xe7\x9a\x84\xe5\x88\x97\xe8\xa1\xa8;
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${path}      | Set Variable           | InternetGatewayDevice.DeviceInfo.                 |      |
        | ${name}      | Set Variable           | InternetGatewayDevice.DeviceInfo.ManufacturerOUI  |      |
        | ${ret_list}  | Get Parameter Names    | ${path }                                          | True |
        | ${ret_list}  | Get Parameter Names    | ${name}                                           |      |
        | ${ret_list}  | Get Parameter Names    |                                                   |      |
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        ret_list = []
        ret_api, ret_data = user1.get_parameter_names(ParameterPath=parameter_path, NextLevel=next_level)
        if ret_api == ERR_SUCCESS:
            desc = u'\u83b7\u53d6CPE\u4e0a\u53ef\u4ee5\u8bbf\u95ee\u7684\u53c2\u6570\u6210\u529f\u3002'
            self._user_info(desc)
            if 'ParameterList' in ret_data:
                tmp_ret_list = ret_data['ParameterList']
                for item in tmp_ret_list:
                    ret_list.append([item['Name'], item['Writable']])

                ret_out = ret_list
            else:
                desc = u'\u83b7\u53d6CPE\u4e0a\u53ef\u4ee5\u8bbf\u95ee\u7684\u53c2\u6570\u5931\u8d25(\u89e3\u6790\u5931\u8d25)\u3002'
                raise RuntimeError(desc)
        else:
            desc = u'\u83b7\u53d6CPE\u4e0a\u53ef\u4ee5\u8bbf\u95ee\u7684\u53c2\u6570\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def set_parameter_attributes(self, parameter_list):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe4\xbf\xae\xe6\x94\xb9CPE\xe7\x9a\x84\xe4\xb8\x80\xe4\xb8\xaa\xe6\x88\x96\xe5\xa4\x9a\xe4\xb8\xaa\xe5\x8f\x82\xe6\x95\xb0\xe7\x9a\x84\xe5\xb1\x9e\xe6\x80\xa7
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9aparameter_list:  \xe8\xa1\xa8\xe7\xa4\xbaParameterList\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe6\x98\xaf\xe7\x94\xb1
                               [Name,NotificationChang,Notification,AccessListChange,AccessList]
                               \xe7\xbb\x84\xe6\x88\x90\xe7\x9a\x84\xe5\x88\x97\xe8\xa1\xa8\xef\xbc\x8c
                               \xe5\xa6\x82\xe6\x9e\x9c\xe5\x8f\xaa\xe4\xbf\xae\xe6\x94\xb9\xe4\xb8\x80\xe4\xb8\xaa\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe5\x8f\x82\xe6\x95\xb0\xe6\xa0\xbc\xe5\xbc\x8f\xe4\xb8\xba\xef\xbc\x9a[Name,...]\xe6\x88\x96\xe8\x80\x85[[Name,...]]
                               \xe5\xa6\x82\xe6\x9e\x9c\xe5\x90\x8c\xe6\x97\xb6\xe4\xbf\xae\xe6\x94\xb9\xe5\xa4\x9a\xe4\xb8\xaa\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe5\x8f\x82\xe6\x95\xb0\xe6\xa0\xbc\xe5\xbc\x8f\xe4\xb8\xba\xef\xbc\x9a[[Name1,...],[Name2,...]]
                
        Example:
        | ${access_list}           | Create List   | Subscriber                                         |                |
        | ${para_list}             | Create List   | InternetGatewayDevice.DeviceInfo.ManufacturerOUI  | 1              |
        | ...                      |        2      | 1                                                 | ${access_list} |\xe3\x80\x80
        | Set Parameter Attributes | ${para_list}  |                                                   |                |
        | ${two_list}              | Create List   | InternetGatewayDevice.DeviceInfo.ProvisioningCode | 1              |
        | ...                      | 1             | 1                                                 | ${access_list} |
        | ${para_lists}            | Create List   | ${para_list}                                      | ${two_list}    |
        | Set Parameter Attributes | ${para_lists} |                                                   |                |
        
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        tmp_list = []
        tmp_parameter_list = []
        if type(parameter_list[0]) is not list:
            tmp_list.append(parameter_list)
        else:
            tmp_list = parameter_list
        for item in tmp_list:
            if len(item) == 5:
                dict_parameters = {}
                dict_parameters['Name'] = item[0]
                dict_parameters['NotificationChange'] = item[1]
                dict_parameters['Notification'] = item[2]
                dict_parameters['AccessListChange'] = item[3]
                dict_parameters['AccessList'] = item[4]
                tmp_parameter_list.append(dict_parameters)
            else:
                raise RuntimeError(u'\u8f93\u5165\u7684\u53c2\u6570(parameter_list)\u683c\u5f0f\u6709\u8bef')

        ret_api, ret_data = user1.set_parameter_attributes(ParameterList=tmp_parameter_list)
        if ret_api == ERR_SUCCESS:
            desc = u'\u4fee\u6539CPE\u7684\u53c2\u6570\u7684\u5c5e\u6027\u6210\u529f\u3002'
            self._user_info(desc)
            ret_out = ret_data
        else:
            desc = u'\u4fee\u6539CPE\u7684\u53c2\u6570\u7684\u5c5e\u6027\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def get_parameter_attributes(self, parameter_names = []):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\x8e\xb7\xe5\x8f\x96CPE\xe7\x9a\x84\xe4\xb8\x80\xe4\xb8\xaa\xe6\x88\x96\xe5\xa4\x9a\xe4\xb8\xaa\xe5\x8f\x82\xe6\x95\xb0\xe7\x9a\x84\xe5\xb1\x9e\xe6\x80\xa7
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9aparameter_names: \xe8\xa1\xa8\xe7\xa4\xbaParameterNames\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe7\x94\xb1\xe5\x8f\x82\xe6\x95\xb0\xe5\x90\x8d\xe7\xbb\x84\xe6\x88\x90\xe7\x9a\x84\xe5\x88\x97\xe8\xa1\xa8\xef\xbc\x8c
                               \xe5\xa6\x82\xe6\x9e\x9c\xe5\x8f\xaa\xe8\x8e\xb7\xe5\x8f\x96\xe4\xb8\x80\xe4\xb8\xaa\xe5\x8f\x82\xe6\x95\xb0\xe7\x9a\x84\xe5\xb1\x9e\xe6\x80\xa7\xef\xbc\x8c\xe5\x8f\x82\xe6\x95\xb0\xe6\xa0\xbc\xe5\xbc\x8f\xe4\xb8\xba\xef\xbc\x9aname\xe6\x88\x96\xe8\x80\x85[name]
                               \xe5\xa6\x82\xe6\x9e\x9c\xe8\xa6\x81\xe8\x8e\xb7\xe5\x8f\x96\xe5\xa4\x9a\xe4\xb8\xaa\xe5\x8f\x82\xe6\x95\xb0\xe7\x9a\x84\xe5\xb1\x9e\xe6\x80\xa7\xef\xbc\x8c\xe5\x8f\x82\xe6\x95\xb0\xe6\xa0\xbc\xe5\xbc\x8f\xe4\xb8\xba\xef\xbc\x9a[name1,name2,...]
                               \xe5\xa6\x82\xe6\x9e\x9c\xe5\x8f\x82\xe6\x95\xb0\xe5\x90\x8d\xe4\xb8\x8d\xe6\x98\xaf\xe5\xae\x8c\xe6\x95\xb4\xe8\xb7\xaf\xe5\xbe\x84\xef\xbc\x8c\xe4\xbb\xa5\xe7\x82\xb9\xe7\xbb\x93\xe5\xb0\xbe\xef\xbc\x8c\xe8\xa1\xa8\xe7\xa4\xba\xe8\x8e\xb7\xe5\x8f\x96\xe8\xaf\xa5\xe8\xb7\xaf\xe5\xbe\x84\xe4\xb8\x8b\xe6\x89\x80\xe6\x9c\x89\xe7\x9a\x84\xe5\x8f\x82\xe6\x95\xb0\xe7\x9a\x84\xe5\xb1\x9e\xe6\x80\xa7
                               \xe5\xa6\x82\xe6\x9e\x9c\xe5\x8f\x82\xe6\x95\xb0\xe5\x90\x8d\xe4\xb8\xba\xe7\xa9\xba\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2\xef\xbc\x8c\xe8\xa1\xa8\xe7\xa4\xba\xe9\xa1\xb6\xe7\xba\xa7\xe5\x8f\x82\xe6\x95\xb0\xe5\x90\x8d\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba\xe7\xa9\xba
                               
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e \xe7\x94\xb1[Name, Notification, AccessList]\xe7\xbb\x84\xe6\x88\x90\xe7\x9a\x84\xe5\x88\x97\xe8\xa1\xa8;
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${name1}     | Set Variable              | InternetGatewayDevice.DeviceInfo.ManufacturerOUI  |          |
        | ${name2}     | Set Variable              | InternetGatewayDevice.DeviceInfo.ProvisioningCode |          |
        | ${para_list} | Create List               | ${name1}                                          | ${name2} | 
        | ${ret_list}  | Get Parameter Attributes  | ${name1}                                          |          |
        | ${ret_list}  | Get Parameter Attributes  | ${para_list}                                      |          |
        
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        tmp_parameter_names = []
        ret_list = []
        if type(parameter_names) is not list:
            tmp_parameter_names.append(parameter_names)
        else:
            tmp_parameter_names = parameter_names
        ret_api, ret_data = user1.get_parameter_attributes(ParameterNames=tmp_parameter_names)
        if ret_api == ERR_SUCCESS:
            desc = u'\u83b7\u53d6CPE\u7684\u53c2\u6570\u7684\u5c5e\u6027\u6210\u529f\u3002'
            self._user_info(desc)
            if 'ParameterList' in ret_data:
                tmp_ret_list = ret_data['ParameterList']
                for item in tmp_ret_list:
                    ret_list.append([item['Name'], item['Notification'], item['AccessList']])

                ret_out = ret_list
            else:
                desc = u'\u83b7\u53d6CPE\u7684\u53c2\u6570\u7684\u5c5e\u6027\u5931\u8d25(\u89e3\u6790\u5931\u8d25)\u3002'
                raise RuntimeError(desc)
        else:
            desc = u'\u83b7\u53d6CPE\u7684\u53c2\u6570\u7684\u5c5e\u6027\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def get_queued_transfers(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe7\x94\xa8\xe4\xba\x8e\xe8\x8e\xb7\xe5\x8f\x96\xe4\xb9\x8b\xe5\x89\x8d\xe8\xaf\xb7\xe6\xb1\x82\xe7\x9a\x84\xe4\xb8\x8b\xe8\xbd\xbd\xe6\x88\x96\xe4\xb8\x8a\xe4\xbc\xa0\xe7\x9a\x84\xe7\x8a\xb6\xe6\x80\x81
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a\xe6\x97\xa0
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e [CommandKey,State]
               \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
               
        Example:
        | ${ret_list} | Get Queued Transfers  |       |
        
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        tmp_list = []
        ret_api, ret_data = user1.get_queued_transfers()
        if ret_api == ERR_SUCCESS:
            desc = u'\u83b7\u53d6\u4e4b\u524d\u8bf7\u6c42\u7684\u4e0b\u8f7d\u6216\u4e0a\u4f20\u7684\u72b6\u6001\u6210\u529f\u3002'
            self._user_info(desc)
            if 'TransferList' in ret_data:
                transflist = ret_data['TransferList']
                if transflist:
                    transfer_list = transflist[0]
                    tmp_list.append(transfer_list['CommandKey'])
                    tmp_list.append(transfer_list['State'])
                else:
                    tmp_list = []
                ret_out = tmp_list
            else:
                desc = u'\u83b7\u53d6\u4e4b\u524d\u8bf7\u6c42\u7684\u4e0b\u8f7d\u6216\u4e0a\u4f20\u7684\u72b6\u6001\u5931\u8d25(\u89e3\u6790\u5931\u8d25)\u3002'
                raise RuntimeError(desc)
        else:
            desc = u'\u83b7\u53d6\u4e4b\u524d\u8bf7\u6c42\u7684\u4e0b\u8f7d\u6216\u4e0a\u4f20\u7684\u72b6\u6001\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def reboot(self, command_key = 'AUTO'):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\xae\xa9CPE\xe9\x87\x8d\xe5\x90\xaf
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9acommand_key: \xe8\xa1\xa8\xe7\xa4\xbaCommandKey\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba"AUTO"(\xe7\x94\xb1\xe7\xb3\xbb\xe7\xbb\x9f\xe8\x87\xaa\xe5\x8a\xa8\xe7\x94\x9f\xe6\x88\x90\xe9\x9a\x8f\xe6\x9c\xba\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2)
            
        Example:
        | Reboot  |           |
        | Reboot  | some_key  |
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        if command_key == 'AUTO':
            command_key = self._get_random_command_key()
        ret_api, ret_data = user1.reboot(CommandKey=command_key)
        if ret_api == ERR_SUCCESS:
            desc = u'CPE\u91cd\u542f\u6210\u529f\u3002'
            self._user_info(desc)
            ret_out = ret_data
        else:
            desc = u'CPE\u91cd\u542f\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def schedule_inform(self, delay_seconds, command_key = 'AUTO'):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\xaf\xa5\xe6\x96\xb9\xe6\xb3\x95\xe7\xbb\x99CPE\xe5\x8f\x91\xe9\x80\x81\xe4\xb8\x80\xe4\xb8\xaa\xe8\xaf\xb7\xe6\xb1\x82\xef\xbc\x8c\xe8\xa6\x81\xe6\xb1\x82cpe\xe5\x9c\xa8\xe8\xaf\xa5\xe6\x96\xb9\xe6\xb3\x95\xe6\x88\x90\xe5\x8a\x9f\xe7\x9a\x84DelaySeconds\xe4\xb9\x8b\xe5\x90\x8e\xe8\xb0\x83\xe7\x94\xa8Inform\xe6\x96\xb9\xe6\xb3\x95\xe3\x80\x82
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9adelay_seconds: \xe8\xa1\xa8\xe7\xa4\xbaDelaySeconds\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe4\xbb\x8e\xe6\x94\xb6\xe5\x88\xb0\xe6\x96\xb9\xe6\xb3\x95\xe5\x88\xb0\xe5\x88\x9d\xe5\xa7\x8binform\xe9\x9c\x80\xe8\xa6\x81\xe7\xad\x89\xe5\xbe\x85\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x8c
                             \xe8\xaf\xa5\xe5\x8f\x82\xe6\x95\xb0\xe5\x80\xbc\xe5\xbf\x85\xe9\xa1\xbb\xe6\xaf\x940\xe5\xa4\xa7 
              command_key: \xe8\xa1\xa8\xe7\xa4\xbaCommandKey\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba"AUTO"(\xe7\x94\xb1\xe7\xb3\xbb\xe7\xbb\x9f\xe8\x87\xaa\xe5\x8a\xa8\xe7\x94\x9f\xe6\x88\x90\xe9\x9a\x8f\xe6\x9c\xba\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2)
               
        Example:
        | Schedule Inform  |  10  |          |
        | Schedule Inform  |  10  | some_key |
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        if command_key == 'AUTO':
            command_key = self._get_random_command_key()
        ret_api, ret_data = user1.schedule_inform(DelaySeconds=delay_seconds, CommandKey=command_key)
        if ret_api == ERR_SUCCESS:
            desc = u'\u8ba1\u5212inform\u6210\u529f\u3002'
            self._user_info(desc)
            ret_out = ret_data
        else:
            desc = u'\u8ba1\u5212inform\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def set_vouchers(self, voucher_list):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe5\x9c\xa8CPE\xe4\xb8\x8a\xe8\xae\xbe\xe7\xbd\xae\xe4\xb8\x80\xe4\xb8\xaa\xe6\x88\x96\xe5\xa4\x9a\xe4\xb8\xaaoption-vouchers
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9avoucher_list: \xe8\xa1\xa8\xe7\xa4\xbaVoucherList\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe7\x94\xb1Voucher\xe7\xbb\x84\xe6\x88\x90\xe7\x9a\x84list\xef\xbc\x8c
                            \xe6\xaf\x8f\xe4\xb8\xaaVoucher\xe8\xa1\xa8\xe7\x8e\xb0\xe4\xb8\xba\xe4\xb8\x80\xe4\xb8\xaaBase64 encoded octet string
                
        Example:
        | ${voucher}      | Set Variable    | some_string |              |
        | ${voucher_list} | Create List     | some_string | other_string |
        | Set Vouchers    | ${voucher}      |             |              |
        | Set Vouchers    | ${voucher_list} |             |              |
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        ret_api, ret_data = user1.set_vouchers(VoucherList=voucher_list)
        if ret_api == ERR_SUCCESS:
            desc = u'\u8bbe\u7f6eCPE\u51ed\u636e\u9009\u9879\u6210\u529f\u3002'
            self._user_info(desc)
            ret_out = ret_data
        else:
            desc = u'\u8bbe\u7f6eCPE\u51ed\u636e\u9009\u9879\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def upload(self, file_type, url, user_name = '', password = '', delay_seconds = 0, command_key = 'AUTO'):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\xae\xa9CPE\xe4\xb8\x8a\xe4\xbc\xa0\xe6\x9f\x90\xe4\xb8\x80\xe7\x89\xb9\xe5\xae\x9a\xe6\x96\x87\xe4\xbb\xb6\xe5\x88\xb0\xe6\x9f\x90\xe4\xb8\x80\xe7\x89\xb9\xe5\xae\x9a\xe8\xb7\xaf\xe5\xbe\x84
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9afile_type: \xe8\xa1\xa8\xe7\xa4\xbaFileType\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe4\xb8\x80\xe4\xb8\xaa\xe6\x95\xb4\xe6\x95\xb0\xe5\x8a\xa0\xe4\xb8\x80\xe4\xb8\xaa\xe7\xa9\xba\xe6\xa0\xbc\xe5\x8a\xa0\xe6\x96\x87\xe4\xbb\xb6\xe7\xb1\xbb\xe5\x9e\x8b\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x8c\xe7\x9b\xae\xe5\x89\x8d\xe6\x94\xaf\xe6\x8c\x81\xe4\xbb\xa5\xe4\xb8\x8b\xe5\x87\xa0\xe7\xa7\x8d\xef\xbc\x9a
                          "1 Vendor Configuration File"[DEPRECATED]
                          "2 Vendor Log File"[DEPRECATED]
                          "3 Vendor Configuration File <i>"
                          "4 Vendor Log File <i>"
                          "X<VENDOR><Vendor-specific-identifier>"
                          
              url: \xe8\xa1\xa8\xe7\xa4\xbaURL\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe7\x9b\xae\xe6\xa0\x87\xe6\x96\x87\xe4\xbb\xb6\xe8\xb7\xaf\xe5\xbe\x84;
              
              user_name: \xe8\xa1\xa8\xe7\xa4\xbaUsername\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe6\x96\x87\xe4\xbb\xb6\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe8\xae\xa4\xe8\xaf\x81\xe7\x9a\x84\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba\xe7\xa9\xba;
              
              password: \xe8\xa1\xa8\xe7\xa4\xbaPassword\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe6\x96\x87\xe4\xbb\xb6\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe8\xae\xa4\xe8\xaf\x81\xe7\x9a\x84\xe5\xaf\x86\xe7\xa0\x81\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba\xe7\xa9\xba;
              
              delay_seconds: \xe8\xa1\xa8\xe7\xa4\xbaDelaySeconds\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba0;
              
              command_key: \xe8\xa1\xa8\xe7\xa4\xbaCommandKey\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba"AUTO"(\xe7\x94\xb1\xe7\xb3\xbb\xe7\xbb\x9f\xe8\x87\xaa\xe5\x8a\xa8\xe7\x94\x9f\xe6\x88\x90\xe9\x9a\x8f\xe6\x9c\xba\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2)
              
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e [CPE\xe8\xbf\x94\xe5\x9b\x9e\xe7\x9a\x84\xe4\xbf\xae\xe6\x94\xb9\xe7\x8a\xb6\xe6\x80\x81status,StartTime,CompleteTime];
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${ret_list} | Upload  | 1 Vendor Configuration File | http://20.20.20.20:9090/web/upload/ |
        | ${ret_list} | Upload  | 1 Vendor Configuration File | http://20.20.20.20:9090/web/upload/ |
        | ...         | user    | password                    | 10                                  | 
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        tmp_list = []
        if command_key == 'AUTO':
            command_key = self._get_random_command_key()
        ret_api, ret_data = user1.upload(CommandKey=command_key, FileType=file_type, URL=url, Username=user_name, Password=password, DelaySeconds=delay_seconds)
        if ret_api == ERR_SUCCESS:
            desc = u'\u4e0a\u4f20\u6210\u529f\u3002'
            self._user_info(desc)
            if 'Status' in ret_data and 'StartTime' in ret_data and 'CompleteTime' in ret_data:
                tmp_list.append(ret_data['Status'])
                tmp_list.append(ret_data['StartTime'])
                tmp_list.append(ret_data['CompleteTime'])
                ret_out = tmp_list
            else:
                desc = u'\u4e0a\u4f20\u5931\u8d25(\u89e3\u6790\u5931\u8d25)\u3002'
                raise RuntimeError(desc)
        else:
            desc = u'\u4e0a\u4f20\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def _query_cpe_info(self):
        """
        """
        ret = ERR_FAIL
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        ret_api, ret_data = user.query_cpe_info(sn)
        if ret_api == ERR_SUCCESS:
            desc = u'\u67e5\u8be2CPE\u4fe1\u606f\u6210\u529f\u3002'
            ret_out = ret_data
            ret = ERR_SUCCESS
        else:
            desc = u'\u67e5\u8be2CPE\u4fe1\u606f\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            ret = ERR_FAIL
            ret_out = desc
        return (ret, ret_out)

    def _update_cpe_info(self, dict_modify_items):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe6\x9b\xb4\xe6\x96\xb0CPE\xe7\x9b\xb8\xe5\x85\xb3\xe4\xbf\xa1\xe6\x81\xaf\xe5\x88\xb0ACS\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9adict_modify_items: \xe9\x9c\x80\xe8\xa6\x81\xe6\x9b\xb4\xe6\x96\xb0\xe7\x9a\x84\xe4\xbf\xa1\xe6\x81\xaf\xe5\xad\x97\xe5\x85\xb8\xef\xbc\x8c\xe6\xa0\xbc\xe5\xbc\x8f\xe4\xb8\xba{name:value,...}
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e(TR069_SUCCESS(0)\xef\xbc\x8c\xe6\x88\x90\xe5\x8a\x9f\xe4\xbf\xa1\xe6\x81\xaf);
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e(TR069_FAIL(-1)\xef\xbc\x8c\xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf)
        """
        ret = None
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        ret_api, ret_data = user.update_cpe_info(sn, dict_modify_items)
        if ret_api == ERR_SUCCESS:
            desc = u'\u66f4\u65b0CPE\u4fe1\u606f\u6210\u529f\u3002'
            ret = ERR_SUCCESS
            ret_out = ret_data
        else:
            desc = u'\u66f4\u65b0CPE\u4fe1\u606f\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            ret = ERR_FAIL
            ret_out = desc
        return (ret, ret_out)

    def get_acs_auth_info(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\x8e\xb7\xe5\x8f\x96CPE\xe7\x9a\x84\xe6\xad\xa3\xe5\x90\x91\xe8\xae\xa4\xe8\xaf\x81\xe4\xbf\xa1\xe6\x81\xaf\xef\xbc\x8c\xe5\x8c\x85\xe6\x8b\xac\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d\xe5\x92\x8c\xe5\xaf\x86\xe7\xa0\x81
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a\xe6\x97\xa0
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e [username,password];
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${ret_list} | Get Acs Auth Info  |
        
        """
        ret = None
        ret_data = None
        ret_out = None
        ret, ret_data = self._query_cpe_info()
        if ret == ERR_SUCCESS:
            desc = u'\u83b7\u53d6CPE\u7684\u6b63\u5411\u8ba4\u8bc1\u4fe1\u606f\u6210\u529f\u3002'
            self._user_info(desc)
            username = ret_data.cpe2acs_loginname
            password = ret_data.cpe2acs_loginpassword
            ret_out = [username, password]
        else:
            desc = u'\u83b7\u53d6CPE\u7684\u6b63\u5411\u8ba4\u8bc1\u4fe1\u606f\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def set_acs_auth_info(self, username = 'admin', password = 'admin'):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe4\xbf\xae\xe6\x94\xb9\xe6\xad\xa3\xe5\x90\x91\xe8\xbf\x9e\xe6\x8e\xa5\xe8\xae\xa4\xe8\xaf\x81\xe7\x9a\x84\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d\xe5\x92\x8c\xe5\xaf\x86\xe7\xa0\x81
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a username: acs\xe8\xae\xa4\xe8\xaf\x81cpe\xe7\x9a\x84\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d;
               password: acs\xe8\xae\xa4\xe8\xaf\x81cpe\xe7\x9a\x84\xe5\xaf\x86\xe7\xa0\x81
                
        Example:
        | Set Acs Auth Info  | username  | password  |
        
        """
        ret = None
        ret_data = None
        ret_out = None
        d1 = {}
        d1['acs_auth_cpe_username'] = username
        d1['acs_auth_cpe_password'] = password
        ret, ret_data = self._update_cpe_info(d1)
        if ret == ERR_SUCCESS:
            desc = u'\u4fee\u6539\u6b63\u5411\u8fde\u63a5\u8ba4\u8bc1\u7684\u7528\u6237\u540d\u548c\u5bc6\u7801\u6210\u529f\u3002'
            self._user_info(desc)
            ret_out = ret_data
        else:
            desc = u'\u4fee\u6539\u6b63\u5411\u8fde\u63a5\u8ba4\u8bc1\u7684\u7528\u6237\u540d\u548c\u5bc6\u7801\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def get_acs_auth_method(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\x8e\xb7\xe5\x8f\x96CPE\xe7\x9a\x84\xe6\xad\xa3\xe5\x90\x91\xe8\xae\xa4\xe8\xaf\x81\xe6\x96\xb9\xe5\xbc\x8f
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a\xe6\x97\xa0
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e \xe8\xae\xa4\xe8\xaf\x81\xe6\x96\xb9\xe5\xbc\x8f;
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${auth_method} | Get Acs Auth Method  |
        
        """
        ret = None
        ret_data = None
        ret_out = None
        ret, ret_data = self._query_cpe_info()
        if ret == ERR_SUCCESS:
            desc = u'\u83b7\u53d6CPE\u7684\u6b63\u5411\u8ba4\u8bc1\u65b9\u5f0f\u6210\u529f\u3002'
            self._user_info(desc)
            ret_out = ret_data.auth_type
        else:
            desc = u'\u83b7\u53d6CPE\u7684\u6b63\u5411\u8ba4\u8bc1\u65b9\u5f0f\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def set_acs_auth_method(self, method = 'digest'):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe4\xbf\xae\xe6\x94\xb9\xe6\xad\xa3\xe5\x90\x91\xe8\xbf\x9e\xe6\x8e\xa5\xe8\xae\xa4\xe8\xaf\x81\xe6\x96\xb9\xe5\xbc\x8f
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a method: acs\xe8\xae\xa4\xe8\xaf\x81cpe\xe7\x9a\x84\xe8\xae\xa4\xe8\xaf\x81\xe6\x96\xb9\xe5\xbc\x8f\xef\xbc\x8ceg\xef\xbc\x9a"digest", "basic", "None"(\xe6\x97\xa0\xe8\xae\xa4\xe8\xaf\x81)
                       \xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba"digest"   
               
        Example:
        | Set Acs Auth Method  | baisc  |
        | Set Acs Auth Method  | None  |
        """
        ret = None
        ret_data = None
        ret_out = None
        if method not in ('digest', 'basic', 'None'):
            desc = u'\u53c2\u6570(method) \u4e0d\u652f\u6301'
            RuntimeError(desc)
        d1 = {}
        d1['cpe_authtype'] = method
        ret, ret_data = self._update_cpe_info(d1)
        if ret == ERR_SUCCESS:
            desc = u'\u4fee\u6539\u6b63\u5411\u8fde\u63a5\u8ba4\u8bc1\u65b9\u5f0f\u6210\u529f\u3002'
            self._user_info(desc)
            ret_out = ret_data
        else:
            desc = u'\u4fee\u6539\u6b63\u5411\u8fde\u63a5\u8ba4\u8bc1\u65b9\u5f0f\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            RuntimeError(desc)
        return ret_out

    def get_max_session_timeout(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\x8e\xb7\xe5\x8f\x96CPE\xe4\xb8\x8eACS\xe7\x9a\x84\xe6\x9c\x80\xe9\x95\xbf\xe4\xbc\x9a\xe8\xaf\x9d\xe6\x97\xb6\xe9\x95\xbf
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a\xe6\x97\xa0
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e \xe6\x9c\x80\xe9\x95\xbf\xe4\xbc\x9a\xe8\xaf\x9d\xe6\x97\xb6\xe9\x95\xbf;
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${max_session} | Get Max Session Timeout  |
        
        """
        ret = None
        ret_data = None
        ret_out = None
        ret, ret_data = self._query_cpe_info()
        if ret == ERR_SUCCESS:
            desc = u'\u83b7\u53d6CPE\u4e0eACS\u7684\u6700\u957f\u4f1a\u8bdd\u65f6\u957f\u6210\u529f\u3002'
            self._user_info(desc)
            ret_out = ret_data.soap_inform_timeout
        else:
            desc = u'\u83b7\u53d6CPE\u4e0eACS\u7684\u6700\u957f\u4f1a\u8bdd\u65f6\u957f\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def set_max_session_timeout(self, timeout = 180):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe4\xbf\xae\xe6\x94\xb9CPE\xe4\xb8\x8eACS\xe7\x9a\x84\xe6\x9c\x80\xe9\x95\xbf\xe4\xbc\x9a\xe8\xaf\x9d\xe8\xb6\x85\xe6\x97\xb6
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a timeout: \xe8\xb6\x85\xe6\x97\xb6\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4180s 
                
        Example:
        | Set Max Session Timeout  |  180  |
        
        \xe6\xb3\xa8\xe6\x84\x8f:\xe7\xa6\x81\xe6\xad\xa2\xe8\xae\xbe\xe7\xbd\xae\xe5\xa4\xa7\xe4\xba\x8e\xe7\xad\x89\xe4\xba\x8e300S.\xe5\x90\xa6\xe5\x88\x99\xe5\xbd\x93CPE\xe5\xbc\x82\xe5\xb8\xb8\xe6\x97\xb6ACS\xe5\x92\x8cAgent\xe5\xaf\xb9\xe6\xad\xa4CPE\xe7\x9a\x84\xe7\x8a\xb6\xe6\x80\x81\xe6\x81\xa2\xe5\xa4\x8d\xe4\xbc\x9a\xe4\xb8\x8d\xe5\x90\x8c\xe6\xad\xa5\xe5\xaf\xbc\xe8\x87\xb4\xe5\x90\x8e\xe7\xbb\xad\xe6\xb5\x8b\xe8\xaf\x95\xe5\xbc\x82\xe5\xb8\xb8.
            timeout\xe5\x90\x88\xe7\x90\x86\xe5\x80\xbc\xe8\x8c\x83\xe5\x9b\xb4 [60, 300]
        """
        ret = None
        ret_data = None
        ret_out = None
        d1 = {}
        timeout2 = int(timeout)
        if timeout2 < 60:
            timeout2 = 60
        elif timeout2 > 300:
            timeout2 = 300
        d1['soap_inform_timeout'] = timeout2
        ret, ret_data = self._update_cpe_info(d1)
        if ret == ERR_SUCCESS:
            desc = u'\u4fee\u6539CPE\u4e0eACS\u7684\u6700\u957f\u4f1a\u8bdd\u8d85\u65f6\u6210\u529f\u3002'
            self._user_info(desc)
            ret_out = ret_data
        else:
            desc = u'\u4fee\u6539CPE\u4e0eACS\u7684\u6700\u957f\u4f1a\u8bdd\u8d85\u65f6\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def get_cpe_software_version(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\x8e\xb7\xe5\x8f\x96CPE\xe7\x9a\x84\xe8\xbd\xaf\xe4\xbb\xb6\xe7\x89\x88\xe6\x9c\xac\xe5\x8f\xb7
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a\xe6\x97\xa0
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e CPE\xe7\x9a\x84\xe8\xbd\xaf\xe4\xbb\xb6\xe7\x89\x88\xe6\x9c\xac\xe5\x8f\xb7;
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${soft_version_num} | Get Cpe Software Version  |
        
        """
        ret = None
        ret_data = None
        ret_out = None
        ret, ret_data = self._query_cpe_info()
        if ret == ERR_SUCCESS:
            if not ret_data.soap_inform:
                desc = u'\u83b7\u53d6CPE\u7684\u8f6f\u4ef6\u7248\u672c\u53f7\u4e3a\u7a7a'
                ret_out = ''
            else:
                desc = u'\u83b7\u53d6CPE\u7684\u8f6f\u4ef6\u7248\u672c\u53f7\u6210\u529f\u3002'
                ret_out = ret_data.soap_inform.DeviceId.Softwareversion
            self._user_info(desc)
        else:
            desc = u'\u83b7\u53d6CPE\u7684\u8f6f\u4ef6\u7248\u672c\u53f7\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def get_cpe_hardware_version(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\x8e\xb7\xe5\x8f\x96CPE\xe7\x9a\x84\xe7\xa1\xac\xe4\xbb\xb6\xe7\x89\x88\xe6\x9c\xac\xe5\x8f\xb7
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a\xe6\x97\xa0
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e CPE\xe7\x9a\x84\xe7\xa1\xac\xe4\xbb\xb6\xe7\x89\x88\xe6\x9c\xac\xe5\x8f\xb7;
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${hard_version_num} | Get Cpe Hardware Version  |
        
        """
        ret = None
        ret_data = None
        ret_out = None
        ret, ret_data = self._query_cpe_info()
        if ret == ERR_SUCCESS:
            if not ret_data.soap_inform:
                desc = u'\u83b7\u53d6CPE\u7684\u786c\u4ef6\u7248\u672c\u53f7\u4e3a\u7a7a'
                ret_out = ''
            else:
                desc = u'\u83b7\u53d6CPE\u7684\u786c\u4ef6\u7248\u672c\u53f7\u6210\u529f\u3002'
                ret_out = ret_data.soap_inform.DeviceId.Hardwareversion
            self._user_info(desc)
        else:
            desc = u'\u83b7\u53d6CPE\u7684\u786c\u4ef6\u7248\u672c\u53f7\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def get_cpe_connection_request_url(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\x8e\xb7\xe5\x8f\x96CPE\xe7\x9a\x84\xe5\x8f\x8d\xe5\x90\x91\xe8\xbf\x9e\xe6\x8e\xa5url
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a\xe6\x97\xa0
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e CPE\xe7\x9a\x84\xe5\x8f\x8d\xe5\x90\x91\xe8\xbf\x9e\xe6\x8e\xa5url;
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${url} | Get Cpe Connection Request Url  |
        
        """
        ret = None
        ret_data = None
        ret_out = None
        ret, ret_data = self._query_cpe_info()
        if ret == ERR_SUCCESS:
            if not ret_data.soap_inform:
                desc = u'\u83b7\u53d6CPE\u7684\u53cd\u5411\u8fde\u63a5url\u4e3a\u7a7a\u3002'
                ret_out = ''
            else:
                desc = u'\u83b7\u53d6CPE\u7684\u53cd\u5411\u8fde\u63a5url\u6210\u529f\u3002'
                ret_out = ret_data.soap_inform.DeviceId.ConnectionRequestURL
            self._user_info(desc)
        else:
            desc = u'\u83b7\u53d6CPE\u7684\u53cd\u5411\u8fde\u63a5url\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def get_cpe_connection_request_ip(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\x8e\xb7\xe5\x8f\x96CPE\xe7\x9a\x84\xe5\x8f\x8d\xe5\x90\x91\xe8\xbf\x9e\xe6\x8e\xa5ip
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a\xe6\x97\xa0
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e CPE\xe7\x9a\x84\xe5\x8f\x8d\xe5\x90\x91\xe8\xbf\x9e\xe6\x8e\xa5ip;
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${ip} | Get Cpe Connection Request Ip  |
        
        """
        ret = None
        ret_data = None
        ret_out = None
        ret, ret_data = self._query_cpe_info()
        if ret == ERR_SUCCESS:
            if not ret_data.soap_inform:
                desc = u'\u83b7\u53d6CPE\u7684\u53cd\u5411\u8fde\u63a5ip\u4e3a\u7a7a\u3002'
                ret_out = ''
            else:
                desc = u'\u83b7\u53d6CPE\u7684\u53cd\u5411\u8fde\u63a5ip\u6210\u529f\u3002'
                url = ret_data.soap_inform.DeviceId.ConnectionRequestURL
                ip_start = url.find(':') + 3
                ip_end = url.find(':', 6)
                ret_out = url[ip_start:ip_end]
            self._user_info(desc)
        else:
            desc = u'\u83b7\u53d6CPE\u7684\u53cd\u5411\u8fde\u63a5url\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def get_cpe_auth_info(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\x8e\xb7\xe5\x8f\x96CPE\xe7\x9a\x84\xe5\x8f\x8d\xe5\x90\x91\xe8\xae\xa4\xe8\xaf\x81\xe4\xbf\xa1\xe6\x81\xaf\xef\xbc\x8c\xe5\x8c\x85\xe6\x8b\xac\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d\xe5\x92\x8c\xe5\xaf\x86\xe7\xa0\x81
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a\xe6\x97\xa0
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e [username,password];
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${ret_list} | Get Cpe Auth Info  |
        
        """
        ret = None
        ret_data = None
        ret_out = None
        ret, ret_data = self._query_cpe_info()
        if ret == ERR_SUCCESS:
            desc = u'\u83b7\u53d6CPE\u7684\u53cd\u5411\u8ba4\u8bc1\u4fe1\u606f\u6210\u529f\u3002'
            self._user_info(desc)
            username = ret_data.acs2cpe_loginname
            password = ret_data.acs2cpe_loginpassword
            ret_out = [username, password]
        else:
            desc = u'\u83b7\u53d6CPE\u7684\u53cd\u5411\u8ba4\u8bc1\u4fe1\u606f\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def set_cpe_auth_info(self, username = 'admin', password = 'admin'):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe4\xbf\xae\xe6\x94\xb9\xe5\x8f\x8d\xe5\x90\x91\xe8\xbf\x9e\xe6\x8e\xa5\xe8\xae\xa4\xe8\xaf\x81\xe7\x9a\x84\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d\xe5\x92\x8c\xe5\xaf\x86\xe7\xa0\x81
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a username: cpe\xe8\xae\xa4\xe8\xaf\x81acs\xe7\x9a\x84\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d;
               password: cpe\xe8\xae\xa4\xe8\xaf\x81acs\xe7\x9a\x84\xe5\xaf\x86\xe7\xa0\x81
                 
        Example:
        | Set Cpe Auth Info  |username1  | password1  |
        """
        ret = None
        ret_data = None
        ret_out = None
        d1 = {}
        d1['cpe_auth_acs_username'] = username
        d1['cpe_auth_acs_password'] = password
        ret, ret_data = self._update_cpe_info(d1)
        if ret == ERR_SUCCESS:
            desc = u'\u4fee\u6539\u53cd\u5411\u8fde\u63a5\u8ba4\u8bc1\u7684\u7528\u6237\u540d\u548c\u5bc6\u7801\u6210\u529f\u3002'
            self._user_info(desc)
            ret_out = ret_data
        else:
            desc = u'\u4fee\u6539\u53cd\u5411\u8fde\u63a5\u8ba4\u8bc1\u7684\u7528\u6237\u540d\u548c\u5bc6\u7801\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def get_cpe_cwmp_version(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\x8e\xb7\xe5\x8f\x96CPE\xe7\x9a\x84TR069\xe7\x89\x88\xe6\x9c\xac\xe5\x8f\xb7
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a\xe6\x97\xa0
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e TR069\xe7\x89\x88\xe6\x9c\xac\xe5\x8f\xb7;
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${cwmp_version} | Get Cpe Cwmp Version  |
        
        """
        ret = None
        ret_data = None
        ret_out = None
        ret, ret_data = self._query_cpe_info()
        if ret == ERR_SUCCESS:
            desc = u'\u83b7\u53d6CPE\u7684TR069\u7248\u672c\u53f7\u6210\u529f\u3002'
            self._user_info(desc)
            ret_out = ret_data.cwmp_version
        else:
            desc = u'\u83b7\u53d6CPE\u7684TR069\u7248\u672c\u53f7\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def set_cpe_cwmp_version(self, version = 'cwmp-1-0'):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe4\xbf\xae\xe6\x94\xb9CPE\xe6\x94\xaf\xe6\x8c\x81\xe7\x9a\x84TR069\xe7\x89\x88\xe6\x9c\xac\xe5\x8f\xb7
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a version: TR069\xe7\x89\x88\xe6\x9c\xac\xe5\x8f\xb7\xef\xbc\x8ceg\xef\xbc\x9a"cwmp-1-0", "cwmp-1-1", "cwmp-1-2", "cwmp-1-3" \xe7\xad\x89
                       \xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba"cwmp-1-0"   
                 
        Example:
        | Set Cpe Cwmp Version  | cwmp-1-3  |
        """
        ret = None
        ret_data = None
        ret_out = None
        d1 = {}
        d1['cwmp_version'] = version
        ret, ret_data = self._update_cpe_info(d1)
        if ret == ERR_SUCCESS:
            desc = u'\u4fee\u6539CPE\u652f\u6301\u7684TR069\u7248\u672c\u53f7\u6210\u529f\u3002'
            self._user_info(desc)
            ret_out = ret_data
        else:
            desc = u'\u4fee\u6539CPE\u652f\u6301\u7684TR069\u7248\u672c\u53f7\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def get_cpe_online_status(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\x8e\xb7\xe5\x8f\x96CPE\xe7\x9a\x84\xe5\x9c\xa8\xe7\xba\xbf\xe7\x8a\xb6\xe6\x80\x81
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a\xe6\x97\xa0
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e \xe5\x9c\xa8\xe7\xba\xbf\xe7\x8a\xb6\xe6\x80\x81;
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${online_status}  | Get Cpe Online Status |
        
        """
        ret_api = None
        ret_data = None
        ret_out = None
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        ret_api, ret_data = user1.get_rpc_methods()
        if ret_api == ERR_SUCCESS:
            ret_out = 'online'
        else:
            ret_out = 'offline'
            self._user_info('%s:%s' % (ret_out, ret_data))
        desc = u'\u5f53\u524dcpe\u72b6\u6001:%s' % ret_out
        self._user_info(desc)
        return ret_out

    def get_cpe_operator(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0: \xe8\x8e\xb7\xe5\x8f\x96\xe5\xbd\x93\xe5\x89\x8dcpe\xe7\x9a\x84\xe8\xbf\x90\xe8\x90\xa5\xe5\x95\x86\xe5\xb1\x9e\xe6\x80\xa7 
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a\xe7\xa9\xba
            
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e "CT"\xe8\xa1\xa8\xe7\xa4\xbaChina Telecom; \xe8\xbf\x94\xe5\x9b\x9e"CU"\xe8\xa1\xa8\xe7\xa4\xbaChina Unicom
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
        
        Example:
        |  ${cpe_operator}  |  Get Cpe Operator  |
        
        """
        ret = None
        ret_data = ''
        ret_out = ''
        desc = ''
        ret, ret_data = self._query_cpe_info()
        if ret == ERR_SUCCESS:
            ret_out = ret_data.cpe_operator
            desc = u'\u83b7\u53d6\u5f53\u524dcpe\u7684\u8fd0\u8425\u5546\u5c5e\u6027\u6210\u529f\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % ret_out
            self._user_info(desc)
        else:
            desc = u'%s' % ret_data
            desc = u'\u83b7\u53d6\u5f53\u524dcpe\u7684\u8fd0\u8425\u5546\u5c5e\u6027\u5931\u8d25\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % desc
            raise RuntimeError(desc)
        return ret_out

    def set_cpe_operator(self, operator = 'CT'):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\xae\xbe\xe7\xbd\xaecpe \xe8\xbf\x90\xe8\x90\xa5\xe5\x95\x86\xe5\xb1\x9e\xe6\x80\xa7
        
        \xe5\x8f\x82\xe6\x95\xb0:
            operator: "CT"\xe8\xa1\xa8\xe7\xa4\xbaChina Telecom;
                      "CU"\xe8\xa1\xa8\xe7\xa4\xbaChina Unicom;
                      "standard"\xe8\xa1\xa8\xe7\xa4\xba\xe6\xa0\x87\xe5\x87\x86TR069(\xe4\xb8\x8d\xe8\x83\xbd\xe6\x89\xa7\xe8\xa1\x8c\xe5\xb7\xa5\xe5\x8d\x95).
            
        Example:
        |  Set Cpe Operator  |  CT  |
        
        """
        ret = None
        d1 = dict()
        d1['cpe_operator'] = operator
        ret, ret_data = self._update_cpe_info(d1)
        if ret == ERR_SUCCESS:
            desc = u'\u8bbe\u7f6ecpe \u8fd0\u8425\u5546\u5c5e\u6027\u6210\u529f, \u65b0\u7684operator=%s' % operator
            self._user_info(desc)
        else:
            desc = u'\u8bbe\u7f6ecpe \u8fd0\u8425\u5546\u5c5e\u6027\u5931\u8d25, \u539f\u56e0\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return

    def get_cpe_rollback(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0: \xe8\x8e\xb7\xe5\x8f\x96\xe6\x9f\x90\xe5\xb7\xa5\xe5\x8d\x95\xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xe6\x98\xaf\xe5\x90\xa6\xe6\x89\xa7\xe8\xa1\x8c\xe5\x9b\x9e\xe6\xbb\x9a\xe6\x93\x8d\xe4\xbd\x9c\xe7\x9a\x84\xe6\xa0\x87\xe8\xaf\x86 
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a\xe7\xa9\xba
            
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e "True" \xe6\x88\x96\xe8\x80\x85 "False" (True\xe8\xa1\xa8\xe7\xa4\xba\xe5\xb7\xa5\xe5\x8d\x95\xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xe6\x97\xb6\xe8\xa6\x81\xe5\x9b\x9e\xe6\xbb\x9a);              
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
        
        Example:
        |  ${rollback}  |  Get Cpe Rollback  |
        
        """
        ret = None
        ret_data = ''
        ret_out = ''
        desc = ''
        ret, ret_data = self._query_cpe_info()
        if ret == ERR_SUCCESS:
            ret_out = ret_data.worklist_rollback
            desc = u'\u83b7\u53d6\u67d0\u5de5\u5355\u6267\u884c\u5931\u8d25\u662f\u5426\u6267\u884c\u56de\u6eda\u64cd\u4f5c\u7684\u6807\u8bc6\u6210\u529f\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % ret_out
            self._user_info(desc)
        else:
            desc = u'%s' % ret_data
            desc = u'\u83b7\u53d6\u67d0\u5de5\u5355\u6267\u884c\u5931\u8d25\u662f\u5426\u6267\u884c\u56de\u6eda\u64cd\u4f5c\u7684\u6807\u8bc6\u5931\u8d25\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % desc
            raise RuntimeError(desc)
        return ret_out

    def set_cpe_rollback(self, rollback = 'False'):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\xae\xbe\xe7\xbd\xaecpe\xe6\x89\xa7\xe8\xa1\x8c\xe5\xb7\xa5\xe5\x8d\x95\xe5\xa4\xb1\xe8\xb4\xa5\xe6\x97\xb6\xe6\x98\xaf\xe5\x90\xa6\xe5\x9b\x9e\xe6\xbb\x9a\xe7\x9a\x84\xe5\x8f\x82\xe6\x95\xb0
        
        \xe5\x8f\x82\xe6\x95\xb0:
            rollback: CPE\xe6\x89\xa7\xe8\xa1\x8c\xe5\xb7\xa5\xe5\x8d\x95\xe5\xa4\xb1\xe8\xb4\xa5\xe6\x97\xb6 \xe6\x98\xaf\xe5\x90\xa6\xe9\x9c\x80\xe8\xa6\x81\xe5\x9b\x9e\xe6\xbb\x9a/\xe5\x9b\x9e\xe9\x80\x80, True\xe8\xa1\xa8\xe7\xa4\xba\xe9\x9c\x80\xe8\xa6\x81;False\xe8\xa1\xa8\xe7\xa4\xba\xe4\xb8\x8d\xe9\x9c\x80\xe8\xa6\x81
            
        Example:
        |  Set Cpe Rollback  |  True  |        
        """
        ret = None
        d1 = dict()
        rollback = str(rollback)
        if rollback.lower() == 'true':
            rollback = True
        elif rollback.lower() == 'false':
            rollback = False
        else:
            desc = u'rollback\u53c2\u6570\u8f93\u5165\u9519\u8bef,\u8bf7\u68c0\u67e5'
            raise RuntimeError(desc)
        d1['worklist_rollback'] = rollback
        ret, ret_data = self._update_cpe_info(d1)
        return

    def get_cpe_device_type(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\x8e\xb7\xe5\x8f\x96CPE\xe7\x9a\x84 \xe8\xae\xbe\xe5\xa4\x87\xe7\xb1\xbb\xe5\x9e\x8b
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a\xe6\x97\xa0
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e CPE\xe7\x9a\x84 \xe8\xae\xbe\xe5\xa4\x87\xe7\xb1\xbb\xe5\x9e\x8b;
                \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8craise \xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf
                
        Example:
        | ${device type} | Get Cpe Device Type  |
        
        """
        ret = None
        ret_data = None
        ret_out = None
        ret, ret_data = self._query_cpe_info()
        if ret == ERR_SUCCESS:
            ret_out = ret_data.worklist_domain
            desc = u'\u83b7\u53d6CPE\u7684 \u8bbe\u5907\u7c7b\u578b\u6210\u529f, \u7ed3\u679c\u5982\u4e0b:%s' % ret_out
            self._user_info(desc)
        else:
            desc = u'\u83b7\u53d6CPE\u7684 \u8bbe\u5907\u7c7b\u578b\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def set_cpe_device_type(self, device_type):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\xae\xbe\xe7\xbd\xaeCPE\xe7\x9a\x84\xe8\xae\xbe\xe5\xa4\x87\xe7\xb1\xbb\xe5\x9e\x8b(\xe8\xae\xbe\xe5\xa4\x87\xe7\xb1\xbb\xe5\x9e\x8b\xe6\xa8\xa1\xe6\x9d\xbf)
        
        \xe5\x8f\x82\xe6\x95\xb0:
            device_type: CPE\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xb1\xbb\xe5\x9e\x8b, \xe4\xb8\xba\xe4\xba\x86\xe4\xbe\xbf\xe4\xba\x8e\xe6\x89\xa9\xe5\xb1\x95,\xe7\x9b\xae\xe5\x89\x8d\xe4\xb8\x8d\xe5\x81\x9a\xe5\x90\x88\xe6\xb3\x95\xe6\x80\xa7\xe5\x88\xa4\xe6\x96\xad,
            \xe4\xbd\x86\xe5\x9c\xa8\xe6\x89\xa7\xe8\xa1\x8c\xe5\xb7\xa5\xe5\x8d\x95\xe6\x97\xb6\xe5\xa6\x82\xe6\x9e\x9c\xe6\xb2\xa1\xe6\x9c\x89\xe6\x89\xbe\xe5\x88\xb0\xe7\x9b\xb8\xe5\xba\x94\xe7\x9a\x84\xe6\xa8\xa1\xe6\x9d\xbf\xe7\x9b\xae\xe5\xbd\x95,\xe5\x88\x99\xe4\xbc\x9a\xe5\xb7\xa5\xe5\x8d\x95\xe5\x87\xba\xe9\x94\x99.
            \xe6\x89\x80\xe4\xbb\xa5,\xe5\xbb\xba\xe8\xae\xae\xe8\xae\xbe\xe7\xbd\xae\xe4\xb8\xba\xe4\xbb\xa5\xe4\xb8\x8b\xe5\x87\xa0\xe4\xb8\xaa\xe5\x8f\x82\xe8\x80\x83\xe5\x80\xbc,\xe4\xb8\x8d\xe5\x8c\xba\xe5\x88\x86\xe5\xa4\xa7\xe5\xb0\x8f\xe5\x86\x99:
            | ADSL_2LAN | ADSL\xe4\xb8\x8a\xe8\xa1\x8c,\xe4\xba\x8cLAN\xe5\x8f\xa3  |
            | ADSL_4+1  | ADSL\xe4\xb8\x8a\xe8\xa1\x8c,\xe5\x9b\x9bLAN\xe5\x8f\xa3,\xe4\xb8\x80POST\xe5\x8f\xa3 |
            | ADSL_4LAN | ADSL\xe4\xb8\x8a\xe8\xa1\x8c,\xe5\x9b\x9bLAN\xe5\x8f\xa3 |
            | EPON_1+1  | EPON\xe4\xb8\x8a\xe8\xa1\x8c,\xe4\xb8\x80LAN\xe5\x8f\xa3,\xe4\xb8\x80POST\xe5\x8f\xa3 |
            | EPON_2+1  | EPON\xe4\xb8\x8a\xe8\xa1\x8c,\xe4\xba\x8cLAN\xe5\x8f\xa3,\xe4\xb8\x80POST\xe5\x8f\xa3 |
            | EPON_4+2  | EPON\xe4\xb8\x8a\xe8\xa1\x8c,\xe5\x9b\x9bLAN\xe5\x8f\xa3,\xe4\xba\x8cPOST\xe5\x8f\xa3 |
            | EPON_4LAN | EPON\xe4\xb8\x8a\xe8\xa1\x8c,\xe5\x9b\x9bLAN\xe5\x8f\xa3 |
            | GPON_1+1  | GPON\xe4\xb8\x8a\xe8\xa1\x8c,\xe4\xb8\x80LAN\xe5\x8f\xa3,\xe4\xb8\x80POST\xe5\x8f\xa3 |
            | GPON_2+1  | GPON\xe4\xb8\x8a\xe8\xa1\x8c,\xe4\xba\x8cLAN\xe5\x8f\xa3,\xe4\xb8\x80POST\xe5\x8f\xa3 |
            | GPON_4+2  | GPON\xe4\xb8\x8a\xe8\xa1\x8c,\xe5\x9b\x9bLAN\xe5\x8f\xa3,\xe4\xba\x8cPOST\xe5\x8f\xa3 |
            | GPON_4LAN | GPON\xe4\xb8\x8a\xe8\xa1\x8c,\xe5\x9b\x9bLAN\xe5\x8f\xa3 |
            | LAN_4+1   | LAN\xe4\xb8\x8a\xe8\xa1\x8c,\xe5\x9b\x9bLAN\xe5\x8f\xa3,\xe4\xb8\x80POST\xe5\x8f\xa3 |
            | LAN_4+2   | LAN\xe4\xb8\x8a\xe8\xa1\x8c,\xe5\x9b\x9bLAN\xe5\x8f\xa3,\xe4\xba\x8cPOST\xe5\x8f\xa3 |
            | LAN_4LAN  | LAN\xe4\xb8\x8a\xe8\xa1\x8c,\xe5\x9b\x9bLAN\xe5\x8f\xa3 |
            | VDSL_4+1  | VDSL\xe4\xb8\x8a\xe8\xa1\x8c,\xe5\x9b\x9bLAN\xe5\x8f\xa3,\xe4\xb8\x80POST\xe5\x8f\xa3 |
            | VDSL_4+2  | VDSL\xe4\xb8\x8a\xe8\xa1\x8c,\xe5\x9b\x9bLAN\xe5\x8f\xa3,\xe4\xba\x8cPOST\xe5\x8f\xa3 |
            | VDSL_4LAN | VDSL\xe4\xb8\x8a\xe8\xa1\x8c,\xe5\x9b\x9bLAN\xe5\x8f\xa3 |
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe6\x97\xa0\xe8\xbf\x94\xe5\x9b\x9e
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
               
        Example:
        |  Set Cpe Device Type  |  ADSL_4LAN  |        
        """
        ret = None
        d1 = {}
        device_type = device_type.upper()
        d1['worklist_domain'] = device_type
        ret, ret_data = self._update_cpe_info(d1)
        desc = u'\u8bbe\u7f6eCPE\u7684\u8bbe\u5907\u7c7b\u578b(\u8bbe\u5907\u7c7b\u578b\u6a21\u677f)\u6210\u529f, \u65b0\u7684device_type=%s' % device_type
        self._user_info(desc)
        return

    def get_last_faults(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\x8e\xb7\xe5\x8f\x96\xe5\xbd\x93\xe5\x89\x8dcpe\xe4\xb8\x8a\xe4\xb8\x80\xe6\xac\xa1rpc\xe8\xaf\xb7\xe6\xb1\x82\xe7\x9a\x84\xe9\x94\x99\xe8\xaf\xaf\xe4\xbb\xa3\xe7\xa0\x81\xe5\x92\x8c\xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf, 
                \xe5\xa6\x82\xe6\x9e\x9c\xe4\xb8\x8a\xe4\xb8\x80\xe4\xb8\xaarpc\xe6\x98\xaf\xe6\xad\xa3\xe5\xb8\xb8\xe7\x9a\x84\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xe4\xb8\xba[];
                \xe5\xa6\x82\xe6\x9e\x9c\xe4\xb8\x8a\xe4\xb8\x80\xe4\xb8\xaarpc\xe6\x98\xaf\xe9\x94\x99\xe8\xaf\xaf\xe7\x9a\x84\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe9\x94\x99\xe8\xaf\xaf\xe5\x88\x97\xe8\xa1\xa8.
        
        \xe5\x8f\x82\xe6\x95\xb0: \xe6\x97\xa0
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x88\x90\xe5\x8a\x9f,\xe8\xbf\x94\xe5\x9b\x9e\xe9\x94\x99\xe8\xaf\xaf\xe4\xbb\xa3\xe7\xa0\x81\xe5\x92\x8c\xe9\x94\x99\xe8\xaf\xaf\xe4\xbf\xa1\xe6\x81\xaf\xe7\x9a\x84\xe5\x88\x97\xe8\xa1\xa8\xe3\x80\x82
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
        
        Example:
        | ${faultinfolist} | Get Last Faults  |
        """
        ret_api = ERR_FAIL
        ret_data = ''
        ret_obj = None
        ret_out = ''
        sn = self._get_sn()
        ret_api, ret_data = user.query_cpe_last_faults(sn)
        if ret_api == ERR_SUCCESS:
            ret_obj = ret_data
            ret_out = eval(ret_obj.dict_ret['str_result'])
            desc = u'\u83b7\u53d6\u5f53\u524dCPE\u4e0a\u4e00\u6b21rpc\u8bf7\u6c42\u7684\u9519\u8bef\u4ee3\u7801\u548c\u9519\u8bef\u4fe1\u606f\u6210\u529f\u3002'
            self._user_info(desc)
        else:
            desc = u'\u83b7\u53d6\u5f53\u524dCPE\u4e0a\u4e00\u6b21rpc\u8bf7\u6c42\u7684\u9519\u8bef\u4ee3\u7801\u548c\u9519\u8bef\u4fe1\u606f\u5931\u8d25, \u8be6\u7ec6\u4fe1\u606f\u4e3a: %s:' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def manual_get_connection_request(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe6\x89\x8b\xe5\x8a\xa8\xe5\x90\x91CPE\xe5\x8f\x91\xe8\xb5\xb7\xe4\xb8\x80\xe4\xb8\xaa\xe5\x8f\x8d\xe5\x90\x91\xe8\xbf\x9e\xe6\x8e\xa5\xe8\xaf\xb7\xe6\xb1\x82, 
                \xe6\x88\x90\xe5\x8a\x9f, \xe9\x80\x9a\xe8\xbf\x87\xe6\x8a\x93\xe5\x8c\x85, CPE\xe4\xbc\x9a\xe5\x9b\x9e\xe4\xb8\x80\xe4\xb8\xaa "6 CONNECTION REQUEST"\xe7\x9a\x84inform; 
                \xe5\xa4\xb1\xe8\xb4\xa5, CPE\xe6\x97\xa0\xe5\x93\x8d\xe5\xba\x94.        
        
        \xe5\x8f\x82\xe6\x95\xb0: \xe6\x97\xa0
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x97\xa0
        
        Example:
        |  Manual Get Connection Request  |
        """
        ret_api = ERR_FAIL
        ret_data = ''
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        ret_api, ret_data = user1.connection_request()
        if ret_api == ERR_SUCCESS:
            desc = u'\u624b\u52a8\u5411CPE\u53d1\u8d77\u4e00\u4e2a\u53cd\u5411\u8fde\u63a5\u8bf7\u6c42\u6210\u529f\u3002'
            self._user_info(desc)
        else:
            desc = u'\u624b\u52a8\u5411CPE\u53d1\u8d77\u4e00\u4e2a\u53cd\u5411\u8fde\u63a5\u8bf7\u6c42\u5931\u8d25, \u8be6\u7ec6\u4fe1\u606f\u4e3a: %s:' % ret_data
            raise RuntimeError(desc)
        return None

    def set_cpe_interface_version(self, interface_version = 'AUTO'):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\xae\xbe\xe7\xbd\xaeCPE\xe6\x94\xaf\xe6\x8c\x81\xe7\x9a\x84 \xe8\xa7\x84\xe8\x8c\x83\xe7\x89\x88\xe6\x9c\xac\xe5\x8f\xb7
        
        \xe5\x8f\x82\xe6\x95\xb0:
            interface_version: CPE\xe6\x94\xaf\xe6\x8c\x81\xe7\x9a\x84 \xe8\xa7\x84\xe8\x8c\x83\xe7\x89\x88\xe6\x9c\xac\xe5\x8f\xb7.
            | v3.0 | \xe6\x94\xaf\xe6\x8c\x81\xe7\x9a\x84\xe6\x8e\xa5\xe5\x8f\xa3\xe8\xa7\x84\xe8\x8c\x83\xe4\xb8\xba v3.0  |
            | v4.0 | \xe6\x94\xaf\xe6\x8c\x81\xe7\x9a\x84\xe6\x8e\xa5\xe5\x8f\xa3\xe8\xa7\x84\xe8\x8c\x83\xe4\xb8\xba v4.0  |
            | AUTO | \xe9\xbb\x98\xe8\xae\xa4\xe5\x8f\x96\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe6\x94\xaf\xe6\x8c\x81\xe7\x9a\x84\xe7\x89\x88\xe6\x9c\xac\xe7\xb3\xbb\xe5\x88\x97\xe4\xb8\xad\xe7\x9a\x84\xe6\x9c\x80\xe5\xb0\x8f\xe7\x89\x88\xe6\x9c\xac |            
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe6\x97\xa0\xe8\xbf\x94\xe5\x9b\x9e
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
               
        Example:
        |  Set Cpe Interface Version  |  AUTO  |        
        """
        ret_api = ERR_FAIL
        ret_data = ''
        ret_obj = None
        ret_out = ''
        desc = ''
        sn = self._get_sn()
        user1 = user.UserRpc(sn)
        interface_version = interface_version.lower()
        d1 = {}
        d1['interface_version'] = interface_version
        ret, ret_data = self._update_cpe_info(d1)
        if ret == ERR_SUCCESS:
            desc = u'\u8bbe\u7f6eCPE\u652f\u6301\u7684 \u89c4\u8303\u7248\u672c\u53f7 \u6210\u529f, \u65b0\u7684 interface_version=%s' % interface_version
            self._user_info(desc)
        else:
            desc = u'\u8bbe\u7f6ecpe \u89c4\u8303\u7248\u672c\u53f7 \u5931\u8d25, \u539f\u56e0\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return

    def get_cpe_interface_version(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe8\x8e\xb7\xe5\x8f\x96CPE\xe6\x94\xaf\xe6\x8c\x81\xe7\x9a\x84 \xe8\xa7\x84\xe8\x8c\x83\xe7\x89\x88\xe6\x9c\xac\xe5\x8f\xb7
        
        \xe5\x8f\x82\xe6\x95\xb0: \xe6\x97\xa0
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe6\x97\xa0\xe8\xbf\x94\xe5\x9b\x9e
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
               
        Example:
        |  ${interface version}  |  Get Cpe Interface Version  |        
        """
        ret_api = ERR_FAIL
        ret_data = ''
        ret_obj = None
        ret_out = ''
        sn = self._get_sn()
        ret_api, ret_data = user.query_cpe_interface_version(sn)
        if ret_api == ERR_SUCCESS:
            ret_obj = ret_data
            ret_out = ret_obj.dict_ret['str_result']
            desc = u'\u83b7\u53d6CPE\u652f\u6301\u7684 \u89c4\u8303\u7248\u672c\u53f7 \u6210\u529f\u3002'
            self._user_info(desc)
        else:
            desc = u'\u83b7\u53d6CPE\u652f\u6301\u7684 \u89c4\u8303\u7248\u672c\u53f7 \u5931\u8d25, \u8be6\u7ec6\u4fe1\u606f\u4e3a: %s:' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def _download_worklist(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe5\x9c\xa8\xe5\xb7\xa5\xe5\x8d\x95\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe4\xb8\x8a\xe6\x9f\xa5\xe8\xaf\xa2\xe5\xb7\xa5\xe5\x8d\x95\xe7\x9b\xb8\xe5\x85\xb3\xe7\x9a\x84\xe6\x89\x80\xe6\x9c\x89\xe4\xbf\xa1\xe6\x81\xaf\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe5\xbd\x93\xe5\x89\x8d\xe6\x94\xaf\xe6\x8c\x81\xe7\x9a\x84\xe6\x89\x80\xe6\x9c\x89\xe5\xb7\xa5\xe5\x8d\x95
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a\xe6\x97\xa0
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x88\x90\xe5\x8a\x9f \xe8\xbf\x94\xe5\x9b\x9e\xe6\x89\x80\xe6\x9c\x89\xe5\xb7\xa5\xe5\x8d\x95\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe4\xb8\x8a\xe6\x94\xaf\xe6\x8c\x81\xe7\x9a\x84\xe4\xb8\x9a\xe5\x8a\xa1\xe8\x84\x9a\xe6\x9c\xac\xe9\x9b\x86\xe5\x90\x88 
        
        Example:
        |  Download Worklist  |                 
        """
        ret_api = ERR_FAIL
        ret_data = ''
        obj = user.UserWorklist()
        ret_api, ret_data = obj.worklistprocess_download()
        if ret_api == ERR_SUCCESS:
            desc = u'\u4e0b\u8f7d\u5de5\u5355\u4fe1\u606f\u6210\u529f\u3002'
            self._user_info(desc)
        else:
            desc = u'\u4e0b\u8f7d\u5de5\u5355\u4fe1\u606f\u5931\u8d25\uff0c\u7ed3\u679c\u5982\u4e0b%s:' % ret_data
            raise RuntimeError(desc)
        return ret_data

    def _get_worklist_record(self, obj_database):
        """
        obj_database = MsgWorklist
        """
        desc = '\n        \nid=%s\nworklist_name=%s\nsn=%s\ncpe device type=%s\ntype=%s\nusername=%s\nuserid=%s\nstatus=%s\nrollback=%s\ndict_data=%s\ntime_build=%s\ntime_bind=%s\ntime_reserve=%s\ntime_exec_start=%s\ntime_exec_end=%s\n\n    ' % (obj_database.id_,
         obj_database.worklist_name,
         obj_database.sn,
         obj_database.domain,
         obj_database.type_,
         obj_database.username,
         obj_database.userid,
         obj_database.status,
         obj_database.rollback,
         obj_database.dict_data,
         obj_database.time_build,
         obj_database.time_bind,
         obj_database.time_reserve,
         obj_database.time_exec_start,
         obj_database.time_exec_end)
        return desc

    def get_worklist_name(self, worklist_id):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0: \xe8\x8e\xb7\xe5\x8f\x96\xe6\x9f\x90\xe5\xb7\xa5\xe5\x8d\x95\xe7\x9a\x84\xe5\x90\x8d\xe5\xad\x97
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
            worklist_id: \xe9\x9c\x80\xe8\xa6\x81\xe6\x9f\xa5\xe8\xaf\xa2\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95id
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x88\x90\xe5\x8a\x9f,\xe8\xbf\x94\xe5\x9b\x9e\xe5\xb7\xa5\xe5\x8d\x95\xe5\x90\x8d\xe5\xad\x97;
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
        
        Example:
        |  ${worklist_name}  |  Get Worklist Name  |  ID_1364950237391  |
        
        """
        ret_api = ERR_FAIL
        ret_data = ''
        ret_obj = None
        ret_out = ''
        desc = ''
        obj = user.UserWorklist()
        dict_data = {}
        dict_data['id_'] = worklist_id
        ret_api, ret_data = obj.worklistprocess_query(**dict_data)
        if ret_api == ERR_SUCCESS:
            ret_obj = ret_data
            ret_out = ret_obj.worklist_name
            desc = u'\u83b7\u53d6\u67d0\u5de5\u5355\u7684\u540d\u5b57\u6210\u529f\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % ret_out
            self._user_info(desc)
        else:
            desc = u'%s' % ret_data
            desc = u'\u83b7\u53d6\u67d0\u5de5\u5355\u7684\u540d\u5b57\u5931\u8d25\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % desc
            raise RuntimeError(desc)
        return ret_out

    def get_worklist_bind_cpe_sn(self, worklist_id):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0: \xe8\x8e\xb7\xe5\x8f\x96\xe6\x9f\x90\xe5\xb7\xa5\xe5\x8d\x95\xe7\xbb\x91\xe5\xae\x9a\xe7\x9a\x84CPE oui-sn
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
            worklist_id: \xe9\x9c\x80\xe8\xa6\x81\xe6\x9f\xa5\xe8\xaf\xa2\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95id
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x88\x90\xe5\x8a\x9f,\xe8\xbf\x94\xe5\x9b\x9e\xe5\xb7\xa5\xe5\x8d\x95\xe7\xbb\x91\xe5\xae\x9a\xe7\x9a\x84CPE oui-sn;
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
                
        Example:
        |  ${sn}  |  Get Worklist Bind Cpe Sn  |  ID_1364950237391  |
        
        """
        ret_api = ERR_FAIL
        ret_data = ''
        ret_obj = None
        ret_out = ''
        desc = ''
        obj = user.UserWorklist()
        dict_data = {}
        dict_data['id_'] = worklist_id
        ret_api, ret_data = obj.worklistprocess_query(**dict_data)
        if ret_api == ERR_SUCCESS:
            ret_obj = ret_data
            ret_out = ret_obj.sn
            desc = u'\u83b7\u53d6\u67d0\u5de5\u5355\u7ed1\u5b9a\u7684CPE oui-sn\u6210\u529f\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % ret_out
            self._user_info(desc)
        else:
            desc = u'%s' % ret_data
            desc = u'\u83b7\u53d6\u67d0\u5de5\u5355\u7ed1\u5b9a\u7684CPE oui-sn\u5931\u8d25\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % desc
            raise RuntimeError(desc)
        return ret_out

    def get_worklist_bind_cpe_device_type(self, worklist_id):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0: \xe8\x8e\xb7\xe5\x8f\x96\xe6\x9f\x90\xe5\xb7\xa5\xe5\x8d\x95\xe7\xbb\x91\xe5\xae\x9a\xe7\x9a\x84CPE Device Type
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
            worklist_id: \xe9\x9c\x80\xe8\xa6\x81\xe6\x9f\xa5\xe8\xaf\xa2\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95id
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x88\x90\xe5\x8a\x9f,\xe8\xbf\x94\xe5\x9b\x9e\xe5\xb7\xa5\xe5\x8d\x95\xe7\xbb\x91\xe5\xae\x9a\xe7\x9a\x84CPE Device Type;
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
                
        Example:
        |  ${cpe_device_type}  |  Get Worklist Bind Cpe Device Type  |  ID_1364950237391  |
        
        """
        ret_api = ERR_FAIL
        ret_data = ''
        ret_obj = None
        ret_out = ''
        desc = ''
        obj = user.UserWorklist()
        dict_data = {}
        dict_data['id_'] = worklist_id
        ret_api, ret_data = obj.worklistprocess_query(**dict_data)
        if ret_api == ERR_SUCCESS:
            ret_obj = ret_data
            ret_out = ret_obj.domain
            desc = u'\u83b7\u53d6\u67d0\u5de5\u5355\u7ed1\u5b9a\u7684CPE Device Type\u6210\u529f\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % ret_out
            self._user_info(desc)
        else:
            desc = u'%s' % ret_data
            desc = u'\u83b7\u53d6\u67d0\u5de5\u5355\u7ed1\u5b9a\u7684CPE Device Type\u5931\u8d25\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % desc
            raise RuntimeError(desc)
        return ret_out

    def get_worklist_type(self, worklist_id):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0: \xe8\x8e\xb7\xe5\x8f\x96\xe6\x9f\x90\xe5\xb7\xa5\xe5\x8d\x95\xe7\x9a\x84\xe7\xb1\xbb\xe5\x9e\x8b
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
            worklist_id: \xe9\x9c\x80\xe8\xa6\x81\xe6\x9f\xa5\xe8\xaf\xa2\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95id
            
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x88\x90\xe5\x8a\x9f,\xe8\xbf\x94\xe5\x9b\x9e\xe5\xb7\xa5\xe5\x8d\x95\xe7\x9a\x84\xe7\xb1\xbb\xe5\x9e\x8b;
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
                
        Example:
        |  ${worklist_type}  |  Get Worklist Type  |  ID_1364950237391  |
        
        """
        ret_api = ERR_FAIL
        ret_data = ''
        ret_obj = None
        ret_out = ''
        desc = ''
        obj = user.UserWorklist()
        dict_data = {}
        dict_data['id_'] = worklist_id
        ret_api, ret_data = obj.worklistprocess_query(**dict_data)
        if ret_api == ERR_SUCCESS:
            ret_obj = ret_data
            ret_out = ret_obj.type_
            desc = u'\u83b7\u53d6\u67d0\u5de5\u5355\u7684\u7c7b\u578b\u6210\u529f\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % ret_out
            self._user_info(desc)
        else:
            desc = u'%s' % ret_data
            desc = u'\u83b7\u53d6\u67d0\u5de5\u5355\u7684\u7c7b\u578b\u5931\u8d25\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % desc
            raise RuntimeError(desc)
        return ret_out

    def get_worklist_userinfo(self, worklist_id):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0: \xe8\x8e\xb7\xe5\x8f\x96\xe6\x9f\x90\xe5\xb7\xa5\xe5\x8d\x95\xe7\x9a\x84\xe7\x94\xa8\xe6\x88\xb7\xe4\xbf\xa1\xe6\x81\xaf        
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
            worklist_id: \xe9\x9c\x80\xe8\xa6\x81\xe6\x9f\xa5\xe8\xaf\xa2\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95id
            
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e(username, userid);
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
        
        Example:
        |  ${username}  |  ${userid}  |  Get Worklist Userinfo  |  ID_1364950237391  |
        
        \xe6\xb3\xa8\xe6\x84\x8f\xef\xbc\x9a\xe8\xbf\x99\xe9\x87\x8c\xe7\x9a\x84username\xe5\x92\x8cid,\xe6\x98\xaf\xe6\x8c\x87\xe6\x89\xa7\xe8\xa1\x8c\xe9\x80\xbb\xe8\xbe\x91\xe5\xb7\xa5\xe5\x8d\x95\xe6\x97\xb6\xe7\x9a\x84username\xe5\x92\x8cid\xe3\x80\x82
        
        """
        ret_api = ERR_FAIL
        ret_data = ''
        ret_obj = None
        ret_out = ''
        desc = ''
        obj = user.UserWorklist()
        dict_data = {}
        dict_data['id_'] = worklist_id
        ret_api, ret_data = obj.worklistprocess_query(**dict_data)
        if ret_api == ERR_SUCCESS:
            ret_obj = ret_data
            ret_out = (ret_obj.username, ret_obj.userid)
            desc = u'\u83b7\u53d6\u67d0\u5de5\u5355\u7684\u7528\u6237\u4fe1\u606f\u6210\u529f\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % str(ret_out)
            self._user_info(desc)
        else:
            desc = u'%s' % ret_data
            desc = u'\u83b7\u53d6\u67d0\u5de5\u5355\u7684\u7528\u6237\u4fe1\u606f\u5931\u8d25\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % desc
            raise RuntimeError(desc)
        return ret_out

    def get_worklist_status(self, worklist_id):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0: \xe6\x9f\xa5\xe8\xaf\xa2\xe6\x9f\x90\xe5\xb7\xa5\xe5\x8d\x95\xe7\x9a\x84\xe7\x8a\xb6\xe6\x80\x81
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
            worklist_id: \xe9\x9c\x80\xe8\xa6\x81\xe6\x9f\xa5\xe8\xaf\xa2\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95id
            
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe5\xb7\xa5\xe5\x8d\x95\xe7\x9a\x84\xe7\x8a\xb6\xe6\x80\x81;
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
        
        Example:
        |  ${status}  |  Get Worklist Status  |  ID_1364950237391  |
        
        """
        ret_api = ERR_FAIL
        ret_data = ''
        ret_obj = None
        ret_out = ''
        desc = ''
        obj = user.UserWorklist()
        dict_data = {}
        dict_data['id_'] = worklist_id
        ret_api, ret_data = obj.worklistprocess_query(**dict_data)
        if ret_api == ERR_SUCCESS:
            ret_obj = ret_data
            ret_out = ret_obj.status
            desc = u'\u67e5\u8be2\u67d0\u5de5\u5355\u7684\u72b6\u6001\u6210\u529f\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % ret_out
            self._user_info(desc)
        else:
            desc = u'%s' % ret_data
            desc = u'\u67e5\u8be2\u67d0\u5de5\u5355\u7684\u72b6\u6001\u5931\u8d25\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % desc
            raise RuntimeError(desc)
        return ret_out

    def get_worklist_args(self, worklist_id):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0: \xe8\x8e\xb7\xe5\x8f\x96\xe6\x9f\x90\xe5\xb7\xa5\xe5\x8d\x95\xe7\x9a\x84\xe9\x85\x8d\xe7\xbd\xae\xe5\x8f\x82\xe6\x95\xb0
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
            worklist_id: \xe9\x9c\x80\xe8\xa6\x81\xe6\x9f\xa5\xe8\xaf\xa2\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95id
            
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe5\xb7\xa5\xe5\x8d\x95\xe7\x9a\x84\xe9\x85\x8d\xe7\xbd\xae\xe5\x8f\x82\xe6\x95\xb0(\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2\xe7\xb1\xbb\xe5\x9e\x8b);
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
        
        Example:
        |  ${args}  |  Get Worklist Args  |  ID_1364950237391  |
        
        """
        ret_api = ERR_FAIL
        ret_data = ''
        ret_obj = None
        ret_out = ''
        desc = ''
        obj = user.UserWorklist()
        dict_data = {}
        dict_data['id_'] = worklist_id
        ret_api, ret_data = obj.worklistprocess_query(**dict_data)
        if ret_api == ERR_SUCCESS:
            ret_obj = ret_data
            ret_out = str(ret_obj.dict_data)
            desc = u'\u83b7\u53d6\u67d0\u5de5\u5355\u7684\u914d\u7f6e\u53c2\u6570\u6210\u529f\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % ret_out
            self._user_info(desc)
        else:
            desc = u'%s' % ret_data
            desc = u'\u83b7\u53d6\u67d0\u5de5\u5355\u7684\u914d\u7f6e\u53c2\u6570\u5931\u8d25\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % desc
            raise RuntimeError(desc)
        return ret_out

    def get_worklist_times(self, worklist_id):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0: \xe8\x8e\xb7\xe5\x8f\x96\xe6\x9f\x90\xe5\xb7\xa5\xe5\x8d\x95\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4\xe8\xae\xb0\xe5\xbd\x95\xe4\xbf\xa1\xe6\x81\xaf
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
            worklist_id: \xe9\x9c\x80\xe8\xa6\x81\xe6\x9f\xa5\xe8\xaf\xa2\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95id
            
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e(build\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4, bind\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4, \xe5\xb7\xa5\xe5\x8d\x95\xe6\x89\xa7\xe8\xa1\x8c\xe5\xbc\x80\xe5\xa7\x8b\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4, \xe6\x89\xa7\xe8\xa1\x8c\xe7\xbb\x93\xe6\x9d\x9f\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4);
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
        
        Example:
        |  ${build_time}  |  ${bind_time}  |  ${start_exec_time}  |  ${end_exec_time}  |  Get Worklist Times  |  ID_1364950237391  |
        
        """
        ret_api = ERR_FAIL
        ret_data = ''
        ret_obj = None
        ret_out = ''
        desc = ''
        obj = user.UserWorklist()
        dict_data = {}
        dict_data['id_'] = worklist_id
        ret_api, ret_data = obj.worklistprocess_query(**dict_data)
        if ret_api == ERR_SUCCESS:
            ret_obj = ret_data
            ret_out = (ret_obj.time_build,
             ret_obj.time_bind,
             ret_obj.time_exec_start,
             ret_obj.time_exec_end)
            desc = u'\u83b7\u53d6\u67d0\u5de5\u5355\u7684\u65f6\u95f4\u8bb0\u5f55\u4fe1\u606f\u6210\u529f\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % str(ret_out)
            self._user_info(desc)
        else:
            desc = u'%s' % ret_data
            desc = u'\u83b7\u53d6\u67d0\u5de5\u5355\u7684\u65f6\u95f4\u8bb0\u5f55\u4fe1\u606f\u5931\u8d25\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % desc
            raise RuntimeError(desc)
        return ret_out

    def get_worklist_logs(self, worklist_id):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0: \xe8\x8e\xb7\xe5\x8f\x96\xe6\x9f\x90\xe5\xb7\xa5\xe5\x8d\x95\xe6\x89\xa7\xe8\xa1\x8c\xe8\xbf\x87\xe7\xa8\x8b\xe6\x97\xa5\xe5\xbf\x97.
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
            worklist_id: \xe9\x9c\x80\xe8\xa6\x81\xe6\x9f\xa5\xe8\xaf\xa2\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95id
            
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe5\xb7\xa5\xe5\x8d\x95\xe7\x9a\x84\xe8\xbf\x87\xe7\xa8\x8b\xe6\x97\xa5\xe5\xbf\x97;
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
        
        Example:
        |  ${dict_data}  |  Get Worklist Logs  |  ID_1364950237391  |
        
        """
        ret_api = ERR_FAIL
        ret_data = ''
        ret_obj = None
        ret_out = ''
        desc = ''
        obj = user.UserWorklist()
        dict_data = {}
        dict_data['id_'] = worklist_id
        ret_api, ret_data = obj.worklistprocess_query(**dict_data)
        if ret_api == ERR_SUCCESS:
            ret_obj = ret_data
            ret_status = ret_obj.status
            if ret_status not in ('fail', 'success'):
                desc = u'\u5de5\u5355\u7684\u5f53\u524d\u72b6\u6001(%s)\u4e3a\u975e\u7ed3\u675f\u72b6\u6001,\u4e0d\u652f\u6301\u5bf9\u5176\u67e5\u8be2\u6d4b\u8bd5\u7ed3\u679c\u65e5\u5fd7' % ret_status
                self._user_info(desc)
                return
            ret_out = ret_obj.dict_ret
            ret_out = ret_out['str_result']
            desc = u'\u83b7\u53d6\u67d0\u5de5\u5355\u6267\u884c\u8fc7\u7a0b\u65e5\u5fd7\u6210\u529f\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % ret_out
            self._user_info(desc)
        else:
            desc = u'%s' % ret_data
            desc = u'\u83b7\u53d6\u67d0\u5de5\u5355\u6267\u884c\u8fc7\u7a0b\u65e5\u5fd7\u5931\u8d25\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % desc
            raise RuntimeError(desc)
        return ret_out

    def get_telecom_account_password(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0: \xe8\x8e\xb7\xe5\x8f\x96\xe7\xbb\xb4\xe6\x8a\xa4\xe5\xb8\x90\xe5\x8f\xb7\xe5\xaf\x86\xe7\xa0\x81
        
        \xe5\x8f\x82\xe6\x95\xb0:\xe6\x97\xa0
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe7\xbb\xb4\xe6\x8a\xa4\xe5\xaf\x86\xe7\xa0\x81(WEB\xe9\xa1\xb5\xe9\x9d\xa2\xe7\x99\xbb\xe5\xbd\x95\xe5\xaf\x86\xe7\xa0\x81);
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
                
        Example:
        |  ${password}  |  Get Telecom Account Password  |
        
        """
        ret_api = ERR_FAIL
        dict_args = {}
        ret_out = ''
        sn = self._get_sn()
        id_ = self._init_worklist('Auto_GetTelecomAccountPassword', str(dict_args), 'SYS')
        self.bind_physic_worklist(id_, sn)
        self.execute_worklist(id_)
        ret_out = self.get_worklist_logs(id_)
        return ret_out

    def _init_worklist(self, worklist_name, str_dict_args, group = 'SYS'):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe9\x9c\x80\xe8\xa6\x81\xe6\x89\xa7\xe8\xa1\x8c\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95\xe5\x8f\x82\xe6\x95\xb0
        
        \xe5\x8f\x82\xe6\x95\xb0:
            worklist_name: \xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe9\x9c\x80\xe8\xa6\x81\xe6\x89\xa7\xe8\xa1\x8c\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95\xe5\x90\x8d\xe5\xad\x97;
            str_dict_args: \xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe9\x9c\x80\xe8\xa6\x81\xe6\x89\xa7\xe8\xa1\x8c\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95\xe5\x8f\x82\xe6\x95\xb0
            group       :   "USER" or "SYS"
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe5\xb7\xa5\xe5\x8d\x95ID\xe5\x8f\xb7
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
               
        Example:
        |  ${id}  |  Init Worklist  |  WLAN_ADD  |  {"Num":("4", "1")}  |
        
        \xe6\xb3\xa8\xe6\x84\x8f:\xe6\xad\xa4\xe5\x85\xb3\xe9\x94\xae\xe5\xad\x97\xe6\x98\xaf\xe4\xb8\xba\xe4\xbb\xa5\xe5\x90\x8e\xe6\x89\xa9\xe5\xb1\x95\xe7\x94\xa8\xe6\x88\xb7\xe8\x87\xaa\xe5\xae\x9a\xe4\xb9\x89\xe5\xb7\xa5\xe5\x8d\x95\xe7\x94\xa8,\xe6\x9a\x82\xe6\x97\xb6\xe4\xb8\x8d\xe5\xbb\xba\xe8\xae\xae\xe7\x94\xa8\xe6\x88\xb7\xe4\xbd\xbf\xe7\x94\xa8.
        """
        ret_api = ERR_FAIL
        ret_data = ''
        ret_obj = None
        ret_out = ''
        desc = ''
        obj = user.UserWorklist()
        dict_data = {}
        dict_data['worklist_name'] = worklist_name
        dict_data['dict_data'] = eval(str_dict_args)
        dict_data['group'] = group
        ret_api, ret_data = obj.worklistprocess_build(**dict_data)
        if ret_api == ERR_SUCCESS:
            ret_obj = ret_data
            ret_out = ret_obj.id_
            desc = u'%s' % ret_out
            desc = u'\u521d\u59cb\u5316\u5de5\u5355(%s)\u6210\u529f\uff0c\u8fd4\u56de\u5de5\u5355\u5e8f\u53f7:%s' % (worklist_name, desc)
            self._user_info(desc)
        else:
            desc = u'%s' % ret_data
            desc = u'\u521d\u59cb\u5316\u5de5\u5355(%s)\u5931\u8d25\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % (worklist_name, desc)
            raise RuntimeError(desc)
        return ret_out

    def init_worklist(self, worklist_name, *args):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe9\x9c\x80\xe8\xa6\x81\xe6\x89\xa7\xe8\xa1\x8c\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95\xe5\x8f\x82\xe6\x95\xb0
        
        \xe5\x8f\x82\xe6\x95\xb0:
            worklist_name: \xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe9\x9c\x80\xe8\xa6\x81\xe6\x89\xa7\xe8\xa1\x8c\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95\xe5\x90\x8d\xe5\xad\x97;
            args:          \xe8\xa1\xa8\xe7\xa4\xba\xe5\x8f\xaf\xe9\x80\x89\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe4\xbc\xa0\xe5\x85\xa5\xe7\x9a\x84\xe6\xa0\xbc\xe5\xbc\x8f\xe4\xb8\xba"varname=value",\xe5\x85\xb7\xe4\xbd\x93\xe5\x8f\x82\xe6\x95\xb0\xe6\x8f\x8f\xe8\xbf\xb0\xe5\xa6\x82\xe4\xb8\x8b;
        
        *\xe6\xb3\xa8\xef\xbc\x9a\xe5\xbd\x93\xe7\x94\xa8\xe6\x88\xb7\xe4\xb8\x8d\xe8\xbe\x93\xe5\x85\xa5\xe6\x97\xb6\xe4\xbd\xbf\xe7\x94\xa8\xe6\xa8\xa1\xe6\x9d\xbf\xe4\xb8\xad\xe7\x9a\x84\xe9\xbb\x98\xe8\xae\xa4\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8cargs\xe6\x94\xaf\xe6\x8c\x81\xe5\x8d\x95\xe4\xb8\xaa\xe8\xbe\x93\xe5\x85\xa5\xe5\x8d\x95\xe4\xb8\xaa\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8c\xe4\xbd\x86\xe5\xbf\x85\xe9\xa1\xbb\xe8\xa6\x81\xe6\x8c\x89\xe5\x8f\x82\xe6\x95\xb0\xe9\xa1\xba\xe5\xba\x8f\xe8\xbe\x93\xe5\x85\xa5\xef\xbc\x8c\xe5\xbb\xba\xe8\xae\xae\xe4\xbd\xbf\xe7\x94\xa8"varname=value"\xe6\xa0\xbc\xe5\xbc\x8f\xef\xbc\x9b
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe5\xb7\xa5\xe5\x8d\x95ID\xe5\x8f\xb7
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
               
        Example:
        
        |  ${id}  |  Init Worklist  |  QoS_IP  |
        |  ${id}  |  Init Worklist  |  QoS_IP  | Min=222.66.65.57 | DSCPMarkValue=2 | M802_1_P_Value=2 |ClassQueue=1 |
        |  ${id}  |  Init Worklist  |  QoS_IP  | 222.66.65.57 | DSCPMarkValue=2 | M802_1_P_Value=2 |ClassQueue=1 |
        |  ${id}  |  Init Worklist  |  QoS_IP  | 222.66.65.57 |  | ClassQueue=1 | 2 |
        
        """
        ret_api = ERR_FAIL
        ret_data = ''
        ret_obj = None
        ret_out = ''
        desc = ''
        obj = user.UserWorklist()
        dict_data = {}
        dict_data['worklist_name'] = worklist_name
        if len(args) == 1:
            try:
                temp_data = eval(args[0])
                if isinstance(temp_data, dict):
                    dict_data['dict_data'] = temp_data
                else:
                    dict_data['dict_data'] = self._convert_worklist_args(args)
            except Exception:
                dict_data['dict_data'] = self._convert_worklist_args(args)

        else:
            dict_data['dict_data'] = self._convert_worklist_args(args)
        ret_api, ret_data = obj.worklistprocess_build(**dict_data)
        if ret_api == ERR_SUCCESS:
            ret_obj = ret_data
            ret_out = ret_obj.id_
            desc = u'%s' % ret_out
            desc = u'\u521d\u59cb\u5316\u5de5\u5355(%s)\u6210\u529f\uff0c\u8fd4\u56de\u5de5\u5355\u5e8f\u53f7:%s' % (worklist_name, desc)
            self._user_info(desc)
        else:
            desc = u'%s' % ret_data
            desc = u'\u521d\u59cb\u5316\u5de5\u5355(%s)\u5931\u8d25\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % (worklist_name, desc)
            raise RuntimeError(desc)
        return ret_out

    def bind_physic_worklist(self, worklist_id, sn = ''):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe7\xbb\x91\xe5\xae\x9a\xe7\x89\xa9\xe7\x90\x86\xe5\xb7\xa5\xe5\x8d\x95 
        
        \xe5\x8f\x82\xe6\x95\xb0:
            worklist_id: \xe9\x9c\x80\xe8\xa6\x81\xe7\xbb\x91\xe5\xae\x9a\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95id;
            sn: cpe\xe7\x9a\x84oui-sn\xef\xbc\x8c\xe4\xb8\xba\xe7\xa9\xba\xe8\xa1\xa8\xe7\xa4\xba\xe5\xbd\x93\xe5\x89\x8dcpe
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe6\x97\xa0\xe8\xbf\x94\xe5\x9b\x9e;
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
               
        Example:
        |  Bind Physic Worklist  |  ID_1364950237391  |  00904C-2013012901  |
        
        """
        ret_api = ERR_FAIL
        ret_data = ''
        desc = ''
        if sn == '':
            sn = self._get_sn()
        obj = user.UserWorklist()
        dict_data = {}
        dict_data['id_'] = worklist_id
        dict_data['sn'] = sn
        ret_api, ret_data = obj.worklistprocess_bind_physical(**dict_data)
        if ret_api == ERR_SUCCESS:
            desc = u'\u7ed1\u5b9a\u7269\u7406\u5de5\u5355\u6210\u529f\u3002'
            self._user_info(desc)
        else:
            desc = u'\u7ed1\u5b9a\u7269\u7406\u5de5\u5355\u5931\u8d25\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % ret_data
            raise RuntimeError(desc)
        return None

    def bind_logic_worklist(self, worklist_id, username, userid):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe7\xbb\x91\xe5\xae\x9a\xe9\x80\xbb\xe8\xbe\x91\xe5\xb7\xa5\xe5\x8d\x95 
        
        \xe5\x8f\x82\xe6\x95\xb0:
            worklist_id:        \xe9\x9c\x80\xe8\xa6\x81\xe7\xbb\x91\xe5\xae\x9a\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95id;
            username:   \xe9\x80\xbb\xe8\xbe\x91\xe5\xb7\xa5\xe5\x8d\x95\xe7\x9a\x84username;
            userid:     \xe9\x80\xbb\xe8\xbe\x91\xe5\xb7\xa5\xe5\x8d\x95\xe7\x9a\x84userid
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe6\x97\xa0\xe8\xbf\x94\xe5\x9b\x9e;
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
               
        Example:
        |  Bind Logic Worklist  |  ID_1364950237391  |  username  |  userid  |
        
        """
        ret_api = ERR_FAIL
        ret_data = ''
        desc = ''
        obj = user.UserWorklist()
        dict_data = {}
        dict_data['id_'] = worklist_id
        dict_data['username'] = username
        dict_data['userid'] = userid
        ret_api, ret_data = obj.worklistprocess_bind_logical(**dict_data)
        if ret_api == ERR_SUCCESS:
            desc = u'\u7ed1\u5b9a\u903b\u8f91\u5de5\u5355\u6210\u529f\u3002'
            self._user_info(desc)
        else:
            desc = u'\u7ed1\u5b9a\u903b\u8f91\u5de5\u5355\u5931\u8d25\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % ret_data
            raise RuntimeError(desc)
        return None

    def _get_worklist_exec_info(self, worklist_id):
        """
        """
        ret_api = ERR_FAIL
        ret_data = ''
        ret_obj = None
        ret_out = ''
        desc = ''
        obj = user.UserWorklist()
        dict_data = {}
        dict_data['id_'] = worklist_id
        ret_api, ret_data = obj.worklistprocess_query(**dict_data)
        if ret_api != ERR_SUCCESS:
            desc = u'%s' % ret_data
            desc = u'\u67e5\u8be2\u67d0\u5de5\u5355\u7684\u8be6\u7ec6\u4fe1\u606f\u5931\u8d25\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % desc
            raise RuntimeError(desc)
        ret_obj = ret_data
        ret_api, ret_data = user.query_cpe_info(ret_obj.sn)
        if ret_api != ERR_SUCCESS:
            desc = u'\u67e5\u8be2CPE\u4fe1\u606f\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        ret_obj = ret_data
        desc = u' \u6267\u884c\u5de5\u5355\u524d\u7684CPE\u4fe1\u606f:\noperator\u8fd0\u8425\u5546=%s,\ninterface version\u63a5\u53e3\u89c4\u8303=%s,\ncpe device type\u8bbe\u5907\u7c7b\u578b=%s\n' % (ret_obj.cpe_operator, ret_obj.interface_version, ret_obj.worklist_domain)
        return desc

    def execute_worklist(self, worklist_id):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe5\xb7\xa5\xe5\x8d\x95 
        
        \xe5\x8f\x82\xe6\x95\xb0:
            worklist_id:\xe9\x9c\x80\xe8\xa6\x81\xe6\x89\xa7\xe8\xa1\x8c\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95id
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe6\x97\xa0\xe8\xbf\x94\xe5\x9b\x9e;
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
               
        Example:
        |  Execute Worklist  |  ID_1364950237391  |
        
        """
        ret_api = ERR_FAIL
        ret_data = ''
        ret_obj = None
        ret_out = ''
        desc = ''
        obj = user.UserWorklist()
        dict_data = {}
        dict_data['id_'] = worklist_id
        ret_api, ret_data = obj.worklistprocess_execute(**dict_data)
        if ret_api == ERR_SUCCESS:
            ret_obj = ret_data
            ret_out = ret_obj.dict_ret.get('str_result')
            desc = u'\u6267\u884c\u5de5\u5355\u6210\u529f\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % ret_out
            self._user_info(desc)
        else:
            if isinstance(ret_data, Exception) or isinstance(ret_data, basestring):
                desc = ret_data
            else:
                ret_obj = ret_data
                ret_out = ret_obj.dict_ret.get('str_result')
                desc = ret_out
            desc = u'\u6267\u884c\u5de5\u5355\u5931\u8d25\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % desc
            raise RuntimeError(desc)
        return

    def query_worklist(self, worklist_id):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0: \xe6\x9f\xa5\xe8\xaf\xa2\xe6\x9f\x90\xe5\xb7\xa5\xe5\x8d\x95\xe7\x9a\x84\xe8\xaf\xa6\xe7\xbb\x86\xe4\xbf\xa1\xe6\x81\xaf
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
            worklist_id: \xe9\x9c\x80\xe8\xa6\x81\xe6\x9f\xa5\xe8\xaf\xa2\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95id
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe6\x97\xa0\xe8\xbf\x94\xe5\x9b\x9e;
                \xe5\xa4\xb1\xe8\xb4\xa5,\xe6\x8a\x9b\xe5\x87\xba\xe5\xbc\x82\xe5\xb8\xb8
               
        Example:
        |  Query Worklist  |  ID_1364950237391  |
        
        """
        ret_api = ERR_FAIL
        ret_data = ''
        ret_obj = None
        desc = ''
        obj = user.UserWorklist()
        dict_data = {}
        dict_data['id_'] = worklist_id
        ret_api, ret_data = obj.worklistprocess_query(**dict_data)
        if ret_api == ERR_SUCCESS:
            ret_obj = ret_data
            desc = self._get_worklist_record(ret_obj)
            desc = u'\u67e5\u8be2\u67d0\u5de5\u5355\u7684\u8be6\u7ec6\u4fe1\u606f\u6210\u529f\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % desc
            self._user_info(desc)
        else:
            desc = u'%s' % ret_data
            desc = u'\u67e5\u8be2\u67d0\u5de5\u5355\u7684\u8be6\u7ec6\u4fe1\u606f\u5931\u8d25\uff0c\u7ed3\u679c\u5982\u4e0b:%s' % desc
            raise RuntimeError(desc)
        return desc

    def wait_next_inform(self, timeout = 120):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe5\x8f\x91\xe9\x80\x81\xe5\x91\xbd\xe4\xbb\xa4\xef\xbc\x8c\xe7\xad\x89\xe5\xbe\x85CPE\xe7\x9a\x84\xe4\xb8\x8b\xe4\xb8\x80\xe4\xb8\xaainform(\xe4\xbb\xbb\xe4\xbd\x95eventcode\xe5\x80\xbc)
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
        | timeout | \xe8\xb6\x85\xe6\x97\xb6\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x8c\xe5\x8d\x95\xe4\xbd\x8d\xe7\xa7\x92 |
        
        Example:
        | Wait Next Inform | 120 |
        
        """
        ret_api = None
        ret_data = None
        sn = self._get_sn()
        timeout2 = int(timeout)
        ret_api, ret_data = user.wait_next_inform(sn, timeout2)
        if ret_api == ERR_SUCCESS:
            desc = u'\u7b49\u5f85CPE\u7684\u4e0b\u4e00\u4e2ainform\u6210\u529f\u3002'
            self._user_info(desc)
        else:
            desc = u'\u7b49\u5f85CPE\u7684\u4e0b\u4e00\u4e2ainform\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return

    def init_wait_eventcode(self, include_eventcodes, exclude_eventcodes = []):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe7\x94\x9f\xe6\x88\x90\xe4\xb8\x80\xe4\xb8\xaa wait_eventcode \xe7\x9a\x84\xe4\xbb\xbb\xe5\x8a\xa1
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
        | include_eventcodes | \xe5\x90\x8c\xe4\xb8\x80\xe4\xb8\xaa inform \xe9\x87\x8c\xe9\x9d\xa2\xe5\x8c\x85\xe5\x90\xab\xe7\x9a\x84 eventcode \xe5\x88\x97\xe8\xa1\xa8 |
        | exclude_eventcodes | \xe5\x90\x8c\xe4\xb8\x80\xe4\xb8\xaa inform \xe9\x87\x8c\xe9\x9d\xa2\xe4\xb8\x8d\xe8\x83\xbd\xe8\xa2\xab\xe5\x8c\x85\xe5\x90\xab\xe7\x9a\x84 eventcode \xe5\x88\x97\xe8\xa1\xa8 |
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a
        | \xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f | \xe8\xbf\x94\xe5\x9b\x9e\xe6\x9c\xac\xe6\xac\xa1 wait_eventcode \xe4\xbb\xbb\xe5\x8a\xa1ID |        
        
        Example:
        | ${id} | Init Wait EventCode | 8 DIAGNOSTICS COMPLETE |
        | ${id} | Init Wait EventCode | 8 DIAGNOSTICS COMPLETE | 6 CONNECTION REQUEST  |
        
        | ${include_eventcodes} | Create List  | 1 BOOT |  2 PERIODIC  |  |
        | ${exclude_eventcodes} | Create List  | 6 CONNECTION REQUEST |  8 DIAGNOSTICS COMPLETE | X CT-COM ALARM |
        | ${id} | Init Wait EventCode | ${include_eventcodes} | ${exclude_eventcodes}  |        
        
        """
        ret_api = None
        ret_data = None
        ret_obj = None
        ret_out = ''
        sn = self._get_sn()
        include_eventcodes2 = include_eventcodes
        exclude_eventcodes2 = exclude_eventcodes
        if not isinstance(include_eventcodes, list):
            include_eventcodes2 = []
            include_eventcodes2.append(include_eventcodes)
        if not isinstance(exclude_eventcodes, list):
            exclude_eventcodes2 = []
            exclude_eventcodes2.append(exclude_eventcodes)
        ret_api, ret_data = user.init_wait_eventcode(sn, include_eventcodes2, exclude_eventcodes2)
        if ret_api == ERR_SUCCESS:
            ret_obj = ret_data
            ret_out = ret_obj.id_
            desc = u'\u521d\u59cb\u5316\u751f\u6210\u4e00\u4e2a wait_eventcode \u7684\u4efb\u52a1\u6210\u529f\u3002'
            self._user_info(desc)
        else:
            desc = u'\u521d\u59cb\u5316\u751f\u6210\u4e00\u4e2a wait_eventcode \u7684\u4efb\u52a1\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def start_wait_eventcode(self, wait_eventcode_id):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe5\xbc\x80\xe5\xa7\x8b wait_eventcode \xe4\xbb\xbb\xe5\x8a\xa1
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
        | wait_eventcode_id | init_wait_eventcode \xe8\xbf\x94\xe5\x9b\x9e\xe7\x9a\x84id |
        
        Example:               
        | start_wait_eventcode | ID_wait_eventcode_2013-08-06_10:33:42.241000_12345678 |
        
        """
        ret_api = None
        ret_data = None
        sn = self._get_sn()
        ret_api, ret_data = user.start_wait_eventcode(sn, wait_eventcode_id)
        if ret_api == ERR_SUCCESS:
            desc = u'\u5f00\u59cb wait_eventcode \u4efb\u52a1\u6210\u529f\u3002'
            self._user_info(desc)
        else:
            desc = u'\u5f00\u59cb wait_eventcode \u4efb\u52a1\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return

    def check_result_and_stop_wait_eventcode(self, wait_eventcode_id, timeout = 120):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe5\x9c\xa8timeout\xe6\x97\xb6\xe9\x97\xb4\xe5\x86\x85\xef\xbc\x8c\xe6\xaf\x8f\xe9\x9a\x94\xe4\xb8\x80\xe6\xae\xb5\xe6\x97\xb6\xe9\x97\xb4(3s) \xe5\x90\x91\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe6\x9f\xa5\xe8\xaf\xa2\xef\xbc\x8c\xe6\x98\xaf\xe5\x90\xa6\xe6\xbb\xa1\xe8\xb6\xb3 init_wait_eventcode \xe7\x9a\x84\xe9\x85\x8d\xe7\xbd\xae\xe8\xa6\x81\xe6\xb1\x82\xe3\x80\x82
                \xe6\xbb\xa1\xe8\xb6\xb3\xe8\xa6\x81\xe6\xb1\x82\xe5\x88\x99\xe7\xab\x8b\xe5\x88\xbb\xe8\xbf\x94\xe5\x9b\x9e\xe6\x88\x90\xe5\x8a\x9f; \xe4\xb8\x8d\xe6\xbb\xa1\xe8\xb6\xb3\xe8\xa6\x81\xe6\xb1\x82\xef\xbc\x8c\xe5\x88\x99\xe5\xbb\xb6\xe6\x97\xb6\xe7\xad\x89\xe5\x80\x99\xe6\x9c\x80\xe9\x95\xbftimeout\xe6\x97\xb6\xe9\x97\xb4\xe3\x80\x82
                \xe8\xaf\xa5\xe5\x85\xb3\xe9\x94\xae\xe5\xad\x97\xe8\xbf\x94\xe5\x9b\x9e\xe5\x89\x8d, \xe4\xbc\x9a\xe8\x87\xaa\xe5\x8a\xa8\xe7\xbb\x93\xe6\x9d\x9f\xe6\x8e\x89 init_wait_eventcode \xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe4\xbb\xbb\xe5\x8a\xa1\xe3\x80\x82
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
        | wait_eventcode_id | init_wait_eventcode \xe8\xbf\x94\xe5\x9b\x9e\xe7\x9a\x84id |
        | timeout | \xe5\x90\x91\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe6\x9f\xa5\xe8\xaf\xa2\xe6\x8c\x81\xe7\xbb\xad\xe7\x9a\x84\xe6\x9c\x80\xe9\x95\xbf\xe6\x97\xb6\xe9\x97\xb4, \xe5\x8d\x95\xe4\xbd\x8d\xe7\xa7\x92 |
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a
        | \xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f | \xe8\xaf\xb4\xe6\x98\x8e\xe6\xbb\xa1\xe8\xb6\xb3 init_wait_eventcode \xe4\xbb\xbb\xe5\x8a\xa1\xe7\x9a\x84\xe9\x85\x8d\xe7\xbd\xae\xe8\xa6\x81\xe6\xb1\x82 |
        | \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5 | \xe8\xaf\xb4\xe6\x98\x8e\xe4\xb8\x8d\xe6\xbb\xa1\xe8\xb6\xb3 init_wait_eventcode \xe4\xbb\xbb\xe5\x8a\xa1\xe7\x9a\x84\xe9\x85\x8d\xe7\xbd\xae\xe8\xa6\x81\xe6\xb1\x82 |
        
        Example:               
        | Check Result and Stop Wait EventCode | ID_wait_eventcode_2013-08-06_10:33:42.241000_12345678 |
        | Check Result and Stop Wait EventCode | ID_wait_eventcode_2013-08-06_10:33:42.241000_12345678 | 300 |
        
        """
        ret_api = None
        ret_data = None
        sn = self._get_sn()
        timeout2 = int(timeout)
        ret_api, ret_data = user.check_result_and_stop_wait_eventcode(sn, wait_eventcode_id, timeout2)
        if ret_api == ERR_SUCCESS:
            desc = u'\u68c0\u67e5wait_eventcode\u4efb\u52a1\u6210\u529f\u3002'
            self._user_info(desc)
        else:
            desc = u'\u68c0\u67e5wait_eventcode\u4efb\u52a1\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return

    def init_alarm(self, parameterlist, limit_min, limit_max, timelist = 1, mode = 1):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe4\xb8\x80\xe4\xb8\xaa\xe5\x91\x8a\xe8\xad\xa6\xe6\xb5\x81\xe7\xa8\x8b
        
        \xe6\xb3\xa8\xe6\x84\x8f: \xe8\x81\x94\xe9\x80\x9a\xe7\x9a\x84CPE\xef\xbc\x8c\xe5\x91\x8a\xe8\xad\xa6\xe8\xa7\x84\xe5\x88\x99\xe5\x9b\xba\xe5\xae\x9a\xef\xbc\x8c\xe5\x8f\xaa\xe9\x9c\x80\xe8\xa6\x81init_alram\xe5\x8a\xa8\xe4\xbd\x9c\xef\xbc\x8c\xe5\x8f\x82\xe6\x95\xb0\xe4\xbb\xbb\xe6\x84\x8f\xe9\x85\x8d\xe7\xbd\xae
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
        | parameterlist | \xe9\x9c\x80\xe8\xa6\x81\xe7\x9b\x91\xe6\x8e\xa7\xe7\x9a\x84\xe5\x85\xb3\xe9\x94\xae\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x88TR069\xe5\x8f\x82\xe6\x95\xb0\xe6\xa8\xa1\xe5\x9e\x8b\xe5\x85\xa8\xe8\xb7\xaf\xe5\xbe\x84\xef\xbc\x89\xef\xbc\x8c\xe4\xbe\x8b\xe5\xa6\x82\xef\xbc\x9aInternetGatewayDevice.WANDevice.{i}.X_CT-COM_EponInterfaceConfig.Stats. BytesSent  |
        | limit_min     | \xe9\x9c\x80\xe8\xa6\x81\xe7\x9b\x91\xe6\x8e\xa7\xe7\x9a\x84\xe5\x85\xb3\xe9\x94\xae\xe5\x8f\x82\xe6\x95\xb0\xe7\x9a\x84\xe6\x9c\x80\xe5\xb0\x8f\xe8\x8c\x83\xe5\x9b\xb4 |
        | limit_max     | \xe9\x9c\x80\xe8\xa6\x81\xe7\x9b\x91\xe6\x8e\xa7\xe7\x9a\x84\xe5\x85\xb3\xe9\x94\xae\xe5\x8f\x82\xe6\x95\xb0\xe7\x9a\x84\xe6\x9c\x80\xe5\xa4\xa7\xe8\x8c\x83\xe5\x9b\xb4 |        
        | timelist      | \xe5\x91\x8a\xe8\xad\xa6\xe5\x91\xa8\xe6\x9c\x9f\xef\xbc\x8c\xe5\x8d\x95\xe4\xbd\x8d\xe4\xb8\xba\xef\xbc\x9a\xe5\x88\x86\xe9\x92\x9f  |
        | mode          | \xe5\x91\x8a\xe8\xad\xa6\xe5\x8f\x96\xe5\x80\xbc\xe6\x96\xb9\xe5\xbc\x8f\xef\xbc\x8c1\xef\xbc\x9a\xe7\xb4\xaf\xe5\x8a\xa0\xe5\x80\xbc\xef\xbc\x8c2\xef\xbc\x9a\xe5\xb9\xb3\xe5\x9d\x87\xe5\x80\xbc\xef\xbc\x8c3\xef\xbc\x9a\xe7\x9e\xac\xe9\x97\xb4\xe5\x80\xbc |
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a
        | \xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f | \xe8\xbf\x94\xe5\x9b\x9e\xe6\x9c\xac\xe6\xac\xa1\xe5\x91\x8a\xe8\xad\xa6\xe6\xb5\x81\xe7\xa8\x8bID |
        
        Example:
        | ${id} | Init Alarm | InternetGatewayDevice.WANDevice.1.WANConnectionDevice.7.WANIPConnection.1.Stats.EthernetBytesReceived | 2000 | 3000 | 1 | 1 |
        
        """
        ret_api = None
        ret_data = None
        ret_obj = None
        ret_out = ''
        sn = self._get_sn()
        ret_api, ret_data = user.init_alarm(sn, parameterlist, limit_max, limit_min, timelist, mode)
        if ret_api == ERR_SUCCESS:
            desc = u'\u521d\u59cb\u5316\u4e00\u4e2a\u544a\u8b66\u6d41\u7a0b\u6210\u529f\u3002'
            self._user_info(desc)
            ret_obj = ret_data
            ret_out = ret_obj.id_
        else:
            desc = u'\u521d\u59cb\u5316\u4e00\u4e2a\u544a\u8b66\u6d41\u7a0b\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def start_alarm(self, alarm_id):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe5\xbc\x80\xe5\xa7\x8b\xe5\x91\x8a\xe8\xad\xa6\xe6\xb5\x81\xe7\xa8\x8b
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
        | alarm_id | Init Alarm \xe8\xbf\x94\xe5\x9b\x9e\xe7\x9a\x84ID |
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a
        | \xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f | \xe8\xbf\x94\xe5\x9b\x9eNone |
        | \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5 | \xe5\xbc\x82\xe5\xb8\xb8 |
        
        Example:
        | Start Alarm | ID_alarm_2013-05-30_10:33:42.241000  |
        
        """
        ret_api = None
        ret_data = None
        sn = self._get_sn()
        ret_api, ret_data = user.start_alarm(sn, alarm_id)
        if ret_api == ERR_SUCCESS:
            desc = u'\u5f00\u59cb\u544a\u8b66\u6d41\u7a0b\u6210\u529f\u3002'
            self._user_info(desc)
        else:
            desc = u'\u5f00\u59cb\u544a\u8b66\u6d41\u7a0b\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return

    def stop_alarm(self, alarm_id):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe5\x81\x9c\xe6\xad\xa2\xe5\x91\x8a\xe8\xad\xa6\xe6\xb5\x81\xe7\xa8\x8b
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
        | ${alarm_id} | Init Alarm \xe8\xbf\x94\xe5\x9b\x9e\xe7\x9a\x84ID |
        
        Example:
        | Stop Alarm |  ID_alarm_2013-05-30_10:33:42.241000 |
        
        """
        ret_api = None
        ret_data = None
        sn = self._get_sn()
        ret_api, ret_data = user.stop_alarm(sn, alarm_id)
        if ret_api == ERR_SUCCESS:
            desc = u'\u505c\u6b62\u544a\u8b66\u6d41\u7a0b\u6210\u529f\u3002'
            self._user_info(desc)
        else:
            desc = u'\u505c\u6b62\u544a\u8b66\u6d41\u7a0b\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return

    def get_alarm_values(self, alarm_id):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe5\x91\x8a\xe8\xad\xa6\xe6\xb5\x81\xe7\xa8\x8b\xe5\xbc\x80\xe5\xa7\x8b\xe5\x90\x8e\xef\xbc\x8c\xe4\xbb\x8e\xe6\xbb\xa1\xe8\xb6\xb3\xe5\x91\x8a\xe8\xad\xa6\xe6\x9d\xa1\xe4\xbb\xb6\xe7\x9a\x84inform\xe4\xb8\xad\xe8\x8e\xb7\xe5\xbe\x97\xe7\x9b\x91\xe6\x8e\xa7\xe8\x8a\x82\xe7\x82\xb9\xe5\x80\xbc
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
        | ${alarm_id} | Start Alarm\xe8\xbf\x94\xe5\x9b\x9e\xe7\x9a\x84ID |
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc: [(time1, value1), (time2, value2), ...]
        
        \xe6\xb3\xa8\xe6\x84\x8f\xef\xbc\x9a\xe8\x81\x94\xe9\x80\x9a\xe7\x9a\x84CPE\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc[(time1, inform1), (time2, inform2), ...]
        
        Example:
        | ${values}  | Get Alarm Values |  ID_alarm_2013-05-30_10:33:42.241000 |
        
        """
        ret_api = None
        ret_data = None
        ret_obj = None
        ret_out = None
        ret_out_4log = None
        ret_out_4ret = None
        values = ''
        sn = self._get_sn()
        ret_api, ret_data = user.get_alarm_values(sn, alarm_id)
        if ret_api == ERR_SUCCESS:
            desc = u'\u83b7\u53d6\u544a\u8b66\u503c\u6210\u529f\u3002\u8fd4\u56de\u503c\u5982\u4e0b:'
            self._user_info(desc)
            ret_obj = ret_data
            ret_out = ret_obj.parameter_values
            ret_out_4log = []
            ret_out_4ret = []
            for time1, value1 in ret_out:
                time1.strftime('%Y-%m-%d %H:%M:%S %f')
                ret_out_4log.append((str(time1), value1))
                seconds = (time1 - datetime(1970, 1, 1)).total_seconds()
                seconds = int(round(seconds))
                ret_out_4ret.append((seconds, value1))
                values = values + value1 + '\r\n'

            self._user_info(str(ret_out_4log))
            desc = u'\u663e\u793a\u503c\u5982\u4e0b:'
            self._user_info(desc)
            self._user_info(values)
            ret_out = ret_out_4ret
        else:
            desc = u'\u83b7\u53d6\u544a\u8b66\u503c\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def init_monitor(self, parameterlist, timelist = 1):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe4\xb8\x80\xe4\xb8\xaa\xe7\x9b\x91\xe6\x8e\xa7\xe6\xb5\x81\xe7\xa8\x8b
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
        | parameterlist | \xe9\x9c\x80\xe8\xa6\x81\xe7\x9b\x91\xe6\x8e\xa7\xe7\x9a\x84\xe5\x85\xb3\xe9\x94\xae\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x88TR069\xe5\x8f\x82\xe6\x95\xb0\xe6\xa8\xa1\xe5\x9e\x8b\xe5\x85\xa8\xe8\xb7\xaf\xe5\xbe\x84\xef\xbc\x89\xef\xbc\x8c\xe4\xbe\x8b\xe5\xa6\x82\xef\xbc\x9aInternetGatewayDevice.WAN\xc2\xacDevice.{i}.X_CT-COM_EponInterfaceConfig.Stats.BytesSent |
        | timelist      | \xe9\x87\x87\xe6\xa0\xb7\xe5\x91\xa8\xe6\x9c\x9f\xef\xbc\x8c\xe5\x8d\x95\xe4\xbd\x8d\xe4\xb8\xba\xef\xbc\x9a\xe5\x88\x86\xe9\x92\x9f  |
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a
        | \xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f | \xe8\xbf\x94\xe5\x9b\x9e\xe6\x9c\xac\xe6\xac\xa1\xe7\x9b\x91\xe6\x8e\xa7\xe6\xb5\x81\xe7\xa8\x8bID |
        
        Example:
        | ${id} | Init Monitor | InternetGatewayDevice.WANDevice.1.WANConnectionDevice.7.WANIPConnection.1.Stats.EthernetBytesReceived | 1 |
        
        """
        ret_api = None
        ret_data = None
        ret_obj = None
        ret_out = ''
        sn = self._get_sn()
        ret_api, ret_data = user.init_monitor(sn, parameterlist, timelist)
        if ret_api == ERR_SUCCESS:
            desc = u'\u521d\u59cb\u5316\u4e00\u4e2a\u76d1\u63a7\u6d41\u7a0b\u6210\u529f\u3002'
            self._user_info(desc)
            ret_obj = ret_data
            ret_out = ret_obj.id_
        else:
            desc = u'\u521d\u59cb\u5316\u4e00\u4e2a\u76d1\u63a7\u6d41\u7a0b\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def start_monitor(self, monitor_id):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe5\xbc\x80\xe5\xa7\x8b\xe7\x9b\x91\xe6\x8e\xa7\xe6\xb5\x81\xe7\xa8\x8b
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
        | ${monitor_id} | Init Monitor \xe8\xbf\x94\xe5\x9b\x9e\xe7\x9a\x84ID |
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a
        | \xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f | \xe8\xbf\x94\xe5\x9b\x9e None |
        | \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5 | \xe5\xbc\x82\xe5\xb8\xb8 |
        
        Example:
        | Start Monitor | ID_monitor_2013-05-30_10:33:42.241000 |
        
        """
        ret_api = None
        ret_data = None
        sn = self._get_sn()
        ret_api, ret_data = user.start_monitor(sn, monitor_id)
        if ret_api == ERR_SUCCESS:
            desc = u'\u5f00\u59cb\u76d1\u63a7\u6d41\u7a0b\u6210\u529f\u3002'
            self._user_info(desc)
        else:
            desc = u'\u5f00\u59cb\u76d1\u63a7\u6d41\u7a0b\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return

    def stop_monitor(self, monitor_id):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe5\x81\x9c\xe6\xad\xa2\xe7\x9b\x91\xe6\x8e\xa7\xe6\xb5\x81\xe7\xa8\x8b
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
        | ${monitor_id} | Init Monitor \xe8\xbf\x94\xe5\x9b\x9e\xe7\x9a\x84ID |
        
        Example:
        | Stop Monitor |  ID_monitor_2013-05-30_10:33:42.241000 |
        
        """
        ret_api = None
        ret_data = None
        sn = self._get_sn()
        ret_api, ret_data = user.stop_monitor(sn, monitor_id)
        if ret_api == ERR_SUCCESS:
            desc = u'\u505c\u6b62\u76d1\u63a7\u6d41\u7a0b\u6210\u529f\u3002'
            self._user_info(desc)
        else:
            desc = u'\u505c\u6b62\u76d1\u63a7\u6d41\u7a0b\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return

    def get_monitor_values(self, monitor_id):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe7\x9b\x91\xe6\x8e\xa7\xe6\xb5\x81\xe7\xa8\x8b\xe5\xbc\x80\xe5\xa7\x8b\xe5\x90\x8e\xef\xbc\x8c\xe4\xbb\x8e\xe6\xbb\xa1\xe8\xb6\xb3\xe7\x9b\x91\xe6\x8e\xa7\xe6\x9d\xa1\xe4\xbb\xb6\xe7\x9a\x84inform\xe4\xb8\xad\xe8\x8e\xb7\xe5\xbe\x97\xe7\x9b\x91\xe6\x8e\xa7\xe8\x8a\x82\xe7\x82\xb9\xe7\x9a\x84\xe5\x80\xbc
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
        | monitor_id | Start Monitor \xe8\xbf\x94\xe5\x9b\x9e\xe7\x9a\x84ID |
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc: [(time1, value1), (time2, value2), ...]        
        
        Example:    
        | ${values}  | Get Monitor Values |  ID_monitor_2013-05-30_10:33:42.241000 |
        
        """
        ret_api = None
        ret_data = None
        ret_obj = None
        ret_out = None
        ret_out_4log = None
        ret_out_4ret = None
        sn = self._get_sn()
        ret_api, ret_data = user.get_monitor_values(sn, monitor_id)
        if ret_api == ERR_SUCCESS:
            desc = u'\u83b7\u53d6\u76d1\u63a7\u503c\u6210\u529f\u3002\u8fd4\u56de\u503c\u5982\u4e0b:'
            self._user_info(desc)
            ret_obj = ret_data
            ret_out = ret_obj.parameter_values
            ret_out_4log = []
            ret_out_4ret = []
            for time1, value1 in ret_out:
                time1.strftime('%Y-%m-%d %H:%M:%S %f')
                ret_out_4log.append((str(time1), value1))
                seconds = (time1 - datetime(1970, 1, 1)).total_seconds()
                seconds = int(round(seconds))
                ret_out_4ret.append((seconds, value1))

            self._user_info(str(ret_out_4log))
            ret_out = ret_out_4ret
        else:
            desc = u'\u83b7\u53d6\u76d1\u63a7\u503c\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def get_last_session_soap(self):
        """
        \xe5\x8a\x9f\xe8\x83\xbd\xe6\x8f\x8f\xe8\xbf\xb0\xef\xbc\x9a\xe5\xbe\x97\xe5\x88\xb0\xe4\xb8\x8a\xe4\xb8\x80\xe6\xac\xa1ACS\xe4\xb8\x8eCPE\xe4\xba\xa4\xe4\xba\x92\xe7\x9a\x84RPC\xe7\x9a\x84SOAP\xe5\x8c\x85
        
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a\xe7\xa9\xba
        
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a
        | \xe6\x89\xa7\xe8\xa1\x8c\xe6\x88\x90\xe5\x8a\x9f | \xe4\xbb\xa5\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2\xe5\xbd\xa2\xe5\xbc\x8f\xe8\xbf\x94\xe5\x9b\x9esoap\xe5\x8c\x85 |
        | \xe6\x89\xa7\xe8\xa1\x8c\xe5\xa4\xb1\xe8\xb4\xa5 | \xe5\xbc\x82\xe5\xb8\xb8 |        
        
        Example:
        | ${soap} |  Get Last Session Soap  |
        
        """
        ret_api = None
        ret_data = None
        ret_obj = None
        ret_out = ''
        sn = self._get_sn()
        ret_api, ret_data = user.query_last_session_soap(sn)
        if ret_api == ERR_SUCCESS:
            desc = u'\u5f97\u5230\u4e0a\u4e00\u6b21ACS\u4e0eCPE\u4ea4\u4e92\u7684RPC\u7684SOAP\u5305\u6210\u529f\u3002'
            self._user_info(desc)
            ret_obj = ret_data
            ret_out = ret_obj.dict_ret['str_result']
        else:
            desc = u'\u5f97\u5230\u4e0a\u4e00\u6b21ACS\u4e0eCPE\u4ea4\u4e92\u7684RPC\u7684SOAP\u5305\u5931\u8d25\uff0c\u8be6\u7ec6\u4fe1\u606f\u4e3a\uff1a%s' % ret_data
            raise RuntimeError(desc)
        return ret_out

    def _get_random_command_key(self):
        """
        string(32)
        eg = 2013-11-22_15:02:49.845000_8819
        """
        dt1 = datetime.now()
        random1 = random.randrange(1000, 10000)
        command_key = '%s_%s_%s' % (dt1.date(), dt1.time(), random1)
        desc = 'auto command_key = %s' % command_key
        self._user_info(desc)
        return command_key

    def _convert_worklist_args(self, list_args):
        """
        \xe5\x87\xbd\xe6\x95\xb0\xe5\x8a\x9f\xe8\x83\xbd\xef\xbc\x9a\xe5\xaf\xb9\xe7\x94\xa8\xe6\x88\xb7\xe8\xbe\x93\xe5\x85\xa5\xe7\x9a\x84list\xe7\xb1\xbb\xe5\x9e\x8b\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95\xe5\x8f\x82\xe6\x95\xb0\xe5\x81\x9a\xe8\xbd\xac\xe6\x8d\xa2\xef\xbc\x8c\xe8\xbd\xac\xe4\xb8\xbadict
        \xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x9a
            list_args\xef\xbc\x9a list\xe5\x9e\x8b\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8d\x95\xe5\x8f\x82\xe6\x95\xb0\xef\xbc\x8clist\xe4\xb8\xad\xe7\x9a\x84\xe5\x8f\x82\xe6\x95\xb0\xe5\x8f\xaf\xe8\x83\xbd\xe6\x98\xaf\xe5\x8d\x95\xe4\xb8\xaa\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2\xef\xbc\x8c\xe5\x8f\xaf\xe8\x83\xbd\xe6\x98\xaf\xe7\x94\xb1"key=value"\xe7\xbb\x84\xe6\x88\x90\xe7\x9a\x84\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2
        \xe8\xbf\x94\xe5\x9b\x9e\xe5\x80\xbc\xef\xbc\x9a
            dict_data\xef\xbc\x9a \xe5\xaf\xb9list_args\xe8\xbd\xac\xe6\x8d\xa2\xe5\x90\x8e\xe7\x9a\x84\xe5\xad\x97\xe5\x85\xb8\xe6\x95\xb0\xe6\x8d\xae
        """
        dict_data = {}
        i = 1
        for key_value in list_args:
            index = '%s' % i
            list_data = key_value.split('=', 1)
            if len(list_data) <= 1:
                key = index
                value = list_data[0]
            elif list_data[0].rstrip() == '':
                key = index
                value = key_value
            else:
                key = list_data[0]
                value = list_data[1]
            dict_data.update({key: (value, index)})
            i += 1

        return dict_data


def test_rpc():
    x = obj.set_cpe_interface_version('Auto')
    print x


def test_cpe_query_update():
    x = obj.get_telecom_account_password()
    print x
    x = obj.get_acs_auth_info()
    print x
    x = obj.set_acs_auth_info('admin', 'admin')
    print x
    x = obj.get_acs_auth_method()
    print x
    x = obj.set_acs_auth_method('digest')
    print x
    x = obj.get_max_session_timeout()
    print x
    x = obj.set_max_session_timeout(240)
    print x
    x = obj.get_cpe_software_version()
    print x
    x = obj.get_cpe_hardware_version()
    print x
    x = obj.get_cpe_connection_request_url()
    print x
    x = obj.get_cpe_connection_request_ip()
    print x
    x = obj.get_cpe_auth_info()
    print x
    x = obj.set_cpe_auth_info('admin', 'admin')
    print x
    x = obj.get_cpe_cwmp_version()
    print x
    x = obj.set_cpe_cwmp_version()
    print x
    x = obj.get_cpe_online_status()
    print x
    x = obj.set_cpe_rollback('True')
    print x
    x = obj.get_cpe_rollback()
    print x
    x = obj.set_cpe_device_type('ADSL')
    print x
    x = obj.get_cpe_device_type()
    print x


def test_worklist():
    x = obj.set_cpe_device_type('ADSL')
    x = obj.set_cpe_rollback('True')
    dict_data = {'key1': 'value1',
     'key2': 'value2'}
    str_dict_data = str(dict_data)
    id1 = obj.init_worklist('test', str_dict_data)
    x, y = obj.get_worklist_userinfo(id1)
    obj.query_worklist(id1)
    x1 = obj.bind_physic_worklist(id1)
    obj.query_worklist(id1)
    x2 = obj.execute_worklist(id1)
    obj.query_worklist(id1)
    x = obj.get_telecom_account_password()
    print x
    print 'hold'


def test_monitor_inform():
    x = obj.init_alarm('InternetGatewayDevice.WANDevice.1.WANConnectionDevice.4.WANIPConnection.1.Stats.EthernetPacketsReceived', 3000, 2000)
    print x
    x = obj.start_alarm(x)
    print x


def test():
    test_rpc()
    print 'test end'


if __name__ == '__main__':
    sn = '00904C-2013012901'
    obj = TR069()
    obj.config_remote_server_addr('172.123.117.13', port=50000)
    obj.switch_cpe(sn)
    test()
    obj.switch_cpe(sn)
    print '\n test end \n'