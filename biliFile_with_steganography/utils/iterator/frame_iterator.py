from ..fileio import FileIO
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
                 fps: float,
                 size: Tuple[int, int],
                 fourcc: Any = cv2.VideoWriter_fourcc(*'mp4v')) -> None:
        self.writer = cv2.VideoWriter(file, fourcc, fps, size)

    def write(self, frame: np.array):
        self.writer.write(frame)
