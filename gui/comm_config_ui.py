# -*- coding: utf-8 -*-
# time: 2023/3/15 15:20
# file: comm_config_ui.py
# describe: 通用配置页面
# author: 胡能武
import threading
from tkinter import LEFT, RIGHT, Y, font, DISABLED, NORMAL, filedialog, W, E
from tkinter.ttk import Combobox
import pygame
from analysis.comm_analysis import CommAnalysis
from gui.my_comm_ui import MyCommUI
from utils.comm_utils import CommUtils
import tkinter as tk

from utils.file_utils import FileUtils
from utils.gui_utils import GuiUtils
from utils.read_pcap_get_audio import ReadPcapGetAudio
from utils.scale_utils import ScaleUtils


class CommConfigUI:
    def __init__(self):
        pass


    def show_ui(self, now_ui, w, h):
        move_y = 0
        # 显示已选择的文件路径
        self.select_entry_text = tk.StringVar()
        self.select_label = tk.Entry(now_ui, textvariable=self.select_entry_text, state=DISABLED)
        self.select_label.place(x=30, y=0, width=230, height=25)
        # 选择文件的按钮
        self.l_select_bt = tk.Button(now_ui, text="选pcap文件", command=self.get_select_path)
        self.l_select_bt.place(x=265, y=0, width=80, height=25)

        #音频类型
        MyCommUI.comm_label(now_ui, place_x=42, place_y=30 + move_y, view_w=110, view_h=25,
                            show_val='音频类型：')
        self.c_audio_type = Combobox(now_ui, values=CommUtils.audio_type_list, state="readonly")
        self.c_audio_type.place(x=130, y=30 + move_y, width=160, height=25)
        self.c_audio_type.current(0)

        #波特率
        MyCommUI.comm_label(now_ui, place_x=48, place_y=60 + move_y, view_w=110, view_h=25,
                            show_val='波特率：')
        self.c_interface_type = Combobox(now_ui, values=CommUtils.framerate_list, state="readonly")
        self.c_interface_type.place(x=130, y=60 + move_y, width=160, height=25)
        self.c_interface_type.current(0)

        #用哪种方式解码
        MyCommUI.comm_label(now_ui, place_x=32, place_y=90 + move_y, view_w=110, view_h=25,
                            show_val='解码方式选择：')
        self.c_protocol_type = Combobox(now_ui, values=CommUtils.decode_type_list, state="readonly")
        self.c_protocol_type.place(x=130, y=90 + move_y, width=160, height=25)
        self.c_protocol_type.current(0)

        # 要过滤的payload type
        MyCommUI.comm_label(now_ui, place_x=5, place_y=120 + move_y, view_w=123, view_h=25,show_val='过滤的payload type：')
        self.e_filter_payload_type, self.v_filter_payload_type = MyCommUI.comm_input_entry(
            CommUtils.main_ui, now_ui, place_x=130, place_y=120 + move_y, view_w=160, view_h=25,
            show_val=CommUtils.all_datas['filter_payload_type'], entry_type='comm_str')

        # 启动按钮
        self.start_bt = tk.Button(now_ui, text="保存音频", command=self.start_bt_click)
        self.start_bt.place(x=w/2-80, y=h-435, width=70, height=25)
        CommUtils.start_bt=self.start_bt

        # 打开音频流选择界面
        self.select_stream_bt = tk.Button(now_ui, text="重选音频流", command=self.re_select_stream_click)
        self.select_stream_bt.place(x=w/2+20, y=h-435, width=70, height=25)
        CommUtils.select_stream_bt=self.select_stream_bt
        self.select_stream_bt.config(state=DISABLED)

        # 试听按钮
        self.play_bt = tk.Button(now_ui, text="试听音频", command=self.play_bt_click)
        self.play_bt.place(x=w/2-80, y=h-400, width=70, height=25)
        self.play_bt.config(state=DISABLED)
        CommUtils.play_bt=self.play_bt

        # 停止试听
        self.start_bt = tk.Button(now_ui, text="停止试听", command=self.stop_play_click)
        self.start_bt.place(x=w/2+20, y=h-400, width=70, height=25)
        CommUtils.start_bt=self.start_bt

        # 打开截图目录
        self.show_screen_bt = tk.Button(now_ui, text="查看音频", command=lambda: FileUtils.open_directory(CommUtils.filepath_dict['wav_dir']))
        self.show_screen_bt.place(x=w/2-80, y=h-365, width=70, height=25)

        # 清空日志
        self.show_screen_bt = tk.Button(now_ui, text="清空日志", command=self.clear_log)
        self.show_screen_bt.place(x=w/2+20, y=h-365, width=70, height=25)

    # 获得选择的文件路径
    def get_select_path(self):
        #过滤的payload type
        CommUtils.filter_payload_type=self.e_filter_payload_type.get().split(",")
        s_path = filedialog.askopenfilename(title='请选择文件', filetypes=[("PCAPNG", "pcapng"),("PCAP", "pcap")])
        if len(s_path) > 0:
            self.select_entry_text.set(s_path)  # 直接改变值即可
            CommUtils.all_audio_datas={} #清空之前保存的解析过一遍的音频数据
            self.show_audio_select_page(s_path) #显示音频流选择窗口

    #重选流按钮
    def re_select_stream_click(self):
        self.show_audio_select_page(file_path="",re_analysis=False)

    # 弹出音频流选择框
    def show_audio_select_page(self, file_path, w=600, h=400,re_analysis=True):
        if len(CommUtils.audio_streams)==0 and re_analysis==False:
            GuiUtils.custom_print_only("没有音频流数据，请重新选择pcapng文件")
            return
        pop_win = tk.Toplevel(relief="ridge", borderwidth=1)
        pop_win.title("音频流选择")
        pop_win.resizable(height=False, width=False)
        # 计算中心坐标
        cen_x = (CommUtils.sw - w) / 2
        cen_y = (CommUtils.sh - h) / 2
        # 设置窗口大小并居中
        pop_win.geometry('%dx%d+%d+%d' % (w, h, cen_x, cen_y))

        # 创建 Canvas 和滚动条
        canvas = tk.Canvas(pop_win)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(pop_win, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.config(yscrollcommand=scrollbar.set)

        # 在 Canvas 中创建一个 Frame
        frame = tk.Frame(canvas)

        radio_buttons = []
        # 设置一个变量来存储选中的值
        self.selected_option = tk.StringVar()
        #每次重新解析
        if re_analysis:
            CommUtils.audio_streams = ReadPcapGetAudio.get_audio_dict(file_path=file_path)
        first_data = ''  # 第一个值要默认选中
        hang = 0
        all_ip_list = []
        for i, stream in enumerate(CommUtils.audio_streams.items()):
            key, stats = stream
            src_ip, dst_ip, src_port, dst_port = key
            # 显示的值
            show_info = f'【{stats["agreement_type"]}】源:{src_ip}:{src_port} ID为：{ScaleUtils.get_device_id(stats["id"])}->目标:{dst_ip}:{dst_port}  Payload type:{stats["pt"]}'
            save_info = f'{src_ip}*{src_port}*{dst_ip}*{dst_port}*{stats["agreement_type"]}*{stats["pt"]}*{stats["id"]}'  # 保存的值，选中后，就能取到这个值
            if i == 0:
                first_data = save_info
            temp_option = tk.Radiobutton(frame, text=show_info, variable=self.selected_option, value=save_info)
            radio_buttons.append(temp_option)
            radio_buttons[-1].grid(row=i, column=0, columnspan=2, padx=50, pady=5, sticky=W)
            hang = i
            all_ip_list.append(src_ip)
            all_ip_list.append(dst_ip)
        all_ip_list = list(set(all_ip_list))  # 列表去重
        self.selected_option.set(first_data)
        # 让重选流按钮可点击
        CommUtils.select_stream_bt.config(state=NORMAL)
        # 让播放按钮可点击
        CommUtils.play_bt.config(state=NORMAL)

        # 开始本地分析的按钮
        self.select_audio_bt = tk.Button(frame, text="确定", width=8,command=lambda: self.select_audio_ok(self.selected_option.get(),pop_win))
        radio_buttons.append(self.select_audio_bt)
        radio_buttons[-1].grid(row=hang+3, column=0,padx=30, pady=10,sticky=E)
        # 停止按钮
        self.cancel_select_bt = tk.Button(frame, text="取消", width=8,command=lambda: self.select_audio_cancel(pop_win))
        radio_buttons.append(self.cancel_select_bt)
        radio_buttons[-1].grid(row=hang+3, column=1,padx=1, pady=10,sticky=W)

        frame.pack_propagate(False)
        pop_win.columnconfigure(0, weight=1, minsize=20)
        pop_win.columnconfigure(1, weight=1, minsize=20)
        # 通过 create_window 方法将 Frame 添加到 Canvas 中
        canvas.create_window((0, 0), window=frame, anchor='nw')
        pop_win.update_idletasks()

        # 更新 Canvas 的滚动区域
        canvas.config(scrollregion=canvas.bbox('all'))

    #选择了一路声音，在这个入口去触发解析
    def select_audio_ok(self, select_infos, ui_obj):
        # 新增：打印原始数据，方便排查（可选）
        print(f"选中的音频流信息：{select_infos}")
        temp_infos = select_infos.split("*")
        # 新增：数据补全，避免索引越界
        while len(temp_infos) < 7:  # 确保至少7个元素（src_ip*src_port*dst_ip*dst_port*protocol*pt*id）
            temp_infos.append("")

        src_ip = temp_infos[0] if temp_infos[0] else "0.0.0.0"  # 源IP
        src_port = temp_infos[1] if temp_infos[1] else "0"  # 源端口
        dst_ip = temp_infos[2] if temp_infos[2] else "0.0.0.0"  # 目标IP
        dst_port = temp_infos[3] if temp_infos[3] else "0"  # 目标端口
        protocol_type = temp_infos[4] if temp_infos[4] else "sip"  # 协议类型
        payload_type = temp_infos[5] if temp_infos[5] else "0"  # payload_type
        id = temp_infos[6] if temp_infos[6] else "0"

        # 新增：校验核心字段，为空则提示
        if not src_ip or not dst_ip:
            GuiUtils.custom_print_only("⚠️ 音频流IP信息异常，可能是PCAP文件无有效数据！", "red")
            ui_obj.destroy()
            return

        # 拼接key,这个key是用来获取保存的音频数据的
        view_key = (src_ip, dst_ip, int(src_port), int(dst_port))
        CommUtils.real_select_info["src_ip"] = src_ip
        CommUtils.real_select_info["src_port"] = src_port
        CommUtils.real_select_info["dst_ip"] = dst_ip
        CommUtils.real_select_info["dst_port"] = dst_port
        CommUtils.real_select_info["protocol_type"] = protocol_type
        CommUtils.real_select_info["payload_type"] = payload_type
        CommUtils.real_select_info["select_infos"] = select_infos
        CommUtils.real_select_info["key"] = view_key
        CommUtils.real_select_info["id"] = id

        show_info = f'【{protocol_type}】源:{src_ip}:{src_port} ID为：{ScaleUtils.get_device_id(id)}->目标:{dst_ip}:{dst_port}  Payload type:{payload_type}'
        GuiUtils.custom_print_only(f"已选择:{show_info}")
        # 关闭音频选择界面
        ui_obj.destroy()

    #取消选择
    def select_audio_cancel(self,ui_obj):
        # 关闭音频选择界面
        ui_obj.destroy()

    #试听音频
    def play_bt_click(self):
        CommUtils.is_stop=False
        # 当前的波特率
        CommUtils.select_rate = int(self.c_interface_type.get())
        # 过滤的payload type
        CommUtils.filter_payload_type = self.e_filter_payload_type.get().split(",")
        # 当前的解码方式
        CommUtils.select_decode_type = self.c_protocol_type.get()
        #当前的音频类型
        CommUtils.select_audio_type=self.c_audio_type.get()

        if len(CommUtils.real_select_info)>0:
            # 启动一个线程来做数据解析
            comm_analysis = CommAnalysis()
            self.t_play = threading.Thread(target=comm_analysis.analysis_and_play)
            self.t_play.setDaemon(True)
            self.t_play.start()
            self.play_bt.config(state=DISABLED)
        else:
            GuiUtils.custom_print_only("请先选择一路音频流")


    #停止试听
    def stop_play_click(self):
        CommUtils.is_stop=True
        #mp3试听，在这里停止
        if CommUtils.play_audio:
            pygame.mixer.music.stop()
            CommUtils.play_audio=None

    #清空日志
    def clear_log(self):
        CommUtils.show_log_text.config(state=NORMAL)  # 解锁
        #totalLen = len(CommUtils.show_log_text.get(1.0, END).split("\n"))  # 获得日志总行数
        CommUtils.show_log_text.delete('1.0', "end")
        CommUtils.show_log_text.config(state=DISABLED)  # 锁上

    # 启动前的数据和界面初始化
    def init_data_and_ui(self):
        #当前的波特率
        CommUtils.select_rate=int(self.c_interface_type.get())
        # 过滤的payload type
        CommUtils.filter_payload_type = self.e_filter_payload_type.get().split(",")
        #当前的解码方式
        CommUtils.select_decode_type=self.c_protocol_type.get()
        #当前的音频类型
        CommUtils.select_audio_type=self.c_audio_type.get()
        self.start_bt.config(state=DISABLED)
        return True

    # 启动任务的按钮事件
    def start_bt_click(self):
        CommUtils.is_stop=False
        result=self.init_data_and_ui()  # 数据和界面初始化
        if result: #初始化通过才会启动
            if len(CommUtils.real_select_info)>0:
                # 启动一个线程来做数据解析
                comm_analysis = CommAnalysis()
                t_analysis = threading.Thread(target=comm_analysis.analysis_data)
                t_analysis.setDaemon(True)
                t_analysis.start()
            else:
                GuiUtils.custom_print_only("请先选择一路音频流")
                self.start_bt.config(state=NORMAL)

    # 停止测试
    def stop_bt_click(self):
        CommUtils.is_stop = True
        self.start_bt.config(state=NORMAL)
        GuiUtils.custom_print_only("任务手动停止")
