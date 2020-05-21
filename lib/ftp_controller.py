#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time, socket, ftplib, datetime, traceback
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')
success_count = 0       # 下载成功次数
fail_count = 0          # 下载失败次数
reconnect_count = 0     # 重连次数

def log(log_content, log_file='log.txt'):
    """
    保存日志文件

    参数：
        log_file: 日志文件名
        log_content: 日志内容

    返回值：
        无
    """
    log_file = open(log_file, 'a+')
    log_file.write("%s : %s\n" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), log_content))
    log_file.close()

def get_config(config_file):
    try:
        f = open(config_file, 'r')
        conf_list = f.readlines()
        conf_dict = {}
        for conf in conf_list:
            conf = conf[:-1]
            conf = conf.split("=")
            para = conf[0].strip()
            value = conf[1].strip()
            conf_dict[para] = value

        return conf_dict
    except Exception, e:
        return u"读取配置文件出错！"

class FtpLoopDownload():

    def __init__(self, timeout, filename, host, port, username, password):
        """
        初始化

        参数：
            timeout: 连接超时时间
            filename: 要下载的文件名称
            host: ftp 服务器 ip 地址
            port: ftp 服务器端口号
            username: ftp 服务器用户名
            password: ftp 服务器密码

        """
        self.ftp = ftplib.FTP()
        self.logger_pipe = None
        socket.setdefaulttimeout(timeout)       # 连接超时时间
        self.bufsize = 1024                     # 设置缓冲块大小
        self.filename = filename
        self.host = host
        self.port = port
        self.start_state = False
        self.username = username
        self.password = password

    def connect(self):
        """
        登录 FTP 服务器，检查 filename 文件是否存在

        返回值:
            成功返回true，失败返回失败原因
        """
        try:
            self.ftp.connect(str(self.host), int(self.port))
            # self.ftp.connect("182.16.100.206", 21)
            string = u"===================连接 FTP 服务器成功!==================="
            self.logger(string)
        except Exception, e:
            error_string = u"连接 FTP 服务器 %s 失败!" % self.host
            self.logger(error_string + '\n' + traceback.format_exc(e))
            return error_string

        try:
            self.ftp.login(self.username, self.password)   # 登录FTP服务器，如果匿名登录则用空串代替即可
            self.logger(self.ftp.getwelcome())
            string = u"===================登录 FTP 服务器成功!==================="
            self.logger()(string)
        except Exception, e:
            error_string = u"登录 FTP 服务器 %s 失败，请确认用户名：%s 和密码：%s 是否正确!" % (self.host, self.username, self.password)
            self.logger(error_string)
            return error_string

        file_list = self.ftp.nlst()              # 列出服务器上根目录下所有文件名称
        if self.filename not in file_list:
            error_string = u"文件 %s 在服务器上找不到" % self.filename
            self.logger(error_string)
            return error_string
        return True

    def download(self, count, reconnect):
        """
        下载文件

        参数：
            count: 当前下载次数
            reconnect: 断线重连标准，True表示启用断线重连，False表示不启用断线重连
        """
        try:
            global fail_count, reconnect_count
            file_handler = open(self.filename,'wb').write       # 以写模式在本地打开文件
            string = u"===================开始第 %s 次下载===================" % count
            self.logger(string)
            self.ftp.retrbinary('RETR %s' % os.path.basename(self.filename),file_handler,self.bufsize)  # 接收服务器上文件并写入本地文件
            string = u"===================文件第 %s 次下载完成===================" % count
            self.logger(string)
            return True
        except Exception, e:
            fail_count += 1
            if reconnect:
                times = 1
                while True:
                    error_string = u"===================第 %s 次下载过程中断，正在尝试第 %s 次重连...===================" % (count, times)
                    self.logger(error_string)
                    ret = self.connect()
                    if ret == True:
                        string = u"===================第 %s 次重连成功===================" % times
                        self.logger(string)
                        break;
                    else:
                        reconnect_count += 1
            return False

    def logger(self, str):
        if self.logger_pipe is not None:
            if self.start_state:
                self.logger_pipe.send(str)
        else:
            return

def main():
    global success_count
    try:
        conf = get_config('ftp.conf')
        if type(conf) != dict:
            print conf
            return False
        ftpLoopDownload = FtpLoopDownload(int(conf['timeout']), conf['filename'], conf['host'], int(conf['port']), conf['username'], conf['password'])
        ret = ftpLoopDownload.connect()
        # 首次连接服务器失败退出程序并打印失败原因
        if ret != True:
            print ret
            return False
        count = 1
        while True:
            ret = ftpLoopDownload.download(count, conf['reconnect'])
            time.sleep(1)
            os.remove(conf['filename'])
            count += 1
            if ret:
                success_count += 1
    except KeyboardInterrupt, e:
        string = u"===================按下 [Ctrl+C] 手动终止程序，测试结果：==================="
        log(string)
        print string
        string = u"===================下载成功次数：%s===================" % (success_count)
        log(string)
        print string
        string = u"===================下载失败次数：%s===================" % (fail_count)
        log(string)
        print string
        string = u"===================断线重连次数：%s===================" % (reconnect_count)
        log(string)
        print string
    except Exception, e:
        string = traceback.format_exc(e)
        log(string)
        print string


if __name__ == '__main__':
    main()
