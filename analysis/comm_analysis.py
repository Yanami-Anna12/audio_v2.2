# -*- coding: utf-8 -*-
# time: 2023/10/20 13:15
# file: comm_analysis.py
# describe: 通用的解析数据的方法
# author: 胡能武
import audioop
import binascii
import os
import time
import wave

from tkinter import NORMAL, DISABLED
import pyaudio
import pygame

from services.data_decode import DataDecode
from utils.comm_utils import CommUtils
from utils.gui_utils import GuiUtils
from utils.scale_utils import ScaleUtils
from utils.time_utils import TimeUtils


class CommAnalysis():
    def __init__(self):
        pass

    #在这里面做数据解析，将选择的音频信息解析出来
    def analysis_data(self):
        #读取选择的音频源的参数
        src_ip=CommUtils.real_select_info["src_ip"]
        src_port=CommUtils.real_select_info["src_port"]
        dst_ip=CommUtils.real_select_info["dst_ip"]
        dst_port=CommUtils.real_select_info["dst_port"]
        protocol_type=CommUtils.real_select_info["protocol_type"]
        payload_type=CommUtils.real_select_info["payload_type"]
        view_key = CommUtils.real_select_info["key"]
        #拼接要保存的文件路径
        CommUtils.save_wav_name=f'{protocol_type}源_{src_ip}目标{dst_ip} {TimeUtils.get_file_name_by_time().replace("_","")}'
        # 拼接最终的文件路径
        save_path = f'{CommUtils.filepath_dict["wav_dir"]}/{CommUtils.save_wav_name}.{CommUtils.select_audio_type}'

        #读取存储的数据内容
        need_audio_info=CommUtils.all_audio_datas.get(view_key,[])
        #用一个标志记录保存状态
        save_result=True

        if CommUtils.select_audio_type=="mp3":
            save_result=self.save_to_mp3(save_path,need_audio_info,protocol_type)
        else:
            with wave.open(save_path, "wb") as wav_file:
                # 设置wav文件的参数
                wav_file.setnchannels(1)  # 单声道
                wav_file.setsampwidth(2)  # 16位
                wav_file.setframerate(CommUtils.select_rate)  # 44.1kHz
                for infos in need_audio_info:
                    #获取真实音频数据，并从字符流转成字节流
                    if protocol_type=="nas":
                        need_data= binascii.unhexlify(infos[16:])
                    else:
                        need_data = binascii.unhexlify(infos[24:])
                        if payload_type=="0":
                            #将g711 pcmu编码解码出来
                            need_data = audioop.ulaw2lin(need_data, 2)
                        elif payload_type=="8":
                            # 将g711 pcma编码解码出来
                            need_data = audioop.alaw2lin(need_data, 2)
                    #将数据解密
                    need_data, result = self.decode_data(need_data)
                    if not result:
                        GuiUtils.custom_print_only("保存出错了，请检查解码方式是否正确！", "red")
                        save_result=False
                        wav_file.close()
                        os.remove(save_path)
                        break
                    wav_file.writeframes(need_data)  # 写入数据
        #保存文件成功才提示
        if save_result:
            #转换成完成的提示和界面改变操作
            GuiUtils.custom_print_only(f"提取音频成功,文件名：{CommUtils.save_wav_name}.{CommUtils.select_audio_type}\n\n")
        CommUtils.start_bt.config(state=NORMAL)


    #在这里面做数据解析，将选择的音频信息解析出来
    def analysis_and_play(self):
        #读取选择的音频源的参数
        src_ip=CommUtils.real_select_info["src_ip"]
        src_port=CommUtils.real_select_info["src_port"]
        dst_ip=CommUtils.real_select_info["dst_ip"]
        dst_port=CommUtils.real_select_info["dst_port"]
        protocol_type=CommUtils.real_select_info["protocol_type"]
        payload_type=CommUtils.real_select_info["payload_type"]
        view_key = CommUtils.real_select_info["key"]
        id = CommUtils.real_select_info["id"]
        #拼接要保存的文件路径
        show_info=f'【{protocol_type}】源:{src_ip}:{src_port} ID为：{ScaleUtils.get_device_id(id)}->目标:{dst_ip}:{dst_port}  Payload type:{payload_type}'
        GuiUtils.custom_print_only(f"正在试听{show_info}",color_type='green')
        # 读取存储的数据内容
        need_audio_info = CommUtils.all_audio_datas.get(view_key, [])

        #这里试听也有两种情况
        if CommUtils.select_audio_type == "mp3":
            # 拼接要保存的文件路径
            CommUtils.save_wav_name = f'{protocol_type}源_{src_ip}目标{dst_ip} {TimeUtils.get_file_name_by_time().replace("_", "")}'
            # 拼接最终的文件路径
            save_path = f'{CommUtils.filepath_dict["play_dir"]}/{CommUtils.save_wav_name}.{CommUtils.select_audio_type}'
            save_result = self.save_to_mp3(save_path, need_audio_info, protocol_type)
            if save_result: #保存成功了
                try:
                    pygame.mixer.init()
                    pygame.mixer.music.load(save_path)
                    pygame.mixer.music.play()
                    CommUtils.play_audio='playing'
                    while True:
                        if not pygame.mixer.music.get_busy():
                            time.sleep(1)
                            break
                except Exception as e:
                    GuiUtils.custom_print_only(f"{show_info} 数据解码异常，播放出错:{e}！",color_type='red')
        else: #非mp3文件
            # 设置音频参数
            CHANNELS = 1
            WIDTH = 2
            RATE = CommUtils.select_rate
            # 创建PyAudio对象
            p = pyaudio.PyAudio()
            # 打开流
            stream = p.open(format=p.get_format_from_width(WIDTH),
                            channels=CHANNELS,
                            rate=RATE,
                            output=True)

            try:
                # 读取音频数据并播放
                for infos in need_audio_info:
                    if protocol_type == "nas":
                        need_data = binascii.unhexlify(infos[16:])
                    else:
                        need_data = binascii.unhexlify(infos[24:])
                        if payload_type == "0":
                            need_data = audioop.ulaw2lin(need_data, 2)
                        elif payload_type == "8":
                            need_data = audioop.alaw2lin(need_data, 2)
                    if CommUtils.is_stop: #如果点了停止试听，则跳出循环
                        break
                    # 将数据解密
                    need_data,result = self.decode_data(need_data)
                    if not result:
                        GuiUtils.custom_print_only("试听出错了，请检查解码方式是否正确！","red")
                        break
                    stream.write(need_data)
            except Exception as e:
                GuiUtils.custom_print_only(f"试听出错了:{e}","red")

            # 停止数据流
            stream.stop_stream()
            stream.close()

            # 关闭PyAudio
            p.terminate()

        CommUtils.play_bt.config(state=NORMAL)
        GuiUtils.custom_print_only("试听结束")


    #将加密的数据解密
    # # def decode_data(self,data):
    #     try:
    #         if CommUtils.select_decode_type=="Adpcm":
    #             decode_data = DataDecode.ADPCMDecoder(data, len(data))
    #             # 修复1:增加空值/空字节判断
    #             return decode_data if decode_data else (b'', False)
    #         elif CommUtils.select_decode_type=="海康":
    #             decode_data = DataDecode.ADPCMDecoder(data,0x41)
    #             return decode_data if decode_data else (b'', False)
    #         elif CommUtils.select_decode_type=="浩云":
    #             decode_data = DataDecode.ECPT(data, 0x71)
    #             return decode_data if decode_data else (b'', False)
    #         elif CommUtils.select_decode_type=="ECPT":
    #             decode_data = DataDecode.ECPT(data, 0x60)
    #             return decode_data if decode_data else (b'', False)
    #         elif CommUtils.select_decode_type=="98设备":
    #             decode_data = DataDecode.ECPT(data,0x98)
    #             return decode_data if decode_data else (b'', False)
    #         else:
    #             return data,True
    #     except Exception as e:
    #         # # 打印具体的异常信息,方便调试
    #         GuiUtils.custom_print_only(f"解码异常：{str(e)}", "red")
    #         return b'',False


    # 将数据解密
    def decode_data(self, data):
        try:
            if CommUtils.select_decode_type == "Adpcm":
                decoded = DataDecode.ADPCMDecoder(data, len(data))
                if decoded is None or len(decoded) == 0:
                    return b'', False
                return decoded, True

            elif CommUtils.select_decode_type == "海康":
                decoded = DataDecode.ECPT(data, 0x41)
                if decoded is None or len(decoded) == 0:
                    return b'', False
                return decoded, True

            elif CommUtils.select_decode_type == "浩云":
                decoded = DataDecode.ECPT(data, 0x71)
                if decoded is None or len(decoded) == 0:
                    return b'', False
                return decoded, True

            elif CommUtils.select_decode_type == "ECPT":
                decoded = DataDecode.ECPT(data, 0x60)
                if decoded is None or len(decoded) == 0:
                    return b'', False
                return decoded, True

            elif CommUtils.select_decode_type == "98设备":
                decoded = DataDecode.ECPT(data, 0x98)
                if decoded is None or len(decoded) == 0:
                    return b'', False
                return decoded, True

            else:
                # 标准版、五统一 都走这里
                return data, True

        except Exception as e:
            GuiUtils.custom_print_only(f"解码异常：{str(e)}", "red")
            return b'', False

    #将数据保存为mp3格式
    def save_to_mp3(self,save_path,need_audio_info,protocol_type):
        save_result=True
        try:
            with open(save_path, 'wb') as f:
                # 逐帧写入MP3数据
                for infos in need_audio_info:
                    if protocol_type=="nas":
                        need_data= binascii.unhexlify(infos[16:])
                    else:
                        need_data = binascii.unhexlify(infos[24:])
                    # 将数据解密
                    need_data, result = self.decode_data(need_data)
                    if not result:
                        GuiUtils.custom_print_only("保存出错了，请检查解码方式是否正确！", "red")
                        save_result = False
                        break
                    f.write(need_data)
        except Exception as e:
            GuiUtils.custom_print_only(f"保存出错了，{e}", "red")
            save_result = False
        return save_result