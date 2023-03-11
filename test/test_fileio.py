from File_with_steganography.utils.fileio import FileIO


def test():
    try:
        for i in FileIO.read("test_data/test_fileio", 10):
            ...
        return 0
    except:
        raise


if __name__ == "__main__":
    # Test fileio
    print(test())
