from .LSB import LSB

HEADER_MAGIC = b'BILIBILI'
CONTENT_MAGIC = b'Staskaer'


def generate_cls(package: str,
                 class_name: str,
                 args: str):
    try:
        __import__(package, fromlist=True)
    except:
        # TODO 导入报错，可能不存在
        ...
    # TODO 目前所有的cls必须自己解析参数
    return globals()[class_name](args)
