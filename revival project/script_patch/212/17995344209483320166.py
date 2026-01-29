# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileLocalDirectoryHelper.py
from __future__ import absolute_import
from __future__ import print_function
import time
from ..Utils.NileFileSystem import NileFileSystem
from .NileSettings import NileSettings
from ..Utils.NileJsonUtil import NileJsonUtil
from ..Utils.NileSystemInfo import NileSystemInfo
from patch import patch_path

class NileLocalDirectoryHelper(object):
    EXPIRE_TIME = 1296000
    ROOT = ''

    @staticmethod
    def Initialize():
        NileLocalDirectoryHelper.ROOT = NileSystemInfo.GetLocalStorageRoot()
        NileLocalDirectoryHelper._CreateIfNotExist()
        NileLocalDirectoryHelper.DeleteFiles(NileLocalDirectoryHelper.GetLogDirectoryPath())
        NileLocalDirectoryHelper.DeleteFiles(NileLocalDirectoryHelper.GetAssetDirectoryPath())
        NileLocalDirectoryHelper.DeletePatchFiles(NileLocalDirectoryHelper.GetMetaDirectoryPath())
        if NileSettings.GetIsUnderConstruction():
            NileLocalDirectoryHelper.DeletePatchFiles(NileLocalDirectoryHelper.GetMetaDirectoryPath(), False)

    @staticmethod
    def _CreateIfNotExist():
        try:
            NileFileSystem.CreateDirectory(NileLocalDirectoryHelper.ROOT)
            NileFileSystem.CreateDirectory(NileLocalDirectoryHelper.GetCookieDirectoryPath())
            NileFileSystem.CreateDirectory(NileLocalDirectoryHelper.GetLogDirectoryPath())
            NileFileSystem.CreateDirectory(NileLocalDirectoryHelper.GetMetaDirectoryPath())
            NileFileSystem.CreateDirectory(NileLocalDirectoryHelper.GetSettingsDirectoryPath())
            NileFileSystem.CreateDirectory(NileLocalDirectoryHelper.GetAssetDirectoryPath())
            NileFileSystem.CreateDirectory(NileLocalDirectoryHelper.GetTempDirectoryPath())
        except OSError as osError:
            print(str(osError))

    @staticmethod
    def GetCookieDirectoryPath():
        return NileFileSystem.JoinPath(NileLocalDirectoryHelper.ROOT, 'cookies')

    @staticmethod
    def GetLogDirectoryPath():
        return NileFileSystem.JoinPath(NileLocalDirectoryHelper.ROOT, 'logs')

    @staticmethod
    def GetSettingsDirectoryPath():
        return NileFileSystem.JoinPath(NileLocalDirectoryHelper.ROOT, 'settings')

    @staticmethod
    def GetSettingsPath():
        return NileFileSystem.JoinPath(NileLocalDirectoryHelper.GetSettingsDirectoryPath(), 'settings.txt')

    @staticmethod
    def GetMetaDirectoryPath():
        return NileFileSystem.JoinPath(NileLocalDirectoryHelper.ROOT, 'metas')

    @staticmethod
    def GetMetaFilePath(name):
        return NileFileSystem.JoinPath(NileLocalDirectoryHelper.GetMetaDirectoryPath(), name)

    @staticmethod
    def GetAssetDirectoryPath():
        return NileFileSystem.JoinPath(NileLocalDirectoryHelper.ROOT, 'assets')

    @staticmethod
    def GetAssetFilePath(name):
        return NileFileSystem.JoinPath(NileLocalDirectoryHelper.GetAssetDirectoryPath(), name)

    @staticmethod
    def GetTempDirectoryPath():
        return NileFileSystem.JoinPath(NileLocalDirectoryHelper.ROOT, 'temp')

    @staticmethod
    def GetTempFilePath(name):
        return NileFileSystem.JoinPath(NileLocalDirectoryHelper.GetTempDirectoryPath(), name)

    @staticmethod
    def GetResDirectoryPath():
        return NileSystemInfo.EnsureUTF8Str(patch_path.get_res_patch_path())

    @staticmethod
    def GetScriptDirectoryPath():
        return NileSystemInfo.EnsureUTF8Str(patch_path.get_script_patch_path())

    @staticmethod
    def GetNileNpkRootPath--- This code section failed: ---

 112       0  LOAD_GLOBAL           0  'NileSystemInfo'
           3  LOAD_ATTR             1  'EnsureUTF8Str'
           6  LOAD_GLOBAL           2  'patch_path'
           9  LOAD_ATTR             3  'get_neox_dir'
          12  CALL_FUNCTION_0       0 
          15  CALL_FUNCTION_1       1 
          18  STORE_FAST            0  'neoxDir'

 113      21  LOAD_GLOBAL           4  'NileFileSystem'
          24  LOAD_ATTR             5  'JoinPath'
          27  LOAD_ATTR             1  'EnsureUTF8Str'
          30  CALL_FUNCTION_2       2 
          33  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 30

    @staticmethod
    def GetPatchScriptListPath(name):
        fileName = NileLocalDirectoryHelper.GetPatchScriptListName(name)
        return NileFileSystem.JoinPath(NileLocalDirectoryHelper.GetTempDirectoryPath(), fileName)

    @staticmethod
    def GetPatchScriptListName(name):
        return 'nile_%s_script_list.txt' % name

    @staticmethod
    def DeleteFiles(dirPath, isExpired=True):
        try:
            pathList = NileFileSystem.GetFiles(dirPath)
            for p in pathList:
                filePath = NileFileSystem.JoinPath(dirPath, p)
                if NileFileSystem.IsFile(filePath):
                    modifyTime = NileFileSystem.GetLastModifyTime(filePath)
                    if not isExpired or time.time() - modifyTime > NileLocalDirectoryHelper.EXPIRE_TIME:
                        NileFileSystem.Delete(filePath)

        except OSError as osError:
            print(str(osError))

    @staticmethod
    def DeletePatchFiles(dirPath, isExpired=True):
        try:
            pathList = NileFileSystem.GetFiles(dirPath)
            for p in pathList:
                filePath = NileFileSystem.JoinPath(dirPath, p)
                if NileFileSystem.IsFile(filePath):
                    modifyTime = NileFileSystem.GetLastModifyTime(filePath)
                    if not isExpired or time.time() - modifyTime > NileLocalDirectoryHelper.EXPIRE_TIME * 2:
                        jsonStr = NileFileSystem.ReadText(filePath)
                        meta = NileJsonUtil.Deserialize(jsonStr)
                        from .NilePatchExtractor import NilePatchExtractor
                        NilePatchExtractor.DeleteUnmatchedFileList(meta.get('pathList', list()))
                        NileFileSystem.Delete(filePath)

        except OSError as osError:
            print(str(osError))

    @staticmethod
    def ClearDirectory(dirPath):
        try:
            pathList = NileFileSystem.GetFiles(dirPath)
            for p in pathList:
                subPath = NileFileSystem.JoinPath(dirPath, p)
                if NileFileSystem.IsFile(subPath):
                    NileFileSystem.Delete(subPath)
                else:
                    NileLocalDirectoryHelper.ClearDirectory(subPath)
                    NileFileSystem.DeleteDir(subPath)

        except OSError as osError:
            print(str(osError))

    @staticmethod
    def GetActivityScriptRoot():
        return NileFileSystem.JoinPath(NileLocalDirectoryHelper.GetScriptDirectoryPath(), 'nileActivity')

    @staticmethod
    def GetNileScriptRoot():
        return NileLocalDirectoryHelper.GetScriptDirectoryPath()

    @staticmethod
    def Clear():
        NileLocalDirectoryHelper.DeleteFiles(NileLocalDirectoryHelper.GetLogDirectoryPath(), False)
        NileLocalDirectoryHelper.DeleteFiles(NileLocalDirectoryHelper.GetCookieDirectoryPath(), False)
        NileLocalDirectoryHelper.DeleteFiles(NileLocalDirectoryHelper.GetAssetDirectoryPath(), False)
        NileLocalDirectoryHelper.DeleteFiles(NileLocalDirectoryHelper.GetMetaDirectoryPath(), False)
        NileLocalDirectoryHelper.DeleteFiles(NileLocalDirectoryHelper.GetSettingsDirectoryPath(), False)
        NileLocalDirectoryHelper.DeleteFiles(NileLocalDirectoryHelper.GetTempDirectoryPath(), False)