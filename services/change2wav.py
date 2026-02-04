# -*- coding: utf-8 -*-
# time: 2023/11/24 15:38
# file: change2wav.py
# describe: 文件功能描述
# author: 胡能武
import subprocess
import wave
import array

# 使用Tshark命令行工具解析PCAP文件中的RTP流
tshark_cmd = 'tshark -r input.pcap -Y "rtp" -T fields -e rtp.payload'
output = subprocess.check_output(tshark_cmd, shell=True).decode('utf-8')

# 将16位G.711 PCMU数据转换为PCM格式的WAV文件
pcm_data = array.array('h', bytes.fromhex(output))
wav_file = wave.open('output.wav', 'w')
wav_file.setnchannels(1)  # 单声道
wav_file.setsampwidth(2)  # 16位
wav_file.setframerate(8000)  # 8kHz采样率
wav_file.writeframes(pcm_data.tobytes())
wav_file.close()
