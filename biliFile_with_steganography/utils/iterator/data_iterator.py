from ..fileio import FileIO
from typing import Tuple, Any
import numpy as np
import threading
import cv2


class DataReadIterator:
    def __init__(self, file: str) -> None:
        self.f = open(file, 'rb')
        self.file = file

    def reload(self):
        self.f.close()
        self.f = open(self.file, 'rb')

    def __del__(self):
        self.f.close()

    def __iter__(self):
        return self

    def __next__(self):
        data = self.f.read(512)
        if data:
            return data
        else:
            raise StopIteration


class DataWriteIterator:
    def __init__(self, file: str) -> None:
        self.f = open(file, 'wb')
        self.file = file
        self._cond = threading.Condition()
        self.writing = []
        self.queue = b""
        self.close = False
        threading.Thread(target=self.do_flush).start()

    def flush(self):
        with self._cond:
            self.writing.append(self.queue)
            self.queue = b""
            self._cond.notify_all()

    def do_flush(self):
        while not self.close:
            with self._cond:
                while len(self.writing) == 0:
                    self._cond.wait()
                for data in self.writing:
                    self.f.write(data)
                self.writing = []

    def write(self, data: bytes):
        self.queue += data
        if len(self.queue) > 512:
            self.flush()

    def stop(self):
        self.flush()
        self.close = True
        self.f.flush()

    def __del__(self):
        self.f.close()
