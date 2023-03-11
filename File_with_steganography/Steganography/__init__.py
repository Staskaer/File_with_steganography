import numpy as np
from .LSB import LSB
from typing import Tuple

HEADER_MAGIC = b'BILIBILI'
CONTENT_MAGIC = b'Staskaer'
EMPTY_MAGIC = b'12345678'


def trans2str_from_obj(module: str,
                       class_: str,
                       args: str) -> str:
    '''
    将类的模块、类名、参数转换为字符串

    Returns:
        str: _description_
    '''
    return f'{module}|{class_}|{args}'


def decode_from_str(args) -> Tuple[str, str, str]:
    '''
    将字符串转换为模块、类名、参数

    Returns:
        Tuple[str,str,str]: _description_
    '''
    return tuple(args.split('|'))


def generate_cls(package: str,
                 class_name: str,
                 args: str):
    try:
        __import__(package, fromlist=True)
    except:
        # TODO 导入报错，可能不存在
        raise
    # TODO 目前所有的cls必须自己解析参数
    return globals()[class_name](args)
