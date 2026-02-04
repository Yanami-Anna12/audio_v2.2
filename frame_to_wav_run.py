# -*- coding: utf-8 -*-
# time: 2023/2/27 8:54
# file: frame_to_wav_run.py
# describe: 文件功能描述
# author: 胡能武

import encodings.idna
from business.init_folder import InitFolder
from gui.real_gui import RealGui
from utils.yaml_utils import m_yml

if __name__ == "__main__":
    # 先将yml文件中的数据解析出来
    m_yml.get_real_yaml()

    # 初始化目录
    InitFolder.init_folder()

    #GUI
    rg=RealGui()
    rg.start_draw_gui()
