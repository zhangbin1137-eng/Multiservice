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
## Class voip_config_win
###########################################################################

class voip_config_win(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"语音配置界面", pos=wx.DefaultPosition, size=wx.Size(500, 700),
                          style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_NO_TASKBAR | wx.FRAME_SHAPED | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.ico = None
        self.keygoe_conf = {}
        self.config_obj = None

        vbox_voip_comman_config = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"东进语音卡通用配置"), wx.VERTICAL)

        hbox_server_config = wx.BoxSizer(wx.HORIZONTAL)

        self.label_voip_server_ip = wx.StaticText(self, wx.ID_ANY, u"语音卡服务IP地址",
                                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_voip_server_ip.Wrap(-1)
        hbox_server_config.Add(self.label_voip_server_ip, 0, wx.ALL, 5)

        self.text_server_ip = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        hbox_server_config.Add(self.text_server_ip, 0, wx.ALL, 5)

        vbox_voip_comman_config.Add(hbox_server_config, 1, wx.EXPAND, 5)

        hbox_server_port = wx.BoxSizer(wx.HORIZONTAL)

        self.label_server_port = wx.StaticText(self, wx.ID_ANY, u"语音卡服务端口号",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_server_port.Wrap(-1)
        hbox_server_port.Add(self.label_server_port, 0, wx.ALL, 5)

        self.spin_server_port = wx.SpinCtrl(self, wx.ID_ANY, u"9000",
                                            wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000, 9000)
        hbox_server_port.Add(self.spin_server_port, 0, wx.ALL, 5)

        vbox_voip_comman_config.Add(hbox_server_port, 1, wx.EXPAND, 5)

        hbox_server_username = wx.BoxSizer(wx.HORIZONTAL)

        self.label_server_username = wx.StaticText(self, wx.ID_ANY, u"语音卡服务用户名",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_server_username.Wrap(-1)
        hbox_server_username.Add(self.label_server_username, 0, wx.ALL, 5)

        self.text_server_username = wx.TextCtrl(self, wx.ID_ANY, u"admin",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        hbox_server_username.Add(self.text_server_username, 0, wx.ALL, 5)

        vbox_voip_comman_config.Add(hbox_server_username, 1, wx.EXPAND, 5)

        hbox_server_pwd = wx.BoxSizer(wx.HORIZONTAL)

        self.label_server_pwd = wx.StaticText(self, wx.ID_ANY, u"语音卡服务密码",
                                              wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_server_pwd.Wrap(-1)
        hbox_server_pwd.Add(self.label_server_pwd, 0, wx.ALL, 5)

        self.text_server_pwd = wx.TextCtrl(self, wx.ID_ANY, u"1234",
                                           wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD)
        hbox_server_pwd.Add(self.text_server_pwd, 0, wx.ALL, 5)

        vbox_voip_comman_config.Add(hbox_server_pwd, 1, wx.EXPAND, 5)

        hbox_is_test = wx.BoxSizer(wx.HORIZONTAL)

        radio_is_testChoices = [u"是", u"否"]
        self.radio_is_test = wx.RadioBox(self, wx.ID_ANY, u"是否测试", wx.DefaultPosition,
                                         wx.DefaultSize, radio_is_testChoices, 2, wx.RA_SPECIFY_COLS)
        self.radio_is_test.SetSelection(0)
        hbox_is_test.Add(self.radio_is_test, 0, wx.ALL, 5)

        vbox_voip_comman_config.Add(hbox_is_test, 1, wx.EXPAND, 5)

        vbox.Add(vbox_voip_comman_config, 1, wx.EXPAND, 5)

        vbox_phone_config = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"主叫被叫方配置"), wx.VERTICAL)

        hbox_caller = wx.BoxSizer(wx.HORIZONTAL)

        self.label_caller = wx.StaticText(self, wx.ID_ANY, u"主叫方号码", wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        self.label_caller.Wrap(-1)
        hbox_caller.Add(self.label_caller, 0, wx.ALL, 5)

        self.text_caller = wx.TextCtrl(self, wx.ID_ANY, u"10086", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        hbox_caller.Add(self.text_caller, 0, wx.ALL, 5)

        vbox_phone_config.Add(hbox_caller, 1, wx.EXPAND, 5)

        hbox_called = wx.BoxSizer(wx.HORIZONTAL)

        self.label_called = wx.StaticText(self, wx.ID_ANY, u"被叫方号码", wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        self.label_called.Wrap(-1)
        hbox_called.Add(self.label_called, 0, wx.ALL, 5)

        self.text_called = wx.TextCtrl(self, wx.ID_ANY, u"10000", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        hbox_called.Add(self.text_called, 0, wx.ALL, 5)

        vbox_phone_config.Add(hbox_called, 1, wx.EXPAND, 5)

        hbox_caller_trunk_id = wx.BoxSizer(wx.HORIZONTAL)

        self.label_caller_trunk_id = wx.StaticText(self, wx.ID_ANY, u"主叫方Trunk ID",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_caller_trunk_id.Wrap(-1)
        hbox_caller_trunk_id.Add(self.label_caller_trunk_id, 0, wx.ALL, 5)

        self.spin_caller_trunk_id = wx.SpinCtrl(self, wx.ID_ANY, u"1", wx.DefaultPosition,
                                                wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 16, 1)
        hbox_caller_trunk_id.Add(self.spin_caller_trunk_id, 0, wx.ALL, 5)

        vbox_phone_config.Add(hbox_caller_trunk_id, 1, wx.EXPAND, 5)

        hbox_called_trunk_id = wx.BoxSizer(wx.HORIZONTAL)

        self.label_trunk_id = wx.StaticText(self, wx.ID_ANY, u"被叫方Trunk ID",
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_trunk_id.Wrap(-1)
        hbox_called_trunk_id.Add(self.label_trunk_id, 0, wx.ALL, 5)

        self.spin_called_trunk_id = wx.SpinCtrl(self, wx.ID_ANY, u"2", wx.DefaultPosition,
                                                wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 16, 1)
        hbox_called_trunk_id.Add(self.spin_called_trunk_id, 0, wx.ALL, 5)

        vbox_phone_config.Add(hbox_called_trunk_id, 1, wx.EXPAND, 5)

        vbox.Add(vbox_phone_config, 1, wx.EXPAND, 5)

        config_submit = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_config_submit = wx.Button(self, wx.ID_ANY, u"保存配置", wx.DefaultPosition, wx.DefaultSize, 0)
        config_submit.Add(self.btn_config_submit, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        vbox.Add(config_submit, 1, wx.BOTTOM, 5)
        self.SetSizer(vbox)
        self.Layout()
        # Connect Events
        self.btn_config_submit.Bind(wx.EVT_BUTTON, self.on_dut_config_submit)

    def window_show(self):
        try:
            self.text_server_ip.SetValue(self.keygoe_conf['keygoe_server_ip'])
            self.text_server_username.SetValue(self.keygoe_conf['keygoe_server_username'])
            self.text_server_pwd.SetValue(self.keygoe_conf['keygoe_server_pwd'])
            self.text_called.SetValue(self.keygoe_conf['keygoe_called'])
            self.text_caller.SetValue(self.keygoe_conf['keygoe_caller'])
            self.spin_server_port.SetValue(self.keygoe_conf['keygoe_server_port'])
            self.spin_called_trunk_id.SetValue(int(self.keygoe_conf['keygoe_called_trunk_id']))
            self.spin_caller_trunk_id.SetValue(int(self.keygoe_conf['keygoe_caller_trunk_id']))
            self.radio_is_test.SetSelection(int(self.keygoe_conf['keygoe_is_test']))
        except Exception, e:
            wx.MessageBox(u"待测设备配置初始化失败，请检查配置菜单中是否正常", u"警告", wx.OK | wx.ICON_INFORMATION)
        self.SetIcon(self.ico)
        self.Centre(wx.BOTH)
        self.Show(True)
        #self.Fit()

    def __del__(self):
        pass

    def on_dut_config_submit(self, event):
        dict_config_items = {}
        dict_config_items['keygoe_server_ip'] = self.text_server_ip.GetValue()
        dict_config_items['keygoe_server_port'] = self.spin_server_port.GetValue()
        dict_config_items['keygoe_server_username'] = self.text_server_username.GetValue()
        dict_config_items['keygoe_server_pwd'] = self.text_server_pwd.GetValue()
        dict_config_items['keygoe_caller'] = self.text_caller.GetValue()
        dict_config_items['keygoe_called'] = self.text_called.GetValue()
        dict_config_items['keygoe_called_trunk_id'] = self.spin_called_trunk_id.GetValue()
        dict_config_items['keygoe_caller_trunk_id'] = self.spin_caller_trunk_id.GetValue()
        dict_config_items['keygoe_is_test'] = self.radio_is_test.GetSelection()
        event.Skip()
        n_ret, str_ret = self.config_obj.save_keygoe_cfg(dict_config_items)

        if n_ret == self.test_cfg_suc:
            self.keygoe_conf = dict_config_items
        self.Close()


