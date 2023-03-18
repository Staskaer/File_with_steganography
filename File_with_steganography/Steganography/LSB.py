from scipy.signal import convolve2d
import cv2
import numpy as np
from ._baseclass import Steganography_base
from typing import List, Tuple
import hashlib
from File_with_steganography.utils.iterator import *
from File_with_steganography.utils.exceptions import *
from File_with_steganography.Steganography import (
    HEADER_MAGIC,
    CONTENT_MAGIC,
    EMPTY_MAGIC,
    trans2str_from_obj,
    generate_cls)
from File_with_steganography.utils.exceptions import *


def LSB(kernel: int = 2):
    '''
    创建LSB类
    '''
    return _LSB(f'kernel=int({kernel})')


class _LSB(Steganography_base):
    '''
    LSB类需要自己解析参数并动态创建

    参数：
    kernel: int = 2 # 用于嵌入的核大小，表示2x2的像素块作为一个二进制位
    '''

    def __init__(self, args: str) -> None:
        # 保证IDE工作
        self.kernel: int = None

        self.create = args
        args = [arg for arg in args.replace(" ", "").split(',')]
        # TODO 也许需要参数检查？
        for arg in args:
            setattr(self, arg.split('=')[0], eval(arg.split('=')[1]))

        assert self.kernel >= 2, 'kernel必须大于等于2'

    def _self2bytes(self) -> bytes:
        '''
        将自身信息编码成bytes
        '''
        result = trans2str_from_obj(
            self.__class__.__module__, self.__class__.__name__, self.create)
        return bytes(result, encoding='utf-8')

    def encode(self,
               image: FrameReadIterator,
               data: DataReadIterator,
               dst: FrameWriteIterator,
               *,
               loop: int = True) -> bool:
        self.frame_size = image.frame_size
        # 计算每帧能存放多少数据
        data_total_pre_frame = int(int(
            self.frame_size[0]/self.kernel)*int(self.frame_size[1]/self.kernel)/8)
        # print(data_total_pre_frame)
        # 计算每帧能存放多少荷载数据
        # 64位头部信息，32*2位置信息，32位长度前缀，256位哈希值
        data_payload_pre_frame = data_total_pre_frame - 8 - 4 * 2 - 4 - 32
        assert data_payload_pre_frame > 0, '载波太小，无法存放数据'

        # 获取总尺寸
        file_total_size = data.size
        for index, d in enumerate(data.read(data_payload_pre_frame)):
            if len(d) < data_payload_pre_frame:
                # 填充数据
                d = d + b'\x00' * (data_payload_pre_frame - len(d))
            # 每次拿出数据进行调制
            # 首先计算总页数和当前页数
            total_page = 1 + file_total_size // data_payload_pre_frame
            current_page = index + 1
            # 计算哈希值
            h = hashlib.md5()
            h.update(d)
            h = h.hexdigest().encode("utf-8")
            # 给出写入数据
            # 64位头部信息，32*2位置信息，32位长度前缀，数据，32位哈希值
            write_data = CONTENT_MAGIC + \
                current_page.to_bytes(4, 'little') +\
                total_page.to_bytes(4, 'little') +\
                data_payload_pre_frame.to_bytes(4, 'little') +\
                d +\
                h
            # 写入两帧
            for i in range(2):
                try:
                    frame = next(image)
                except:
                    if loop:
                        image.reload()
                        frame = next(image)
                    else:
                        raise NoEnoughFrameException('没有足够的帧来存放数据')
                frame = self._do_encode(frame, write_data)
                dst.write(frame)
            # for frame in image:
            #     frame1 = self._do_encode(frame, write_data)
            #     dst.write(frame1)
            #     frame2 = self._do_encode(frame, write_data)
            #     dst.write(frame2)
            # if loop:
            #     image.reload()
            # else:
            #     raise NoEnoughFrameException('没有足够的帧来存放数据')
        for frame in image:
            # 剩余部分直接写入即可
            dst.write(frame)
            # 如果是循环使用载波，写入当前循环次剩余的载波
            # 否则写入剩下的载波

    def _do_encode(self,
                   image: np.array,
                   data: bytes) -> np.array:
        '''
        用于对单帧进行编码的函数
        '''
        # 先截断
        image = image/10
        image = image.astype(np.uint8)
        image = image*10
        # 用于存放数据的矩阵
        dst_size = (self.frame_size[1]//self.kernel,
                    self.frame_size[0]//self.kernel)
        data_array = np.frombuffer(data, dtype=np.uint8)
        data_array = np.unpackbits(data_array).reshape(dst_size)
        data_array = np.repeat(data_array, self.kernel, axis=0)
        data_array = np.repeat(data_array, self.kernel, axis=1)

        # 整合矩阵
        data_array = np.pad(data_array,
                            ((0, image.shape[0]-dst_size[0]*self.kernel),
                             (0, image.shape[1]-dst_size[1]*self.kernel)),
                            'constant')
        result = image + data_array

        # data = self._do_decode(result)
        return result

    def decode(self,
               image: FrameReadIterator,
               dst: DataWriteIterator) -> bool:
        # parsed_positon记录了最后处理完成的页面位置
        parsed_positon = 0
        for img in image:
            data = self._do_decode(img)
            magic = data[:8]
            # Header部分应该已经被处理了，故此处直接跳过
            # 可能出现一种情况
            # 由于Header存在冗余，所以可能会把Header帧遗留到数据处理部分
            if magic == HEADER_MAGIC:
                continue
            if magic == EMPTY_MAGIC:
                continue
            # 如果否则说明损坏
            if magic != CONTENT_MAGIC:
                # print('可能损坏的数据帧')
                continue

            # 下面开始处理数据
            current_page = int.from_bytes(data[8:12], 'little')
            if current_page == parsed_positon:
                # 当前页面已经处理过，跳过
                continue
            total_page = int.from_bytes(data[12:16], 'little')
            data_length = int.from_bytes(data[16:20], 'little')
            hash_value = data[-4:].decode('utf-8')
            data = data[20:20+data_length]
            h = hashlib.md5()
            h.update(data)
            if hash_value == h.hexdigest():
                # 此时表明数据正确
                dst.write(data)
                parsed_positon += 1

            if current_page == total_page:
                # 此时表明数据已经处理完毕
                break

    def _do_decode(self, image: np.array) -> bytes:
        '''
        用于对单帧进行解码的函数
        '''
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = image % 10
        kernel = np.ones((self.kernel, self.kernel), dtype=np.uint8)
        result = convolve2d(image, kernel, mode='valid')
        result = result[::self.kernel, ::self.kernel]/self.kernel**2
        # 至此，截取出了数据块平均后的数据
        # 接下来需要将数据块平均后的数据转换为二进制数据
        result = result.reshape(-1).astype(np.uint8)
        result = np.packbits(result)
        return result.tobytes()
