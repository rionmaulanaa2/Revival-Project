# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Utils/NileFileSystem.py
from __future__ import absolute_import
import os
import six

class NileFileSystem(object):

    def __init__(self):
        pass

    @staticmethod
    def IndicateUTF8(inputPath):
        from .NileSystemInfo import NileSystemInfo
        if NileSystemInfo.GetOsName() == 'windows':
            try:
                return six.ensure_text(inputPath)
            except UnicodeDecodeError:
                return inputPath

        return inputPath

    @staticmethod
    def CreateDirectory(dirPath):
        dirPath = NileFileSystem.IndicateUTF8(dirPath)
        if not dirPath:
            return
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

    @staticmethod
    def GetDirectoryName(path):
        return os.path.dirname(path)

    @staticmethod
    def GetFileName(path):
        path = NileFileSystem.IndicateUTF8(path)
        return os.path.basename(path)

    @staticmethod
    def GetFilePostfix(path):
        path = NileFileSystem.IndicateUTF8(path)
        fileName = os.path.basename(path)
        if '.' in fileName:
            lastDotIndex = fileName.rindex('.')
            return fileName[lastDotIndex:]
        return ''

    @staticmethod
    def GetFileNameWithoutPostfix(path):
        return NileFileSystem.GetFileName(path).replace(NileFileSystem.GetFilePostfix(path), '')

    @staticmethod
    def Exists(path):
        path = NileFileSystem.IndicateUTF8(path)
        return os.path.exists(path)

    @staticmethod
    def GetLastModifyTime(filePath):
        filePath = NileFileSystem.IndicateUTF8(filePath)
        return os.path.getmtime(filePath)

    @staticmethod
    def DeleteDir(path):
        path = NileFileSystem.IndicateUTF8(path)
        os.rmdir(path)

    @staticmethod
    def Delete(path):
        path = NileFileSystem.IndicateUTF8(path)
        os.remove(path)

    @staticmethod
    def GetFiles(dirPath):
        dirPath = NileFileSystem.IndicateUTF8(dirPath)
        return os.listdir(dirPath)

    @staticmethod
    def GetSize(filePath):
        filePath = NileFileSystem.IndicateUTF8(filePath)
        return os.path.getsize(filePath)

    @staticmethod
    def WriteBytes--- This code section failed: ---

 109       0  LOAD_GLOBAL           0  'NileFileSystem'
           3  LOAD_ATTR             1  'IndicateUTF8'
           6  LOAD_FAST             0  'filePath'
           9  CALL_FUNCTION_1       1 
          12  STORE_FAST            0  'filePath'

 110      15  LOAD_GLOBAL           0  'NileFileSystem'
          18  LOAD_ATTR             2  'CreateDirectory'
          21  LOAD_GLOBAL           3  'os'
          24  LOAD_ATTR             4  'path'
          27  LOAD_ATTR             5  'dirname'
          30  LOAD_FAST             0  'filePath'
          33  CALL_FUNCTION_1       1 
          36  CALL_FUNCTION_1       1 
          39  POP_TOP          

 111      40  LOAD_GLOBAL           6  'open'
          43  LOAD_GLOBAL           1  'IndicateUTF8'
          46  LOAD_FAST             2  'buffering'
          49  CALL_FUNCTION_3       3 
          52  SETUP_WITH           20  'to 75'
          55  STORE_FAST            3  'f'

 112      58  LOAD_FAST             3  'f'
          61  LOAD_ATTR             7  'write'
          64  LOAD_FAST             1  'data'
          67  CALL_FUNCTION_1       1 
          70  POP_TOP          
          71  POP_BLOCK        
          72  LOAD_CONST            0  ''
        75_0  COME_FROM_WITH           '52'
          75  WITH_CLEANUP     
          76  END_FINALLY      

Parse error at or near `CALL_FUNCTION_3' instruction at offset 49

    @staticmethod
    def AppendBytes--- This code section failed: ---

 116       0  LOAD_GLOBAL           0  'NileFileSystem'
           3  LOAD_ATTR             1  'IndicateUTF8'
           6  LOAD_FAST             0  'filePath'
           9  CALL_FUNCTION_1       1 
          12  STORE_FAST            0  'filePath'

 117      15  LOAD_GLOBAL           2  'open'
          18  LOAD_GLOBAL           1  'IndicateUTF8'
          21  LOAD_FAST             2  'buffering'
          24  CALL_FUNCTION_3       3 
          27  SETUP_WITH           20  'to 50'
          30  STORE_FAST            3  'f'

 118      33  LOAD_FAST             3  'f'
          36  LOAD_ATTR             3  'write'
          39  LOAD_FAST             1  'data'
          42  CALL_FUNCTION_1       1 
          45  POP_TOP          
          46  POP_BLOCK        
          47  LOAD_CONST            0  ''
        50_0  COME_FROM_WITH           '27'
          50  WITH_CLEANUP     
          51  END_FINALLY      

Parse error at or near `CALL_FUNCTION_3' instruction at offset 24

    @staticmethod
    def ReadBytes--- This code section failed: ---

 125       0  LOAD_GLOBAL           0  'NileFileSystem'
           3  LOAD_ATTR             1  'IndicateUTF8'
           6  LOAD_FAST             0  'filePath'
           9  CALL_FUNCTION_1       1 
          12  STORE_FAST            0  'filePath'

 126      15  LOAD_CONST            0  ''
          18  STORE_FAST            3  'data'

 127      21  LOAD_GLOBAL           3  'os'
          24  LOAD_ATTR             4  'path'
          27  LOAD_ATTR             5  'exists'
          30  LOAD_FAST             0  'filePath'
          33  CALL_FUNCTION_1       1 
          36  POP_JUMP_IF_TRUE     43  'to 43'

 128      39  LOAD_FAST             3  'data'
          42  RETURN_END_IF    
        43_0  COME_FROM                '36'

 129      43  LOAD_GLOBAL           6  'open'
          46  LOAD_GLOBAL           1  'IndicateUTF8'
          49  LOAD_FAST             2  'buffering'
          52  CALL_FUNCTION_3       3 
          55  SETUP_WITH           22  'to 80'
          58  STORE_FAST            4  'f'

 130      61  LOAD_FAST             4  'f'
          64  LOAD_ATTR             7  'read'
          67  LOAD_FAST             1  'size'
          70  CALL_FUNCTION_1       1 
          73  STORE_FAST            3  'data'
          76  POP_BLOCK        
          77  LOAD_CONST            0  ''
        80_0  COME_FROM_WITH           '55'
          80  WITH_CLEANUP     
          81  END_FINALLY      

 131      82  LOAD_FAST             3  'data'
          85  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 52

    @staticmethod
    def WriteText--- This code section failed: ---

 135       0  LOAD_GLOBAL           0  'NileFileSystem'
           3  LOAD_ATTR             1  'IndicateUTF8'
           6  LOAD_FAST             0  'filePath'
           9  CALL_FUNCTION_1       1 
          12  STORE_FAST            0  'filePath'

 136      15  LOAD_GLOBAL           0  'NileFileSystem'
          18  LOAD_ATTR             2  'CreateDirectory'
          21  LOAD_GLOBAL           3  'os'
          24  LOAD_ATTR             4  'path'
          27  LOAD_ATTR             5  'dirname'
          30  LOAD_FAST             0  'filePath'
          33  CALL_FUNCTION_1       1 
          36  CALL_FUNCTION_1       1 
          39  POP_TOP          

 137      40  LOAD_GLOBAL           6  'open'
          43  LOAD_GLOBAL           1  'IndicateUTF8'
          46  LOAD_FAST             2  'buffering'
          49  CALL_FUNCTION_3       3 
          52  SETUP_WITH           20  'to 75'
          55  STORE_FAST            3  'f'

 138      58  LOAD_FAST             3  'f'
          61  LOAD_ATTR             7  'write'
          64  LOAD_FAST             1  'text'
          67  CALL_FUNCTION_1       1 
          70  POP_TOP          
          71  POP_BLOCK        
          72  LOAD_CONST            0  ''
        75_0  COME_FROM_WITH           '52'
          75  WITH_CLEANUP     
          76  END_FINALLY      

Parse error at or near `CALL_FUNCTION_3' instruction at offset 49

    @staticmethod
    def AppendText--- This code section failed: ---

 142       0  LOAD_GLOBAL           0  'NileFileSystem'
           3  LOAD_ATTR             1  'IndicateUTF8'
           6  LOAD_FAST             0  'filePath'
           9  CALL_FUNCTION_1       1 
          12  STORE_FAST            0  'filePath'

 143      15  LOAD_GLOBAL           2  'open'
          18  LOAD_GLOBAL           1  'IndicateUTF8'
          21  LOAD_FAST             2  'buffering'
          24  CALL_FUNCTION_3       3 
          27  SETUP_WITH           20  'to 50'
          30  STORE_FAST            3  'f'

 144      33  LOAD_FAST             3  'f'
          36  LOAD_ATTR             3  'write'
          39  LOAD_FAST             1  'text'
          42  CALL_FUNCTION_1       1 
          45  POP_TOP          
          46  POP_BLOCK        
          47  LOAD_CONST            0  ''
        50_0  COME_FROM_WITH           '27'
          50  WITH_CLEANUP     
          51  END_FINALLY      

Parse error at or near `CALL_FUNCTION_3' instruction at offset 24

    @staticmethod
    def ReadText--- This code section failed: ---

 148       0  LOAD_GLOBAL           0  'NileFileSystem'
           3  LOAD_ATTR             1  'IndicateUTF8'
           6  LOAD_FAST             0  'filePath'
           9  CALL_FUNCTION_1       1 
          12  STORE_FAST            0  'filePath'

 149      15  LOAD_CONST            0  ''
          18  STORE_FAST            2  'data'

 150      21  LOAD_GLOBAL           3  'os'
          24  LOAD_ATTR             4  'path'
          27  LOAD_ATTR             5  'exists'
          30  LOAD_FAST             0  'filePath'
          33  CALL_FUNCTION_1       1 
          36  POP_JUMP_IF_TRUE     43  'to 43'

 151      39  LOAD_FAST             2  'data'
          42  RETURN_END_IF    
        43_0  COME_FROM                '36'

 152      43  LOAD_GLOBAL           6  'open'
          46  LOAD_GLOBAL           1  'IndicateUTF8'
          49  LOAD_FAST             1  'buffering'
          52  CALL_FUNCTION_3       3 
          55  SETUP_WITH           19  'to 77'
          58  STORE_FAST            3  'f'

 153      61  LOAD_FAST             3  'f'
          64  LOAD_ATTR             7  'read'
          67  CALL_FUNCTION_0       0 
          70  STORE_FAST            2  'data'
          73  POP_BLOCK        
          74  LOAD_CONST            0  ''
        77_0  COME_FROM_WITH           '55'
          77  WITH_CLEANUP     
          78  END_FINALLY      

 154      79  LOAD_FAST             2  'data'
          82  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 52

    @staticmethod
    def IsFile(path):
        path = NileFileSystem.IndicateUTF8(path)
        return os.path.isfile(path)

    @staticmethod
    def IsDir(path):
        path = NileFileSystem.IndicateUTF8(path)
        return os.path.isdir(path)

    @staticmethod
    def JoinPath(left, right):
        return os.path.join(left, right)

    @staticmethod
    def ReplacePath(path, token):
        return os.path.relpath(path, token)

    @staticmethod
    def GetPathSep():
        return '/'

    @staticmethod
    def NormPath(path):
        return path.replace('\\', '/')