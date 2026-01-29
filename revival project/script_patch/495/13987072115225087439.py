# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NilePatchLoader.py
from __future__ import absolute_import
from ..Utils.NileCallbackWeakRef import NileCallbackWeakRef
from .NilePatchExtractor import NilePatchExtractor
from .NileLogger import NileLogger
from .NilePatchHttpLoader import NilePatchHttpLoader

class NilePatchLoader(object):
    CONCURRENT_COUNT = 4

    def __init__(self, activityConfigList, activityLoadedCallback):
        self._activityConfigList = activityConfigList or list()
        self._activityLoadedCallback = NileCallbackWeakRef(activityLoadedCallback)
        self._toLoadList = list()
        self._toLoadCount = 0
        self._loadedSet = set()
        self._executedActivitySet = set()
        self._loadingCount = 0
        self._paused = False
        self._ProcessActivityConfigList()

    def _ProcessActivityConfigList(self):
        for activity in self._activityConfigList:
            for url in activity.urlList:
                if url not in self._toLoadList:
                    if NilePatchExtractor.IsValidPatchName(url):
                        self._toLoadList.append(url)

        self._toLoadCount = len(self._toLoadList)

    def LoadActivity(self, name):
        if name in self._executedActivitySet:
            NileLogger.Info('\xe8\xaf\xa5\xe6\xb4\xbb\xe5\x8a\xa8\xe5\xb7\xb2\xe7\xbb\x8f\xe6\x89\xa7\xe8\xa1\x8c\xe8\xbf\x87\xe4\xba\x86')
            return
        activity = self._GetActivityConfigByName(name)
        if not activity:
            NileLogger.Error('\xe8\xaf\xa5\xe6\xb4\xbb\xe5\x8a\xa8\xe4\xb8\x8d\xe5\xad\x98\xe5\x9c\xa8')
            return
        for url in activity.urlList:
            if url not in self._toLoadList:
                self._toLoadList.append(url)
                self._toLoadCount += 1

        self._LoadNextPatch()

    def _GetActivityConfigByName(self, name):
        for activity in self._activityConfigList:
            if activity.name == name:
                return activity

        return None

    def Start(self):
        self._LoadNextPatch()

    def _LoadNextPatch(self):
        while self._loadingCount < NilePatchLoader.CONCURRENT_COUNT and len(self._toLoadList) > 0 and self._paused == False:
            self._loadingCount += 1
            url = self._toLoadList.pop(0)
            NileLogger.Info('\xe5\xbc\x80\xe5\xa7\x8b\xe5\x8a\xa0\xe8\xbd\xbdPatch, url: %s' % url)
            NilePatchHttpLoader().SendGetRequest(url, self._OnPatchLoaded)

    def _OnPatchLoaded(self, bodyInTuple):
        isSuccess, url = bodyInTuple
        if isSuccess:
            NileLogger.Info('Patch\xe5\x8a\xa0\xe8\xbd\xbd\xe6\x88\x90\xe5\x8a\x9f, Url: %s' % url)
            self._loadedSet.add(url)
            self._CheckActivityLoaded()
        self._loadingCount -= 1
        self._toLoadCount -= 1
        self._LoadNextPatch()

    def _CheckActivityLoaded(self):
        for config in self._activityConfigList:
            urlCount = 0
            for url in config.urlList:
                if url in self._loadedSet:
                    urlCount += 1

            if urlCount >= len(config.urlList):
                if config.name not in self._executedActivitySet:
                    self._executedActivitySet.add(config.name)
                    self._activityLoadedCallback.Execute(config.name)

    def GetToLoadCount(self):
        return self._toLoadCount

    def IsActivityExecuted(self, name):
        return name in self._executedActivitySet

    def Pause(self):
        self._paused = True

    def Resume(self):
        self._paused = False
        self._LoadNextPatch()