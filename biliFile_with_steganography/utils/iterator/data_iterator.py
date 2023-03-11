import threading


class DataReadIterator:
    '''
    二进制数据读取迭代器，分块读取
    '''

    def __init__(self, file: str) -> None:
        self.f = open(file, 'rb')
        self.file = file

    def reload(self):
        '''
        重置迭代器
        '''
        self.f.close()
        self.f = open(self.file, 'rb')

    def __del__(self):
        self.f.close()

    def __iter__(self):
        return self

    def __next__(self):
        '''
        每次读取512字节
        '''
        data = self.f.read(512)
        if data:
            return data
        else:
            raise StopIteration


class DataWriteIterator:
    '''
    数据写入迭代器，多线程写入，512字节缓冲
    '''

    def __init__(self, file: str) -> None:
        self.f = open(file, 'wb')
        self.file = file

        # 下面是锁结构和写入队列
        # 当前数据是queue，写入就是加入writing，
        # 写入线程将writing写入文件，写入完成后清空writing
        self._cond = threading.Condition()
        self.writing = []
        self.queue = b""
        self.close = False
        threading.Thread(target=self.do_flush).start()

    def flush(self):
        '''
        将当前数据加入到写入队列
        '''
        with self._cond:
            self.writing.append(self.queue)
            self.queue = b""
            self._cond.notify_all()

    def do_flush(self):
        '''
        写入线程，将写入队列写入文件,通过条件变量绑定
        '''
        while not self.close:
            with self._cond:
                while len(self.writing) == 0:
                    self._cond.wait()
                for data in self.writing:
                    self.f.write(data)
                self.writing = []

    def write(self, data: bytes):
        '''
        接口，写入
        '''
        self.queue += data
        if len(self.queue) > 512:
            self.flush()

    def stop(self):
        '''
        写入完成，需要将最后的写入队列写入文件
        '''
        self.flush()
        self.close = True
        self.f.flush()

    def __del__(self):
        self.flush()
        self.f.close()
