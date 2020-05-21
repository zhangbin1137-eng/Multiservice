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
## Class config_win
###########################################################################

class config_win(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"配置窗口", pos=wx.DefaultPosition, size=wx.Size(800, 600),
                          style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_NO_TASKBAR | wx.FRAME_SHAPED | wx.TAB_TRAVERSAL)
        # 配置窗口的样式设置
        self.config_win_text_ctrl_width = 200
        self.config_win_text_ctrl_hight = 20
        self.service_cfg = {}
        self.config_obj = None
        self.test_cfg_suc = None
        self.ico = None


        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        #self.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, "@Dotum"))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        vbox_config = wx.BoxSizer(wx.VERTICAL)

        vbox_http_config = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"HTTP相关配置"), wx.VERTICAL)

        hbox_new_url = wx.BoxSizer(wx.HORIZONTAL)

        self.new_add_url = wx.StaticText(self, wx.ID_ANY, u"新增加的URL", wx.DefaultPosition,
                                         wx.DefaultSize, wx.ALIGN_LEFT)
        self.new_add_url.Wrap(-1)
        hbox_new_url.Add(self.new_add_url, 0, wx.ALL, 5)

        self.text_new_url = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.DefaultSize, wx.TE_LEFT)
        self.text_new_url.SetMinSize(wx.Size(self.config_win_text_ctrl_width, self.config_win_text_ctrl_hight))
        hbox_new_url.Add(self.text_new_url, 0, wx.ALL, 5)

        vbox_http_config.Add(hbox_new_url, 1, wx.EXPAND, 5)

        hbox_is_http_test = wx.BoxSizer(wx.HORIZONTAL)

        self.label_is_http_test = wx.StaticText(self, wx.ID_ANY, u"是否测试", wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        self.label_is_http_test.Wrap(-1)
        hbox_is_http_test.Add(self.label_is_http_test, 0, wx.ALL, 5)

        combo_is_http_testChoices = [u"是", u"否"]
        self.combo_is_http_test = wx.ComboBox(self, wx.ID_ANY, u"是", wx.DefaultPosition,
                                              wx.DefaultSize, combo_is_http_testChoices, 0)
        hbox_is_http_test.Add(self.combo_is_http_test, 0, wx.ALL, 5)

        vbox_http_config.Add(hbox_is_http_test, 1, wx.EXPAND, 5)

        vbox_config.Add(vbox_http_config, 1, wx.EXPAND, 5)

        vbox_thunder_config = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"迅雷相关配置:暂时因API问题解决不了，暂不可用"), wx.VERTICAL)

        hbox_thunder_job_config = wx.BoxSizer(wx.HORIZONTAL)

        self.label_add_new_task = wx.StaticText(self, wx.ID_ANY, u"任务路径",
                                                wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT)
        self.label_add_new_task.Wrap(-1)
        hbox_thunder_job_config.Add(self.label_add_new_task, 0, wx.ALL, 5)

        self.text_thunder_task = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                             wx.DefaultPosition, wx.DefaultSize, wx.TE_LEFT)

        self.text_thunder_task.SetMinSize(wx.Size(self.config_win_text_ctrl_width, self.config_win_text_ctrl_hight))
        hbox_thunder_job_config.Add(self.text_thunder_task, 0, wx.ALL, 5)

        vbox_thunder_config.Add(hbox_thunder_job_config, 1, wx.EXPAND, 5)

        hbox_saved_filename = wx.BoxSizer(wx.HORIZONTAL)

        self.label_save_as_file_name = wx.StaticText(self, wx.ID_ANY, u"保存文件名",
                                                     wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT)
        self.label_save_as_file_name.Wrap(-1)
        hbox_saved_filename.Add(self.label_save_as_file_name, 0, wx.ALL, 5)

        self.text_saved_as_filename = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                                  wx.DefaultPosition, wx.DefaultSize, wx.TE_LEFT)
        self.text_saved_as_filename.SetMinSize(wx.Size(self.config_win_text_ctrl_width,
                                                       self.config_win_text_ctrl_hight))
        hbox_saved_filename.Add(self.text_saved_as_filename, 0, wx.ALL, 5)

        vbox_thunder_config.Add(hbox_saved_filename, 1, wx.EXPAND, 5)

        hbox_saved_path = wx.BoxSizer(wx.HORIZONTAL)

        self.label_saved_path = wx.StaticText(self, wx.ID_ANY, u"保存路径",
                                              wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT)
        self.label_saved_path.Wrap(-1)
        hbox_saved_path.Add(self.label_saved_path, 0, wx.ALL, 5)

        self.file_thunder_path = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString,
                                                   u"Select a folder", wx.DefaultPosition, wx.DefaultSize,
                                                   wx.DIRP_DEFAULT_STYLE )
        self.file_thunder_path.SetMinSize(wx.Size(self.config_win_text_ctrl_width, self.config_win_text_ctrl_hight))
        hbox_saved_path.Add(self.file_thunder_path, 0, wx.ALL, 5)

        vbox_thunder_config.Add(hbox_saved_path, 1, wx.EXPAND, 5)

        hbox_is_thunder_test = wx.BoxSizer(wx.HORIZONTAL)

        self.label_is_thunder_test = wx.StaticText(self, wx.ID_ANY, u"是否测试",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_is_thunder_test.Wrap(-1)
        hbox_is_thunder_test.Add(self.label_is_thunder_test, 0, wx.ALL, 5)

        combo_is_thunder_testChoices = [u"是", u"否"]
        self.combo_is_thunder_test = wx.ComboBox(self, wx.ID_ANY, u"是",
                                                 wx.DefaultPosition, wx.DefaultSize, combo_is_thunder_testChoices, 0)
        hbox_is_thunder_test.Add(self.combo_is_thunder_test, 0, wx.ALL, 5)

        vbox_thunder_config.Add(hbox_is_thunder_test, 1, wx.EXPAND, 5)

        vbox_config.Add(vbox_thunder_config, 1, wx.EXPAND, 5)
        self.text_thunder_task.Enable(False)
        self.text_saved_as_filename.Enable(False)
        self.file_thunder_path.Enable(False)
        self.combo_is_thunder_test.Enable(False)


        vbox_FTP_config = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"FTP相关配置"), wx.VERTICAL)

        hbox_ftp_user_config = wx.BoxSizer(wx.HORIZONTAL)

        self.label_ftp_username = wx.StaticText(self, wx.ID_ANY, u"FTP用户名",
                                                wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT)
        self.label_ftp_username.Wrap(-1)
        hbox_ftp_user_config.Add(self.label_ftp_username, 0, wx.ALL, 5)

        self.text_ftp_username = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                             wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_ftp_username.SetMinSize(wx.Size(self.config_win_text_ctrl_width, self.config_win_text_ctrl_hight))
        hbox_ftp_user_config.Add(self.text_ftp_username, 0, wx.ALL, 5)

        self.label_ftp_password = wx.StaticText(self, wx.ID_ANY, u"FTP密码", wx.DefaultPosition,
                                                wx.DefaultSize, wx.ALIGN_LEFT)
        self.label_ftp_password.Wrap(-1)
        hbox_ftp_user_config.Add(self.label_ftp_password, 0, wx.ALL, 5)

        self.text_ftp_password = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                             wx.DefaultPosition, wx.DefaultSize, wx.TE_LEFT | wx.TE_PASSWORD)
        self.text_ftp_password.SetMinSize(wx.Size(self.config_win_text_ctrl_width, self.config_win_text_ctrl_hight))
        hbox_ftp_user_config.Add(self.text_ftp_password, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        vbox_FTP_config.Add(hbox_ftp_user_config, 1, wx.EXPAND, 5)

        hbox_ftp_host = wx.BoxSizer(wx.HORIZONTAL)

        self.label_ftp_host = wx.StaticText(self, wx.ID_ANY, u"FTP服务器", wx.DefaultPosition,
                                            wx.DefaultSize, wx.ALIGN_LEFT)
        self.label_ftp_host.Wrap(-1)
        hbox_ftp_host.Add(self.label_ftp_host, 0, wx.ALL, 5)

        self.text_ftp_host = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        self.text_ftp_host.SetMinSize(wx.Size(self.config_win_text_ctrl_width, self.config_win_text_ctrl_hight))
        hbox_ftp_host.Add(self.text_ftp_host, 0, wx.ALL, 5)

        self.label_ftp_port = wx.StaticText(self, wx.ID_ANY, u"FTP服务器端口", wx.DefaultPosition,
                                            wx.DefaultSize, wx.ALIGN_LEFT)

        self.label_ftp_port.Wrap(-1)
        hbox_ftp_host.Add(self.label_ftp_port, 0, wx.ALL, 5)

        self.text_ftp_port = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                         wx.DefaultSize, wx.TE_LEFT)
        self.text_ftp_port.SetMinSize(wx.Size(self.config_win_text_ctrl_width, self.config_win_text_ctrl_hight))
        hbox_ftp_host.Add(self.text_ftp_port, 0, wx.ALL, 5)

        vbox_FTP_config.Add(hbox_ftp_host, 1, wx.ALIGN_LEFT | wx.EXPAND, 5)

        hbox_ftp_file = wx.BoxSizer(wx.HORIZONTAL)

        self.label_file = wx.StaticText(self, wx.ID_ANY, u"下载文件", wx.DefaultPosition,
                                        wx.DefaultSize, wx.ALIGN_LEFT)
        self.label_file.Wrap(-1)
        hbox_ftp_file.Add(self.label_file, 0, wx.ALL, 5)

        self.text_file = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                     wx.DefaultSize, wx.TE_LEFT)
        self.text_file.SetMinSize(wx.Size(self.config_win_text_ctrl_width, self.config_win_text_ctrl_hight))
        hbox_ftp_file.Add(self.text_file, 0, wx.ALL, 5)
        self.label_timeout = wx.StaticText(self, wx.ID_ANY, u"超时时间", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.label_timeout.Wrap(-1)
        hbox_ftp_file.Add(self.label_timeout, 0, wx.ALL, 5)

        self.spin_timeout = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.DefaultSize, wx.SP_ARROW_KEYS, 2, 100, 2)
        hbox_ftp_file.Add(self.spin_timeout, 0, wx.ALL, 5)
        vbox_FTP_config.Add(hbox_ftp_file, 1, wx.ALIGN_LEFT | wx.EXPAND, 5)
        hbox_is_ftp_test = wx.BoxSizer(wx.HORIZONTAL)

        self.label_is_ftp_test = wx.StaticText(self, wx.ID_ANY, u"是否测试", wx.DefaultPosition,
                                               wx.DefaultSize, wx.ALIGN_LEFT)
        self.label_is_ftp_test.Wrap(-1)
        hbox_is_ftp_test.Add(self.label_is_ftp_test, 0, wx.ALL, 5)

        combo_is_ftp_testChoices = [u"是", u"否", wx.EmptyString]
        self.combo_is_ftp_test = wx.ComboBox(self, wx.ID_ANY, u"是", wx.DefaultPosition,
                                             wx.DefaultSize, combo_is_ftp_testChoices, 0)
        hbox_is_ftp_test.Add(self.combo_is_ftp_test, 0, wx.ALL, 5)

        vbox_FTP_config.Add(hbox_is_ftp_test, 1, wx.ALIGN_LEFT | wx.EXPAND, 5)

        vbox_config.Add(vbox_FTP_config, 1, wx.EXPAND, 5)

        vbox_vlc_config = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"VLC相关配置"), wx.VERTICAL)

        hbox_vlc_task = wx.BoxSizer(wx.HORIZONTAL)

        self.label_vlc_task = wx.StaticText(self, wx.ID_ANY, u"VLC 任务", wx.DefaultPosition,
                                            wx.DefaultSize, wx.ALIGN_LEFT)
        self.label_vlc_task.Wrap(-1)
        hbox_vlc_task.Add(self.label_vlc_task, 0, wx.ALL, 5)

        self.text_vlc_task = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                         wx.DefaultSize, wx.TE_LEFT)
        self.text_vlc_task.SetMinSize(wx.Size(self.config_win_text_ctrl_width, self.config_win_text_ctrl_hight))
        hbox_vlc_task.Add(self.text_vlc_task, 0, wx.ALL, 5)

        vbox_vlc_config.Add(hbox_vlc_task, 1, wx.EXPAND, 5)

        hbox_is_vlc_test = wx.BoxSizer(wx.HORIZONTAL)

        self.label_is_vlc_test = wx.StaticText(self, wx.ID_ANY, u"是否测试", wx.DefaultPosition,
                                               wx.DefaultSize, wx.ALIGN_LEFT)
        self.label_is_vlc_test.Wrap(-1)
        hbox_is_vlc_test.Add(self.label_is_vlc_test, 0, wx.ALL, 5)

        combo_is_vlc_testChoices = [u"是", u"否"]
        self.combo_is_vlc_test = wx.ComboBox(self, wx.ID_ANY, u"是", wx.DefaultPosition,
                                             wx.DefaultSize, combo_is_vlc_testChoices, 0)
        hbox_is_vlc_test.Add(self.combo_is_vlc_test, 0, wx.ALL, 5)

        vbox_vlc_config.Add(hbox_is_vlc_test, 1, wx.EXPAND, 5)

        vbox_config.Add(vbox_vlc_config, 1, wx.EXPAND, 5)



        vbox_btn = wx.BoxSizer(wx.VERTICAL)

        self.btn_config_submit = wx.Button(self, wx.ID_ANY, u"保存配置", wx.DefaultPosition, wx.DefaultSize, 0)
        vbox_btn.Add(self.btn_config_submit, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        vbox_config.Add(vbox_btn, 1, wx.ALIGN_CENTER | wx.EXPAND, 5)

        self.SetSizer(vbox_config)
        self.Layout()


        # Connect Events
        self.file_thunder_path.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_file_change)
        self.btn_config_submit.Bind(wx.EVT_BUTTON, self.on_submit)

    def __del__(self):
        pass

    def window_show(self):
        try:
            self.text_vlc_task.SetValue(self.service_cfg['vlc_task'])
            self.text_saved_as_filename.SetValue(self.service_cfg['thunder_saved_filename'])
            self.text_thunder_task.SetValue(self.service_cfg['thunder_task'])
            self.file_thunder_path.SetPath(self.service_cfg['thunder_saved_path'])
            self.text_file.SetValue(self.service_cfg['ftp_file'])
            self.text_ftp_password.SetValue(self.service_cfg['ftp_pwd'])
            self.text_ftp_port.SetValue(self.service_cfg['ftp_port'])
            self.text_ftp_host.SetValue(self.service_cfg['ftp_host'])
            self.text_ftp_username.SetValue(self.service_cfg['ftp_username'])
            self.combo_is_ftp_test.SetValue(self.service_cfg['is_ftp_test'])
            self.combo_is_http_test.SetValue(self.service_cfg['is_http_test'])
            self.combo_is_vlc_test.SetValue(self.service_cfg['is_vlc_test'])
            self.combo_is_thunder_test.SetValue(self.service_cfg['is_thunder_test'])
            self.spin_timeout.SetValue(int(self.service_cfg['ftp_timeout']))
        except Exception, e:
            wx.MessageBox(u"配置初始化失败，请检查配置菜单中是否正常", u"警告", wx.OK | wx.ICON_INFORMATION)
        self.SetIcon(self.ico)
        self.Centre(wx.BOTH)
        self.Show(True)
        self.Fit()
    # Virtual event handlers, overide them in your derived class
    def on_file_change(self, event):
        event.Skip()

    def on_submit(self, event):
        dict_config_items = {}
        list_url_config = []
        for i in self.service_cfg.keys():
            if i.startswith('url'):
                list_url_config.append(int(i.lstrip("url")))
        a = max(list_url_config)
        dict_config_items['url%d' % a] = self.text_new_url.GetValue()
        dict_config_items['vlc_task'] = self.text_vlc_task.GetValue()
        dict_config_items['thunder_saved_path'] = self.file_thunder_path.GetPath()
        dict_config_items['thunder_saved_filename'] = self.text_saved_as_filename.GetValue()
        dict_config_items['thunder_task'] = self.text_thunder_task.GetValue()
        dict_config_items['ftp_file'] = self.text_file.GetValue()
        dict_config_items['ftp_pwd'] = self.text_ftp_password.GetValue()
        dict_config_items['ftp_port'] = self.text_ftp_port.GetValue()
        dict_config_items['ftp_host'] = self.text_ftp_host.GetValue()
        dict_config_items['ftp_username'] = self.text_ftp_username.GetValue()
        dict_config_items['is_ftp_test'] = self.combo_is_ftp_test.GetValue()
        dict_config_items['is_http_test'] = self.combo_is_http_test.GetValue()
        dict_config_items['is_vlc_test'] = self.combo_is_vlc_test.GetValue()
        dict_config_items['is_thunder_test'] = self.combo_is_thunder_test.GetValue()
        dict_config_items['ftp_timeout'] = self.spin_timeout.GetValue()
        event.Skip()
        n_ret, str_ret = self.config_obj.save_cfg(dict_config_items)

        if n_ret == self.test_cfg_suc:
            self.service_cfg = dict_config_items
        self.Close()



