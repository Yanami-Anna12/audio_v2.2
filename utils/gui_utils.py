# -*- coding: utf-8 -*-
# time: 2023/3/9 16:10
# file: gui_utils.py
# describe: GUI常用方法
# author: 胡能武
from tkinter import NORMAL, END, DISABLED

from utils.comm_utils import CommUtils
from utils.file_utils import FileUtils


class GuiUtils:
    @staticmethod
    # 限制entry仅能输入数字
    def input_only_number(content,max_value):
        if (content.isdigit() and int(content) <= int(max_value)) or content == "":
            return True
        else:
            return False

    @staticmethod
    # 限制输入框只能输入IP
    def only_ip_input(content):
        allow_ip_data = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
        input_data = content[-1:]
        if (content == "" or input_data in allow_ip_data) and len(content)<=15:
            return True
        else:
            return False

    @staticmethod
    def check_is_ip(ip_str,more_info=""):
        ip_str = ip_str.strip()  # 去掉前后空格
        ip_list = ip_str.split(".")  # 将字符串按点分割成列表
        flag = True
        for num in ip_list:
            if len(ip_list) == 4 and num.isdigit() and 0 <= int(num) <= 255:
                continue
            else:
                flag = False
                break
        if flag:
            return True, ""
        else:
            return False, f"{more_info}ip地址不合法"


    #界面信息打印
    @staticmethod
    def custom_print_only(real_info,color_type="black"):
        CommUtils.show_log_text.config(state=NORMAL)  # 解锁
        totalLen = len(CommUtils.show_log_text.get(1.0, END).split("\n"))  # 获得日志总行数
        if totalLen - 2 >= 1000:  # 大于1000行就每次删除第一行
            CommUtils.show_log_text.delete('1.0', '2.0')
        show_info = f'{real_info}\n'.replace("\n\n", '\n')
        CommUtils.show_log_text.insert(END, show_info,(color_type,))  # 写入新的日志
        CommUtils.show_log_text.see("end")  # 显示最后的数据
        CommUtils.show_log_text.config(state=DISABLED)  # 锁上


    #批量打印信息
    @staticmethod
    def batch_print_only(info_list):
        CommUtils.show_log_text.config(state=NORMAL)  # 解锁
        need_save_context=CommUtils.title_info #默认先加上标题
        for info in info_list:
            totalLen = len(CommUtils.show_log_text.get(1.0, END).split("\n"))  # 获得日志总行数
            if totalLen - 2 >= 1000:  # 大于1000行就每次删除第一行
                CommUtils.show_log_text.delete('1.0', '2.0')
            show_info = f'{info[0]}\n'.replace("\n\n", '\n')
            need_save_context+=show_info #将所有日志拼在一起，一次写入txt时用到
            CommUtils.show_log_text.insert(END, show_info,(info[1],))  # 写入新的日志
        CommUtils.show_log_text.see("end")  # 显示最后的数据
        CommUtils.show_log_text.config(state=DISABLED)  # 锁上
        #保存数据到txt中
        FileUtils.save_txt(CommUtils.result_path,need_save_context+"\n")

    #点了停止按钮或测试结束时要做的事情
    @staticmethod
    def stop_dothing():
        GuiUtils.custom_print_only("已停止数据抓取")
        CommUtils.is_stop = True
        CommUtils.start_bt.config(state=NORMAL)
        CommUtils.stop_bt.config(state=DISABLED)