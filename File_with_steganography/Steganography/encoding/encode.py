import hashlib


def encode_16(data: bytes) -> bytes:
    '''
    将数据编码成前缀码，前缀码长度为16位
    '''
    # 生成前缀码
    l = len(data)
    pre = l.to_bytes(2, 'little')
    return pre + data


def encode_32(data: bytes) -> bytes:
    '''
    将数据编码成前缀码，前缀码长度为32位
    '''
    # 生成前缀码
    l = len(data)
    pre = l.to_bytes(4, 'little')
    return pre + data
