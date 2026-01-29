# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Utils/NilePatchPacker.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import zip
import os
from io import BytesIO
from .NileFileSystem import NileFileSystem

class NilePatchPacker(object):
    FILE_INFO_LEN = 8
    FORMAT_NPK = 0
    FORMAT_DISCRETE = 1

    @staticmethod
    def Pack(filePathList, pathRootToRemove, outputPath, contentFormat=1):
        try:
            truncatePathList = NilePatchPacker._GetTruncatePathList(filePathList, pathRootToRemove)
            fileDataList = NilePatchPacker._GetFileDataList(filePathList)
            fileInfoLen = NilePatchPacker._GetFileInfoStrLength(truncatePathList)
            offset = NilePatchPacker.FILE_INFO_LEN + fileInfoLen
            fileInfoStr = NilePatchPacker._GenerateFileInfoStr(truncatePathList, fileDataList, offset)
            stream = BytesIO()
            stream.write('%08d' % fileInfoLen)
            stream.write(fileInfoStr)
            for fileData in fileDataList:
                stream.write(fileData)

            stream.write('%08d' % contentFormat)
            NilePatchPacker._WriteStream(outputPath, stream)
            return True
        except Exception as e:
            print('\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3\xe8\xb5\x84\xe6\xba\x90\xe6\x89\x93\xe5\x8c\x85\xe5\xa4\xb1\xe8\xb4\xa5, Message: %s' % str(e))

        return False

    @staticmethod
    def _GetTruncatePathList(filePathList, pathRoot):
        return [ os.path.relpath(path, pathRoot) for path in filePathList ]

    @staticmethod
    def _GetFileInfoStrLength(truncatePathList):
        result = ''
        for path in truncatePathList:
            result += '%s,%s,%s;' % (path, '00000000', '00000000')

        result = result[0:-1]
        return NilePatchPacker._GetStrLength(result)

    @staticmethod
    def _GetStrLength(content):
        temp = BytesIO()
        temp.write(content)
        return temp.tell()

    @staticmethod
    def _GenerateFileInfoStr(truncatePathList, fileDataList, offset):
        result = ''
        current = offset
        for path, data in zip(truncatePathList, fileDataList):
            path = NileFileSystem.NormPath(path)
            start = '%08d' % current
            end = '%08d' % (current + len(data))
            current = int(end)
            result += '%s,%s,%s;' % (path, start, end)

        result = result[0:-1]
        return result

    @staticmethod
    def _GetFileDataList(filePathList):
        fileDataList = list()
        for path in filePathList:
            if not NileFileSystem.Exists(path):
                print('\xe8\xb5\x84\xe6\xba\x90\xe4\xb8\x8d\xe5\xad\x98\xe5\x9c\xa8\xef\xbc\x8c Path: %s' % path)
                continue
            data = NileFileSystem.ReadBytes(path)
            fileDataList.append(data)

        return fileDataList

    @staticmethod
    def _WriteStream(outputPath, data):
        data.seek(0)
        NileFileSystem.WriteBytes(outputPath, data.read())

    @staticmethod
    def ExtractFileInfo(fileData):
        result = dict()
        stream = BytesIO(fileData)
        fileInfoStrLen = int(stream.read(NilePatchPacker.FILE_INFO_LEN))
        import six
        fileInfoStr = six.ensure_str(stream.read(fileInfoStrLen))
        subFileInfoStr = fileInfoStr.split(';')
        for rawInfo in subFileInfoStr:
            info = rawInfo.split(',')
            key = NileFileSystem.NormPath(info[0])
            result[key] = (int(info[1]), int(info[2]))

        return result

    @staticmethod
    def Unpack(inputPath, outputPathRoot):
        try:
            packageData = NileFileSystem.ReadBytes(inputPath)
            fileInfo = NilePatchPacker.ExtractFileInfo(packageData)
            stream = BytesIO(packageData)
            for key in fileInfo:
                start, end = fileInfo[key]
                stream.seek(start)
                fileData = stream.read(end - start)
                filePath = NileFileSystem.JoinPath(outputPathRoot, key)
                NileFileSystem.WriteBytes(filePath, fileData)

        except Exception as e:
            print('\xe5\xb0\xbc\xe7\xbd\x97\xe6\xb2\xb3\xe8\xb5\x84\xe6\xba\x90\xe8\xa7\xa3\xe5\x8c\x85\xe5\x87\xba\xe9\x94\x99, Message: %s' % str(e))

    @staticmethod
    def UnpackBytes(fileData):
        result = dict()
        fileInfoDict = NilePatchPacker.ExtractFileInfo(fileData)
        lastFilePosition = 0
        stream = BytesIO(fileData)
        for key in fileInfoDict:
            start, end = fileInfoDict[key]
            stream.seek(start)
            data = stream.read(end - start)
            result[key] = data
            if lastFilePosition > end:
                lastFilePosition = lastFilePosition if 1 else end

        if len(stream.getvalue()) == lastFilePosition:
            return (result, NilePatchPacker.FORMAT_DISCRETE)
        stream.seek(lastFilePosition)
        contentFormat = int(stream.read(NilePatchPacker.FILE_INFO_LEN))
        return (
         result, contentFormat)