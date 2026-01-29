# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/Backend/Transaction/MicroBranch.py
import weakref
from .MontageProxy import MontageTrackProxy
from .. import PrintFunc

class MicroBranchHelper(object):
    MASTER = '_master'

    def __init__(self, media):
        self._media = weakref.ref(media)
        self._currentBranch = self.MASTER
        self.tempBranchUuids = []

    def init(self):
        isModified = False

        def setTrackUuidDisable(uuid):
            proxy = self._media().getProxy(uuid)
            if proxy and proxy.isValid() and proxy.getProperty('disabled'):
                proxy.setProperty('visible', False, systemname='Core')
                proxy.setProperty('disabled', False, systemname='Core')

        for branchname, trackInfo in self.branchInfo.items():
            if branchname == self.MASTER:
                continue
            addUuids = trackInfo.get('add', [])
            for branchUuid in addUuids:
                setTrackUuidDisable(branchUuid)

            modUuids = trackInfo.get('mod')
            for branchUuid in modUuids:
                setTrackUuidDisable(branchUuid)

        return isModified

    def _initBranchInfo(self):
        self._media().setProperty('branchInfo', {}, systemname='_Bypass')
        self._media().getProperty('branchInfo').setdefault(self.MASTER, [])

    @property
    def branchInfo(self):
        media = self._media()
        if media:
            ret = media.getProperty('branchInfo')
            if not ret:
                self._initBranchInfo()
                return media.getProperty('branchInfo')
            else:
                return ret

    @property
    def currentBranch(self):
        return self._currentBranch

    @currentBranch.setter
    def currentBranch(self, value):
        self._currentBranch = value
        self._media().setProperty('currentBranch', value, '_Bypass')

    def createBranch(self, name):
        if name == self.MASTER:
            return False
        else:
            if name in self.branchInfo:
                return False
            self.branchInfo[name] = {'add': [],'mod': dict(),'del': []}
            return True

    def deleteBranch(self, name):
        if name == self.MASTER:
            return False
        else:
            if name in self.branchInfo:
                self.branchInfo.pop(name)
                return True
            return False

    def getBranches(self):
        return list(self.branchInfo.keys())

    def _checkBranchnameAndProxy(self, branchname, proxy):
        if branchname not in self.branchInfo.keys():
            return False
        if not isinstance(proxy, MontageTrackProxy):
            return False
        return True

    def addChildInCurrentBranch(self, proxy, *args, **kwargs):
        return self.addChildInBranch(self.currentBranch, proxy, *args, **kwargs)

    def addChildInBranch(self, branchname, proxy, trackType, trackName=None, systemname='Default'):
        if not self._checkBranchnameAndProxy(branchname, proxy):
            return False
        if not trackName:
            trackMeta = proxy.meta.VALID_CHILDREN.get(trackType)
            if not trackMeta:
                return False
            trackName = trackMeta['name']
        trackName = trackName + '_' + branchname
        child = proxy.addChildInBranch(trackType, trackName, systemname)
        if child is False:
            return False
        childid = child.uuid
        self.branchInfo[branchname]['add'].append(childid)
        return child

    def modifyTrackInBranch(self, branchname, proxy, switchto=False):
        newproxy = None

        def _switchactive():
            self.setActivateTrack(newproxy, switchto)
            self.setActivateTrack(proxy, not switchto)

        if not self._checkBranchnameAndProxy(branchname, proxy):
            return False
        else:
            uuid = proxy.uuid
            srcbranch = self._getBranchOfProxy(proxy)
            if srcbranch != self.MASTER and uuid not in self.branchInfo[srcbranch]['add']:
                masteruuid = self.branchInfo[srcbranch]['mod'][uuid]
            else:
                masteruuid = uuid
            for k, v in self.branchInfo[branchname]['mod'].items():
                if masteruuid == v:
                    newproxy = self._media().getProxy(k)
                    _switchactive()
                    return newproxy

            if uuid in self.branchInfo[branchname]['del']:
                self.branchInfo[branchname]['del'].remove(uuid)
            elif uuid in self.branchInfo[branchname]['add']:
                newproxy = self._media().getProxy(uuid)
                _switchactive()
                return newproxy
            trackdata = proxy.getModelData()
            newproxy = proxy.getParent().pasteTrack(trackdata)
            newproxy.setProperty('name', proxy.name + '_' + branchname)
            newuuid = newproxy.uuid
            srcbranch = self._getBranchOfProxy(proxy)
            if srcbranch == self.MASTER:
                self.branchInfo[branchname]['mod'][newuuid] = uuid
                self._updateMasterTracks()
            elif uuid in self.branchInfo[srcbranch]['add']:
                self.branchInfo[branchname]['add'].append(uuid)
            else:
                self.branchInfo[branchname]['mod'][newuuid] = self.branchInfo[srcbranch]['mod'][uuid]
            self.setActivateTrack(newproxy, switchto)
            self.setActivateTrack(proxy, not switchto)
            return newproxy

    def unModifyTrackInBranch(self, branchname, proxy):
        if not self._checkBranchnameAndProxy(branchname, proxy):
            return False
        uuid = proxy.uuid
        if uuid in self.branchInfo[branchname]['mod']:
            masterid = self.branchInfo[branchname]['mod'].pop(uuid)
            proxy.getParent().deleteChild(proxy)
            self.setActivateTrackByID(masterid, True)
            self._updateMasterTracks()

    def deleteTrackInCurrentBranch(self, proxy):
        self.deleteTrackInBranch(self.currentBranch, proxy)

    def deleteTrackInBranch(self, branchname, proxy):
        if not self._checkBranchnameAndProxy(branchname, proxy):
            return False
        uuid = proxy.uuid
        if uuid in self.branchInfo[branchname]['add']:
            self.branchInfo[branchname]['add'].remove(uuid)
            self._updateMasterTracks()
            proxy.getParent().deleteChild(proxy)
        elif uuid in self.branchInfo[branchname]['mod']:
            self.unModifyTrackInBranch(branchname, proxy)
        else:
            self.branchInfo[branchname]['del'].append(uuid)
            self._updateMasterTracks()
            if self.currentBranch != self.MASTER:
                self.setActivateTrack(proxy, False)

    def unDeleteTrackInBranch(self, branchname, proxy):
        if not self._checkBranchnameAndProxy(branchname, proxy):
            return False
        uuid = proxy.uuid
        if uuid in self.branchInfo[branchname]['del']:
            self.branchInfo[branchname]['del'].remove(uuid)
            self._updateMasterTracks()
            if self.currentBranch == branchname:
                self.setActivateTrack(proxy, True)

    def setActivateTrackByID(self, uuid, isActivate=True):
        p = self._media().getProxy(uuid)
        if not p or not p.isValid():
            return
        return self.setActivateTrack(self._media().getProxy(uuid), isActivate)

    def setActivateTrack(self, proxy, isActivate=True):

        def setActivateChildTrack(child):
            child.setProperty('visible', isActivate, systemname='Core')

        setActivateChildTrack(proxy)
        children = proxy.getChildren()
        while children:
            nextChildren = []
            for c in children:
                setActivateChildTrack(c)
                nextChildren.extend(c.getChildren())

            children = nextChildren

    def getBranchOfProxy(self, proxy):
        return self._getBranchOfProxy(proxy)

    def _getBranchOfProxy(self, proxy):
        uuid = proxy.uuid
        for branchname, info in self.branchInfo.items():
            if branchname == self.MASTER:
                if uuid in info:
                    return self.MASTER
                continue
            if uuid in info['add'] or uuid in info['mod'].keys():
                return branchname

        return self.MASTER

    def _updateMasterTracks(self):
        dataset = set()
        for branchname, info in self.branchInfo.items():
            if branchname == self.MASTER:
                continue
            dataset.update(info['del'])
            dataset.update(info['mod'].values())

        self.branchInfo[self.MASTER] = list(dataset)

    def _getBranchAct(self, branchname):
        if branchname == self.MASTER:
            return set()
        if branchname not in self.branchInfo:
            return set()
        ret = set(self.branchInfo[branchname]['add'])
        ret.update(self.branchInfo[branchname]['mod'].keys())
        return ret

    def _getBranchDeact(self, branchname):
        if branchname == self.MASTER:
            return set()
        if branchname not in self.branchInfo:
            return set()
        ret = set(self.branchInfo[branchname]['del'])
        ret.update(self.branchInfo[branchname]['mod'].values())
        return ret

    def _getMasterDeact(self):
        uuids = set()
        for b in self.getBranches():
            if b == self.MASTER:
                continue
            act = self._getBranchAct(b)
            uuids = uuids.union(act)

        return uuids

    def getActDeact(self, dstbranch, srcbranch=MASTER, isEditor=False):
        if srcbranch == self.MASTER:
            dea = self._getMasterDeact()
            act = set()
            if dstbranch != self.MASTER:
                act = act.union(self._getBranchAct(dstbranch))
                dea = dea.union(self._getBranchDeact(dstbranch))
            diff = dea.intersection(act)
            dea.difference_update(diff)
        elif dstbranch == self.MASTER:
            dea = self._getBranchAct(srcbranch)
            act = self._getBranchDeact(srcbranch)
        else:
            act1, dea1 = self.getActDeact(self.MASTER, srcbranch, isEditor)
            act2, dea2 = self.getActDeact(dstbranch, self.MASTER, isEditor)
            act = act1.union(act2)
            dea = dea1.union(dea2)
            diff = act.intersection(dea)
            act.difference_update(diff)
            dea.difference_update(diff)
        if not isEditor and act:
            act = self._filterDisabledUuids(act)
        return (act, dea)

    def _filterDisabledUuids(self, uuids):
        filtered = [ u for u in uuids if self._media().getProxy(u).getProperty('disabled') is False ]
        return set(filtered)

    def switchToBranch(self, dstbranch, srcbranch=None):
        if srcbranch == dstbranch:
            return
        else:
            if srcbranch is None:
                srcbranch = self._currentBranch
            self.currentBranch = dstbranch
            act, dea = self.getActDeact(dstbranch, srcbranch, isEditor=True)
            for uuid in act:
                self.setActivateTrackByID(uuid, True)

            for uuid in dea:
                self.setActivateTrackByID(uuid, False)

            return

    def getProxyUuidInBranch(self, uuid, dstBranch=None, srcBranch=None):
        if dstBranch is None:
            dstBranch = self.currentBranch
        if srcBranch is None:
            if uuid in self.branchInfo['_master']:
                srcBranch = self.MASTER
            else:
                for branch, infos in self.branchInfo.items():
                    if branch == '_master':
                        continue
                    if uuid in list(infos.get('mod', {}).keys()):
                        srcBranch = branch
                        break

                if srcBranch is None:
                    PrintFunc('[WARNING]The uuid you search for is public on every branch.')
                    return uuid
        if srcBranch != self.MASTER:
            srcBranchInfo = self.branchInfo[srcBranch]['mod']
            masterUuid = srcBranchInfo.get(uuid, '')
        else:
            masterUuid = uuid
        if not masterUuid:
            return
        else:
            if dstBranch == self.MASTER:
                return masterUuid
            for branchTrack, masterTrack in self.branchInfo[dstBranch]['mod'].items():
                if masterTrack == masterUuid:
                    return branchTrack

            return