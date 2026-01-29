# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/VenusPlugin/VenusPluginClient.py
from ..EditorPlugin import EditorPluginClient
from .VenusPluginServer import VenusPluginServer
UUID = '7260c21e-8e6e-11e7-b0eb-e8b1fc1a5d1e'

class VenusPluginClient(EditorPluginClient):
    SUNSHINE_UUID = UUID
    PLUGIN_NAME = 'Venus'
    OneArgMap = {'Trigger': lambda x, y: x.SetTrigger(y),
       'Speed': lambda x, y: x.SetSpeed(y),
       'RestTrigger': lambda x, y: x.ResetTrigger(y)
       }
    TwoArgMap = {'Int': lambda x, y, z: x.SetInt(y, z),
       'Float': lambda x, y, z: x.SetFloat(y, z),
       'Bool': lambda x, y, z: x.SetBool(y, z)
       }

    def __init__(self, *args):
        super(VenusPluginClient, self).__init__(*args)

    def GetAvailableEntityIDTypeDict(self):
        raise NotImplementedError

    def SetEditEntity(self, uid):
        raise NotImplementedError

    def GetAnimatorNameByEntityUUID(self, uuid):
        raise NotImplementedError

    def GetEditAnimator(self):
        raise NotImplementedError

    def GetEditModel(self):
        raise NotImplementedError

    def PreviewModel(self, model_info):
        raise NotImplementedError

    def SceneLoaded(self, val):
        self.GetServer().SceneLoadedCallback(val)

    def GetClipNamesByEntityUUID(self, uid):
        raise NotImplementedError

    def GetAnimatorNodeInfoByUuidParms(self, UUID_params):
        animator = self.GetEditAnimator()
        ret = {'nodes': {},'param': {}}
        childStates = {}
        nodeActives = {}
        nodesUids = {}
        UUIDs, paramInfos = UUID_params
        for name, typ in paramInfos:
            val = ''
            if typ == 'Int':
                val = animator.GetInt(name)
            elif typ == 'Float':
                val = animator.GetFloat(name)
            elif typ == 'Bool':
                val = animator.GetBool(name)
            elif typ == 'Trigger':
                val = animator.GetTrigger(name)
            ret['param'][name] = val

        for uid in UUIDs:
            try:
                node = animator.FindById(uid)
                nodesUids[uid] = node
            except:
                print (
                 'FindByID Error, NodeID:', uid)
                continue

            if not node:
                continue
            nodeActives[uid] = node.active
            if hasattr(node, 'GetChildStates'):
                cstates = node.GetChildStates()
                for cs in cstates:
                    childStates[cs.childNode.id] = cs

        for uid in UUIDs:
            if uid in childStates:
                cs = childStates[uid]
                ret['nodes'][uid] = (cs.currentWeight, cs.targetWeight, cs.childNode.active, cs.childNode.phase)
            elif uid in nodeActives:
                if uid in nodesUids:
                    ret['nodes'][uid] = (
                     1, 1, nodeActives[uid], nodesUids[uid].phase)
                else:
                    ret['nodes'][uid] = (
                     1, 1, nodeActives[uid], 0)

        self.GetServer().GetAnimatorNodeInfoByUuidParmsCallback(ret)

    def GetAvailableEntities(self):
        type_uuids = self.GetAvailableEntityIDTypeDict()
        self.GetServer().GetAvailableEntitiesCallback(type_uuids)

    def ReloadAnimator(self, animatorFileName):
        print (
         'animator-file-name', animatorFileName)
        self._load(animatorFileName)

    def _load(self, animatorFilePath):
        import world
        loader = world.get_animation_tree_loader()
        animator = self.GetEditAnimator()
        animator.SetEmptyTree()
        loader.ClearCache()
        loader.EnableCache(False)
        try:
            root_node = loader.LoadTree(animator, animatorFilePath)
            print ('_load', animatorFilePath, root_node)
            animator.SetAnimationTree(root_node)
            animator.ActivateAnimationTree()
        except TypeError:
            model = self.GetEditModel()
            loader.LoadTree(model, animatorFilePath, 4, self.OnAnimatorLoaded)

    def OnAnimatorLoaded(self, animator):
        raise NotImplementedError

    def GetAnimatorParams(self):
        raise NotImplementedError

    def PushAnimatorState(self, data):
        raise NotImplementedError

    def SetAnimatorParam(self, key, data):
        pydata = data
        animator = self.GetEditAnimator()
        typ = pydata['type']
        func = self.OneArgMap.get(typ, None)
        if func:
            func(animator, pydata['val'])
        func = self.TwoArgMap.get(typ, None)
        if func:
            func(animator, pydata['name'], pydata['val'])
        return

    def ActivateAnimationTree(self):
        val = self.GetEditAnimator().ActivateAnimationTree()
        self.GetServer().ActivateAnimationTreeCallback(val)

    def DeactivateAnimationTree(self):
        val = self.GetEditAnimator().DeactivateAnimationTree()
        self.GetServer().DeactivateAnimationTreeCallback(val)

    def AddParameter(self, paramType, paramName, paramVal):
        val = self.GetEditAnimator().AddParameter(paramType, paramName, paramVal)
        self.GetServer().AddParameterCallback(val)

    def CopyFrom(self, animator):
        raise NotImplementedError

    def CopyNode(self, animNode):
        raise NotImplementedError

    def CreateNode(self, nodeType, nodeName):
        val = self.GetEditAnimator().CreateNode(nodeType, nodeName)
        self.GetServer().CreateNodeCallback(val)

    def Find(self, nodeName):
        val = self.GetEditAnimator().Find(nodeName)
        self.GetServer().FindCallback(val)

    def FindParameter(self, paramName):
        val = self.GetEditAnimator().FindParameter(paramName)
        self.GetServer().FindParameterCallback(val)

    def GetAnimatorFileName(self):
        val = self.GetEditAnimator().GetAnimatorFileName()
        self.GetServer().GetAnimatorFileNameCallback(val)

    def GetInt(self, paramName):
        val = self.GetEditAnimator().GetInt(paramName)
        self.GetServer().GetIntCallback(val)

    def GetNodes(self):
        val = self.GetEditAnimator().GetNodes()
        self.GetServer().GetNodesCallback(val)

    def GetRootNode(self):
        val = self.GetEditAnimator().GetRootNode()
        self.GetServer().GetRootNodeCallback(val)

    def GetSpeed(self):
        val = self.GetEditAnimator().GetSpeed()
        self.GetServer().GetSpeedCallback(val)

    def HasAnimationTree(self):
        val = self.GetEditAnimator().HasAnimationTree()
        self.GetServer().HasAnimationTreeCallback(val)

    def IsAnimationTreeActive(self):
        val = self.GetEditAnimator().IsAnimationTreeActive()
        self.GetServer().IsAnimationTreeActiveCallback(val)

    def Reset(self):
        val = self.GetEditAnimator().Reset()
        self.GetServer().ResetCallback(val)

    def ResetParameter(self, paramName):
        val = self.GetEditAnimator().ResetParameter(paramName)
        self.GetServer().ResetParameterCallback(val)

    def ResetTrigger(self, paramName):
        val = self.GetEditAnimator().ResetTrigger(paramName)
        self.GetServer().ResetTriggerCallback(val)

    def SetAnimationTree(self, rootNode, activate):
        val = self.GetEditAnimator().SetAnimationTree(rootNode, activate)
        self.GetServer().SetAnimationTreeCallback(val)

    def SetBool(self, paramName, bVal):
        val = self.GetEditAnimator().SetBool(paramName, bVal)
        self.GetServer().SetBoolCallback(val)

    def SetEmptyTree(self):
        val = self.GetEditAnimator().SetEmptyTree()
        self.GetServer().SetEmptyTreeCallback(val)

    def SetFloat(self, paramName, fVal):
        val = self.GetEditAnimator().SetFloat(paramName, fVal)
        self.GetServer().SetFloatCallback(val)

    def SetInt(self, paramName, iVal):
        val = self.GetEditAnimator().SetInt(paramName, iVal)
        self.GetServer().SetIntCallback(val)

    def SetSpeed(self, speed):
        val = self.GetEditAnimator().SetSpeed(speed)
        self.GetServer().SetSpeedCallback(val)

    def SetStateLeaveCallback(self, callback):
        val = self.GetEditAnimator().SetStateLeaveCallback(callback)
        self.GetServer().SetStateLeaveCallbackCallback(val)

    def SetTrigger(self, paramName):
        val = self.GetEditAnimator().SetTrigger(paramName)
        self.GetServer().SetTriggerCallback(val)

    def ToString(self):
        raise NotImplementedError

    def SetNodeProp(self, nodeInfoPack):
        uid, propName, propVal, pType = nodeInfoPack
        animator = self.GetEditAnimator()
        try:
            node = animator.FindById(uid)
        except:
            print (
             'FindByID Error, NodeID:', uid)
            self.GetServer().SetNodePropCallback(False)
            return

        if pType == 'vector':
            import math3d
            vec = math3d.vector(*propVal)
            setattr(node, propName, vec)
        else:
            setattr(node, propName, propVal)
        self.GetServer().SetNodePropCallback(True)

    def Register(self):
        methodMap = super(VenusPluginClient, self).Register()
        methodMap.update({(UUID, 'GetAvailableEntities'): self.GetAvailableEntities,
           (UUID, 'SetEditEntity'): self.SetEditEntity,
           (UUID, 'GetAnimatorNameByEntityUUID'): self.GetAnimatorNameByEntityUUID,
           (UUID, 'GetClipNamesByEntityUUID'): self.GetClipNamesByEntityUUID,
           (UUID, 'GetAnimatorNodeInfoByUuidParms'): self.GetAnimatorNodeInfoByUuidParms,
           (UUID, 'ReloadAnimator'): self.ReloadAnimator,
           (UUID, 'SetAnimatorParam'): self.SetAnimatorParam,
           (UUID, 'GetAnimatorParams'): self.GetAnimatorParams,
           (UUID, 'PushAnimatorState'): self.PushAnimatorState,
           (UUID, 'ActivateAnimationTree'): self.ActivateAnimationTree,
           (UUID, 'DeactivateAnimationTree'): self.DeactivateAnimationTree,
           (UUID, 'AddParameter'): self.AddParameter,
           (UUID, 'CopyFrom'): self.CopyFrom,
           (UUID, 'CopyNode'): self.CopyNode,
           (UUID, 'CreateNode'): self.CreateNode,
           (UUID, 'Find'): self.Find,
           (UUID, 'FindParameter'): self.FindParameter,
           (UUID, 'GetAnimatorFileName'): self.GetAnimatorFileName,
           (UUID, 'GetInt'): self.GetInt,
           (UUID, 'GetNodes'): self.GetNodes,
           (UUID, 'GetRootNode'): self.GetRootNode,
           (UUID, 'GetSpeed'): self.GetSpeed,
           (UUID, 'HasAnimationTree'): self.HasAnimationTree,
           (UUID, 'IsAnimationTreeActive'): self.IsAnimationTreeActive,
           (UUID, 'Reset'): self.Reset,
           (UUID, 'ResetParameter'): self.ResetParameter,
           (UUID, 'ResetTrigger'): self.ResetTrigger,
           (UUID, 'SetAnimationTree'): self.SetAnimationTree,
           (UUID, 'SetBool'): self.SetBool,
           (UUID, 'SetEmptyTree'): self.SetEmptyTree,
           (UUID, 'SetFloat'): self.SetFloat,
           (UUID, 'SetInt'): self.SetInt,
           (UUID, 'SetSpeed'): self.SetSpeed,
           (UUID, 'SetStateLeaveCallback'): self.SetStateLeaveCallback,
           (UUID, 'SetTrigger'): self.SetTrigger,
           (UUID, 'ToString'): self.ToString,
           (UUID, 'PreviewModel'): self.PreviewModel,
           (UUID, 'SetNodeProp'): self.SetNodeProp
           })
        return methodMap


class _HandlerWrapper(object):

    def __init__(self, plugin):
        self.plugin = plugin