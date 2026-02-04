# -*- coding: utf-8 -*-
# time: 2022/9/27 10:41
# file: yaml_utils.py
# author: 胡能武
import random

import yaml

from utils.comm_utils import CommUtils
from utils.file_utils import FileUtils


class YamlUtils:
    """解析yml文件的工具类"""
    def __init__(self,file_path=''):
        self.file_path=file_path

    #将yml文件初步解析出来
    def get_first_yaml(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            content = f.read()
        #将yaml文件解析成字典数据
        self.yaml_content = yaml.safe_load(content)
        if self.yaml_content is None or len(self.yaml_content)==0:
            self.yaml_content={}
        else:
            #取一下网卡名称
            get_iface=self.yaml_content.get("local_iface")
            #如果yml文件中配置了网卡名称，则以配置的为准
            if len(get_iface)>0:
                CommUtils.local_iface=get_iface
            #取一下是否保存pcap文件的
            CommUtils.save_pcap=self.yaml_content.get("save_pcap")

    #解析出具体的yml文件内容，所有取值过程在这里面完成
    def get_real_yaml(self):
        #先将yml文件中的内容读成字典格式
        self.get_first_yaml()
        CommUtils.all_datas = self.yaml_content


    #修改服务器地址
    def update_server_url(self,new_server):
        self.get_first_yaml() #先取一遍值
        # 将修改后的字典写入yaml
        with open(self.file_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(self.yaml_content, f, default_flow_style=False)

    #修改参数
    def update_yml(self,dicts):
        # 读取yaml文件
        self.get_first_yaml()
        for k,v in dicts.items():
            self.yaml_content[k]=v
        # 将修改后的字典写入yaml
        with open(self.file_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(self.yaml_content, f, default_flow_style=False)


m_yml=YamlUtils(FileUtils.get_local_path()+ "\\get_data\\base\\myconfig.yml")