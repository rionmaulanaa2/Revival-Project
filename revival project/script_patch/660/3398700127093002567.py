# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Storyline/BaseNode/ProcessNodes.py
import threading
import random
from ..NodeMetaManager import storyline_node_meta
from ..NodeManager import storyline_node
from ..CommonNodes import DynamicNode, DynamicNodeMeta
from ...Meta.TypeMeta import OrderedProperties, PInt, PBool, PArray, PCustom

@storyline_node_meta
class RandomProcessMeta(DynamicNodeMeta):
    NODE_CATEGORY = 'BaseNode|ProcessNode'
    CLASS_NAME = 'RandomProcessNode'
    NODE_TEXT = '\xe9\x9a\x8f\xe6\x9c\xba\xe6\x89\xa7\xe8\xa1\x8c'
    EDITOR_NODE_CLS = 'StorylineRandomRelayProxyNode'
    OUTPUT_PORTS = {}
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#random-relay-node'
    NODE_TIPS = '\xe9\x9a\x8f\xe6\x9c\xba\xe9\x80\x89\xe6\x8b\xa9\xe4\xb8\x80\xe4\xb8\xaa\xe8\xbe\x93\xe5\x87\xba\xe5\x8f\xa3\xe6\x89\xa7\xe8\xa1\x8c'
    PROPERTIES = OrderedProperties([
     (
      'byRound',
      PBool(sort=1, text='\xe8\xbd\xae\xe6\x8a\xbd', default=False, tip='\xe5\x8b\xbe\xe9\x80\x89\xe6\x97\xb6\xef\xbc\x8c\xe9\x9a\x8f\xe6\x9c\xba\xe5\xae\x8c\xe4\xb8\x80\xe8\xbd\xae\xe8\xbe\x93\xe5\x87\xba\xef\xbc\x8c\xe6\x89\x8d\xe4\xbc\x9a\xe5\x88\xb0\xe4\xb8\x8b\xe4\xb8\x80\xe8\xbd\xae\xef\xbc\x9b\xe4\xb8\x8d\xe5\x8b\xbe\xe9\x80\x89\xe6\x97\xb6\xef\xbc\x8c\xe5\xae\x8c\xe5\x85\xa8\xe9\x9a\x8f\xe6\x9c\xba\xe6\x89\xa7\xe8\xa1\x8c\xef\xbc\x8c\xe4\xbe\x8b\xe5\xa6\x82A\xe3\x80\x81B\xe3\x80\x81C\xe4\xb8\x89\xe4\xb8\xaa\xe7\xab\xaf\xe5\x8f\xa3\n\xe5\x8b\xbe\xe9\x80\x89\xe6\x97\xb6\xef\xbc\x8c\xe6\x89\xa7\xe8\xa1\x8c\xe9\xa1\xba\xe5\xba\x8f\xe5\x8f\xaf\xe8\x83\xbd\xe4\xb8\xba A C B | C B A | B C A | .....\n\xe4\xb8\x8d\xe5\x8b\xbe\xe9\x80\x89\xe6\x97\xb6\xef\xbc\x8c\xe6\x89\xa7\xe8\xa1\x8c\xe9\xa1\xba\xe5\xba\x8f\xe5\x8f\xaf\xe8\x83\xbd\xe4\xb8\xba A B A C C A B....')),
     (
      'isConfgProbability', PBool(sort=2, text='\xe9\x85\x8d\xe7\xbd\xae\xe6\xa6\x82\xe7\x8e\x87', default=False, tip='\xe6\x98\xaf\xe5\x90\xa6\xe6\x89\x8b\xe5\x8a\xa8\xe9\x85\x8d\xe7\xbd\xae\xe8\xbe\x93\xe5\x87\xba\xe7\xab\xaf\xe5\x8f\xa3\xe7\x9a\x84\xe6\xa6\x82\xe7\x8e\x87\xe5\x86\x85\xe5\xae\xb9')),
     (
      'probabilities',
      PArray(text='\xe6\xa6\x82\xe7\x8e\x87', sort=3, visibleCondition='obj["isConfgProbability"] == True', tip='\xe5\xa1\xab\xe5\x85\xa5\xe7\x9a\x84\xe6\x95\xb0\xe5\xad\x97\xe8\xb6\x8a\xe5\xa4\xa7\xef\xbc\x8c\xe6\xa6\x82\xe7\x8e\x87\xe8\xb6\x8a\xe5\xa4\xa7\xef\xbc\x8c\xe6\xa6\x82\xe7\x8e\x87\xe5\x92\x8c\xe5\xa1\xab\xe5\x85\xa5\xe7\x9a\x84\xe6\x95\xb0\xe5\xad\x97\xe6\x88\x90\xe6\xad\xa3\xe6\xaf\x94', editable=True, addable=False, removable=False, childAttribute=PInt(text='\xe6\xa6\x82\xe7\x8e\x87', min=1, default=1))),
     (
      'inputParams',
      PArray(text='\xe8\xbe\x93\xe5\x85\xa5\xe5\x8f\x82\xe6\x95\xb0', sort=4, maxSize=50, visible=False, childAttribute=PCustom(text='\xe8\xbe\x93\xe5\x85\xa5\xe5\x8f\x82\xe6\x95\xb0', editAttribute='GalaxyDynamicParam', supportedTypes=[], hasExec=False, default={'portName': None,'paramName': 'param','type': 'Bool'}))),
     (
      'outputParams',
      PArray(text='\xe8\xbe\x93\xe5\x87\xba\xe7\xab\xaf\xe5\x8f\xa3', sort=5, maxSize=50, childAttribute=PCustom(text='\xe8\xbe\x93\xe5\x87\xba\xe7\xab\xaf\xe5\x8f\xa3', editAttribute='GalaxyDynamicParam', supportedTypes=[
       'Logic'], hasExec=True, default={'portName': None,'paramName': '\xe7\xab\xaf\xe5\x8f\xa3','type': 'Logic'})))])


@storyline_node
class RandomProcessNode(DynamicNode):
    OUTPUT_PORTS = []

    def __init__(self):
        super(RandomProcessNode, self).__init__()
        self.byRound = False
        self.isConfgProbability = False
        self.probabilities = [1, 1, 1]
        self.outputParams = [{'portName': 'portName0','paramName': '\xe7\xab\xaf\xe5\x8f\xa3','type': 'Logic'}, {'portName': 'portName1','paramName': '\xe7\xab\xaf\xe5\x8f\xa3_1','type': 'Logic'}, {'portName': 'portName2','paramName': '\xe7\xab\xaf\xe5\x8f\xa3_2','type': 'Logic'}]
        self.indexProbDict = {}

    def Start(self, context):
        if not len(self.probabilities):
            return
        if not self.isConfgProbability:
            self.probabilities = [
             1] * len(self.outputParams)
        execIndex = self._getExecIndex()
        param = self.outputParams[execIndex]
        res = {'__out__': [param['portName']]}
        return res

    def _getExecIndex(self):
        execIndex = 0
        if not self.indexProbDict:
            self.indexProbDict = dict(zip(range(len(self.probabilities)), self.probabilities))
        total = sum(list(self.indexProbDict.values()))
        randNum = random.randint(0, total)
        currentProp = 0
        for index, prob in self.indexProbDict.items():
            currentProp += prob
            if currentProp >= randNum:
                execIndex = index
                break

        if self.byRound:
            del self.indexProbDict[execIndex]
        return execIndex

    def EditorOnlyModifyNodeData(self, propertyStr, value):
        super(RandomProcessNode, self).EditorOnlyModifyNodeData(propertyStr, value)
        parts = propertyStr.split('/')
        opt = parts.pop(0)
        if opt == 'del':
            if parts[0] == 'outputParams':
                del self.probabilities[int(parts[1])]
        elif opt == 'add':
            if parts[0] == 'outputParams':
                self.probabilities.append(1)


@storyline_node_meta
class SequencerProcessMeta(DynamicNodeMeta):
    NODE_CATEGORY = 'BaseNode|ProcessNode'
    CLASS_NAME = 'SequencerProcessNode'
    NODE_TEXT = '\xe9\xa1\xba\xe5\xba\x8f\xe6\x89\xa7\xe8\xa1\x8c'
    OUTPUT_PORTS = {}
    NODE_DOC = 'https://sunshine.doc.io.netease.com/storyline/base_node/#sequence-relay-node'
    NODE_TIPS = '\xe6\xa0\xb9\xe6\x8d\xae\xe9\x97\xb4\xe9\x9a\x94\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x8c\xe9\x80\x89\xe6\x8b\xa9\xe7\xab\xaf\xe5\x8f\xa3\xe8\xbf\x9b\xe8\xa1\x8c\xe6\x89\xa7\xe8\xa1\x8c\n\xe4\xbe\x8b\xe5\xa6\x82\xe6\x9c\x89 A\xe3\x80\x81B\xe3\x80\x81C \xe4\xb8\x89\xe4\xb8\xaa\xe7\xab\xaf\xe5\x8f\xa3\xef\xbc\x8c\xe9\x97\xb4\xe9\x9a\x94\xe6\x97\xb6\xe9\x97\xb4\xe4\xb8\xba0.5s\n\xe6\x89\xa7\xe8\xa1\x8c\xe6\x83\x85\xe5\x86\xb5\xe4\xb8\xba\xef\xbc\x9aA ()'
    PROPERTIES = OrderedProperties([
     (
      'interval', PInt(sort=1, text='\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x88\xe7\xa7\x92\xef\xbc\x89', default=False, tip='\xe6\xaf\x8f\xe4\xb8\xaa\xe8\xbe\x93\xe5\x87\xba\xe7\x9a\x84\xe9\x97\xb4\xe9\x9a\x94\xe6\x97\xb6\xe9\x97\xb4')),
     (
      'isFirstNeedWait', PBool(sort=2, text='\xe9\xa6\x96\xe5\x8f\x91\xe7\xad\x89\xe5\xbe\x85', default=True, tip='\xe5\x8b\xbe\xe9\x80\x89\xe6\x97\xb6\xef\xbc\x8c\xe7\xac\xac\xe4\xb8\x80\xe4\xb8\xaa\xe7\xab\xaf\xe5\x8f\xa3\xe4\xb9\x9f\xe4\xbc\x9a\xe5\x85\x88\xe7\xad\x89\xe4\xb8\x80\xe4\xb8\xaa\xe9\x97\xb4\xe9\x9a\x94\xe6\x97\xb6\xe9\x97\xb4\xe5\x86\x8d\xe6\x89\xa7\xe8\xa1\x8c')),
     (
      'inputParams',
      PArray(text='\xe8\xbe\x93\xe5\x85\xa5\xe5\x8f\x82\xe6\x95\xb0', sort=3, maxSize=50, visible=False, childAttribute=PCustom(text='\xe8\xbe\x93\xe5\x85\xa5\xe5\x8f\x82\xe6\x95\xb0', editAttribute='GalaxyDynamicParam', supportedTypes=[], hasExec=False, default={'portName': None,'paramName': 'param','type': 'Bool'}))),
     (
      'outputParams',
      PArray(text='\xe8\xbe\x93\xe5\x87\xba\xe7\xab\xaf\xe5\x8f\xa3', sort=4, maxSize=50, childAttribute=PCustom(text='\xe8\xbe\x93\xe5\x87\xba\xe7\xab\xaf\xe5\x8f\xa3', editAttribute='GalaxyDynamicParam', supportedTypes=[
       'Logic'], hasExec=True, default={'portName': None,'paramName': '\xe7\xab\xaf\xe5\x8f\xa3','type': 'Logic'})))])


@storyline_node
class SequencerProcessNode(DynamicNode):
    OUTPUT_PORTS = []

    def __init__(self):
        super(SequencerProcessNode, self).__init__()
        self.interval = 1
        self.isFirstNeedWait = True
        self.timer = None
        self.runIndex = 0
        self.outputParams = [{'portName': 'portName0','paramName': '\xe7\xab\xaf\xe5\x8f\xa3','type': 'Logic'}, {'portName': 'portName1','paramName': '\xe7\xab\xaf\xe5\x8f\xa3_1','type': 'Logic'}, {'portName': 'portName2','paramName': '\xe7\xab\xaf\xe5\x8f\xa3_2','type': 'Logic'}]
        return

    def processNode(self):
        if hasattr(self.context, 'nodeGraph') and not self.context.nodeGraph.isReleased:
            portName = self.outputParams[self.runIndex]['portName']
            self.context.FinishNode(self, {'__out__': [portName]})
            self.runIndex += 1
            if self.runIndex < len(self.outputParams):
                self.setTimeout(self.processNode)

    def setTimeout(self, callback):
        self.timer = threading.Timer(self.interval, callback)
        self.timer.start()

    def _stop(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None
        return

    def Start(self, context):
        context.nodeGraph.AddFinishCallback(self._stop)
        self.runIndex = 0
        if self.timer:
            self.timer.cancel()
        self.context = context
        if self.isFirstNeedWait:
            self.setTimeout(self.processNode)
        else:
            self.processNode()

    def Release(self, context):
        self.context = None
        return super(SequencerProcessNode, self).Release(context)