import numpy as np
from typing import List
from File_with_steganography.utils.iterator import *


class Steganography_base:
    '''
    图像隐写算法接口类
    '''

    def __init__(self,
                 args: str):
        raise NotImplementedError()

    def encode(self,
               image: FrameReadIterator,
               data: DataReadIterator,
               dst: FrameWriteIterator,
               *,
               loop: bool = True) -> bool:
        '''
        不断读取图像帧、不断读取数据，然后调制，将调制后的帧写入目标位置

        Args:
            image (FrameReadIterator): 读取图像的迭代器
            data (DataReadIterator): 读取数据的迭代器
            dst (FrameWriteIterator): 写入图像的迭代器
            loop (bool, optional): 是否重复使用图像. Defaults to True.

        Returns:
            bool: 是否写入完成
        '''
        raise NotImplementedError()

    def decode(self,
               image: FrameReadIterator,
               dst: DataWriteIterator,
               **kwargs) -> bool:
        '''
        从图像中解码数据

        Args:
            image (FrameReadIterator): 读取图像的迭代器
            dst (DataWriteIterator): 写入数据的迭代器

        Returns:
            bool: 是否完成
        '''
        raise NotImplementedError()
