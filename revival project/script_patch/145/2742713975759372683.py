# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NilePatchModuleHelper.py
from __future__ import absolute_import
import sys
from .NileSettings import NileSettings
from ..Utils.NileFileSystem import NileFileSystem
from .NileLocalDirectoryHelper import NileLocalDirectoryHelper

class NilePatchModuleHelper(object):
    _moduleList = list()

    @staticmethod
    def RecordModules(scriptList):
        for content in scriptList:
            content = NileFileSystem.NormPath(content)
            content = content.replace('.py', '')
            content = content.replace(NileFileSystem.GetPathSep(), '.')
            content = content.strip()
            if content:
                NilePatchModuleHelper._moduleList.append(content)

    @staticmethod
    def UnloadModules():
        if NileSettings.GetIsUnderConstruction():
            NilePatchModuleHelper.UnloadLocalModules()
        else:
            NilePatchModuleHelper.UnloadPatchModules()

    @staticmethod
    def UnloadPatchModules():
        for m in NilePatchModuleHelper._moduleList:
            if m in sys.modules:
                del sys.modules[m]

        NilePatchModuleHelper._moduleList = list()

    @staticmethod
    def UnloadLocalModules():
        moduleList = NilePatchModuleHelper.GetLocalActivityModuleList()
        for m in moduleList:
            if m in sys.modules:
                del sys.modules[m]

    @staticmethod
    def GetLocalActivityModuleList():
        activityRoot = NileLocalDirectoryHelper.GetActivityScriptRoot()
        nileRootToken = NileLocalDirectoryHelper.GetNileScriptRoot()
        fileList = list()
        NilePatchModuleHelper.GetFiles(activityRoot, fileList)
        moduleList = list()
        for p in fileList:
            p = NileFileSystem.ReplacePath(p, nileRootToken)
            p = NileFileSystem.NormPath(p)
            p = p.replace(NileFileSystem.GetPathSep(), '.')
            p = p.replace('.py', '')
            moduleList.append(p)

        return moduleList

    @staticmethod
    def GetFiles(path, result):
        l = NileFileSystem.GetFiles(path)
        for f in l:
            f = NileFileSystem.JoinPath(path, f)
            if '.py' in f and '.pyo' not in f:
                result.append(f)
            elif NileFileSystem.IsDir(f):
                NilePatchModuleHelper.GetFiles(f, result)

    @staticmethod
    def IsModuleImported(fullName):
        return fullName in sys.modules

    @staticmethod
    def GetModule(fullName):
        return sys.modules[fullName]