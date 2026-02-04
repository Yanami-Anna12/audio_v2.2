# -*- coding: utf-8 -*-
# time: 2023/3/15 14:03
# file: my_comm_ui.py
# describe: 通用的UI控件或方法
# author: 胡能武
# 弹出提示框
from tkinter import messagebox, DISABLED
import tkinter as tk

from utils.comm_utils import CommUtils
from utils.gui_utils import GuiUtils


class MyCommUI:
    def __init__(self):
        pass

    # 创建一个显示区
    @staticmethod
    def create_show_label(main_ui,x,y,width,height):
        # 显示提示信息
        CommUtils.show_msg = tk.StringVar()
        show_info_label = tk.Label(main_ui, textvariable=CommUtils.show_msg, font=("楷体", 14), bg="honeydew")
        show_info_label.place(x=x, y=y, width=width, height=height)

    #信息提示框
    @staticmethod
    def show_msg_box(msg_str):
        result = messagebox.askokcancel(title='提示', message=msg_str)
        return result


    # 配置窗口的基本属性
    @staticmethod
    def set_gui_info(now_ui,title, width, height):
        now_ui.title(title)
        now_ui.resizable(height=False, width=False)
        now_page_width = width  # 编辑页面的宽
        now_page_height = height  # 编辑页面的高
        # 计算中心坐标
        cen_x = (CommUtils.sw - now_page_width) / 2
        cen_y = (CommUtils.sh - now_page_height) / 2
        # 设置窗口大小并居中
        now_ui.geometry('%dx%d+%d+%d' % (now_page_width, now_page_height, cen_x, cen_y))
        # now_ui.configure(bg="gainsboro")


    # Entry输入框
    @staticmethod
    def comm_input_entry(base_ui, now_ui, place_x, place_y, view_w, view_h, show_val, entry_type, max_value='',
                         is_int=False):
        if is_int:  # 输入框内容的类型为int型
            v_val = tk.IntVar()
        else:  # 其它的为字符串型
            v_val = tk.StringVar()
        if entry_type == "ip":
            check_ip = base_ui.register(GuiUtils.only_ip_input)
            entry_obj = tk.Entry(now_ui, textvariable=v_val, validate="key", validatecommand=(check_ip, '%P'))
        elif entry_type == "number":
            check_number = base_ui.register(GuiUtils.input_only_number)
            entry_obj = tk.Entry(now_ui, textvariable=v_val, validate='key',
                                 validatecommand=(check_number, '%P', max_value))
        else:
            entry_obj = tk.Entry(now_ui, textvariable=v_val)
        entry_obj.place(x=place_x, y=place_y, width=view_w, height=view_h)
        v_val.set(show_val)
        return entry_obj, v_val

    # Label控件
    @staticmethod
    def comm_label(now_ui, place_x, place_y, view_w, view_h, show_val):
        v_val = tk.StringVar()
        now_label = tk.Label(now_ui, textvariable=v_val)
        now_label.place(x=place_x, y=place_y, width=view_w, height=view_h)
        v_val.set(show_val)
        return now_label, v_val

    #Text控件
    @staticmethod
    def comm_text(now_ui, place_x, place_y, view_w, view_h,scroll_bar=None):
        if scroll_bar: #有滚动条
            now_text=tk.Text(now_ui,yscrollcommand=scroll_bar.set,width=view_w,height=view_h)
        else: #无滚动条
            now_text = tk.Text(now_ui,  width=view_w, height=view_h)
        now_text.place(x=place_x, y=place_y)
        now_text.config(state=DISABLED)
        return now_text


    # 点击取消按钮后，关闭弹出窗口
    @staticmethod
    def cancel_update(ui_obj):
        ui_obj.destroy()

        # 初始化 toplevel 对象

    @staticmethod
    def init_toplevel(title, main_obj, width, height):
        pop_win = tk.Toplevel()
        MyCommUI.set_gui_info(pop_win, title, width, height)
        pop_win.transient(main_obj)  # 只保留关闭按钮，main_obj是启动这个窗口的父窗口对象
        return pop_win, width, height

    # 创建自定义提示框
    @staticmethod
    def custom_msg_box(msg, main_obj):
        get_root, w, h = MyCommUI.init_toplevel("提示框", main_obj, width=200, height=100)
        show_msg = tk.Label(get_root, text=msg,wraplength=190)
        show_msg.place(x=5, y=0, width=190,height=60)

        ok_bt = tk.Button(get_root, text="确定", command=lambda: MyCommUI.cancel_update(get_root))
        ok_bt.place(relx=.5, rely=.7, anchor="center", width=60)
