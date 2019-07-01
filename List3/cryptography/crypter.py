import jks

import Exception

from Crypto.Cipher import AES


class ModeNotSupportedException(Exception):
    pass


class Encoder:

    SUPPORTED_MODES = ["CBC"]

    def __init__(self, mode, key, iv):
        if mode not in self.SUPPORTED_MODES:
            raise Exception()
        self.mode = mode
        self.key = key
        self.iv = iv


