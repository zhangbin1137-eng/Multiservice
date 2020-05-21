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

class dut_config(wx.Frame):

    def __init__(self, parent):
        self.config_obj = None
        self.dut_cfg = {}
        self.test_cfg_suc = None
        self.ico = None
        self.config_win_text_ctrl_width = 200
        self.config_win_text_ctrl_hight = 20
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"DUT配置", pos=wx.DefaultPosition, size=wx.Size(500, 700),
                          style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_NO_TASKBAR | wx.FRAME_SHAPED | wx.TAB_TRAVERSAL)
                          #style=wx.CAPTION | wx.SYSTEM_MENU | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        vbox_config = wx.BoxSizer(wx.VERTICAL)

        general_config = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"通用配置"), wx.VERTICAL)

        hbox_general_ip_config = wx.BoxSizer(wx.HORIZONTAL)

        self.general_ip_config = wx.StaticText(self, wx.ID_ANY, u"DUT IP", wx.DefaultPosition,
                                               wx.DefaultSize, 0)
        self.general_ip_config.Wrap(-1)
        hbox_general_ip_config.Add(self.general_ip_config, 0, wx.ALL, 5)

        self.text_general_ip = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.text_general_ip.SetMinSize(wx.Size(self.config_win_text_ctrl_width, self.config_win_text_ctrl_hight))
        hbox_general_ip_config.Add(self.text_general_ip, 0, wx.ALL, 5)

        general_config.Add(hbox_general_ip_config, 1, wx.EXPAND, 5)

        hbox_general_submask = wx.BoxSizer(wx.HORIZONTAL)

        self.label_general_submask = wx.StaticText(self, wx.ID_ANY, u"DUT LAN掩码",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_general_submask.Wrap(-1)
        hbox_general_submask.Add(self.label_general_submask, 0, wx.ALL, 5)

        self.text_lan_submask = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_lan_submask.SetMinSize(wx.Size(self.config_win_text_ctrl_width, self.config_win_text_ctrl_hight))
        hbox_general_submask.Add(self.text_lan_submask, 0, wx.ALL, 5)

        general_config.Add(hbox_general_submask, 1, wx.EXPAND, 5)

        hbox_dhcp_start_ip1 = wx.BoxSizer(wx.HORIZONTAL)

        self.label_dhcp_start_ip1 = wx.StaticText(self, wx.ID_ANY, u"DHCP起始IP地址",
                                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_dhcp_start_ip1.Wrap(-1)
        hbox_dhcp_start_ip1.Add(self.label_dhcp_start_ip1, 0, wx.ALL, 5)

        self.text_apitest_start_ip = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_apitest_start_ip.SetMinSize(wx.Size(self.config_win_text_ctrl_width, self.config_win_text_ctrl_hight))
        hbox_dhcp_start_ip1.Add(self.text_apitest_start_ip, 0, wx.ALL, 5)

        general_config.Add(hbox_dhcp_start_ip1, 1, wx.EXPAND, 5)

        vbox_config.Add(general_config, 1, wx.EXPAND, 5)

        web_config = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"WEB相关配置"), wx.HORIZONTAL)

        hbox_web_login = wx.BoxSizer(wx.HORIZONTAL)

        self.web_username = wx.StaticText(self, wx.ID_ANY, u"WEB登录名", wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        self.web_username.Wrap(-1)
        hbox_web_login.Add(self.web_username, 0, wx.ALL, 5)

        self.text_web_username = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.text_web_username.SetMinSize(wx.Size(self.config_win_text_ctrl_width, self.config_win_text_ctrl_hight))
        hbox_web_login.Add(self.text_web_username, 0, wx.ALL, 5)

        self.web_password = wx.StaticText(self, wx.ID_ANY, u"WEB密码", wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        self.web_password.Wrap(-1)
        hbox_web_login.Add(self.web_password, 0, wx.ALL, 5)

        self.text_web_password = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                             wx.DefaultSize, wx.TE_PASSWORD)
        self.text_web_password.SetMinSize(wx.Size(self.config_win_text_ctrl_width, self.config_win_text_ctrl_hight))
        hbox_web_login.Add(self.text_web_password, 0, wx.ALL, 5)

        web_config.Add(hbox_web_login, 1, wx.EXPAND, 5)

        vbox_config.Add(web_config, 1, wx.EXPAND, 5)

        telnet_config = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"telnet相关配置"), wx.HORIZONTAL)

        hbox_telnet_user = wx.BoxSizer(wx.HORIZONTAL)

        self.label_telnet_user = wx.StaticText(self, wx.ID_ANY, u"Telnet用户名",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_telnet_user.Wrap(-1)
        hbox_telnet_user.Add(self.label_telnet_user, 0, wx.ALL, 5)

        self.text_telnet_username = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_telnet_username.SetMinSize(wx.Size(self.config_win_text_ctrl_width, self.config_win_text_ctrl_hight))
        hbox_telnet_user.Add(self.text_telnet_username, 0, wx.ALL, 5)

        self.label_telnet_password = wx.StaticText(self, wx.ID_ANY, u"Telnet密码",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_telnet_password.Wrap(-1)
        hbox_telnet_user.Add(self.label_telnet_password, 0, wx.ALL, 5)

        self.text_telnet_password = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                                wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD)
        self.text_telnet_password.SetMinSize(wx.Size(self.config_win_text_ctrl_width, self.config_win_text_ctrl_hight))
        hbox_telnet_user.Add(self.text_telnet_password, 0, wx.ALL, 5)

        telnet_config.Add(hbox_telnet_user, 1, wx.EXPAND, 5)

        vbox_config.Add(telnet_config, 1, wx.EXPAND, 5)

        smartgateway_config = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"智能相关配置"), wx.HORIZONTAL)

        self.m_radioBox1Choices = [u"中国移动", u"中国电信"]
        self.m_radioBox1 = wx.RadioBox(self, wx.ID_ANY, u"选择待测设备运营商", wx.DefaultPosition,
                                       wx.DefaultSize, self.m_radioBox1Choices, 1, wx.RA_SPECIFY_COLS)
        self.m_radioBox1.SetSelection(0)
        smartgateway_config.Add(self.m_radioBox1, 0, wx.ALL, 5)

        cn_smartgateway_config = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, u"中国电信智能相关配置"), wx.HORIZONTAL)

        smartgateway_config.Add(cn_smartgateway_config, 1, wx.EXPAND, 5)

        cm_smartgateway_config = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, u"中国移动智能相关配置"), wx.HORIZONTAL)

        vbox_apitest_config = wx.BoxSizer(wx.VERTICAL)

        hbox_cm_apitest_port_config = wx.BoxSizer(wx.HORIZONTAL)

        self.label_cm_apitest_port = wx.StaticText(self, wx.ID_ANY, u"Apitest界面端口",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_cm_apitest_port.Wrap(-1)
        hbox_cm_apitest_port_config.Add(self.label_cm_apitest_port, 0, wx.ALL, 5)

        self.spin_apitest_port = wx.SpinCtrl(self, wx.ID_ANY, u"8080",
                                             wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 65535, 0)
        hbox_cm_apitest_port_config.Add(self.spin_apitest_port, 0, wx.ALL, 5)

        vbox_apitest_config.Add(hbox_cm_apitest_port_config, 1, wx.EXPAND, 5)

        hbox_apitest_host_mac = wx.BoxSizer(wx.HORIZONTAL)

        self.label_cm_apitest_host_mac = wx.StaticText(self, wx.ID_ANY, u"主机MAC地址",
                                                       wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_cm_apitest_host_mac.Wrap(-1)
        hbox_apitest_host_mac.Add(self.label_cm_apitest_host_mac, 0, wx.ALL, 5)

        self.text_cm_host_mac = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        hbox_apitest_host_mac.Add(self.text_cm_host_mac, 0, wx.ALL, 5)

        vbox_apitest_config.Add(hbox_apitest_host_mac, 1, wx.EXPAND, 5)

        cm_smartgateway_config.Add(vbox_apitest_config, 1, wx.EXPAND, 5)

        smartgateway_config.Add(cm_smartgateway_config, 1, wx.EXPAND, 5)

        vbox_config.Add(smartgateway_config, 1, wx.EXPAND, 5)

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
            self.text_general_ip.SetValue(self.dut_cfg['dut_ip'])
            self.text_lan_submask.SetValue(self.dut_cfg['dut_mask'])
            self.text_apitest_start_ip.SetValue(self.dut_cfg['dhcp_start_ip'])
            self.text_web_username.SetValue(self.dut_cfg['web_username'])
            self.text_web_password.SetValue(self.dut_cfg['web_password'])
            self.text_telnet_username.SetValue(self.dut_cfg['telnet_username'])
            self.text_telnet_password.SetValue(self.dut_cfg['telnet_password'])
            self.m_radioBox1.SetSelection(int(self.dut_cfg['dut_isp']))
            self.spin_apitest_port.SetValue(int(self.dut_cfg['apitest_port']))
            self.text_cm_host_mac.SetValue(self.dut_cfg['cm_host_mac'])
        except Exception, e:
            wx.MessageBox(u"待测设备配置初始化失败，请检查配置菜单中是否正常", u"警告", wx.OK | wx.ICON_INFORMATION)
        self.SetIcon(self.ico)
        self.Centre(wx.BOTH)
        self.Show(True)
        self.Fit()

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def on_dut_config_submit(self, event):
        dict_config_items = {}
        dict_config_items['dut_ip'] = self.text_general_ip.GetValue()
        dict_config_items['dut_mask'] = self.text_lan_submask.GetValue()
        dict_config_items['dhcp_start_ip'] = self.text_apitest_start_ip.GetValue()
        dict_config_items['web_username'] = self.text_web_username.GetValue()
        dict_config_items['web_password'] = self.text_web_password.GetValue()
        dict_config_items['telnet_username'] = self.text_telnet_username.GetValue()
        dict_config_items['telnet_password'] = self.text_telnet_password.GetValue()
        dict_config_items['dut_isp'] = self.m_radioBox1.GetSelection()
        dict_config_items['apitest_port'] = self.spin_apitest_port.GetValue()
        dict_config_items['cm_host_mac'] = self.text_cm_host_mac.GetValue()
        event.Skip()
        n_ret, str_ret = self.config_obj.save_dut_cfg(dict_config_items)

        if n_ret == self.test_cfg_suc:
            self.dut_cfg = dict_config_items
        self.Close()


