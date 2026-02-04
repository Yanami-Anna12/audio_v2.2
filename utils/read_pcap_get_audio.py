# -*- coding: utf-8 -*-
# time: 2023/6/8 15:15
# file: read_pcap_get_audio.py
# describe: 从pcap文件中读出音频信息
# author: 胡能武

import dpkt
from scapy.all import *
from utils.comm_utils import CommUtils


class ReadPcapGetAudio:
    # h264的payload_type,用来过滤掉h264的数据
    h264_payload_type = []

    @staticmethod
    def get_audio_dict(file_path,num_lines=5000):
        #用一个字典存一下数据出现的次数，因为只出现一次的音频流要排除掉，因为没有数据
        show_count_dict={}
        check_count=0
        # 统计音频流数量
        audio_streams = {}
        pkt_type=ReadPcapGetAudio.check_pkt_type(file_path) #判断数据包的类型
        # 打开PCAP文件
        with open(file_path, 'rb') as f:
            # 使用pcap.pcap创建一个pcap文件的迭代器
            if pkt_type=="pcap":
                pcap = dpkt.pcap.Reader(f)
            elif pkt_type=="pcapng":
                pcap = dpkt.pcapng.Reader(f)
            else:
                return audio_streams
            # 遍历每个数据包
            for ts, buf in pcap:
                # 解析以太网头部
                eth = dpkt.ethernet.Ethernet(buf)
                if not isinstance(eth.data, dpkt.ip.IP): #不包含IP层，就不往下解析
                    continue
                # 解析IP头部
                ip = eth.data
                if not isinstance(ip.data, dpkt.udp.UDP): #判断是否为UDP数据包
                    continue
                # 解析UDP头部
                udp = ip.data
                udp_data=udp.data
                # 检查UDP长度是否大于12字节
                udp_len = len(udp_data)
                if udp_len <= 12:
                    continue
                # 判断是否为RTCP包,如果是RTCP包，直接抛弃
                if udp_data[1] == 200 or udp_data[1] == 201:
                    continue

                is_sip = False #sip的音频类型
                is_nas = False
                id = "无"
                # 检测是否为RTP包
                rtp_flag = (udp_data[0] >> 6) & 0x03
                # #在特定端口内的才判断为RTP包
                if rtp_flag == 2 and (udp.sport in range(16384, 32768) or udp.dport in range(16384, 32768)):
                    check_count += 1
                    is_sip=True
                    # 解析RTP头
                    rtp = dpkt.rtp.RTP(udp.data)
                    # 读取RTP包的payload type数据
                    payload_type = rtp.pt
                    #在这里判断是否为h264的数据,如果是h264的数据，这个数据就不往下解析了
                    if str(payload_type) in CommUtils.filter_payload_type:
                        continue
                #如果是nas协议，则抓一下ID
                if not is_sip:
                    data_type = udp_data[2:3].hex().upper()  # 数据类型
                    is_nas = data_type in CommUtils.nas_audio_type  # nas的音频类型
                    if is_nas:
                        id=udp_data[:2].hex().upper()
                #如果是nas的音频类型或sip的音频类型，则保存起来
                if is_sip or is_nas:
                    src_ip = socket.inet_ntoa(ip.src)
                    dst_ip = socket.inet_ntoa(ip.dst)
                    src_port = udp.sport
                    dst_port = udp.dport
                    key = (src_ip, dst_ip, src_port, dst_port)
                    if is_nas:
                        audio_streams[key] = {'agreement_type': "nas","pt":"无","id":id}
                    else:
                        audio_streams[key] = {'agreement_type': "sip","pt":payload_type,'id':id}
                    # 记录音频流的数据数量
                    show_count_dict = ReadPcapGetAudio.calc_stream_count(key, show_count_dict)
                    #将数据保存起来,后面解析成音频时就不要重复来解析数据包了
                    if key not in CommUtils.all_audio_datas.keys():
                        CommUtils.all_audio_datas[key]=[]
                    temp_value=CommUtils.all_audio_datas.get(key,[])
                    temp_value.append(udp_data.hex())
                    #这是一个全局的字典
                    CommUtils.all_audio_datas[key]=temp_value
        # 删除数据量少的流
        ReadPcapGetAudio.del_audio_streams(audio_streams, show_count_dict)
        return audio_streams

    #删除数据量少的流
    @staticmethod
    def del_audio_streams(audio_streams,show_count_dict):
        # 将SIP协议下只出现几次的数据删除掉
        for k, v in show_count_dict.items():
            if v <= 5:
                del audio_streams[k]

    #在单独的方法中统计音频流的数据量
    @staticmethod
    def calc_stream_count(key,show_count_dict):
        show_count = show_count_dict.get(key, 0)
        show_count_dict[key] = show_count + 1
        return show_count_dict

    #判断这个数据是否为h264,这个判断不准确
    @staticmethod
    def is_h264(udp_data,payload_type):
        # 判断是否为h264数据，如果是，则抛弃这个数据
        if udp_data[12:15].hex() == "010000":
            if payload_type not in ReadPcapGetAudio.h264_payload_type:
                ReadPcapGetAudio.h264_payload_type.append(payload_type)
                print(udp_data[12:15].hex(), payload_type)
            return True
        # 这里还是判断是否为h264,如果这个payload_type在h264_payload_type中，则抛弃这个数据
        if payload_type in ReadPcapGetAudio.h264_payload_type:
            return True
        return False


    #检查数据文件为pcap还是pcapng文件
    @staticmethod
    def check_pkt_type(file_path):
        # 打开PCAP文件
        with open(file_path, 'rb') as f:
            magic=f.read(4)
        # 判断文件类型
        if magic == b'\xd4\xc3\xb2\xa1': #pcap文件
            return "pcap"
        elif magic == b'\x0a\x0d\x0d\x0a': #pcapng文件
            return "pcapng"
        else:
            return "unknow"