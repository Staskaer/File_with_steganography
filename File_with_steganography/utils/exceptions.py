class EncoderException(Exception):
    def __init__(self, message):
        self.message = message


class DecoderException(Exception):
    def __init__(self, message):
        self.message = message


class NoEnoughFrameException(EncoderException):
    def __init__(self, message):
        self.message = message


class HeaderException(EncoderException):
    def __init__(self, message):
        self.message = message
