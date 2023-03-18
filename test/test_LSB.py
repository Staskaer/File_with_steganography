from File_with_steganography.Steganography.LSB import LSB
from File_with_steganography.utils.iterator import *

import numpy as np

from math import sqrt


def test_encode_decode():

    kernel = 4
    data = b"abcdefgh"

    size = int(kernel * sqrt(len(data)*8))
    dsize = (size, size)

    l = LSB(kernel)

    pic = np.zeros(dsize, dtype=np.uint8)

    l.frame_size = pic.shape

    enpic = l._do_encode(pic, data)
    dedata = l._do_decode(enpic)

    assert dedata == data


def test_LSB_write():
    kernel = 4
    datariterator = DataReadIterator("testlsb.txt")
    frameriterator = FrameReadIterator("video.mp4")
    fourcc = cv2.VideoWriter_fourcc('I', '4', '2', '0')
    framewiterator = FrameWriteIterator("video_out.avi",
                                        fourcc,
                                        frameriterator.fps,
                                        frameriterator.frame_size
                                        )
    lsb = LSB(kernel)
    lsb.encode(frameriterator, datariterator, framewiterator)
    framewiterator.stop()
    del framewiterator
    print("frame done")


def test_LSB_read():
    kernel = 4
    datawiterator = DataWriteIterator("testlsb_out.txt")
    lsb = LSB(kernel)
    frameriterator = FrameReadIterator("video_out.avi")
    lsb.decode(frameriterator, datawiterator)
    datawiterator.stop()
    del datawiterator
    print("data done")


test_encode_decode()
test_LSB_write()
test_LSB_read()
