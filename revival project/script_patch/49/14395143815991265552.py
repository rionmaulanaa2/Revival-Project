# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NilePatchExtractor.py
from __future__ import absolute_import
from six.moves import zip
from io import BytesIO
from .NileLocalDirectoryHelper import NileLocalDirectoryHelper
from .NileLogReporter import NileLogReporter
from .NileLogger import NileLogger
from .NilePatchModuleHelper import NilePatchModuleHelper
from .NileUtil import NileUtil
from ..Utils.NileFileSystem import NileFileSystem
from ..Utils.NileJsonUtil import NileJsonUtil
from ..Utils.NileMD5Util import NileMD5Util
from ..Utils.NilePatchPacker import NilePatchPacker
from ..Utils.NileSystemInfo import NileSystemInfo

class NilePatchExtractor(object):

    @staticmethod
    def IsValidPatchName(url):
        rawName = NileFileSystem.GetFileNameWithoutPostfix(url)
        tokenList = rawName.split('_')
        if len(tokenList) != 3:
            NileLogReporter.GetInstance().ReportError(NileLogReporter.ERROR_PATCH, '\xe8\xb5\x84\xe6\xba\x90\xe5\x91\xbd\xe5\x90\x8d\xe4\xb8\x8d\xe7\xac\xa6\xe5\x90\x88\xe8\xa7\x84\xe8\x8c\x83: %s' % rawName)
            return False
        from .NileService import NileService
        if tokenList[0] != NileService.GetInstance().GetUserData().platform:
            NileLogReporter.GetInstance().ReportError(NileLogReporter.ERROR_PATCH, '\xe8\xb5\x84\xe6\xba\x90\xe5\x91\xbd\xe5\x90\x8d\xe4\xb8\x8d\xe7\xac\xa6\xe5\x90\x88\xe8\xa7\x84\xe8\x8c\x83, \xe5\xb9\xb3\xe5\x8f\xb0\xe5\x89\x8d\xe7\xbc\x80\xe9\x94\x99\xe8\xaf\xaf: %s' % rawName)
            return False
        return True

    @staticmethod
    def GetNameTuple(url):
        rawName = NileFileSystem.GetFileNameWithoutPostfix(url)
        tokenList = rawName.split('_')
        return (
         tokenList[0], tokenList[1], tokenList[2])

    @staticmethod
    def IsPatchExists(url):
        platform, name, md5 = NilePatchExtractor.GetNameTuple(url)
        metaPath = NileLocalDirectoryHelper.GetMetaFilePath(name + '.txt')
        try:
            if not NileFileSystem.Exists(metaPath):
                NilePatchExtractor.FileDeletePreprocessing(name)
                return False
            metaMd5, metaPathList = NilePatchExtractor.ParseMeta(metaPath)
            if metaMd5 != md5 or NileMD5Util.GetFileListHexValue(metaPathList) != md5:
                NilePatchExtractor.FileDeletePreprocessing(name)
                NilePatchExtractor.DeleteUnmatchedFileList(metaPathList)
                return False
            return NilePatchExtractor.FileCheckPostprocessing(name)
        except BaseException as e:
            message = 'Patch: %s \xe6\xa0\xa1\xe9\xaa\x8c\xe6\x9c\xac\xe5\x9c\xb0\xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe7\xbb\x8f\xe5\xad\x98\xe5\x9c\xa8\xe6\x97\xb6\xe9\x94\x99\xe8\xaf\xaf: %s, trace: %s' % (url, str(e), NileUtil.GetTraceback())
            NileLogger.Error(message)

        return False

    @staticmethod
    def ParseMeta(metaPath):
        jsonStr = NileFileSystem.ReadText(metaPath)
        meta = NileJsonUtil.Deserialize(jsonStr)
        metaMd5 = meta.get('md5', '')
        metaPathList = meta.get('pathList', list())
        return (
         metaMd5, metaPathList)

    @staticmethod
    def DeleteUnmatchedFileList(fileList):
        for f in fileList:
            if NileFileSystem.Exists(f):
                NileFileSystem.Delete(f)

    @staticmethod
    def FileDeletePreprocessing(name):
        resNpkPath = NilePatchExtractor.GetResNpkPath(name)
        scriptNpkPath = NilePatchExtractor.GetScriptNpkPath(name)
        if NileFileSystem.Exists(resNpkPath):
            NilePatchExtractor.UnloadNpk(resNpkPath)
            NileFileSystem.Delete(resNpkPath)
        if NileFileSystem.Exists(scriptNpkPath):
            NilePatchExtractor.UnloadNpk(scriptNpkPath)
            NileFileSystem.Delete(scriptNpkPath)

    @staticmethod
    def FileCheckPostprocessing(name):
        NilePatchExtractor.UnloadNpk(NilePatchExtractor.GetScriptNpkPath(name))
        if NilePatchExtractor.LoadScriptNpk(NilePatchExtractor.GetScriptNpkPath(name)):
            NilePatchExtractor.ReadScriptListFile(name)
        else:
            return False
        NilePatchExtractor.UnloadNpk(NilePatchExtractor.GetResNpkPath(name))
        return NilePatchExtractor.LoadResNpk(NilePatchExtractor.GetResNpkPath(name))

    @staticmethod
    def Extract(url, fileData):
        try:
            platform, fileName, md5 = NilePatchExtractor.GetNameTuple(url)
            fileDataDict, contentFormat = NilePatchPacker.UnpackBytes(fileData)
            pathList, nameList = NilePatchExtractor._PlaceFileDataDict(fileDataDict, contentFormat)
            NilePatchExtractor._WriteMeta(pathList, nameList, fileName, md5)
            return ''
        except Exception as e:
            message = 'Patch\xe8\xa7\xa3\xe5\x8e\x8b,\xe7\x94\x9f\xe6\x88\x90Meta\xe6\x96\x87\xe4\xbb\xb6, \xe6\xb7\xbb\xe5\x8a\xa0\xe8\x84\x9a\xe6\x9c\xac\xe8\xbf\x87\xe7\xa8\x8b\xe5\x8f\x91\xe7\x94\x9f\xe9\x94\x99\xe8\xaf\xaf, url: %s message: %s, trace: %s' % (url, str(e), NileUtil.GetTraceback())
            NileLogger.Error(message)
            return message

    @staticmethod
    def _PlaceFileDataDict(fileDataDict, contentFormat):
        if contentFormat == NilePatchPacker.FORMAT_DISCRETE:
            return NilePatchExtractor._PlaceDiscrete(fileDataDict)
        else:
            return NilePatchExtractor._PlaceNpk(fileDataDict)

    @staticmethod
    def _PlaceNpk(fileDataDict):
        pathList = list()
        nameList = list()
        resDir = NileLocalDirectoryHelper.GetNileNpkRootPath()
        scriptDir = NileLocalDirectoryHelper.GetNileNpkRootPath()
        for name in fileDataDict:
            if name.startswith('compatible_') or name.startswith('res_'):
                filePath = NileFileSystem.JoinPath(resDir, name)
                NileFileSystem.WriteBytes(filePath, fileDataDict[name])
            elif name.startswith('script_'):
                filePath = NileFileSystem.JoinPath(scriptDir, name)
                NileFileSystem.WriteBytes(filePath, fileDataDict[name])
            else:
                filePath = NileFileSystem.JoinPath(NileLocalDirectoryHelper.GetTempDirectoryPath(), name)
                NileFileSystem.WriteBytes(filePath, fileDataDict[name])
            pathList.append(filePath)
            nameList.append(name)

        return (pathList, nameList)

    @staticmethod
    def _PlaceDiscrete(fileDataDict):
        pathList = list()
        nameList = list()
        resDir = NileLocalDirectoryHelper.GetResDirectoryPath()
        scriptDir = NileLocalDirectoryHelper.GetScriptDirectoryPath()
        for name in fileDataDict:
            if name.startswith('compatible_') or name.startswith('res_'):
                subPathList, subNameList = NilePatchExtractor._UnzipPatch(fileDataDict[name], resDir)
                pathList = pathList + subPathList
                nameList = nameList + subNameList
            elif name.startswith('script_'):
                subPathList, subNameList = NilePatchExtractor._UnzipPatch(fileDataDict[name], scriptDir)
                pathList = pathList + subPathList
                nameList = nameList + subNameList
            else:
                filePath = NileFileSystem.JoinPath(NileLocalDirectoryHelper.GetTempDirectoryPath(), name)
                NileFileSystem.WriteBytes(filePath, fileDataDict[name])
                pathList.append(filePath)
                nameList.append(name)

        return (
         pathList, nameList)

    @staticmethod
    def GetResNpkPath(name):
        resDir = NileLocalDirectoryHelper.GetNileNpkRootPath()
        npkName = 'compatible_%s.npk' % name
        return NileFileSystem.JoinPath(resDir, npkName)

    @staticmethod
    def GetScriptNpkPath(name):
        scriptDir = NileLocalDirectoryHelper.GetNileNpkRootPath()
        npkName = 'script_%s.npk' % name
        return NileFileSystem.JoinPath(scriptDir, npkName)

    @staticmethod
    def _UnzipPatch(fileData, targetDir):
        import zipfile
        pathList = list()
        nameList = list()
        with zipfile.ZipFile(BytesIO(fileData), mode='r') as zf:
            for name in zf.namelist():
                path = zf.extract(name, targetDir)
                pathList.append(path)
                nameList.append(name)

        return (
         pathList, nameList)

    @staticmethod
    def _WriteMeta(pathList, nameList, fileName, md5):
        metaPathList = [ x for y, x in sorted(zip(nameList, pathList)) ]
        meta = dict()
        meta['md5'] = md5
        meta['pathList'] = metaPathList
        metaJson = NileJsonUtil.Serialize(meta)
        metaPath = NileLocalDirectoryHelper.GetMetaFilePath(fileName + '.txt')
        NileFileSystem.WriteText(metaPath, metaJson)

    @staticmethod
    def ReadScriptListFile(fileName):
        filePath = NileLocalDirectoryHelper.GetPatchScriptListPath(fileName)
        scriptListTxt = NileFileSystem.ReadText(filePath)
        if not scriptListTxt:
            return list()
        scriptList = scriptListTxt.split(';')
        NilePatchModuleHelper.RecordModules(scriptList)

    @staticmethod
    def LoadResNpk--- This code section failed: ---

 211       0  LOAD_GLOBAL           0  'NileSystemInfo'
           3  LOAD_ATTR             1  'IsSupportNpk'
           6  CALL_FUNCTION_0       0 
           9  POP_JUMP_IF_TRUE     16  'to 16'

 212      12  LOAD_GLOBAL           2  'True'
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

 213      16  LOAD_GLOBAL           3  'NileFileSystem'
          19  LOAD_ATTR             4  'Exists'
          22  LOAD_FAST             0  'path'
          25  CALL_FUNCTION_1       1 
          28  POP_JUMP_IF_TRUE     35  'to 35'

 214      31  LOAD_GLOBAL           2  'True'
          34  RETURN_END_IF    
        35_0  COME_FROM                '28'

 215      35  LOAD_CONST            1  ''
          38  LOAD_CONST            0  ''
          41  IMPORT_NAME           5  'C_file'
          44  STORE_FAST            1  'C_file'

 217      47  LOAD_GLOBAL           3  'NileFileSystem'
          50  LOAD_ATTR             6  'GetFileNameWithoutPostfix'
          53  LOAD_FAST             0  'path'
          56  CALL_FUNCTION_1       1 
          59  STORE_FAST            2  'tag'

 218      62  LOAD_FAST             1  'C_file'
          65  LOAD_ATTR             7  'add_res_npk_loader'
          68  LOAD_ATTR             2  'True'
          71  SLICE+2          
          72  LOAD_CONST            1  ''
          75  LOAD_FAST             2  'tag'
          78  CALL_FUNCTION_3       3 
          81  STORE_FAST            3  'result'

 219      84  LOAD_FAST             3  'result'
          87  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `SLICE+2' instruction at offset 71

    @staticmethod
    def LoadScriptNpk--- This code section failed: ---

 223       0  LOAD_GLOBAL           0  'NileSystemInfo'
           3  LOAD_ATTR             1  'IsSupportNpk'
           6  CALL_FUNCTION_0       0 
           9  POP_JUMP_IF_TRUE     16  'to 16'

 224      12  LOAD_GLOBAL           2  'True'
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

 225      16  LOAD_GLOBAL           3  'NileFileSystem'
          19  LOAD_ATTR             4  'Exists'
          22  LOAD_FAST             0  'path'
          25  CALL_FUNCTION_1       1 
          28  POP_JUMP_IF_TRUE     35  'to 35'

 226      31  LOAD_GLOBAL           2  'True'
          34  RETURN_END_IF    
        35_0  COME_FROM                '28'

 227      35  LOAD_CONST            1  ''
          38  LOAD_CONST            0  ''
          41  IMPORT_NAME           5  'C_file'
          44  STORE_FAST            1  'C_file'

 229      47  LOAD_GLOBAL           3  'NileFileSystem'
          50  LOAD_ATTR             6  'GetFileNameWithoutPostfix'
          53  LOAD_FAST             0  'path'
          56  CALL_FUNCTION_1       1 
          59  STORE_FAST            2  'tag'

 230      62  LOAD_GLOBAL           7  'hasattr'
          65  LOAD_FAST             1  'C_file'
          68  LOAD_CONST            2  'add_script_npk_loader'
          71  CALL_FUNCTION_2       2 
          74  POP_JUMP_IF_FALSE    97  'to 97'

 231      77  LOAD_FAST             1  'C_file'
          80  LOAD_ATTR             8  'add_script_npk_loader'
          83  LOAD_ATTR             3  'NileFileSystem'
          86  SLICE+2          
          87  LOAD_CONST            1  ''
          90  LOAD_FAST             2  'tag'
          93  CALL_FUNCTION_3       3 
          96  RETURN_END_IF    
        97_0  COME_FROM                '74'

 232      97  LOAD_FAST             1  'C_file'
         100  LOAD_ATTR             9  'insert_script_npk_loader'
         103  LOAD_ATTR             3  'NileFileSystem'
         106  SLICE+2          
         107  LOAD_FAST             2  'tag'
         110  LOAD_CONST            1  ''
         113  LOAD_CONST            4  2
         116  CALL_FUNCTION_4       4 
         119  LOAD_CONST            1  ''
         122  COMPARE_OP            5  '>='
         125  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `SLICE+2' instruction at offset 86

    @staticmethod
    def UnloadNpk(path):
        if not NileSystemInfo.IsSupportNpk():
            return True
        if not NileFileSystem.Exists(path):
            return True
        import C_file
        tag = NileFileSystem.GetFileNameWithoutPostfix(path)
        result = C_file.del_fileloader_by_tag(tag)
        return result >= 0