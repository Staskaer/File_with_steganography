from typing import Tuple, Any
import numpy as np
import threading
import cv2


class FrameReadIterator:
    def __init__(self, file: str) -> None:
        self.file = file
        self.cap = cv2.VideoCapture(file)

    def reload(self):
        self.cap = cv2.VideoCapture(self.file)

    @property
    def fps(self) -> float:
        return self.cap.get(cv2.CAP_PROP_FPS)

    @property
    def frame_size(self) -> Tuple[int, int]:
        return (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    def __iter__(self):
        return self

    def __next__(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return frame
        else:
            raise StopIteration

    def __del__(self):
        self.cap.release()


class FrameWriteIterator:
    def __init__(self,
                 file: str,
                 fourcc: Any,
                 fps: float,
                 size: Tuple[int, int]) -> None:
        self.writer = cv2.VideoWriter(file, fourcc, fps, size, False)
        self.queue = []
        self.writing = []
        self.cond = threading.Condition()
        self._stop = False
        threading.Thread(target=self.do_flush).start()

    def flush(self):
        with self.cond:
            self.writing = self.queue
            self.queue = []
            self.cond.notify_all()

    def do_flush(self):
        while (not self._stop):
            with self.cond:
                # 测试条件
                while len(self.writing) == 0:
                    self.cond.wait()
                for img in self.writing:
                    self.writer.write(img)
                self.writing = []

    def write(self, frame: np.array):
        self.queue.append(frame)
        if len(self.queue) > 600:
            self.flush()

    def stop(self):
        self.flush()
        self._stop = True

    def __del__(self):
        self.writer.release()
