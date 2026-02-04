# -*- coding: utf-8 -*-
# time: 2023/12/1 11:37
# file: g711_to_pcm.py
# describe: 文件功能描述
# author: 胡能武

class G711_To_PCM:
    # 定义一个静态方法，将G.711 a-law编码的数据转换为PCM数据
    @staticmethod
    def convertG711aToPcm(g711Buffer, length, pcmBuffer):
        # 如果pcmBuffer为空，则创建一个新的字节数组，长度为length*2
        if pcmBuffer is None:
            pcmBuffer = bytearray(length * 2)
            # 遍历g711Buffer中的每个元素
        for i in range(length):
            # 获取当前元素的值
            alaw = g711Buffer[i]
            # 对当前元素的值进行位反转（ucval）
            alaw ^= 0x55  # ucval

            # 获取当前元素的符号位
            sign = alaw & 0x80
            # 获取当前元素的指数值（nseg）
            exponent = (alaw & 0x70) >> 4  # nseg
            # 获取当前元素的值（ntemp）
            value = (alaw & 0x0F) << 4  # ntemp
            # 根据指数值进行不同的偏移（如果指数为0或1，则进行不同的偏移）
            if exponent == 0:
                value += 8
            elif exponent == 1:
                value += 0x108
            else:
                value += 0x108
                value <<= exponent - 1
                # 根据符号位对值进行正负转换，然后将其存储到pcmBuffer中
            value = value if sign == 0 else -value
            pcmBuffer[i * 2] = value & 0xFF
            pcmBuffer[i * 2 + 1] = (value >> 8) & 0xFF
            # 返回转换后的PCM数据缓冲区
        return pcmBuffer

    # 定义一个静态方法，将G.711 u-law编码的数据转换为PCM数据
    @staticmethod
    def convertG711uToPcm(g711Buffer, length, pcmBuffer=None):
        # 如果pcmBuffer为空，则创建一个新的字节数组，长度为length*2
        if pcmBuffer is None:
            pcmBuffer = bytearray(length * 2)
            # 遍历g711Buffer中的每个元素
        for i in range(length):
            # 获取当前元素的值并进行位反转（ucval）
            alaw = g711Buffer[i]
            alaw = ~alaw & 0xFF # ucval

            # 获取当前元素的符号位
            sign = alaw & 0x80
            # 根据alaw的值计算当前元素的值（ntemp）并进行不同的偏移（根据指数值进行左移）
            value = ((alaw & 0xF) << 3) + 0x84  # ntemp
            value <<= (alaw & 0x0F) >> 0x70  # ntemp

            # 根据符号位对值进行正负转换，然后将其存储到pcmBuffer中
            value = 0x84 - value if sign == 0 else value - 0x84
            pcmBuffer[i * 2] = value & 0xFF
            pcmBuffer[i * 2 + 1] = (value >> 8) & 0xFF
            # 返回转换后的PCM数据缓冲区
        return pcmBuffer