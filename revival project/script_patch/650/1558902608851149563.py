# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Utils/NileMD5Util.py
from __future__ import absolute_import
from .NileFileSystem import NileFileSystem
import hashlib

class NileMD5Util(object):
    FILE_CHUNK_SIZE = 8192

    def __init__(self):
        pass

    @staticmethod
    def GetByteArrayHexValue(data):
        md5 = hashlib.md5(data)
        return md5.hexdigest()

    @staticmethod
    def GetFileHexValue(filePath, size=8192):
        data = NileFileSystem.ReadBytes(filePath, size)
        return NileMD5Util.GetByteArrayHexValue(data)

    @staticmethod
    def GetFileListHexValue(filePathList):
        md5 = hashlib.md5()
        for path in filePathList:
            chunk = NileFileSystem.ReadBytes(path, NileMD5Util.FILE_CHUNK_SIZE)
            if chunk:
                md5.update(chunk)

        return md5.hexdigest()