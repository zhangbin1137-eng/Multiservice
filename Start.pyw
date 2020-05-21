# -*- coding: utf-8 -*-

###########################################################################
## 创建时间：2019-06-03
## 作者：张斌
## 说明：ONU重启恢复性能测试工具
###########################################################################


import os
import sys

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'lib'))
sys.path.append(os.path.join(os.getcwd(), 'lib', 'win32'))
sys.path.append(os.path.join(os.getcwd(), 'lib', 'chariot'))

from lib.pysnooper.pysnooper import
import wx
import wx.xrc

reload(sys)
sys.setdefaultencoding('utf-8')
import time
from time import sleep
from time import ctime
import threading
import multiprocessing as mp
import socket

try:
    from lib.dut_config_win import dut_config
    from lib.TR069_config_win import TR069_config
    from lib.VoIP_config_win import VoIP_config
    from lib.IPTV_config_win import IPTV_config
    from lib.Internet_config_win import Internet_config
    from lib.WLAN_config_win import WLAN_config
    from lib.Power_config_win import Power_config
except ImportError, e:
    wx.MessageBox(u"当前没有加载到相关对象，请检查", u"警告", wx.OK | wx.ICON_INFORMATION)
    exit(-1)

try:
    from lib.console import Console
except ImportError, e:
    exit(-1)

try:
    from lib.config import Config
    from lib.config import TESTCFG_FAIL
    from lib.config import TESTCFG_SUC
except ImportError, e:
    wx.MessageBox(u"当前没有加载到lib/config中的Config对象，请检查", u"警告", wx.OK | wx.ICON_INFORMATION)
    exit(-1)

try:
    from lib.thunder_controller import Thunder
except ImportError, e:
    wx.MessageBox(u"当前没有加载到lib/thunder_controller中的Thunder对象，请检查", u"警告", wx.OK | wx.ICON_INFORMATION)
    exit(-1)

try:
    from lib.Keygoe import *
except ImportError, e:
    wx.MessageBox(u"当前没有加载到lib/keygoe中的keygoe对象，请检查", u"警告", wx.OK | wx.ICON_INFORMATION)
    exit(-1)
try:
    from user_lib.HTTP_send import *
except ImportError, e:
    exit(-1)

try:
    from lib.chariot.ChariotATT import ChariotATT
except ImportError, e:
    exit(-1)


class App(wx.App):
    @pysnooper.snoop("D:\\oninit.log")
    def OnInit(self):
        slogan = u"测试之路，路长而岐"
        try:
            bmp = wx.Image("./img/welcome.jpg", wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
            wx.SplashScreen(bmp, wx.SPLASH_CENTER_ON_SCREEN | wx.SPLASH_TIMEOUT, 3000, None, -1)
            wx.Yield()
        except Exception, e:
            raise RuntimeWarning(u"欢迎图片是被你吃了么....")
        try:
            frame = MainFrame(None)
        except Exception, e:
            wx.MessageBox(u"MainFrame没有实例化成功，请检查", u"警告", wx.OK | wx.ICON_INFORMATION)
            exit(-1)
        sleep(4)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True


###########################################################################
## Class MainFrame
## 程序主界面
## 作者：张斌
###########################################################################

class MainFrame(wx.Frame):

    def __init__(self, parent):
        self.parent = parent
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"ONU业务恢复性能测试工具", pos=wx.DefaultPosition,
                          size=wx.Size(862, 600), style=wx.DEFAULT_FRAME_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False, "微软雅黑"))
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        # try:

        #     from lib.get_os_info import Get_system_info
        #     self.sys_info_obj = Get_system_info()
        #     self.sys_arh_obj = self.sys_info_obj.get_system_architecture()
        #     self.sys_info_obj.get_network_info()
        #     self.sys_info_obj.get_cpu_info()
        #     self.sys_info_obj.get_memory_info()
        #     self.sys_info_obj.get_system_info()
        #     self.nic_mac_list = self.sys_info_obj.get_network_mac_info()
        # except Exception, e:
        #     raise RuntimeError(u"get_os_info.py不会被你给吃了吧.......")

        # 各配置初始化
        self.config_obj = Config()
        self.config_obj.dut_config_file = os.getcwd() + "\\conf\\dut_config.json"
        self.config_obj.tr069_config_file = os.getcwd() + "\\conf\\TR069_config.json"
        self.config_obj.voip_config_file = os.getcwd() + "\\conf\\VoIP_config.json"
        self.config_obj.iptv_config_file = os.getcwd() + "\\conf\\IPTV_config.json"
        self.config_obj.internet_config_file = os.getcwd() + "\\conf\\Internet_config.json"
        self.config_obj.wlan_config_file = os.getcwd() + "\\conf\\WLAN_config.json"
        self.config_obj.power_config_file = os.getcwd() + "\\conf\\power_config.json"
        self.test_cfg_suc = TESTCFG_SUC
        self.test_cfg_fail = TESTCFG_FAIL
        self.dut_cfg = {}
        self.tr069_cfg = {}
        self.voip_cfg = {}
        self.iptv_cfg = {}
        self.internet_cfg = {}
        self.wlan_cfg = {}
        self.success_count = 0
        self.tested_times = 0
        self.console_log_file = os.getcwd() + "\\log\\serial_%s.log" % (time.strftime('%y %m %d', time.localtime()))
        self.error_log_file = os.getcwd() + "\\log\\error.log"
        self.restore_time_file = os.getcwd() + "\\log\\restore_time"
        self.tw_icon = './img/tw.ico'

        self.logger_pipe = mp.Pipe()
        self.record_file = os.getcwd() + "\\log\\voip\\"

        # 创建菜单
        self.m_menubar1 = wx.MenuBar(0)
        self.m_menubar1.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False,
                    "微软雅黑"))

        self.opration = wx.Menu()
        self.start_menu = wx.MenuItem(self.opration, wx.ID_ANY, u"开始", u"开始执行预定义的测试行为", wx.ITEM_NORMAL)
        self.start_menu.SetBitmap(wx.Bitmap(u"F:\\MS_Restore_Test\\trunk\\img\\start1.ico", wx.BITMAP_TYPE_ANY))
        self.opration.Append(self.start_menu)

        self.opration.AppendSeparator()

        self.stop_menu = wx.MenuItem(self.opration, wx.ID_ANY, u"停止", u"停止已经在执行中的测试行为", wx.ITEM_NORMAL)
        self.stop_menu.SetBitmap(wx.Bitmap(u"F:\\MS_Restore_Test\\trunk\\img\\Stop2.ico", wx.BITMAP_TYPE_ANY))
        self.opration.Append(self.stop_menu)

        self.opration.AppendSeparator()

        self.save_menu = wx.MenuItem(self.opration, wx.ID_ANY, u"保存", u"保存当前日志框中的日志到文件", wx.ITEM_NORMAL)
        self.save_menu.SetBitmap(wx.Bitmap(u"F:\\MS_Restore_Test\\trunk\\img\\Save.ico", wx.BITMAP_TYPE_ANY))
        self.opration.Append(self.save_menu)

        self.opration.AppendSeparator()

        self.exit_menu = wx.MenuItem(self.opration, wx.ID_ANY, u"退出", u"退出", wx.ITEM_NORMAL)
        self.exit_menu.SetBitmap(wx.Bitmap(u"F:\\MS_Restore_Test\\trunk\\img\\exit.ico", wx.BITMAP_TYPE_ANY))
        self.opration.Append(self.exit_menu)

        self.m_menubar1.Append(self.opration, u"操作")

        self.configuration = wx.Menu()
        self.dut_cfg_menu = wx.MenuItem(self.configuration, wx.ID_ANY, u"DUT配置", wx.EmptyString, wx.ITEM_NORMAL)
        self.dut_cfg_menu.SetBitmap(wx.Bitmap(u"F:\\MS_Restore_Test\\trunk\\img\\DUT.ico", wx.BITMAP_TYPE_ANY))
        self.configuration.Append(self.dut_cfg_menu)

        self.configuration.AppendSeparator()

        self.tr069_cfg_menu = wx.MenuItem(self.configuration, wx.ID_ANY, u"TR069业务配置", wx.EmptyString, wx.ITEM_NORMAL)
        self.tr069_cfg_menu.SetBitmap(wx.Bitmap(u"F:\\MS_Restore_Test\\trunk\\img\\ACS.ico", wx.BITMAP_TYPE_ANY))
        self.configuration.Append(self.tr069_cfg_menu)

        self.configuration.AppendSeparator()

        self.voip_cfg_menu = wx.MenuItem(self.configuration, wx.ID_ANY, u"VoIP业务配置", wx.EmptyString, wx.ITEM_NORMAL)
        self.voip_cfg_menu.SetBitmap(wx.Bitmap(u"F:\\MS_Restore_Test\\trunk\\img\\VOIP.ico", wx.BITMAP_TYPE_ANY))
        self.configuration.Append(self.voip_cfg_menu)

        self.configuration.AppendSeparator()

        self.iptv_cfg_menu = wx.MenuItem(self.configuration, wx.ID_ANY, u"IPTV业务配置", wx.EmptyString, wx.ITEM_NORMAL)
        self.iptv_cfg_menu.SetBitmap(wx.Bitmap(u"F:\\MS_Restore_Test\\trunk\\img\\IPTV.ico", wx.BITMAP_TYPE_ANY))
        self.configuration.Append(self.iptv_cfg_menu)

        self.configuration.AppendSeparator()

        self.internet_cfg_menu = wx.MenuItem(self.configuration, wx.ID_ANY, u"Internet业务配置", wx.EmptyString,
                                             wx.ITEM_NORMAL)
        self.internet_cfg_menu.SetBitmap(
            wx.Bitmap(u"F:\\MS_Restore_Test\\trunk\\img\\internet.ico", wx.BITMAP_TYPE_ANY))
        self.configuration.Append(self.internet_cfg_menu)

        self.configuration.AppendSeparator()

        self.wlan_cfg_menu = wx.MenuItem(self.configuration, wx.ID_ANY, u"Wlan业务配置", wx.EmptyString, wx.ITEM_NORMAL)
        self.wlan_cfg_menu.SetBitmap(wx.Bitmap(u"F:\\MS_Restore_Test\\trunk\\img\\wlan.ico", wx.BITMAP_TYPE_ANY))
        self.configuration.Append(self.wlan_cfg_menu)

        self.configuration.AppendSeparator()

        self.power_cfg_menu = wx.MenuItem(self.configuration, wx.ID_ANY, u"继电器设置", wx.EmptyString, wx.ITEM_NORMAL)
        self.power_cfg_menu.SetBitmap(wx.Bitmap(u"F:\\MS_Restore_Test\\trunk\\img\\power.ico", wx.BITMAP_TYPE_ANY))
        self.configuration.Append(self.power_cfg_menu)

        self.m_menubar1.Append(self.configuration, u"配置")

        self.help = wx.Menu()
        self.help_menu = wx.MenuItem(self.help, wx.ID_ANY, u"帮助", wx.EmptyString, wx.ITEM_NORMAL)
        self.help_menu.SetBitmap(wx.Bitmap(u"F:\\MS_Restore_Test\\trunk\\img\\help.ico", wx.BITMAP_TYPE_ANY))
        self.help.Append(self.help_menu)

        self.help.AppendSeparator()

        self.version_info_menu = wx.MenuItem(self.help, wx.ID_ANY, u"版本信息", wx.EmptyString, wx.ITEM_NORMAL)
        self.version_info_menu.SetBitmap(wx.Bitmap(u"F:\\MS_Restore_Test\\trunk\\img\\notes.ico", wx.BITMAP_TYPE_ANY))
        self.help.Append(self.version_info_menu)

        self.m_menubar1.Append(self.help, u"帮助")

        self.SetMenuBar(self.m_menubar1)

        # 创建工具栏
        self.m_toolBar2 = self.CreateToolBar(wx.TB_HORIZONTAL, wx.ID_ANY)
        self.m_toolBar2.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False,
                    "微软雅黑"))
        self.m_toolBar2.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))

        self.start_tool = self.m_toolBar2.AddLabelTool(wx.ID_ANY, u"start",
                                                       wx.Bitmap(u"F:\\MS_Restore_Test\\trunk\\img\\Start.ico",
                                                                 wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL,
                                                       wx.EmptyString, wx.EmptyString, None)

        self.m_toolBar2.AddSeparator()

        self.stop_tool = self.m_toolBar2.AddLabelTool(wx.ID_ANY, u"stop",
                                                      wx.Bitmap(u"F:\\MS_Restore_Test\\trunk\\img\\stop.ico",
                                                                wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL,
                                                      wx.EmptyString, wx.EmptyString, None)

        self.m_toolBar2.Realize()

        # 创建checkbox栏
        gSizer4 = wx.GridSizer(0, 2, 0, 0)

        sbSizer11 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"业务类型"), wx.VERTICAL)

        self.tr069_checkBox = wx.CheckBox(sbSizer11.GetStaticBox(), wx.ID_ANY, u"TR069业务", wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        self.tr069_checkBox.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False,
                    "微软雅黑"))

        sbSizer11.Add(self.tr069_checkBox, 0, wx.ALL, 5)

        self.voip_checkBox = wx.CheckBox(sbSizer11.GetStaticBox(), wx.ID_ANY, u"VoIP业务", wx.DefaultPosition,
                                         wx.DefaultSize,
                                         0)
        self.voip_checkBox.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False,
                    "微软雅黑"))

        sbSizer11.Add(self.voip_checkBox, 0, wx.ALL, 5)

        self.iptv_checkBox = wx.CheckBox(sbSizer11.GetStaticBox(), wx.ID_ANY, u"IPTV业务", wx.DefaultPosition,
                                         wx.DefaultSize,
                                         0)
        self.iptv_checkBox.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False,
                    "微软雅黑"))

        sbSizer11.Add(self.iptv_checkBox, 0, wx.ALL, 5)

        self.ping_internet_checkBox = wx.CheckBox(sbSizer11.GetStaticBox(), wx.ID_ANY, u"PING外网业务", wx.DefaultPosition,
                                                  wx.DefaultSize, 0)
        self.ping_internet_checkBox.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False,
                    "微软雅黑"))

        sbSizer11.Add(self.ping_internet_checkBox, 0, wx.ALL, 5)

        self.smart_checkBox = wx.CheckBox(sbSizer11.GetStaticBox(), wx.ID_ANY, u"智能业务", wx.DefaultPosition,
                                          wx.DefaultSize,
                                          0)
        self.smart_checkBox.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False,
                    "微软雅黑"))

        sbSizer11.Add(self.smart_checkBox, 0, wx.ALL, 5)

        self.http_checkBox = wx.CheckBox(sbSizer11.GetStaticBox(), wx.ID_ANY, u"HTTP业务", wx.DefaultPosition,
                                         wx.DefaultSize,
                                         0)
        self.http_checkBox.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False,
                    "微软雅黑"))

        sbSizer11.Add(self.http_checkBox, 0, wx.ALL, 5)

        self.ftp_checkBox = wx.CheckBox(sbSizer11.GetStaticBox(), wx.ID_ANY, u"FTP业务", wx.DefaultPosition,
                                        wx.DefaultSize,
                                        0)
        self.ftp_checkBox.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False,
                    "微软雅黑"))

        sbSizer11.Add(self.ftp_checkBox, 0, wx.ALL, 5)

        self.sta_ping_checkBox = wx.CheckBox(sbSizer11.GetStaticBox(), wx.ID_ANY, u"STA PING", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.sta_ping_checkBox.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False,
                    "微软雅黑"))

        sbSizer11.Add(self.sta_ping_checkBox, 0, wx.ALL, 5)

        self.chariot_checkBox = wx.CheckBox(sbSizer11.GetStaticBox(), wx.ID_ANY, u"Chariot Test", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.chariot_checkBox.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False,
                    "微软雅黑"))

        sbSizer11.Add(self.chariot_checkBox, 0, wx.ALL, 5)

        # 创建基本信息栏
        sbSizer13 = wx.StaticBoxSizer(wx.StaticBox(sbSizer11.GetStaticBox(), wx.ID_ANY, u"基本信息"), wx.VERTICAL)

        fgSizer5 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer5.SetFlexibleDirection(wx.BOTH)
        fgSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.timeout_staticText = wx.StaticText(sbSizer13.GetStaticBox(), wx.ID_ANY, u"业务超时时长", wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        self.timeout_staticText.Wrap(-1)

        self.timeout_staticText.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False,
                    "微软雅黑"))

        fgSizer5.Add(self.timeout_staticText, 0, wx.ALL, 5)

        self.m_panel4 = wx.Panel(sbSizer13.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                 wx.TAB_TRAVERSAL)
        self.m_panel4.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False,
                    "微软雅黑"))

        fgSizer5.Add(self.m_panel4, 1, wx.EXPAND | wx.ALL, 5)

        self.power_staticText = wx.StaticText(sbSizer13.GetStaticBox(), wx.ID_ANY, u"断电次数", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.power_staticText.Wrap(-1)

        self.power_staticText.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False,
                    "微软雅黑"))

        fgSizer5.Add(self.power_staticText, 0, wx.ALL, 5)

        self.m_textCtrl1 = wx.TextCtrl(sbSizer13.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.m_textCtrl1.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False,
                    "微软雅黑"))

        fgSizer5.Add(self.m_textCtrl1, 0, wx.ALL, 5)

        sbSizer13.Add(fgSizer5, 1, wx.EXPAND, 5)

        sbSizer11.Add(sbSizer13, 1, wx.EXPAND, 5)

        gSizer4.Add(sbSizer11, 1, wx.EXPAND, 5)

        # 创建程序执行栏
        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        excute_log = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"程序执行LOG"), wx.VERTICAL)

        self.m_panel1 = wx.Panel(excute_log.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                 wx.TAB_TRAVERSAL)
        self.m_panel1.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False,
                    "微软雅黑"))
        self.m_panel1.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))

        excute_log.Add(self.m_panel1, 1, wx.EXPAND | wx.ALL, 5)

        bSizer2.Add(excute_log, 1, wx.EXPAND, 5)

        srial_log = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"串口打印LOG"), wx.VERTICAL)

        self.m_panel2 = wx.Panel(srial_log.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                 wx.TAB_TRAVERSAL)
        self.m_panel2.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False,
                    "微软雅黑"))
        self.m_panel2.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))

        srial_log.Add(self.m_panel2, 1, wx.EXPAND | wx.ALL, 5)

        bSizer2.Add(srial_log, 1, wx.EXPAND, 5)

        chart = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"重启恢复性能折线图"), wx.VERTICAL)

        self.m_panel3 = wx.Panel(chart.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel3.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False,
                    "微软雅黑"))
        self.m_panel3.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))

        chart.Add(self.m_panel3, 1, wx.EXPAND | wx.ALL, 5)

        bSizer2.Add(chart, 1, wx.EXPAND, 5)

        gSizer4.Add(bSizer2, 1, wx.EXPAND, 5)

        # 创建状态栏
        self.SetSizer(gSizer4)
        self.Layout()
        self.m_statusBar2 = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)
        self.m_statusBar2.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False,
                    "微软雅黑"))

        self.Centre(wx.VERTICAL)
        # 状态线程

        self.event_log = threading.Event()
        self.event_start = threading.Event()
        self.event_tr069_start = threading.Event()
        self.event_voip_start = threading.Event()
        self.event_iptv_start = threading.Event()
        self.event_ping_start = threading.Event()
        self.event_smart_start = threading.Event()
        self.event_http_start = threading.Event()
        self.event_ftp_start = threading.Event()
        self.event_staping_start = threading.Event()
        self.event_chariot_start = threading.Event()
        self.event_log_lock = threading.Lock()

        self.error_times = 0
        self.suc_rate = 0

        # 定义行为
        self.Bind(wx.EVT_MENU, self.on_start, id=self.start_menu.GetId())
        self.Bind(wx.EVT_MENU, self.on_stop, id=self.stop_menu.GetId())
        self.Bind(wx.EVT_MENU, self.on_save, id=self.save_menu.GetId())
        self.Bind(wx.EVT_MENU, self.on_exit, id=self.exit_menu.GetId())
        self.Bind(wx.EVT_MENU, self.on_dut_cfg, id=self.dut_cfg_menu.GetId())
        self.Bind(wx.EVT_MENU, self.on_tr069_cfg, id=self.tr069_cfg_menu.GetId())
        self.Bind(wx.EVT_MENU, self.on_voip_cfg, id=self.voip_cfg_menu.GetId())
        self.Bind(wx.EVT_MENU, self.on_iptv_cfg, id=self.iptv_cfg_menu.GetId())
        self.Bind(wx.EVT_MENU, self.on_internet_cfg, id=self.internet_cfg_menu.GetId())
        self.Bind(wx.EVT_MENU, self.on_wlan_cfg, id=self.wlan_cfg_menu.GetId())
        self.Bind(wx.EVT_MENU, self.on_power_cfg, id=self.power_cfg_menu.GetId())
        self.Bind(wx.EVT_MENU, self.on_help, id=self.help_menu.GetId())
        self.Bind(wx.EVT_MENU, self.on_version_info, id=self.version_info_menu.GetId())
        self.Bind(wx.EVT_TOOL, self.on_start, id=self.start_tool.GetId())
        self.Bind(wx.EVT_TOOL, self.on_stop, id=self.stop_tool.GetId())
        self.tr069_checkBox.Bind(wx.EVT_CHECKBOX, self.enable_tr069)
        self.voip_checkBox.Bind(wx.EVT_CHECKBOX, self.enable_voip)
        self.iptv_checkBox.Bind(wx.EVT_CHECKBOX, self.enable_iptv)
        self.ping_internet_checkBox.Bind(wx.EVT_CHECKBOX, self.enable_ping_internet)
        self.smart_checkBox.Bind(wx.EVT_CHECKBOX, self.enable_smart)
        self.http_checkBox.Bind(wx.EVT_CHECKBOX, self.enable_http)
        self.ftp_checkBox.Bind(wx.EVT_CHECKBOX, self.enable_ftp)
        self.sta_ping_checkBox.Bind(wx.EVT_CHECKBOX, self.enable_sta_ping)
        self.chariot_checkBox.Bind(wx.EVT_CHECKBOX, self.enable_chariot)
        self.m_panel1.Bind(wx.EVT_CHAR, self.excute_log)
        self.m_panel2.Bind(wx.EVT_CHAR, self.serial_log)
        self.m_panel3.Bind(wx.EVT_CHAR, self.chart_log)

        self.start_status = False

        # 加载各项配置参数
        try:
            n_ret, str_ret = self.config_obj.load_dut_cfg()
            if n_ret == TESTCFG_SUC:
                self.dut_cfg = self.config_obj.dut_dict_config_items
            else:
                self.dut_cfg = {}
        except Exception, e:
            self.dut_cfg = {}
            wx.MessageBox(u"DUT配置初始化失败，请检查配置菜单中是否正常", u"警告", wx.OK | wx.ICON_INFORMATION)

        try:
            n_ret, str_ret = self.config_obj.load_tr069_cfg()
            if n_ret == TESTCFG_SUC:
                self.tr069_cfg = self.config_obj.tr069_dict_config_items
            else:
                self.tr069_cfg = {}
        except Exception, e:
            self.tr069_cfg = {}
            wx.MessageBox(u"DUT配置初始化失败，请检查配置菜单中是否正常", u"警告", wx.OK | wx.ICON_INFORMATION)

        try:
            n_ret, str_ret = self.config_obj.load_voip_cfg()
            if n_ret == TESTCFG_SUC:
                self.voip_cfg = self.config_obj.voip_dict_config_items
            else:
                self.voip_cfg = {}
        except Exception, e:
            self.voip_cfg = {}
            wx.MessageBox(u"DUT配置初始化失败，请检查配置菜单中是否正常", u"警告", wx.OK | wx.ICON_INFORMATION)

        try:
            n_ret, str_ret = self.config_obj.load_iptv_cfg()
            if n_ret == TESTCFG_SUC:
                self.iptv_cfg = self.config_obj.iptv_dict_config_items
            else:
                self.iptv_cfg = {}
        except Exception, e:
            self.iptv_cfg = {}
            wx.MessageBox(u"DUT配置初始化失败，请检查配置菜单中是否正常", u"警告", wx.OK | wx.ICON_INFORMATION)

        try:
            n_ret, str_ret = self.config_obj.load_internet_cfg()
            if n_ret == TESTCFG_SUC:
                self.internet_cfg = self.config_obj.internet_dict_config_items
            else:
                self.internet_cfg = {}
        except Exception, e:
            self.internet_cfg = {}
            wx.MessageBox(u"DUT配置初始化失败，请检查配置菜单中是否正常", u"警告", wx.OK | wx.ICON_INFORMATION)

        try:
            n_ret, str_ret = self.config_obj.load_wlan_cfg()
            if n_ret == TESTCFG_SUC:
                self.wlan_cfg = self.config_obj.wlan_dict_config_items
            else:
                self.wlan_cfg = {}
        except Exception, e:
            self.wlan_cfg = {}
            wx.MessageBox(u"DUT配置初始化失败，请检查配置菜单中是否正常", u"警告", wx.OK | wx.ICON_INFORMATION)

        try:
            n_ret, str_ret = self.config_obj.load_power_cfg()
            if n_ret == TESTCFG_SUC:
                self.power_cfg = self.config_obj.power_dict_config_items
            else:
                self.power_cfg = {}
        except Exception, e:
            self.power_cfg = {}
            wx.MessageBox(u"DUT配置初始化失败，请检查配置菜单中是否正常", u"警告", wx.OK | wx.ICON_INFORMATION)

    # 行为定义

    def on_start(self, event):
        event.Skip()

    def on_stop(self, event):
        event.Skip()

    def on_save(self, event):
        event.Skip()

    def on_exit(self, event):
        event.Skip()

    def on_dut_cfg(self, event):
        event.Skip()

    def on_tr069_cfg(self, event):
        event.Skip()

    def on_voip_cfg(self, event):
        event.Skip()

    def on_iptv_cfg(self, event):
        event.Skip()

    def on_internet_cfg(self, event):
        event.Skip()

    def on_wlan_cfg(self, event):
        event.Skip()

    def on_power_cfg(self, event):
        event.Skip()

    def on_help(self, event):
        event.Skip()

    def on_version_info(self, event):
        event.Skip()

    def enable_tr069(self, event):
        event.Skip()

    def enable_voip(self, event):
        event.Skip()

    def enable_iptv(self, event):
        event.Skip()

    def enable_ping_internet(self, event):
        event.Skip()

    def enable_smart(self, event):
        event.Skip()

    def enable_http(self, event):
        event.Skip()

    def enable_ftp(self, event):
        event.Skip()

    def enable_sta_ping(self, event):
        event.Skip()

    def enable_chariot(self, event):
        event.Skip()

    def excute_log(self, event):
        event.Skip()

    def serial_log(self, event):
        event.Skip()

    def chart_log(self, event):
        event.Skip()

    def get_static_log_header(self):
        self.text_log_info.AppendText(u"系统日志:\n")
        self.text_log_info.AppendText(u"当前系统版本:%s\n" % self.sys_info_obj.system_obj['Version'])
        self.text_log_info.AppendText(u"当前系统序列号:%s\n" % self.sys_info_obj.system_obj['Vernum'])
        # self.text_log_info.AppendText(u"当前主机名称为:%s\n" % self.host_name)
        self.text_log_info.AppendText(u"当前CPU类型:%s\n" % self.sys_info_obj.cpu_obj['CpuType'])
        self.text_log_info.AppendText(u"当前CPU的主频:%s\n" % self.sys_info_obj.cpu_obj['CpuClock'])
        self.text_log_info.AppendText(u"当前CPU核数:%d\n" % self.sys_info_obj.cpu_obj['CpuCores'])
        self.text_log_info.AppendText(u"当前主机内存容量:%d\n" % self.sys_info_obj.memory_obj['TotalPhysicalMemory'])
        cpu_clock_total = int(self.sys_info_obj.cpu_obj['CpuClock']) * int(self.sys_info_obj.cpu_obj['CpuCores'])
        if cpu_clock_total > 4000 and int(self.sys_info_obj.memory_obj['TotalPhysicalMemory']) > 3000:
            self.text_log_info.AppendText(u"当前主机的配置可以~\n")
        else:
            self.text_log_info.AppendText(u"当前主机的配置较差，可能会影响任务的执行\n")

    def log(self, str):
        try:
            str.decode('utf8')
        except UnicodeDecodeError, e:
            print e
        self.event_log_lock.acquire()
        try:
            with open(".\\log\\log.txt", "a+") as f:
                f.write(ctime() + str + "\n")
                f.close()
        except Exception, e:
            with open(".\\log\\error.log", 'a+') as f:
                f.write(ctime() + e)
                f.close()
        try:
            self.text_log_info.AppendText("%s\n" % str)
        except Exception, e:
            with open(".\\log\\error.log", 'a+') as f:
                f.write(ctime() + e)
                f.close()
        self.event_log_lock.release()

    def logger_reader(self):
        self.event_log.clear()
        self.event_log.set()
        while self.start_status:  # 只要是开始状态，就一直不停地读取管道中的信息
            try:
                log = str(self.logger_pipe[0].recv())
            except EOFError, e:
                self.log(u"%s: %s" % (ctime(), u"出现了EOF"))
            try:
                log.decode('utf8')
            except UnicodeDecodeError, e:
                self.log(u"%s: %s" % (ctime(), u"Log解析失败"))
                continue
            if len(log):  # 如果长度不是空的话，就写入文本框中
                self.log(u"%s: %s" % (ctime(), log))

    def __del__(self):
        pass


if __name__ == '__main__':
    app = App()
    app.MainLoop()
