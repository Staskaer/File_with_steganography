from biliFile_with_steganography.utils.iterator import DataReadIterator, DataWriteIterator
# 计算两个文件md5值是否相同

import hashlib

f = DataReadIterator("test_data/test1.txt")
w = DataWriteIterator("test_data/test2.txt")
for data in f:
    w.write(data)
w.stop()

# 计算两个文件md5值是否相同


def md5sum(filename):
    with open(filename, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        return hash


print(md5sum("test_data/test1.txt"))
print(md5sum("test_data/test2.txt"))
print(md5sum("test_data/test1.txt") == md5sum("test_data/test2.txt"))
