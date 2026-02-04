# -*- coding: utf-8 -*-
# time: 2023/3/16 9:15
# file: log_ui.py
# describe: 文件功能描述
# author: 胡能武
import json
import tkinter as tk
from tkinter import END, NORMAL, DISABLED, RIGHT, Y, font

from gui.my_comm_ui import MyCommUI
from utils.comm_utils import CommUtils


class LogUI:
    def __init__(self):
        pass

    def show_ui(self, now_ui, w, h):
        move_y = 0
        # 创建滚动条
        scroll_bar = tk.Scrollbar(now_ui)
        # 设置垂直滚动条显示的位置，使得滚动条，靠右侧；通过 fill 沿着 Y 轴填充
        scroll_bar.pack(side=RIGHT, fill=Y)
        CommUtils.show_log_text = MyCommUI.comm_text(now_ui, place_x=6, place_y=5 + move_y, view_w=95, view_h=59,
                                                     scroll_bar=scroll_bar)
        #设置字体大小
        # my_font = font.Font(size=10)
        # CommUtils.show_log_text.config(font=my_font)

        #设置颜色值
        CommUtils.show_log_text.tag_configure("red", foreground="red")
        CommUtils.show_log_text.tag_configure("green", foreground="green")
        CommUtils.show_log_text.tag_configure("blue", foreground="blue") #蓝色
        CommUtils.show_log_text.tag_configure("yellow", foreground="yellow") #黄色
        CommUtils.show_log_text.tag_configure("black", foreground="black") #黑色
        CommUtils.show_log_text.tag_configure("purple", foreground="purple") #紫色
        CommUtils.show_log_text.tag_configure("orange", foreground="orange") #橙色
        CommUtils.show_log_text.tag_configure("blueviolet", foreground="blueviolet")  # 深橙色
        # 设置滚动条，使用 yview使其在垂直方向上滚动 Listbox 组件的内容，通过绑定 Scollbar 组件的 command 参数实现
        scroll_bar.config(command=CommUtils.show_log_text.yview)