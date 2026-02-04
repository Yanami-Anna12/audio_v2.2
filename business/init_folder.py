# -*- coding: utf-8 -*-
# time: 2022/10/28 10:33
# file: init_folder.py
# describe: 初始化文件夹、文件等基本数据
# author: 胡能武
import os
import time

from utils.comm_utils import CommUtils
from utils.file_utils import FileUtils
from utils.time_utils import TimeUtils


class InitFolder:
    def __init__(self):
        pass

    @staticmethod
    # 初始化文件夹、文件相关数据
    def init_folder():
        f_util = FileUtils()
        get_data_dir = os.path.join(FileUtils.get_local_path(), "get_data")  # 外层的get_data目录
        base_dir = os.path.join(get_data_dir, "base")  # 存放空白的音频波形图
        result_dir = os.path.join(get_data_dir, "result")  # 测试结果保存目录
        ico_dir = os.path.join(get_data_dir, "ico")  # ico图片目录
        pcap_dir = os.path.join(get_data_dir, "pcap_data")  # pcap文件数据
        wav_dir=os.path.join(get_data_dir, "save_wav")  # wav文件数据
        play_dir = os.path.join(get_data_dir, "play_wav")  # play音频文件数据临时存储

        #存储需要的目录
        CommUtils.filepath_dict['base_dir'] = base_dir
        CommUtils.filepath_dict['result_dir'] = result_dir
        CommUtils.filepath_dict['wav_dir']=wav_dir
        CommUtils.filepath_dict['play_dir']=play_dir

        CommUtils.ico_path = os.path.join(ico_dir, "main.png")  # GUI图标
        CommUtils.main_ico_path = os.path.join(ico_dir, "main.png")  # 应用图标

        # 创建外层get_data目录
        f_util.create_folder(get_data_dir)
        # 创建base目录
        f_util.create_folder(base_dir)
        # 创建save_wav文件夹
        f_util.create_folder(wav_dir)
        #清空结果文件夹
        InitFolder.clear_result()
        #清空音频文件夹
        f_util.create_folder(play_dir)
        f_util.del_file_by_dir(play_dir)

        # pcap的文件路径存储到工具类中，可全局使用
        CommUtils.pcap_dir = pcap_dir

        # 本次测试获得一次时间
        test_time = TimeUtils.get_file_name_by_time()

        # 保存为pcap文件的路径
        CommUtils.pcap_path = f'{pcap_dir}\\{test_time}.pcap'
        # 保存本次校验结果的文件路径
        CommUtils.result_path = f'{result_dir}\\{test_time}_result.txt'

        return base_dir, result_dir

    # 清空日志文件夹
    @staticmethod
    def clear_result():
        f_util = FileUtils()
        # 创建result目录
        f_util.create_folder(CommUtils.filepath_dict['result_dir'])
        # 删除所有result结果
        f_util.del_file_by_dir(CommUtils.filepath_dict['result_dir'])


    @staticmethod
    #保存校验结果为文件
    def save_result_to_txt():
        while True:
            if CommUtils.result_info.qsize()>0:
                #持续追加写入校验结果到txt中
                InitFolder.batch_save_txt(CommUtils.result_path)
            time.sleep(3)

    @staticmethod
    #追加写入文件
    def batch_save_txt(txt_path):
        # 再创建文件,写入日志
        with open(txt_path, "a+", encoding='utf-8') as f:
            while CommUtils.result_info.qsize()>0: #只要结果队列中有数据，就持续取数据
                info=CommUtils.result_info.get().replace("\033[33m", "").replace("\033[31m", "").replace("\033[32m","").replace("\033[37m", "").replace("\033[0m", "")
                f.write(info)
