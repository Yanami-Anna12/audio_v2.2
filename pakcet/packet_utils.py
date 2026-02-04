# -*- coding: utf-8 -*-
# time: 2022/10/21 14:59
# file: packet_utils.py
# author: 胡能武
import logging
import warnings

from scapy.config import conf
from scapy.layers.inet import TCP, IP

from utils.comm_utils import CommUtils
from utils.gui_utils import GuiUtils

warnings.filterwarnings("ignore")
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) #消除scapy的警告
# # 忽略警告
from utils.time_utils import TimeUtils
import os
from scapy.sendrecv import sniff
from scapy.utils import wrpcap, hexstr, PcapWriter


class PacketUtils:
    '''
    对网络包的处理类,读写pcap文件
    '''

    def __init__(self,file_path):
        self.pkts = []
        self.count = 0
        self.pcapnum = 0

    # 保存packet数据为pcap文件
    def save_packet_as_pcap(self, pkt,file_path):
        with PcapWriter(file_path, sync=True,append=True) as save:
            save.write(pkt)

    # 读取pcap文件
    def read_pcap_file(self, file_path):
        if os.path.exists(file_path):
            pkts = sniff(offline=file_path)
            count = 0
            while (count <= 2):
                count += 1
        else:
            print("dump fie %s not found." % file_path)

    # 批量保存pcap文件
    def batch_save_pcap(self, packet, pcap_path):
        self.pkts.append(packet)
        self.count += 1
        if self.count == 3:
            self.pcapnum += 1
            pname = f"{pcap_path}\pcap{self.pcapnum}.pcap"
            wrpcap(pname, self.pkts)
            self.pkts = []
            self.count = 0

    # 停止抓包
    def stop_filter(self, sniff_obj):
        if CommUtils.is_stop:
            return True
        else:
            return False


    # 保存packet数据
    def save_packet(self,packet):
        # 将包的数据存储到队列中
        CommUtils.my_pkts.put((packet, f'({TimeUtils.get_now_time("ms", only_time=True)})'))
        if CommUtils.save_pcap == 1:  # 为1的时候才保存为文件
            # 将包的数据保存为pcap文件
            self.save_packet_as_pcap(packet, CommUtils.pcap_path)

    '''
    iface:网卡名称
    count:要捕获数据包的数量，0为不限制数量
    filter:流量过滤规则
    prn:定义回调函数
    '''
    # 抓网络数据包
    def do_sniff(self):
        #先获取过滤命令
        real_sniff_code=f"(src host {CommUtils.src_ip} and dst host {CommUtils.dst_ip}) or (src host {CommUtils.dst_ip} and dst host {CommUtils.src_ip}) and (tcp or udp)"
        sniff(filter=real_sniff_code,iface=CommUtils.real_iface, count=0, prn=self.save_packet, stop_filter=self.stop_filter)
