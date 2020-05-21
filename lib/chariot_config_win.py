# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class dut_config
###########################################################################

class chariot_config(wx.Frame):

    def __init__(self, parent):
        self.config_obj = None
        self.chariot_cfg = {}
        self.test_cfg_suc = None
        self.ico = None
        self.config_win_text_ctrl_width = 200
        self.config_win_text_ctrl_hight = 20
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Chariot配置", pos=wx.DefaultPosition, size=wx.Size(700, 400),
                          style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_NO_TASKBAR | wx.FRAME_SHAPED | wx.TAB_TRAVERSAL)
                          #style=wx.CAPTION | wx.SYSTEM_MENU | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        vbox_config = wx.BoxSizer(wx.VERTICAL)
        radioBox_is_testChoices = [u"是", u"否"]
        self.radioBox_is_test = wx.RadioBox(self, wx.ID_ANY, u"是否测试", wx.DefaultPosition,
                                            wx.DefaultSize, radioBox_is_testChoices, 2, wx.RA_SPECIFY_COLS)
        self.radioBox_is_test.SetSelection(0)
        vbox_config.Add(self.radioBox_is_test, 0, wx.ALL, 5)

        vbox_chariot_config = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Chariot相关配置"), wx.VERTICAL)

        vbox_chariot_config.SetMinSize(wx.Size(100, 60))
        bSizer45 = wx.BoxSizer(wx.VERTICAL)

        hbox_endpoint_config = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, u"Endpoint配置"), wx.HORIZONTAL)

        self.label_local_endpoint = wx.StaticText(self, wx.ID_ANY, u"本端IP",
                                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_local_endpoint.Wrap(-1)
        hbox_endpoint_config.Add(self.label_local_endpoint, 0, wx.ALL, 5)

        self.text_local_endpoint = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        hbox_endpoint_config.Add(self.text_local_endpoint, 0, wx.ALL, 5)

        self.label_remote_endpoint = wx.StaticText(self, wx.ID_ANY, u"远端IP",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_remote_endpoint.Wrap(-1)
        hbox_endpoint_config.Add(self.label_remote_endpoint, 0, wx.ALL, 5)

        self.text_remote_endpoint = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        hbox_endpoint_config.Add(self.text_remote_endpoint, 0, wx.ALL, 5)

        bSizer45.Add(hbox_endpoint_config, 1, wx.EXPAND, 5)

        vbox_chariot_config.Add(bSizer45, 1, wx.EXPAND, 5)

        bSizer46 = wx.BoxSizer(wx.VERTICAL)

        vbox_chariot_basic = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, u"Chariot基本配置"), wx.VERTICAL)

        hbox_chariot_basic = wx.BoxSizer(wx.HORIZONTAL)

        self.label_flow_count = wx.StaticText(self, wx.ID_ANY, u"流数目", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.label_flow_count.Wrap(-1)
        hbox_chariot_basic.Add(self.label_flow_count, 0, wx.ALL, 5)

        self.spin_flow_count = wx.SpinCtrl(self, wx.ID_ANY, u"8", wx.DefaultPosition,
                                           wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 8)
        hbox_chariot_basic.Add(self.spin_flow_count, 0, wx.ALL, 5)

        self.label_chariot_time = wx.StaticText(self, wx.ID_ANY, u"持续时间",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_chariot_time.Wrap(-1)
        hbox_chariot_basic.Add(self.label_chariot_time, 0, wx.ALL, 5)

        self.spin_chariot_flow_time = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 65535, 0)
        hbox_chariot_basic.Add(self.spin_chariot_flow_time, 0, wx.ALL, 5)

        self.label_second = wx.StaticText(self, wx.ID_ANY, u"（秒）", wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        self.label_second.Wrap(-1)
        hbox_chariot_basic.Add(self.label_second, 0, wx.ALL, 5)

        self.label_chariot_protocol = wx.StaticText(self, wx.ID_ANY, u"协议",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_chariot_protocol.Wrap(-1)
        hbox_chariot_basic.Add(self.label_chariot_protocol, 0, wx.ALL, 5)

        combo_chariot_protocolChoices = [u"TCP", u"UDP", wx.EmptyString]
        self.combo_chariot_protocol = wx.ComboBox(self, wx.ID_ANY, u"TCP",
                                                  wx.DefaultPosition, wx.DefaultSize, combo_chariot_protocolChoices, 0)
        hbox_chariot_basic.Add(self.combo_chariot_protocol, 0, wx.ALL, 5)

        vbox_chariot_basic.Add(hbox_chariot_basic, 1, wx.EXPAND, 5)

        hbox_chariot_flow_config = wx.BoxSizer(wx.HORIZONTAL)

        vbox_flow_script = wx.BoxSizer(wx.VERTICAL)

        hbox_tcp_script = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText34 = wx.StaticText(self, wx.ID_ANY, u"TCP脚本", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText34.Wrap(-1)
        hbox_tcp_script.Add(self.m_staticText34, 0, wx.ALL, 5)

        combo_tcp_scriptChoices = [u"High_Performance_Throughput.scr", u"Throughput.scr"]
        self.combo_tcp_script = wx.ComboBox(self, wx.ID_ANY,
                                            u"High_Performance_Throughput.scr", wx.DefaultPosition, wx.DefaultSize,
                                            combo_tcp_scriptChoices, 0)
        self.combo_tcp_script.SetSelection(0)
        hbox_tcp_script.Add(self.combo_tcp_script, 0, wx.ALL, 5)

        vbox_flow_script.Add(hbox_tcp_script, 1, wx.EXPAND, 5)

        hbox_udp_script = wx.BoxSizer(wx.HORIZONTAL)

        self.label_chariot_udp = wx.StaticText(self, wx.ID_ANY, u"UDP脚本",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_chariot_udp.Wrap(-1)
        hbox_udp_script.Add(self.label_chariot_udp, 0, wx.ALL, 5)

        combo_tcp_script1Choices = [u"High_Performance_Throughput_UDP.scr", u"Throughput.scr"]
        self.combo_udp_script = wx.ComboBox(self, wx.ID_ANY,
                                             u"High_Performance_Throughput_UDP.scr", wx.DefaultPosition, wx.DefaultSize,
                                             combo_tcp_script1Choices, 0)
        self.combo_udp_script.SetSelection(0)
        hbox_udp_script.Add(self.combo_udp_script, 0, wx.ALL, 5)

        vbox_flow_script.Add(hbox_udp_script, 1, wx.EXPAND, 5)

        hbox_chariot_flow_config.Add(vbox_flow_script, 1, wx.EXPAND, 5)

        hbox_test_mode = wx.BoxSizer(wx.HORIZONTAL)

        radioBox_test_modeChoices = [u"TX", u"RX", u"TX+RX"]
        self.radioBox_test_mode = wx.RadioBox(self, wx.ID_ANY, u"测试模式", wx.DefaultPosition,
                                              wx.DefaultSize, radioBox_test_modeChoices, 3, wx.RA_SPECIFY_COLS)
        self.radioBox_test_mode.SetSelection(1)
        hbox_test_mode.Add(self.radioBox_test_mode, 0, wx.ALL, 5)

        hbox_chariot_flow_config.Add(hbox_test_mode, 1, wx.EXPAND, 5)

        vbox_chariot_basic.Add(hbox_chariot_flow_config, 1, wx.EXPAND, 5)

        bSizer46.Add(vbox_chariot_basic, 1, wx.EXPAND, 5)

        vbox_chariot_config.Add(bSizer46, 1, wx.EXPAND, 5)

        vbox_config.Add(vbox_chariot_config, 1, wx.EXPAND | wx.FIXED_MINSIZE, 5)

        btn_config = wx.BoxSizer(wx.VERTICAL)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"保存配置", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button2.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        btn_config.Add(self.m_button2, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        vbox_config.Add(btn_config, 1, wx.ALIGN_CENTER | wx.EXPAND, 5)

        self.SetSizer(vbox_config)
        self.Layout()
        # Connect Events
        self.m_button2.Bind(wx.EVT_BUTTON, self.on_dut_config_submit)

    def window_show(self):
        try:
            self.radioBox_is_test.SetSelection(int(self.chariot_cfg['is_test']))
            self.text_local_endpoint.SetValue(self.chariot_cfg['local_endpoint'])
            self.text_remote_endpoint.SetValue(self.chariot_cfg['remote_endpoint'])
            self.spin_flow_count.SetValue(int(self.chariot_cfg['flow_count']))
            self.spin_chariot_flow_time.SetValue(int(self.chariot_cfg['flow_time']))
            self.combo_chariot_protocol.SetValue(self.chariot_cfg['flow_protocol'])
            self.combo_tcp_script.SetValue(self.chariot_cfg['tcp_script'])
            self.combo_udp_script.SetValue(self.chariot_cfg['udp_script'])
            self.radioBox_test_mode.SetSelection(int(self.chariot_cfg['test_mode']))
        except Exception, e:
            print e
            wx.MessageBox(u"Chariot配置初始化失败，请检查配置菜单中是否正常", u"警告", wx.OK | wx.ICON_INFORMATION)
        self.SetIcon(self.ico)
        self.Centre(wx.BOTH)
        self.Show(True)
        self.Fit()

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def on_dut_config_submit(self, event):
        dict_config_items = {}
        dict_config_items['is_test'] = self.radioBox_is_test.GetSelection()
        dict_config_items['local_endpoint'] = self.text_local_endpoint.GetValue()
        dict_config_items['remote_endpoint'] = self.text_remote_endpoint.GetValue()
        dict_config_items['flow_count'] = self.spin_flow_count.GetValue()
        dict_config_items['flow_time'] = self.spin_chariot_flow_time.GetValue()
        dict_config_items['flow_protocol'] = self.combo_chariot_protocol.GetValue()
        dict_config_items['tcp_script'] = self.combo_tcp_script.GetValue()
        dict_config_items['udp_script'] = self.combo_udp_script.GetValue()
        dict_config_items['test_mode'] = self.radioBox_test_mode.GetSelection()
        event.Skip()
        n_ret, str_ret = self.config_obj.save_chariot_cfg(dict_config_items)

        if n_ret == self.test_cfg_suc:
            self.chariot_cfg = dict_config_items
        self.Close()


