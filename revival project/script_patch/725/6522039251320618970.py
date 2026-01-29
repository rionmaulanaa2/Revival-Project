# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileServicePanelHub.py
from .NileLogger import NileLogger

class NileServicePanelHub(object):

    def __init__(self):
        self._panelDict = dict()

    def RegisterActivityPanel(self, activityId, panelWidget):
        if activityId in self._panelDict:
            NileLogger.Error('\xe9\x9d\xa2\xe6\x9d\xbf\xe5\xb7\xb2\xe7\xbb\x8f\xe5\xad\x98\xe5\x9c\xa8, ActivityId: %s' % activityId)
            return
        self._panelDict[activityId] = panelWidget

    def UnregisterActivityPanel(self, activityId):
        if activityId in self._panelDict:
            self._panelDict.pop(activityId)

    def IsActivityPanelRegistered(self, activityId):
        return activityId in self._panelDict

    def GetRegisteredActivityPanelCount(self):
        return len(self._panelDict)

    def GetActivityPanel(self, activityId):
        if activityId not in self._panelDict:
            NileLogger.Error('\xe9\x9d\xa2\xe6\x9d\xbf\xe4\xb8\x8d\xe5\xad\x98\xe5\x9c\xa8, ActivityId: %s' % activityId)
            return None
        else:
            return self._panelDict[activityId]

    def _ClearPanelDict(self):
        self._panelDict = dict()