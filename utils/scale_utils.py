# -*- coding: utf-8 -*-
# time: 2022/11/9 13:43
# file: scale_utils.py
# describe: 进制转换辅助类
# author: 胡能武
import binascii


class ScaleUtils:
    #将10进制转成16进制，不足2位自动补0
    @staticmethod
    def dec_2_hex(value,need_length=2):
        hex_value=hex(int(value)).upper()[2:]
        return ScaleUtils.zero_fill(hex_value,need_length)

    #16进制字符串高低位转换
    @staticmethod
    def hex_low_2_high(data):
        list_1 = []  # 建立空列表
        for i in range(0, len(data), 2):
            list_1.append(data[i:i + 2])
        list_1.reverse()
        list_1_str= ''.join(list_1)
        return list_1_str

    #获得设备的ID
    @staticmethod
    def get_device_id(data):
        if len(data)==0 or data=="无":
            return "未知"
        data=ScaleUtils.hex_low_2_high(data)
        id=int(data,16)+1
        return id


    #为字符串数据补0
    @staticmethod
    def zero_fill(data,need_length=2):
        zero_str=""
        for i in range(need_length-len(data)):
            zero_str=zero_str+"0"
        if len(data)<need_length:
            return zero_str+str(data)
        else:
            return str(data)

    #传入一个10进制数，得到一个指定位数的16进制数
    @staticmethod
    def get_hex_from_dec(dec_data,is_reverse=False,need_length=2):
        hex_str=ScaleUtils.dec_2_hex(dec_data,need_length)
        if is_reverse:
            hex_str=ScaleUtils.hex_low_2_high(hex_str)
        return hex_str

    # 16进制字符串转16进制\x格式
    @staticmethod
    def str_to_data16(data):
        data2 = binascii.a2b_hex(data)
        return data2


    #16进制字符串转10进制数
    @staticmethod
    def hex_str2_dec(hex_str,is_reverse=False):
        if hex_str:
            #is_reverse为高低为转换参数
            if is_reverse: #16进制字符串要高低位转换
                return int(ScaleUtils.hex_low_2_high(hex_str), 16)
            else: #不需要高低位转换
                return int(hex_str, 16)

    # 16进制字符串转成16进制
    @staticmethod
    def str2hex(s):
        # s: '0x4B'
        s = s[2:]  # 去掉’0x‘
        odata = 0
        su = s.upper()
        for c in su:
            tmp = ord(c)  # ACSII码
            if tmp <= ord('9'):
                odata = odata << 4  # 高位的数值乘以2^4
                odata += tmp - ord('0')
            elif ord('A') <= tmp <= ord('F'):
                odata = odata << 4
                odata += tmp - ord('A') + 10
        return odata

    #二进制bytes数据转成16进制字符串
    @staticmethod
    def bin2hex(bin_data):
        return binascii.b2a_hex(bin_data).decode('utf-8').upper()


    @staticmethod
    # 计算0x45、0x4E的数据和
    def sum_data_by_2_bytes(data,length,is_reverse=False):
        '''
        data:16进制字符串
        length:一次取几个字符来拆分
        '''
        split_data_list=[]
        for i in range(0,len(data),length):
            if is_reverse: #调换高低位的顺序
                split_data_list.append(ScaleUtils.hex_low_2_high(data[i:i + length]))
            else:
                split_data_list.append(data[i:i + length])
        check_sum_str = ScaleUtils.dec_2_hex(sum([int(i, 16) for i in split_data_list]),need_length=6)
        #累加结果调换顺序后，取前4位
        return ScaleUtils.hex_low_2_high(check_sum_str)[:4]

    @staticmethod
    #16进制转2进制，返回二进制字符串
    def hex_to_bin_str(hex_str,need_length=8):
        if hex_str:
            return bin(int(hex_str,16)).replace("0b", "").zfill(need_length)

    @staticmethod
    #将二进制转十进制
    def bin_to_dec(bin_str):
        return int(bin_str,2)

    @staticmethod
    #将16进制字符串转普通字符串（如68656c6c6f转成hello）
    def hex_str_to_comm_str(hex_str):
        if hex_str:
            temp_hex_str=hex_str.rstrip("0")
            if len(temp_hex_str)%2!=0:
                temp_hex_str=temp_hex_str+"0"
            output = binascii.unhexlify(temp_hex_str).decode('gbk',errors='ignore').strip()
            return output

    @staticmethod
    #将两个字符串拼接起来,适用params取多个值的场景
    def splicing_str(data,index:list):
        if data:
            need_info=""
            for i in index:
                need_info+=data[i]
            return need_info
