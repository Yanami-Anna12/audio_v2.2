# -*- coding: utf-8 -*-
# time: 2023/3/1 10:08
# file: real_gui.py
# describe: 主UI页面
# author: 胡能武
import sys
import tkinter as tk

from gui.comm_config_ui import CommConfigUI
from gui.log_ui import LogUI
from gui.my_comm_ui import MyCommUI
from gui.menu_ui import MenuUI
from utils.comm_utils import CommUtils


class RealGui:
    def __init__(self):
        self.is_runing = False  # 是否在分析数据
        # 创建tkinter主界面
        self.root = tk.Tk()
        CommUtils.main_ui=self.root
        self.width = 1050  # GUI的宽
        self.height = 600  # GUI的高
        CommUtils.sw = self.root.winfo_screenwidth()
        CommUtils.sh = self.root.winfo_screenheight()
        MyCommUI.set_gui_info(self.root,"从数据包提取音频工具", self.width, self.height)  # 设置窗口标题、+居中等属性
        # 禁止改变窗口大小
        self.root.resizable(height=False, width=False)
        # 设置图标
        self.root.iconphoto(True, tk.PhotoImage(file=CommUtils.main_ico_path))
        CommUtils.n_root = self.root
        # 下面这一句最重要，是接收到关闭点击操作的语句,之后调用函数
        self.root.protocol("WM_DELETE_WINDOW", self.real_destroy)

        #配置页
        self.frame0 = tk.LabelFrame(self.root, text="通用配置")
        self.frame0.place(x=700, y=0, width=350, height=self.height)
        config_ui=CommConfigUI()
        config_ui.show_ui(self.frame0,w=350,h=self.height) #显示UI

        # 日志区
        self.frame5 = tk.LabelFrame(self.root, text="实时日志")
        self.frame5.place(x=0, y=0, width=700, height=self.height)
        log_ui=LogUI()
        log_ui.show_ui(self.frame5,w=700,h=self.height) #显示UI

        # 创建菜单栏
        self.create_menu()


    # 创建菜单栏
    def create_menu(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=False)
        filemenu.add_command(label='使用说明', command=lambda: MenuUI.pop_win_command(CommUtils.sw,CommUtils.sh))
        filemenu.add_command(label='关于', command=MenuUI.show_version)
        menubar.add_cascade(label='帮助', menu=filemenu)
        self.root.config(menu=menubar)

    # 停止分析
    def stop_draw(self):
        CommUtils.can_refresh = False  # 所有线程的循环停止
        # CommUtils.clear_queue_data(CommUtils.my_pkts) #清空之前未计算的数据包

    # 点击右上角关闭按钮后触发
    def real_destroy(self):
        CommUtils.can_refresh = False
        self.root.destroy()
        sys.exit(0)

    # 开始绘制
    def start_draw_gui(self):
        self.root.mainloop()