# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Storyline/StorylineSystem.py
import os
import json
from .Storyline import Storyline
from . import NodeMetaManager, NodeManager

def CreateStoryline(context):
    return Storyline(context)


def GetNodeEditorMeta(nodeTypeName):
    nodeMeta = NodeMetaManager.GetNodeMeta(nodeTypeName)
    if not nodeMeta:
        print "[STORYLINE ERROR]: Can't find node meta:%s" % nodeTypeName
        return None
    else:
        nodeCls = NodeManager.GetNodeClass(nodeTypeName)
        if nodeCls:
            return nodeMeta.GetNodeEditorMeta(nodeCls)
        return nodeMeta.GetSelfEditorMeta()
        return None


class RepositoryMgr(object):
    _Workspace = None
    _Repository = {}

    @classmethod
    def SetWorkspace(cls, workspace):
        if not os.path.exists(workspace):
            print 'Warning: storyline workspace not exists: %s' % workspace
        cls._Workspace = workspace
        cls.Update()

    @classmethod
    def GetWorkspace(cls):
        return cls._Workspace

    @classmethod
    def Update(cls):
        repoFile = os.path.join(cls._Workspace, 'repository.json')
        if os.path.isfile(repoFile):
            with open(repoFile) as f:
                cls._Repository = json.loads(f.read())
        else:
            cls._Repository = {}
        macroPath = os.path.join(cls._Workspace, 'Macro')
        if os.path.isdir(macroPath):
            for root, dirs, files in os.walk(macroPath):
                if '.svn' in root or '.git' in root:
                    continue
                for f in files:
                    path = os.path.join(root, f)
                    with open(path) as fp:
                        try:
                            data = json.load(fp)
                        except:
                            continue

                        if isinstance(data, dict) and data.get('Type') == 'Macro' and data.get('Version') >= 2.0:
                            name = os.path.relpath(path, macroPath).replace('\\', '/')
                            cls._Repository.setdefault('Macro', {})[data['Key']] = name

    @classmethod
    def GetMacroName(cls, macroID):
        return cls._Repository.get('Macro', {}).get(macroID, None)

    @classmethod
    def GetMacroData(cls, macroID):
        macroName = cls.GetMacroName(macroID)
        if not macroName:
            return
        else:
            filename = os.path.join(cls._Workspace, 'Macro', macroName)
            with open(filename, 'rb') as f:
                data = json.load(f)
            return data


_gRepositoryMgr = RepositoryMgr()

def GetRepositoryMgr():
    global _gRepositoryMgr
    return _gRepositoryMgr


def SetRepositoryMgr(mgr):
    global _gRepositoryMgr
    _gRepositoryMgr = mgr