from File_with_steganography.utils.iterator import FrameReadIterator, FrameWriteIterator
import cv2
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

f = FrameReadIterator("test/test_data/test1.mp4")
w = FrameWriteIterator("test/test_data/test2.mp4",
                       fourcc,
                       f.fps,
                       f.frame_size)
for img in f:
    w.write(img)
w.stop()
