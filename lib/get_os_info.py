# -*- coding: utf-8 -*-
import wmi
import sys, time, platform

class Get_system_info:
    def __init__(self):
        self.wmi_obj = wmi.WMI()
        self.system_obj = {}
        self.memory_obj = {}
        self.disk_obj = {}
        self.nic_obj = {}
        self.cpu_obj = {}

    def get_system_info(self, os="Windows"):
        """
        获取操作系统版本。
        """
        if os == "Windows":

            for sys in self.wmi_obj.Win32_OperatingSystem():
                self.system_obj['Version'] = sys.Caption.encode("utf-8")
                self.system_obj['Vernum'] = sys.BuildNumber

    def get_system_architecture(self, os="Windows"):
        """
        获取操作系统的位数
        :param os:
        :return:
        """
        if os == "Windows":
            for sys in self.wmi_obj.Win32_OperatingSystem():
                self.system_obj['architecture'] = sys.OSArchitecture

    def get_memory_info(self, os="Windows"):
        """
        获取物理内存和虚拟内存。
        M为单位
        """
        if os == "Windows":
            cs = self.wmi_obj.Win32_ComputerSystem()
            pfu = self.wmi_obj.Win32_PageFileUsage()
            MemTotal = int(cs[0].TotalPhysicalMemory) / 1024 / 1024
            self.memory_obj['TotalPhysicalMemory'] = MemTotal
            SwapTotal = int(pfu[0].AllocatedBaseSize)
            self.memory_obj['SwapTotal'] = SwapTotal

    def get_disk_info(self, os="Windows"):
        """
        获取物理磁盘信息。
        G为单位
        """
        if os == "Windows":
            for physical_disk in self.wmi_obj.Win32_DiskDrive():
                if physical_disk.Size:
                    self.disk_obj[str(physical_disk.Caption)] = str(long(physical_disk.Size) / 1024 / 1024 / 1024)

    def get_cpu_info(self, os="Windows"):
        """
        获取CPU信息。
        """
        if os == "Windows":
            tmpdict = {}
            tmpdict["CpuCores"] = 0
            for cpu in self.wmi_obj.Win32_Processor():
                tmpdict["CpuType"] = cpu.Name
            try:
                tmpdict["CpuCores"] = cpu.NumberOfCores
            except:
                tmpdict["CpuCores"] += 1
            tmpdict["CpuClock"] = cpu.MaxClockSpeed
            self.cpu_obj = tmpdict

    def get_network_info(self, os="Windows"):
        """
        获取网卡信息。
        """
        if os == "Windows":
            tmplist = []
            for interface in self.wmi_obj.Win32_NetworkAdapterConfiguration(IPEnabled=1):
                tmpdict = {}
                tmpdict["Description"] = interface.Description
                tmpdict["IPAddress"] = interface.IPAddress[0]
                tmpdict["IPSubnet"] = interface.IPSubnet[0]
                tmpdict["MAC"] = interface.MACAddress
                tmplist.append(tmpdict)
            for interface in self.wmi_obj.Win32_NetworkAdapterConfiguration(IPEnabled=0):
                tmpdict = {}
                tmpdict["Description"] = interface.Description
                tmpdict["MAC"] = interface.MACAddress
                tmplist.append(tmpdict)
            self.nic_obj = tmplist

    def get_network_mac_info(self):
        tmp_list = []
        for interface in self.nic_obj:
            if interface["MAC"] not in tmp_list and interface["MAC"] is not None:
                tmp_list.append(interface["MAC"])
        return tmp_list