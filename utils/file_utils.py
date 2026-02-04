# -*- coding: utf-8 -*-
# time: 2022/10/28 10:57
# file: file_utils.py
# author: 胡能武
import json
import os
import subprocess


class FileUtils:
    def __init__(self):
        pass

    # 创建文件夹
    def create_folder(self,file_path):
        # 文件夹不存在则创建
        result = os.path.exists(file_path)
        if not result:
            os.mkdir(file_path)

    # 删除文件夹中的所有文件和文件夹
    def del_dir(self,dir):
        if not os.path.exists(dir):
            return False
        if os.path.isfile(dir):
            os.remove(dir)
            return
        for i in os.listdir(dir):
            t = os.path.join(dir, i)
            if os.path.isdir(t):
                self.del_dir(t)  # 重新调用次方法
            else:
                os.unlink(t)
        os.removedirs(dir)  # 递归删除目录下面的空文件夹

    # 仅删除文件夹中的文件
    def del_file_by_dir(self,dir):
        if not os.path.exists(dir):
            return False
        for i in os.listdir(dir):
            file = os.path.join(dir, i)
            os.remove(file)

    # 删除文件夹再创建文件夹
    def clear_folder(self,dir):
        # 删除文件夹及文件夹里面的内容
        self.del_dir(dir)
        # 再创建外层文件夹
        self.create_folder(dir)

    #遍历获取目录中指定文件
    def get_all_video_file(self,file_dir):
        temp_file_list=[]
        #判断给的路径是否为目录
        if not os.path.isdir(file_dir):
            #路径不是目录，直接当文件处理
            temp_file_list.append(file_dir)
            return temp_file_list

        for i in os.listdir(file_dir):
            temp_file_list.append(os.path.join(file_dir, i))
        return temp_file_list

    # 获得当前文件夹路径
    @staticmethod
    def get_local_path():
        current_directory = os.path.dirname(os.path.abspath(__file__))
        return current_directory.replace('\\utils',"")

    @staticmethod
    #追加写入文件
    def save_txt(txt_path,info):
        # 再创建文件,写入日志
        with open(txt_path, "a+", encoding='utf-8') as f:
            f.write(info)

    @staticmethod
    #批量写入文件
    def batch_save_txt(file_path,infos):
        # 覆盖写入文件
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(infos)

    @staticmethod
    #判断文件是否存在
    def file_is_exit(file_path):
        return os.path.exists(file_path)

    @staticmethod
    #打开一个文件夹
    def open_directory(file_path):
        try:
            os.startfile(file_path)
        except:
            subprocess.Popen('xdg-open',file_path)

    @staticmethod
    #将文件转成二进制文件
    def read_file_by_bytes(file_path):
        with open(file_path, mode="rb") as data:
            content = data.read()
            return content

    @staticmethod
    #获得路径的文件名，带后缀
    def get_fileName_by_filePath(file_path):
        return os.path.basename(file_path)

    @staticmethod
    #获得路径的文件名，不带后缀
    def get_only_file_name(file_path):
        return FileUtils.get_fileName_by_filePath(file_path).split(".")[0]

    @staticmethod
    #将json文件中的内容读取出来,保存为一个字典
    def read_json_file_to_dict(file_path):
        with open(file_path, mode="r",encoding='utf-8') as f:
            temp_data=f.read()
            if temp_data.startswith(u'\ufeff'):
                temp_data = temp_data.encode('utf8')[3:].decode('utf8')
            json_data=json.loads(temp_data)
        return json_data