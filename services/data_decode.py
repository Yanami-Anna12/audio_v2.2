# -*- coding: utf-8 -*-
# time: 2023/12/1 10:33
# file: data_decode.py
# describe: 文件功能描述
# author: 胡能武
import struct


class  DataDecode:
    constACMAdptive=[230, 230, 230, 230, 307, 409, 512, 614, 768, 614, 512, 409, 307, 230, 230, 230]

    # # @staticmethod
    # def ADPCMDecoder(Source, nSrcSize, Dest=None):
    #     if Dest is None:
    #         Dest = [0] * 220
    #     Delta = DataDecode.byte_to_int(DataDecode.get_bytes_value(Source[1]), DataDecode.get_bytes_value(Source[2]), 0, 0)
    #     Samp1 = DataDecode.byte_to_int(DataDecode.get_bytes_value(Source[3]), DataDecode.get_bytes_value(Source[4]), 0, 0)
    #     Samp2 = DataDecode.byte_to_int(DataDecode.get_bytes_value(Source[5]), DataDecode.get_bytes_value(Source[6]), 0, 0)
    #     #java中的数据是有符号的，所在在python3中要转换一下
    #     Delta= DataDecode.get_short_value(Delta)
    #     Samp1 = DataDecode.get_short_value(Samp1)
    #     Samp2 = DataDecode.get_short_value(Samp2)
    #     Dest[0] = Samp2
    #     Dest[1] = Samp1
    #
    #     nSrcSize -= 7
    #     for i in range(nSrcSize):
    #         Code = (Source[i + 7] >> 4) & 0x0F
    #         Sample = Samp1 + Delta * (Code - 0x10) if Code > 7 else Samp1 + Delta * Code
    #         Sample = min(32767, max(-32768, Sample))
    #         Dest[i * 2 + 2] = Sample
    #         Delta = Delta * DataDecode.constACMAdptive[Code] // 256
    #         Delta = max(16, Delta)
    #         Samp1 = Sample
    #
    #         Code = Source[i + 7] & 0x0F
    #         Sample = Samp1 + Delta * (Code - 0x10) if Code > 7 else Samp1 + Delta * Code
    #         Sample = min(32767, max(-32768, Sample))
    #         Dest[i * 2 + 3] = Sample
    #         Delta = Delta * DataDecode.constACMAdptive[Code] // 256
    #         Delta = max(16, Delta)
    #         Samp1 = Sample
    #
    #     return DataDecode.convert_ints_to_bytes(Dest)

    @staticmethod
    def ADPCMDecoder(Source, nSrcSize, Dest=None):
        try:
            if Dest is None:
                Dest = [0] * 220
            Delta = DataDecode.byte_to_int(DataDecode.get_bytes_value(Source[1]), DataDecode.get_bytes_value(Source[2]),
                                           0, 0)
            Samp1 = DataDecode.byte_to_int(DataDecode.get_bytes_value(Source[3]), DataDecode.get_bytes_value(Source[4]),
                                           0, 0)
            Samp2 = DataDecode.byte_to_int(DataDecode.get_bytes_value(Source[5]), DataDecode.get_bytes_value(Source[6]),
                                           0, 0)

            Delta = DataDecode.get_short_value(Delta)
            Samp1 = DataDecode.get_short_value(Samp1)
            Samp2 = DataDecode.get_short_value(Samp2)
            Dest[0] = Samp2
            Dest[1] = Samp1

            nSrcSize -= 7
            if nSrcSize < 0:
                return b''

            for i in range(nSrcSize):
                Code = (Source[i + 7] >> 4) & 0x0F
                Sample = Samp1 + Delta * (Code - 0x10) if Code > 7 else Samp1 + Delta * Code
                Sample = min(32767, max(-32768, Sample))
                Dest[i * 2 + 2] = Sample
                Delta = Delta * DataDecode.constACMAdptive[Code] // 256
                Delta = max(16, Delta)
                Samp1 = Sample

                Code = Source[i + 7] & 0x0F
                Sample = Samp1 + Delta * (Code - 0x10) if Code > 7 else Samp1 + Delta * Code
                Sample = min(32767, max(-32768, Sample))
                Dest[i * 2 + 3] = Sample
                Delta = Delta * DataDecode.constACMAdptive[Code] // 256
                Delta = max(16, Delta)
                Samp1 = Sample

            return DataDecode.convert_ints_to_bytes(Dest)
        except:
            # 解码异常直接返回空字节
            return b''

    @staticmethod
    def ECPT(src_bytes, wDeviceType):
        ECPT_DATA_SIZE = 220
        pWords = DataDecode.convert_bytes_to_ints(src_bytes)
        if len(pWords) < ECPT_DATA_SIZE:
        # # 修复点1：长度不足时返回空字节，而不是None
            return b''
        # Step 1: Decrypt the last word using the device type as the key
        pWords[ECPT_DATA_SIZE - 1] ^= (wDeviceType << 8) | (~wDeviceType & 0xFF)
        # pWords[ECPT_DATA_SIZE - 1] ^= (wDeviceType << 8) & 0xFF00
        # pWords[ECPT_DATA_SIZE - 1] ^= (~wDeviceType) & 0x00FF

        # Step 2: Use the last word as a key for encryption
        wEncryptKey = (pWords[ECPT_DATA_SIZE - 1] << 5) | (pWords[ECPT_DATA_SIZE - 1] >> 11)

        # Step 3: XOR each word with the previous word and the encryption key
        for j in range(1, ECPT_DATA_SIZE - 1):
            pWords[j] ^= pWords[j - 1] ^ wEncryptKey

        return  DataDecode.convert_ints_to_bytes(pWords)

    @staticmethod
    def convert_bytes_to_ints(bytes):
        ints = []
        for i in range(0, len(bytes), 2):
            # # 修复点2：处理字节长度为奇数的情况
            if i + 1 >= len(bytes):
                ints.append( DataDecode.byte_to_int(bytes[i], 0, 0, 0))
            else:
                ints.append( DataDecode.byte_to_int(bytes[i], bytes[i + 1], 0, 0))
        return ints

    @staticmethod
    def convert_ints_to_bytes(ints):
        byte_list = []
        for i in range(len(ints)):
            byte_list.append(ints[i] & 0xFF)
            byte_list.append((ints[i] >> 8) & 0xFF)
        return bytes(byte_list)

    @staticmethod
    def byte_to_int(b1, b2, b3, b4):
        return (b1 & 0xFF) | (b2 & 0xFF) << 8 | (b3 & 0xFF) << 16 | (b4 & 0xFF) << 24

    @staticmethod
    #java中的算法是有符号的，所以在python3中，也要转变成有符号的数据，和java保持一致
    def get_bytes_value(value):
        if value > 127:
            value = -(256 - value)
        return value

    @staticmethod
    # java中的算法是有符号的，所以在python3中，也要转变成有符号的数据，和java保持一致
    def get_short_value(value):
        if value > 32767:
            value = -(65536 - value)
        return value

    @staticmethod
    def get_int_value(value):
        if value > 2147483647:
            value = -(4294967296 - value)
        return value
