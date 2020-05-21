# -*- coding: utf-8 -*-
import subprocess,re,time,os,sys
from win32com.client import Dispatch
#import comtypes
reload(sys)
sys.setdefaultencoding("utf-8")


class Thunder:
    def __init__(self, windows_type='64-bit'):
        self.resource = ""
        self.flag = False
        self.log_info = ""
        self.start_status = False
        self.logger_pipe = None
        if windows_type == '64-bit':
            self.thunder_obj = Dispatch("ThunderAgent.Agent.1")
        else:
            self.thunder_obj = Dispatch("ThunderAgent.Agent.1")
        self.download_path = os.getcwd()+r"\download"
        self.saved_name = ""

    def check_thunder_exists(self):
        try:
            return self.thunder_obj.GetInfo("ThunderExists")
        except Exception, e:
            log_info = u"检查迅雷是否存在时发生错误，错误信息：%s" % e
            self.logger(log_info)
            return False

    def get_thunder_platform_version(self):
        try:
            return self.thunder_obj.GetInfo("PlatformVersion")
        except Exception, e:
            log_info = u"获取迅雷平台版本时发生错误，错误信息:%s" % e
            self.logger(log_info)
            return

    def get_thunder_version(self):
        try:
            return self.thunder_obj.GetInfo("ThunderVersion")
        except Exception, e:
            log_info = u"获取迅雷版本时发生错误，错误信息:%s" % e
            self.logger(log_info)
            return

    def check_is_thunder_running(self):
        try:
            return self.thunder_obj.GetInfo("ThunderRunning")
        except Exception, e:
            log_info = u"获取迅雷运行状态时发生错误，错误信息:%s" % e
            self.logger(log_info)
            return

    def add_thunder_task(self):
        try:
            self.cancel_thunder_task()
            self.thunder_obj.AddTask(self.resource, self.saved_name, self.download_path, "", "", 1, 0, 8)
            self.thunder_obj.CommitTasks()
            self.logger(u"往迅雷中添加任务%s成功" % self.resource)
        except Exception, e:
            log_info = u'往迅雷中添加%s任务失败，错误信息为：%s' % (self.resource, e)
            self.logger(log_info)

    def query_thunder_task_status(self):
        status_dict = {"running": "正在运行", "stopped": "停止状态", "failed": "失败状态",
                       "success": "成功", "creatingfile": "正在创建数据文件", "connecting": "正在连接"}
        try:
            status = self.thunder_obj.GetTaskInfo(self.resource, "Status")
            log_info = u"%s任务的状态为：%s" % (self.resource, status_dict.get(status))
            self.logger(log_info)
            return status
        except Exception,e:
            log_info = u"获取%s任务失败，错误信息为：%s" % (self.resource,e)
            self.logger(log_info)

    def check_thunder_task_exist(self):
        try:
            exist = self.thunder_obj.GetTaskInfo(self.resource, "Exists")
            return exist
        except Exception, e:
            log_info = u"获取%s任务是否存在失败，错误信息为：%s" % (self.resource, e)
            self.logger(log_info)

    def query_thunder_task_percent(self):
        try:
            percent = self.thunder_obj.GetTaskInfo(self.resource, "Percent")
            print type(percent)
            log_info = u"%s任务的下载进度为:%s" % (self.resource, percent)
            self.logger(log_info)
            return percent
        except Exception, e:
            log_info = u"获取%s任务的下进度失败, 错误信息为：%s" % (self.resource, e)
            self.logger(log_info)

    def cancel_thunder_task(self):
        try:
            self.thunder_obj.CancelTasks()
            log_info = u"取消下载任务成功"
            self.logger(log_info)
        except Exception, e:
            log_info = u"取消下载任务出错，错误信息为:%s" % e
            self.logger(log_info)

    def logger(self, str):
        if self.logger_pipe is not None:
            if self.start_status:
                self.logger_pipe.send(str)
        else:
            return

    def run_thunder_task(self):
        self.add_thunder_task()
        while self.start_status:
            time.sleep(4)
            status = self.query_thunder_task_status()
            self.query_thunder_task_percent()
            if status == "success":
                self.logger(u"下载%s成功,重新下载" % self.resource)
                self.cancel_thunder_task()
                self.run_thunder_task()
            if status == "failed":
                self.logger(u"下载%s出错，重新下载" % self.resource)
                self.cancel_thunder_task()
                self.run_thunder_task()
            if status == "stopped":
                self.logger(u"下载%s停止了，取消任务重新下载" % self.resource)
                self.cancel_thunder_task()
                self.run_thunder_task()
        self.cancel_thunder_task()


def main():
    th = Thunder("http://10.68.100.51/yuewen/storage/uploads/img/article/2017-05-24-15-07-55-5925314ba05cd.PNG")
    th.add_thunder_task()
    th.query_thunder_task_percent()
    th.query_thunder_task_status()
    th.cancel_thunder_task()
if __name__ == '__main__':
    main()