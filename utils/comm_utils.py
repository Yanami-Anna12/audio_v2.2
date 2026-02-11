# -*- coding: utf-8 -*-
# time: 2022/11/14 15:13
# file: comm_utils.py
# describe: 文件功能描述
# author: 胡能武
import base64
import threading
from queue import Queue
from tkinter import NORMAL, END, DISABLED


class CommUtils:
    #############以上都为ymal数据##################
    # 版本号
    now_version = 'v1.2'

    #接口对应的方法名称
    now_function_name = ""

    #接口返回对应的解析方法
    interface_back_dict={}

    #当前解析出来的数据,一般是从返回的数据中解析，将json数据中的字段全部遍历出来，忽略层级结构
    calc_dict_data={}

    #波特率
    framerate_list = ["8000",'16000','22000',"44100","48000"]

    #音频类型
    audio_type_list=['wav','mp3']

    #解码方式
    decode_type_list = ["标准版","海康","浩云","ECPT","五统一","Adpcm","98设备"]

    #选择的波特率
    select_framerate = ""

    #选择的解码方式
    select_decode_type = ""

    #日志文件路径
    log_file_path=""

    # 存放文件夹的字典
    filepath_dict = {}

    # 保存测试结果的txt文件路径
    save_txt_file_path = {}

    # 图标的路径
    ico_path = ''
    main_ico_path = ""

    #pcap文件路径
    pcap_dir=""
    pcap_path="" #pcap文件路径
    result_path="" #校验的结果文件路径

    #实时日志输入框对象
    show_log_text = None

    # 屏幕默认的宽和高
    sw = 1920
    sh = 1080

    # 主ui对象
    main_ui = None

    #停止标记，用于强制停止测试
    is_stop=False

    #启动、停止按钮
    start_bt=None
    stop_bt=None
    select_stream_bt=None #重选音频流按钮
    play_bt=None #试听按钮


    #定义的nas协议基本数据
    nas_info_dict={}

    #当前接口的标题信息，后面写结果时会用到
    title_info=""

    #yml文件存储的数据
    all_datas={}

    # nas协议的几种音频数据包
    nas_audio_type = ['40', '41', '44', '45', '4E', '94']

    #解析一遍后的音频数据
    all_audio_datas = {}

    #选择的音频流信息
    real_select_info={}

    #选择的文件名称
    save_wav_name=''

    #选择的波特率
    select_rate=8000

    #要过滤的pyload type
    filter_payload_type=[]

    #将拆分出来的音频流保存起来
    audio_streams={}

    #音频类型
    select_audio_type=''

    #正在播放的音频对象
    play_audio=None



