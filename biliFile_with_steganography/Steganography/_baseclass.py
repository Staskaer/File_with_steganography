import numpy as np
from typing import List


class Steganography_base:
    '''
    图像隐写算法接口类

    如果是编码信息，则通过__init__创建类
    如果是解码信息，通过decode_header创建类
    '''

    def __init__(self,
                 args: str):
        raise NotImplementedError()

    def encode_header(self,
                      image: List[np.array],
                      *,
                      loop: bool = False) -> List[np.array]:
        '''
        从图像中解码数据头部信息

        Args:
            image (List[np.array]): 图像
            loop (bool, optional): 是否使用整数倍的载波图像

        Returns:
            List[np.array]: 嵌入后的图像
        '''
        raise NotImplementedError()

    @classmethod
    def decode_header(cls,
                      frame: np.array):
        '''
        此函数应返回一个编码时用的类
        '''
        raise NotImplementedError()

    def encode(self,
               image: List[np.array],
               data: bytes,
               *,
               loop: bool = False) -> List[np.array]:
        '''
        将数据data嵌入到图像image中并返回
        此函数会根据初始化时的设置，来对数据编码成若干个图像
        直到编码完成

        会循环使用image中的图像

        Args:
            List[np.array]: 载波图像列表
            data (np.array): 数据
            loop (bool, optional): 是否使用整数倍的载波图像


        Returns:
            List[np.array]: 嵌入后图像列表
        '''
        raise NotImplementedError()

    def decode(self,
               image: np.array,
               **kwargs) -> bytes:
        '''
        从图像中解码数据

        Args:
            image (np.array): 图像

        Returns:
            bytes: 解码后的数据
        '''
        raise NotImplementedError()
