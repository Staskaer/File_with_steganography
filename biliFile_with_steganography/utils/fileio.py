class FileIO:
    @staticmethod
    def read(file: str, block_size: int):
        with open(file, "rb") as f:
            block = f.read(block_size)
            if block:
                yield block

    @staticmethod
    def write(file: str, data: bytes):
        with open(file, "wb") as f:
            f.write(data)
