from typing import Tuple


def decode_16(data: bytes) -> Tuple[bytes, bytes]:
    '''
    将前缀码解码成数据，前缀码长度为16位
    '''
    # 读取前缀码
    pre = data[:2]
    l = int.from_bytes(pre, 'little')
    # 读取数据
    ret = data[2:2 + l]
    # 把data读取的数据截取掉
    data = data[2 + l:]
    return ret, data


def docede_32(data: bytes) -> Tuple[bytes, bytes]:
    '''
    将前缀码解码成数据，前缀码长度为32位
    '''
    # 读取前缀码
    pre = data[:4]
    l = int.from_bytes(pre, 'little')
    # 读取数据
    ret = data[4:4 + l]
    # 把data读取的数据截取掉
    data = data[4 + l:]
    return ret, data
