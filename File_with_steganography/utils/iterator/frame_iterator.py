from typing import Tuple, Any
import numpy as np
import threading
import cv2


class FrameReadIterator:
    '''
    视频读取迭代器
    '''

    def __init__(self, file: str) -> None:
        '''
        构造函数，初始化视频读取迭代器
        '''
        self.file = file
        self.cap = cv2.VideoCapture(file)

    def reload(self):
        '''
        重新加载视频
        '''
        self.cap = cv2.VideoCapture(self.file)

    @property
    def fps(self) -> float:
        '''
        视频帧率
        '''
        return self.cap.get(cv2.CAP_PROP_FPS)

    @property
    def frame_size(self) -> Tuple[int, int]:
        '''
        帧尺寸
        '''
        return (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    def __iter__(self):
        '''
        迭代器协议相关
        '''
        return self

    def __next__(self):
        '''
        迭代器协议相关
        '''
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return frame
        else:
            raise StopIteration

    def __del__(self):
        '''
        析构函数，释放资源
        '''
        self.cap.release()


class FrameWriteIterator:
    '''
    视频写入迭代器，使用多线程写入
    具有600帧缓存区，写入为单通道
    '''

    def __init__(self,
                 file: str,
                 fourcc: Any,
                 fps: float,
                 size: Tuple[int, int]) -> None:
        '''
        构造函数

        Args:
            file (str): 写入文件
            fourcc (Any): 编码格式
            fps (float): 帧率
            size (Tuple[int, int]): 尺寸
        '''
        self.writer = cv2.VideoWriter(file, fourcc, fps, size, False)
        self.queue = []
        self.writing = []
        # 锁相关
        self.cond = threading.Condition()
        self._stop = False
        threading.Thread(target=self.do_flush).start()

    def flush(self):
        '''
        刷新缓冲区
        '''
        with self.cond:
            self.writing = self.queue
            self.queue = []
            self.cond.notify_all()

    def do_flush(self):
        '''
        另一线程函数，不断写入
        '''
        while (not self._stop):
            with self.cond:
                # 测试条件
                while len(self.writing) == 0:
                    self.cond.wait()
                for img in self.writing:
                    self.writer.write(img)
                self.writing = []

    def write(self, frame: np.array):
        '''
        写接口
        '''
        self.queue.append(frame)
        if len(self.queue) > 600:
            self.flush()

    def stop(self):
        '''
        写入完成后需要调用此函数，
        此函数被调用后，迭代器将不再接受写入
        '''
        self.flush()
        self._stop = True

    def __del__(self):
        '''
        析构函数
        '''
        self.writer.release()
