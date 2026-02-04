# -*- coding: utf-8 -*-
# time: 2022/11/9 13:16
# file: time_utils.py
# describe: 文件功能描述
# author: 胡能武
import datetime
import time


class TimeUtils:
    #将秒钟转成时分秒的格式
    @staticmethod
    def sec_2_hms(sec:int):
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        if s<10:
            s=f"0{s}"
        if m<10:
            m=f"0{m}"
        if h<10:
            h=f"0{h}"
        need_time=f"{h}:{m}:{s}"
        return need_time


    @staticmethod
    # 获得一个时间戳
    def get_time_stamp(length=11):
        ts = int(round(time.time() * 1000))
        if length == 13:
            pass
        elif length == 10:
            ts = int(ts / 1000)
        elif length == 11:
            ts = int(ts / 100)
        return ts

    # 获取当前时间,精确到毫秒
    @staticmethod
    def get_now_time(accuracy='s',only_time=False):
        #accuracy 参数值为s、ms两种可选，精确到秒或毫秒
        if accuracy=="ms":
            if only_time:
                now = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
            else:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        else:
            if only_time:
                now = datetime.datetime.now().strftime('%H:%M:%S')
            else:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return now

    #获得当前时间字符串，用时间当文件名时使用
    @staticmethod
    def get_file_name_by_time():
        return datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
