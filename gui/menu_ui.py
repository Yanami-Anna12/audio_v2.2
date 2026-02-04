# -*- coding: utf-8 -*-
# time: 2023/3/15 14:14
# file: menu_ui.py
# describe: 菜单栏
# author: 胡能武
import tkinter as tk
from tkinter import DISABLED

from gui.my_comm_ui import MyCommUI
from utils.comm_utils import CommUtils


class MenuUI:
    def __init__(self):
        pass

    @staticmethod
    def pop_win_command(sw, sh):
        pop_win = tk.Toplevel()
        pop_win.title("说明内容")
        pop_win.resizable(height=False, width=False)
        # 计算中心坐标
        cen_x = (sw - 1000) / 2
        cen_y = (sh - 450) / 2
        # 设置窗口大小并居中
        pop_win.geometry('%dx%d+%d+%d' % (1000, 450, cen_x, cen_y))

        # 创建滚动条控件
        vertScrollbar = tk.Scrollbar(pop_win, orient='vertical')
        vertScrollbar.pack(side='right', fill='y')

        entry_1 = tk.Text(pop_win, width=50, height=8, bg="whitesmoke", fg='royalblue', font=("微软雅黑", 13))
        entry_1.place(x=0, y=0, width=980, height=450)
        entry_1.insert(tk.INSERT,
                       "功能说明：\r\n1、支持pcap、pcapng格式的数据文件提取出音频文件\r\n2、五统一的解码方式暂未适配，若有数据包请发给我适配\r\n3、过滤payload type是为了避免视频数据的干扰，减少音频源，过滤多个payload type时中间用小写逗号分隔\r\n\r\n")

        # 两个控件关联
        vertScrollbar.config(command=entry_1.yview)
        entry_1.config(yscrollcommand=vertScrollbar.set, state=DISABLED)

    # 显示版本号
    @staticmethod
    def show_version():
        MyCommUI.show_msg_box(f"版本号为：{CommUtils.now_version}")